from os import symlink
from .views import dataB
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from urllib.parse import parse_qs
from django_celery_beat.models import PeriodicTask, IntervalSchedule
import threading
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync, sync_to_async
import re
import requests
import random
import string
from websocket import create_connection
import pandas as pd
from datetime import datetime
from time import sleep
import asyncio


def get_auth_token():
    sign_in_url = 'https://www.tradingview.com/accounts/signin/'
    username = 'YellowCoinapi'
    password = 'Avm@12345'
    data = {"username": username, "password": password, "remember": "on"}
    headers = {
        'Referer': 'https://www.tradingview.com'
    }
    response = requests.post(url=sign_in_url, data=data, headers=headers)
    auth_token = response.json()['user']['auth_token']
    return auth_token


authToken = get_auth_token()


def filter_raw_message(text):
    try:
        found = re.search('"m":"(.+?)",', text).group(1)
        found2 = re.search('"p":(.+?"}"])}', text).group(1)
        print(found)
        print(found2)
        return found, found2
    except AttributeError:
        print("error")


def generateSession():
    stringLength = 12
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters)
                            for i in range(stringLength))
    return "qs_" + random_string


def generateChartSession():
    stringLength = 12
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters)
                            for i in range(stringLength))
    return "cs_" + random_string


def prependHeader(st):
    return "~m~" + str(len(st)) + "~m~" + st


def constructMessage(func, paramList):
    return json.dumps({
        "m": func,
        "p": paramList
    }, separators=(',', ':'))


def createMessage(func, paramList):
    return prependHeader(constructMessage(func, paramList))


def sendRawMessage(ws, message):
    ws.send(prependHeader(message))


def sendMessage(ws, func, args):
    ws.send(createMessage(func, args))


def listToString(s):
    str1 = ""
    for ele in s:
        str1 = str1 + "{"+ele
    return str1


class StockConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        global ws, session, authToken
        headers = json.dumps({
            'Origin': 'https://data.tradingview.com'
        })
        ws = create_connection(
            'wss://data.tradingview.com/socket.io/websocket', headers=headers)
        sendMessage(ws, "set_auth_token", [authToken])
        session = generateSession()
        print("session generated {}".format(session))
        sendMessage(ws, "quote_create_session", [session])
        await self.accept()
        await self.send(text_data=json.dumps({'type': 'connect', 'message': 'connected', 'session': session}))

    async def disconnect(self, close_code):
        # Leave room group
        ws.close()
        pass

    # Receive message from WebSocket
    async def receive(self, text_data):
        global ws, session
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        if message == "new":
            symbol = text_data_json['symbol']
            sendMessage(ws, "quote_add_symbols", symbol)
            sendMessage(ws, "quote_set_fields", [symbol[0], "base-currency-logoid", "ch", "chp", "currency-logoid", "currency_code", "currency_id", "base_currency_id", "current_session", "description", "exchange", "format", "fractional", "is_tradable", "language", "local_description", "listed_exchange", "logoid", "lp", "lp_time", "minmov", "minmove2", "original_name", "pricescale", "pro_name",
                        "short_name", "type", "update_mode", "volume", "ask", "bid", "fundamentals", "high_price", "is_tradable", "low_price", "open_price", "prev_close_price", "rch", "rchp", "rtc", "rtc_time", "status", "basic_eps_net_income", "beta_1_year", "earnings_per_share_basic_ttm", "industry", "market_cap_basic", "price_earnings_ttm", "sector", "volume", "dividends_yield", "timezone"])
            sendMessage(ws, "quote_fast_symbols", symbol)
            await self.send(text_data=json.dumps({'type': 'connect', 'message': "done"}))
        elif message == "add":
            symbol = text_data_json['symbol']
            sendMessage(ws, "quote_add_symbols", [symbol[0], symbol[-1]])
            sendMessage(ws, "quote_set_fields", [symbol[0], "base-currency-logoid", "ch", "chp", "currency-logoid", "currency_code", "currency_id", "base_currency_id", "current_session", "description", "exchange", "format", "fractional", "is_tradable", "language", "local_description", "listed_exchange", "logoid", "lp", "lp_time", "minmov", "minmove2", "original_name", "pricescale", "pro_name",
                        "short_name", "type", "update_mode", "volume", "ask", "bid", "fundamentals", "high_price", "is_tradable", "low_price", "open_price", "prev_close_price", "rch", "rchp", "rtc", "rtc_time", "status", "basic_eps_net_income", "beta_1_year", "earnings_per_share_basic_ttm", "industry", "market_cap_basic", "price_earnings_ttm", "sector", "volume", "dividends_yield", "timezone"])
            sendMessage(ws, "quote_fast_symbols", symbol)
            await self.send(text_data=json.dumps({'type': 'connect', 'message': "done"}))
        elif message == "update":
            try:
                result = ws.recv()
                pattern = re.compile("~m~\d+~m~~h~\d+$")
                if pattern.match(result):
                    ws.recv()
                    ws.send(result)
                data = listToString(result.split("{")[1:])
                data = json.loads(data)
                await self.send(text_data=json.dumps({'type': 'connect', 'message': data["p"][1]}))
            except Exception as e:
                await self.send(text_data=json.dumps({'type': 'connect', 'message': "error"}))
                pass
        elif message == "remove":
            tempL = text_data_json['symbol']
            sendMessage(ws, "quote_remove_symbols", tempL)
        else:
            await self.send(text_data=json.dumps({'type': 'connect', 'message': "error"}))


'''
class StockConsumer(WebsocketConsumer):
    def addToCeleryBeat(self, stocks):
        task = PeriodicTask.objects.filter(name="every-10-seconds")
        if len(task) > 0:
            task = task.first()
            args = json.loads(task.args)
            args = args[0]
            for x in stocks:
                if x not in args:
                    args.append(x)
            task.args = json.dumps([args])
            task.save()
        else:
            schedule, created = IntervalSchedule.objects.get_or_create(every=10, period=IntervalSchedule.SECONDS)
            task = PeriodicTask.objects.create(interval=schedule, name='every-10-seconds',task="yellowcoin.tasks.update_data", args=json.dumps([stocks]))

    def connect(self):
        self.room_name = 'trade'
        self.room_group_name = 'stock_%s' % self.room_name

        # Join room group
        self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        global stocks
        # Parse query string argument
        query_string = parse_qs(self.scope['query_string'].decode())
        stocksf = query_string['stock']
        print(stocksf)
        t = threading.Thread(target=self.addToCeleryBeat, args=(stocksf,))
        t.start()
        #t.join()
        self.accept()
        self.send(text_data=json.dumps({'type' : 'connect', 'message':'connected'}))


    def disconnect(self, close_code):
        # Leave room group
        self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        self.close()


    # Receive message from room group
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # Send message to room group
        print(message)
        channel_layer = get_channel_layer()
        self.channel_layer.send(
            self.channel_name,
            {
                'type': 'send_update',
                'message': message,
            }
        )
        self.send(text_data=json.dumps({'type': 'connect', 'message': message}))

    def send_stock_update(self, event):
        message = event['message']
        # Send message to WebSocket
        self.send(text_data=json.dumps(
            {
                'type': 'stock_update',
                'message': message
            }
        ))

    def send_update(self, text):
        self.send(text_data=json.dumps({'type': 'connect', 'message': text}))

'''
