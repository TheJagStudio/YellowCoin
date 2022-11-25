from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from accounts.models import stack
from .models import trades
import requests
import json
import threading
import csv
import random
from user.models import UserAccount
import os
from django.views.decorators.csrf import csrf_exempt
import threading
import sys
from log.models import tradeEdit
from datetime import datetime
from pathlib import Path
from .nseAPI import nsefetch
BASE_DIR = Path(__file__).resolve().parent.parent
api = "uha6zxzenz17uw2y"
secret = "cwdawxqyp6c0dgdljvffpi4k4nhejnbm"
f = open(os.path.join(BASE_DIR, "static", "config.txt"), "r")
access = str(f.read())
MCX = []
NSE = []
NFO = []
Forex = []
headers = {
    'X-Kite-Version': '3',
    'Authorization': 'token '+api+':'+access,
}

# with open('./static/5paise.csv', mode='r') as file:
#    reader = csv.reader(file)
#    for row in reader:
#        if row[0] == "M":
#            MCX.append(row)
#        elif row[0] == "N" and row[4] == "EQ":
#            NSE.append(row)
#        elif row[0] == "B" and row[1] == "D":
#            NFO.append(row)
with open('./static/NSE.csv', mode='r') as file:
    reader = csv.reader(file)
    for row in reader:
        NSE.append(row)
    file.close()
with open('./static/MCX.csv', mode='r') as file:
    reader = csv.reader(file)
    for row in reader:
        MCX.append(row)
    file.close()
with open('./static/NFO.csv', mode='r') as file:
    reader = csv.reader(file)
    for row in reader:
        NFO.append(row)
    file.close()
with open('./static/Forex.csv', mode='r') as file:
    reader = csv.reader(file)
    for row in reader:
        Forex.append(row)
    file.close()
count = 0
stocksNSE = []
stocksMCX = []
stocksNFO = []
stocksForex = []
for share in NSE:
    if share[10] != "":
        stocksNSE.append(share[10])
        count += 1
for share in MCX:
    if share[3] != "":
        stocksMCX.append(share[3])
        count += 1
for share in NFO:
    if share[3] != "":
        stocksNFO.append(share[3])
        count += 1
for share in Forex:
    if share[3] != "":
        stocksForex.append(share[3])
        count += 1
print(len(stocksNSE), len(stocksMCX), len(stocksNFO), len(stocksForex))
dataArrFinal = []
threads = []
counter = 0


class API:
    def __init__(self, token_to_instrument, api, access):
        self.live_data = {}
        self.token_to_instrument = token_to_instrument
        self.api = api
        self.access = access

    def on_ticks(self, ws, ticks):
        for stock in ticks:
            try:
                self.live_data[self.token_to_instrument[stock['instrument_token']]] = {"Open": stock["ohlc"]["open"],
                                                                                       "High": stock["ohlc"]["high"],
                                                                                       "Low": stock["ohlc"]["low"],
                                                                                       "Close": stock["ohlc"]["close"],
                                                                                       "Last Price": stock["last_price"],
                                                                                       "Volume": stock["volume_traded"],
                                                                                       "change": "%.2f" % stock["change"],
                                                                                       }
            except:
                self.live_data[self.token_to_instrument[stock['instrument_token']]] = {"Open": stock["ohlc"]["open"],
                                                                                       "High": stock["ohlc"]["high"],
                                                                                       "Low": stock["ohlc"]["low"],
                                                                                       "Close": stock["ohlc"]["close"],
                                                                                       "Last Price": stock["last_price"],
                                                                                       "change": "%.2f" % stock["change"],
                                                                                       }

    def on_connect(self, ws, response):
        ws.subscribe(list(self.token_to_instrument.keys()))
        ws.set_mode(ws.MODE_FULL, list(self.token_to_instrument.keys()))

    def Api(self):
        kws = KiteTicker(self.api, self.access)
        kws.on_ticks = self.on_ticks
        kws.on_connect = self.on_connect
        kws.connect(threaded=True)
        while len(self.live_data.keys()) != len(list(self.token_to_instrument.keys())):
            continue

        temp = []
        for i in range(len(list(self.live_data.keys()))):
            temp.append([random.randint(0, 10), random.randint(0, 10), random.randint(0, 10), random.randint(0, 10), random.randint(0, 10),
                         random.randint(0, 10), random.randint(0, 10), random.randint(0, 10)])
        x = 0
        for stock in self.live_data.keys():
            try:
                temp[x][0] = stock
                temp[x][1] = self.live_data[stock]["Open"]
                temp[x][2] = self.live_data[stock]["High"]
                temp[x][3] = self.live_data[stock]["Low"]
                temp[x][4] = self.live_data[stock]["Close"]
                temp[x][5] = self.live_data[stock]["Last Price"]
                temp[x][6] = self.live_data[stock]["Volume"]
                temp[x][7] = self.live_data[stock]["change"]
                x += 1
            except:
                temp[x][0] = stock
                temp[x][1] = self.live_data[stock]["Open"]
                temp[x][2] = self.live_data[stock]["High"]
                temp[x][3] = self.live_data[stock]["Low"]
                temp[x][4] = self.live_data[stock]["Close"]
                temp[x][5] = self.live_data[stock]["Last Price"]
                temp[x][6] = "volume"
                temp[x][7] = self.live_data[stock]["change"]
                x += 1
        return temp


def dataFeed(dataArr):
    url = "https://Openapi.5paisa.com/VendorsAPI/Service1.svc/MarketFeed"
    payload = json.dumps({
        "head": {
            "appName": "5PABCDEGIN",
            "appVer": "1.0",
            "key": "5dedVoMHQQkhWliONJO66gkYv6PX44wG",
            "osName": "Android",
            "requestCode": "5PMD",
            "userId": "RXiTPMsdsad",
            "password": "BlasdasVSs7Dys"
        },
        "body": {
            "Count": 1,
            "MarketFeedData": dataArr,
            "ClientLoginType": 0,
            "LastRequestTime": "/Date(0)/",
            "RefreshRate": "H"
        }
    })
    headers = {
        'Content-Type': 'application/json',
        'Cookie': 'NSC_JOh0em50e1pajl5b5jvyafempnkehc3=ffffffffaf103e0c45525d5f4f58455e445a4a423660'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()


def nse_custom_function_askBid(symbol):
    positions = nsefetch(
        'https://www.nseindia.com/api/quote-equity?symbol='+symbol+'&section=trade_info')
    return positions['marketDeptOrderBook']['bid'][0]["price"], positions['marketDeptOrderBook']['ask'][0]["price"]


def ApiF(market, token):
    ids = token
    rows = []
    names = []
    symbols = []
    for id in ids:
        if market == "NSE":
            for row in NSE:
                if row[2] == id:
                    names.append(row[10])
                    symbols.append(row[16])
                    rows.append({
                        "Exch": row[0],
                        "ExchType": row[1],
                        "Symbol": row[3],
                        "Expiry": row[5],
                        "StrikePrice": "0",
                        "OptionType": ""
                    })
                    break
        if market == "MCX":
            for row in MCX:
                if row[2] == id:
                    names.append(row[3])
                    symbols.append(row[16])
                    rows.append({
                        "Exch": "M",
                        "ExchType": row[1],
                        "Symbol": row[3],
                        "Expiry": row[5],
                        "StrikePrice": row[7],
                        "OptionType": ""
                    })
                    break
        if market == "NFO":
            for row in NFO:
                if row[2] == id:
                    names.append(row[3])
                    symbols.append(row[16])
                    rows.append({
                        "Exch": row[0],
                        "ExchType": row[1],
                        "Symbol": row[3],
                        "Expiry": row[5],
                        "StrikePrice": row[7],
                        "OptionType": ""
                    })
                    break
        if market == "Forex":
            for row in Forex:
                if row[2] == id:
                    names.append(row[3])
                    symbols.append(row[16])
                    rows.append({
                        "Exch": "N",
                        "ExchType": "U",
                        "Symbol": row[3],
                        "Expiry": row[5],
                        "StrikePrice": row[7],
                        "OptionType": ""
                    })
                    break
    req_list = rows
    lastmsg = dataFeed(req_list)
    live_data = lastmsg['body']['Data']
    temp = []
    sName = ""
    #[{'Chg': 299.1, 'ChgPcnt': 0.7371716, 'Exch': 'N', 'ExchType': 'C', 'High': 40904.3, 'LastRate': 40873.1, 'Low': 40693.95, 'PClose': 40574, 'Symbol': 'BANKNIFTY', 'TickDt': '/Date(1663074791000+0530)/', 'Time': 45791, 'Token': 999920005, 'TotalQty': 0}]
    for i in range(len(live_data)):
        try:
            askBid = list(nse_custom_function_askBid(symbols[i]))
        except:
            askBid = ["-", "-"]
        try:
            sName = names[i]
        except:
            sName = "-"
        try:
            sOpen = live_data[i]['Open']
        except:
            sOpen = "-"
        try:
            sHigh = live_data[i]['High']
        except:
            sHigh = "-"
        try:
            sLow = live_data[i]['Low']
        except:
            sLow = "-"
        try:
            sClose = live_data[i]['PClose']
        except:
            sClose = "-"
        try:
            sLTP = live_data[i]['LastRate']
        except:
            sLTP = "-"
        try:
            sVolume = live_data[i]['TotalQty']
        except:
            sVolume = "-"
        try:
            sChange = live_data[i]['Chg']
        except:
            sChange = "-"
        try:
            sPerChange = live_data[i]['ChgPcnt']
        except:
            sPerChange = "-"
        try:
            sSell = askBid[0]  # live_data[i]["BidRate"]
        except:
            sSell = "-"
        try:
            sAsk = askBid[1]  # live_data[i]["AskRate"]
        except:
            sAsk = "-"
        temp.append([sName, sOpen, sHigh, sLow, sClose,
                    sLTP, sVolume, str(sChange) + " / " + str(round(sPerChange, 2)), sSell, sAsk])
    return temp


@ login_required
def home(request):
    """current_user = request.user
    if current_user.username == 'admin':
        return render(request, 'home.html', {'current_user': current_user})
    else:
        return render(request, 'user_home.html', {'current_user': current_user})"""
    return redirect('trading:watchlist')


@ login_required
def ws(request):
    obj = stack.objects.filter(username=request.user).first()
    context = {'stocks': obj.stocks['data']}

    return render(request, 'websockets.html', context=context)


@ login_required
def watchlist(request):
    f = open("static/config.txt", "r")
    try:
        current_user = request.user
        senty = []
        obj = stack.objects.filter(username=request.user).first()
        # obj.stocks = {"data": []}
        # obj.save()
        request.session['live_data'] = {}
        request.session['token_to_instrument_NSE'] = []
        request.session['token_to_instrument_MCX'] = []
        request.session['token_to_instrument_NFO'] = []
        request.session['token_to_instrument_Forex'] = []
        request.session['TempNSE'] = []
        request.session['TempMCX'] = []
        request.session['TempNFO'] = []
        request.session['TempForex'] = []
        if obj.stocks['data'] != []:
            for stock in obj.stocks['data']:
                for share in NSE:
                    if share[2] == stock:
                        request.session['token_to_instrument_NSE'].append(
                            share[2])
                for share in MCX:
                    if share[2] == stock:
                        request.session['token_to_instrument_MCX'].append(
                            share[2])
                for share in NFO:
                    if share[2] == stock:
                        request.session['token_to_instrument_NFO'].append(
                            share[2])
                for share in Forex:
                    if share[2] == stock:
                        request.session['token_to_instrument_Forex'].append(
                            share[2])
            try:
                request.session['TempNSE'] = ApiF(
                    "NSE", request.session['token_to_instrument_NSE'])
            except:
                request.session['TempNSE'] = []
            try:
                request.session['TempMCX'] = ApiF(
                    "MCX", request.session['token_to_instrument_MCX'])
            except:
                request.session['TempMCX'] = []
            try:
                request.session['TempNFO'] = ApiF(
                    "NFO", request.session['token_to_instrument_NFO'])
            except:
                request.session['TempNFO'] = []
            try:
                request.session['TempForex'] = ApiF(
                    "Forex", request.session['token_to_instrument_Forex'])
            except:
                request.session['TempForex'] = []

            request.session['TempNSE'].sort(key=lambda x: x[1])
            request.session['TempMCX'].sort(key=lambda x: x[1])
            request.session['TempNFO'].sort(key=lambda x: x[1])
            request.session['TempForex'].sort(key=lambda x: x[1])
        #senty = [ApiF("NSE", ["NIFTY 50"]), ApiF("BSE", ["SENSEX"])]
        # print(senty)
        if current_user.is_superuser:
            return render(request, 'trade_watchlist.html', {'dataNSE': request.session['TempNSE'], 'dataMCX': request.session['TempMCX'], 'dataNFO': request.session['TempNFO'], 'dataForex': request.session['TempForex'], 'stocksA': stocksNSE, 'stocksB': stocksMCX, 'current_user': current_user, 'senty': senty, 'market': 'NSE'})
        else:
            user_account = UserAccount.objects.filter(
                user=current_user).first()
            if user_account.Account_Type == "User":
                givenUser = "False"
            else:
                givenUser = "True"
            return render(request, 'user_trade_watchlist.html', {'dataNSE': request.session['TempNSE'], 'dataNFO': request.session['TempNFO'], 'dataMCX': request.session['TempMCX'], 'dataForex': request.session['TempForex'], 'givenUser': givenUser, 'stockA': stocksNSE, 'stocksB': stocksMCX, 'current_user': current_user, 'senty': senty, 'market': 'NSE'})
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return redirect('trading:watchlist')


@ login_required
def tradesFunction(request):
    current_user = request.user
    if current_user.is_superuser:
        obj = trades.objects.all()
        return render(request, 'trade_transcation.html', {'trades': obj, 'current_user': current_user, 'stocksMCX': stocksMCX, 'dataArrFinal': dataArrFinal})
    else:
        user_account = UserAccount.objects.filter(user=current_user).first()
        if user_account.Account_Type == "User":
            givenUser = "False"
        else:
            givenUser = "True"
        obj = trades.objects.filter(user_id=request.user).all()
        return render(request, 'user_trade_transcation.html', {'trades': obj, 'current_user': current_user, 'stocksMCX': stocksNSE, 'dataArrFinal': dataArrFinal, 'givenUser': givenUser})


@ login_required
def Create_market(request):
    current_user = request.user
    if current_user.is_superuser:
        if (request.method == 'POST'):
            symbol = request.POST.get('symbol')
            type = request.POST.get('type')
            lot = request.POST.get('Lot')
            qty = request.POST.get('QTY')
            segment = request.POST.get('segment')
            bs = request.POST.get('bs')
            price = request.POST.get('price')
            newentry = tradeEdit(tType="Update", client=current_user.username, symbol=symbol, order_type=type,
                                 lot=lot, qty=qty, order_price=price, market=segment, oTime=datetime.now(), dTime=datetime.now())
            newentry.save()
            newTrade = trades(user_id=request.user, script=symbol, orderType=str(type), qty=int(
                qty), status="executed", orderPrice=float(price), market=segment, bs=bs, lot=int(lot))
            newTrade.save()
            return redirect('trading:tradesFunction')
        obj = trades.objects.filter(user_id=request.user).all()
        return render(request, 'create_market.html', {'trades': obj, 'current_user': current_user, 'stocks': stocksNSE})
    else:
        user_account = UserAccount.objects.filter(user=current_user).first()
        if user_account.Account_Type == "User":
            givenUser = "False"
        else:
            givenUser = "True"
        obj = trades.objects.filter(user_id=request.user).all()
        if (request.method == 'POST'):
            symbol = request.POST.get('symbol')
            type = request.POST.get('type')
            lot = request.POST.get('Lot')
            qty = request.POST.get('QTY')
            segment = request.POST.get('segment')
            bs = request.POST.get('bs')
            price = request.POST.get('price')
            newentry = tradeEdit(tType="Update", client=current_user.username, symbol=symbol, order_type=type,
                                 lot=lot, qty=qty, order_price=price, market=segment, oTime=datetime.now(), dTime=datetime.now())
            newentry.save()
            newTrade = trades(user_id=request.user, script=str(symbol), orderType=str(type), qty=int(
                qty), status="executed", orderPrice=float(price), market=segment, bs=bs, lot=int(lot))
            newTrade.save()
            return redirect('trading:tradesFunction')
        obj = trades.objects.filter(user_id=request.user).all()
        return render(request, 'user_create_market.html', {'trades': obj, 'current_user': current_user, 'stocks': stocksNSE, 'givenUser': givenUser})


@ login_required
def Create_limit(request):
    current_user = request.user
    if current_user.is_superuser:
        if (request.method == 'POST'):
            symbol = request.POST.get('symbol')
            type = request.POST.get('type')
            lot = request.POST.get('Lot')
            qty = request.POST.get('QTY')
            segment = request.POST.get('segment')
            bs = request.POST.get('bs')
            price = request.POST.get('price')
            newentry = tradeEdit(tType="Update", client=current_user.username, symbol=symbol, order_type=type,
                                 lot=lot, qty=qty, order_price=price, market=segment, oTime=datetime.now(), dTime=datetime.now())
            newentry.save()
            newTrade = trades(user_id=request.user, script=symbol, orderType=str(type), qty=int(
                qty), status="executed", orderPrice=float(price), market=segment, bs=bs, lot=int(lot))
            newTrade.save()
            return redirect('trading:tradesFunction')
        obj = trades.objects.filter(user_id=request.user).all()
        return render(request, 'create_limit.html', {'trades': obj, 'current_user': current_user, 'stocks': stocksNSE})
    else:
        user_account = UserAccount.objects.filter(user=current_user).first()
        if user_account.Account_Type == "User":
            givenUser = "False"
        else:
            givenUser = "True"
        obj = trades.objects.filter(user_id=request.user).all()
        if (request.method == 'POST'):
            symbol = request.POST.get('symbol')
            type = request.POST.get('type')
            lot = request.POST.get('Lot')
            qty = request.POST.get('QTY')
            segment = request.POST.get('segment')
            bs = request.POST.get('bs')
            price = request.POST.get('price')
            newentry = tradeEdit(tType="Update", client=current_user.username, symbol=symbol, order_type=type,
                                 lot=lot, qty=qty, order_price=price, market=segment, oTime=datetime.now(), dTime=datetime.now())
            newentry.save()
            newTrade = trades(user_id=request.user, script=str(symbol), orderType=str(type), qty=int(
                qty), status="executed", orderPrice=float(price), market=segment, bs=bs, lot=int(lot))
            newTrade.save()
            return redirect('trading:tradesFunction')
        obj = trades.objects.filter(user_id=request.user).all()
        return render(request, 'user_create_limit.html', {'trades': obj, 'current_user': current_user, 'stocks': stocksNSE, 'givenUser': givenUser})


@ login_required
def Create_stop(request):
    current_user = request.user
    if current_user.is_superuser:
        if (request.method == 'POST'):
            symbol = request.POST.get('symbol')
            type = request.POST.get('type')
            lot = request.POST.get('Lot')
            qty = request.POST.get('QTY')
            segment = request.POST.get('segment')
            bs = request.POST.get('bs')
            price = request.POST.get('price')
            newentry = tradeEdit(tType="Update", client=current_user.username, symbol=symbol, order_type=type,
                                 lot=lot, qty=qty, order_price=price, market=segment, oTime=datetime.now(), dTime=datetime.now())
            newentry.save()
            newTrade = trades(user_id=request.user, script=symbol, orderType=str(type), qty=int(
                qty), status="executed", orderPrice=float(price), market=segment, bs=bs, lot=int(lot))
            newTrade.save()
            return redirect('trading:tradesFunction')
        obj = trades.objects.filter(user_id=request.user).all()
        return render(request, 'create_stop.html', {'trades': obj, 'current_user': current_user, 'stocks': stocksNSE})
    else:
        user_account = UserAccount.objects.filter(user=current_user).first()
        if user_account.Account_Type == "User":
            givenUser = "False"
        else:
            givenUser = "True"
        obj = trades.objects.filter(user_id=request.user).all()
        if (request.method == 'POST'):
            symbol = request.POST.get('symbol')
            type = request.POST.get('type')
            lot = request.POST.get('Lot')
            qty = request.POST.get('QTY')
            segment = request.POST.get('segment')
            bs = request.POST.get('bs')
            price = request.POST.get('price')
            newentry = tradeEdit(tType="Update", client=current_user.username, symbol=symbol, order_type=type,
                                 lot=lot, qty=qty, order_price=price, market=segment, oTime=datetime.now(), dTime=datetime.now())
            newentry.save()
            newTrade = trades(user_id=request.user, script=str(symbol), orderType=str(type), qty=int(
                qty), status="executed", orderPrice=float(price), market=segment, bs=bs, lot=int(lot))
            newTrade.save()
            return redirect('trading:tradesFunction')
        obj = trades.objects.filter(user_id=request.user).all()
        return render(request, 'user_create_stop.html', {'trades': obj, 'current_user': current_user, 'stocks': stocksNSE, 'givenUser': givenUser})


@ login_required
def trading_portfolio(request):
    current_user = request.user
    if current_user.is_superuser:
        transcations = trades.objects.all()
        data = {}
        for i in transcations:
            # market,scripr,tbuy,tswll,netq,autoclosw,close
            data[i.script] = ["", "", 0, 0, 0, 0, 0]
        for i in transcations:
            if (i.orderType == "Buy" or i.orderType == "buy"):
                data[i.script] = [i.market, i.script,
                                  (data[i.script][2] + (i.lot*i.qty)), data[i.script][3], ((data[i.script][2] + (i.lot*i.qty)) - data[i.script][3]), i.orderPrice,  i.oTime.strftime('%d-%m-%Y')]
            elif (i.orderType == "Sell" or i.orderType == "sell"):
                data[i.script] = [i.market, i.script,
                                  data[i.script][2], (data[i.script][3] + (i.lot*i.qty)), (data[i.script][2] - (data[i.script][3] + (i.lot*i.qty))), i.orderPrice, i.oTime.strftime('%d-%m-%Y')]
        keys = list(data.keys())
        print(keys)
        return render(request, 'trading_portfolio.html', {'current_user': current_user, 'data': data, 'keys': keys})
    else:
        user_account = UserAccount.objects.filter(user=current_user).first()
        if user_account.Account_Type == "User":
            givenUser = "False"
        else:
            givenUser = "True"
        return render(request, 'user_trading_portfolio.html', {'current_user': current_user, 'givenUser': givenUser})


@ login_required
def trading_ban(request):
    current_user = request.user
    if current_user.is_superuser:
        return render(request, 'trading_ban.html', {'current_user': current_user})
    else:
        user_account = UserAccount.objects.filter(user=current_user).first()
        if user_account.Account_Type == "User":
            givenUser = "False"
        else:
            givenUser = "True"
        return render(request, 'user_trading_ban.html', {'current_user': current_user, 'givenUser': givenUser})


@ login_required
def trading_margin(request):
    current_user = request.user
    if current_user.is_superuser:
        return render(request, 'trading_margin.html', {'current_user': current_user})


@ login_required
def tradesRemove(request):
    id = request.GET.get('id')
    trade = trades.objects.filter(id=id).first()
    newentry = tradeEdit(tType="Delete", client=trade.user_id.username, Deleted_by=request.user.username, symbol=trade.script, order_type=trade.orderType,
                         lot=trade.lot, qty=trade.qty, order_price=trade.orderPrice, market=trade.market, oTime=trade.oTime, dTime=datetime.now())
    newentry.save()
    trades.objects.filter(id=id).delete()
    return HttpResponse("success")


@ csrf_exempt
@ login_required
def dataDisplay(request):
    # args = request.args
    apiKey = request.GET.get('apiKey')
    symbol = request.GET.get('symbol')
    market = request.GET.get('segment')
    todo = request.GET.get('todo')
    print(apiKey, symbol)
    stringOutput = {"data": []}
    if apiKey == "asdfghjkl":
        if symbol != None:
            try:
                token_to_instrument_NSE = []
                flag = "0"
                for share in NSE:
                    if share[3] == symbol:
                        token_to_instrument_NSE.append(share[2])
                        flag = "NSE"
                        break
                if flag == "0":
                    for share in MCX:
                        if share[3] == symbol:
                            token_to_instrument_NSE.append(share[2])
                            flag = "MCX"
                            break
                if flag == "0":
                    for share in NFO:
                        if share[3] == symbol:
                            token_to_instrument_NSE.append(share[2])
                            flag = "NFO"
                            break
                if flag == "0":
                    for share in Forex:
                        if share[3] == symbol:
                            token_to_instrument_NSE.append(share[2])
                            flag = "Forex"
                            break
                dataArrFinal = ApiF(flag, token_to_instrument_NSE)
                x = {
                    "name": str(dataArrFinal[0][0]),
                    "open": str(dataArrFinal[0][1]),
                    "high": str(dataArrFinal[0][2]),
                    "low": str(dataArrFinal[0][3]),
                    "close": str(dataArrFinal[0][4]),
                    "last price": str(dataArrFinal[0][5]),
                    "volume": str(dataArrFinal[0][6]),
                    "change": str(dataArrFinal[0][7]),
                    "bid": str(dataArrFinal[0][8]),
                    "ask": str(dataArrFinal[0][9]),
                }
                stringOutput["data"].append(x)
                return HttpResponse(json.dumps(stringOutput, indent=4), content_type="application/json")
            except:
                return HttpResponse('Invalid Symbol', content_type="application/json")
        else:
            userStack = stack.objects.filter(username=request.user.id).first()
            if userStack.stocks['data'] != []:
                token_to_instrument_NSE = []
                token_to_instrument_MCX = []
                token_to_instrument_NFO = []
                token_to_instrument_Forex = []
                for stock in userStack.stocks['data']:
                    for share in NSE:
                        if share[2] == stock:
                            token_to_instrument_NSE.append(share[2])
                    for share in MCX:
                        if share[2] == stock:
                            token_to_instrument_MCX.append(share[2])
                    for share in NFO:
                        if share[2] == stock:
                            token_to_instrument_NFO.append(share[2])
                    for share in Forex:
                        if share[2] == stock:
                            token_to_instrument_Forex.append(share[2])
                dataArrFinal1 = []
                try:
                    dataArrFinal1 = ApiF("NSE", token_to_instrument_NSE)
                except:
                    dataArrFinal1 = []
                stringOutput = {"NSE": [], "MCX": [], "NFO": [], "Forex": []}
                for i in dataArrFinal1:
                    x = {
                        "name": str(i[0]),
                        "open": str(i[1]),
                        "high": str(i[2]),
                        "low": str(i[3]),
                        "close": str(i[4]),
                        "last price": str(i[5]),
                        "volume": str(i[6]),
                        "change": str(i[7]),
                        "bid": str(i[8]),
                        "ask": str(i[9]),
                    }
                    stringOutput["NSE"].append(x)
                dataArrFinal2 = []
                try:
                    dataArrFinal2 = ApiF("MCX", token_to_instrument_MCX)
                except:
                    dataArrFinal2 = []
                for i in dataArrFinal2:
                    x = {
                        "name": str(i[0]),
                        "open": str(i[1]),
                        "high": str(i[2]),
                        "low": str(i[3]),
                        "close": str(i[4]),
                        "last price": str(i[5]),
                        "volume": str(i[6]),
                        "change": str(i[7]),
                        "bid": str(i[8]),
                        "ask": str(i[9]),
                    }
                    stringOutput["MCX"].append(x)
                dataArrFinal3 = []
                try:
                    dataArrFinal3 = ApiF("NFO", token_to_instrument_NFO)
                except:
                    dataArrFinal3 = []
                for i in dataArrFinal3:
                    x = {
                        "name": str(i[0]),
                        "open": str(i[1]),
                        "high": str(i[2]),
                        "low": str(i[3]),
                        "close": str(i[4]),
                        "last price": str(i[5]),
                        "volume": str(i[6]),
                        "change": str(i[7]),
                        "bid": str(i[8]),
                        "ask": str(i[9]),
                    }
                    stringOutput["NFO"].append(x)
                dataArrFinal4 = []
                try:
                    dataArrFinal4 = ApiF("Forex", token_to_instrument_NFO)
                except:
                    dataArrFinal4 = []
                for i in dataArrFinal4:
                    x = {
                        "name": str(i[0]),
                        "open": str(i[1]),
                        "high": str(i[2]),
                        "low": str(i[3]),
                        "close": str(i[4]),
                        "last price": str(i[5]),
                        "volume": str(i[6]),
                        "change": str(i[7]),
                        "bid": str(i[8]),
                        "ask": str(i[9]),
                    }
                    stringOutput["Forex"].append(x)
                return HttpResponse(json.dumps(stringOutput, indent=4), content_type="application/json")
            else:
                return HttpResponse('No Stocks', content_type="application/json")
    elif apiKey == "qwertyuiop":
        if todo == "get":
            print(symbol)
            try:
                stock = []
                if market == "NSE":
                    for share in NSE:
                        if share[10] == symbol:
                            stock.append(share[2])
                            symbolCode = share[2]
                            break
                    dataArrFinal = ApiF("NSE", stock)
                elif market == "MCX":
                    for share in MCX:
                        if share[3].replace(" ", "") == symbol.replace(" ", ""):
                            stock.append(share[2])
                            symbolCode = share[2]
                            break
                    dataArrFinal = ApiF("MCX", stock)
                elif market == "NFO":
                    for share in NFO:
                        if share[3] == symbol:
                            stock.append(share[2])
                            symbolCode = share[2]
                            break
                    dataArrFinal = ApiF("NFO", stock)
                elif market == "Forex":
                    for share in Forex:
                        if share[3] == symbol:
                            stock.append(share[2])
                            symbolCode = share[2]
                            break
                    dataArrFinal = ApiF("Forex", stock)

                x = {
                    "name": str(dataArrFinal[0][0]),
                    "open": str(dataArrFinal[0][1]),
                    "high": str(dataArrFinal[0][2]),
                    "low": str(dataArrFinal[0][3]),
                    "close": str(dataArrFinal[0][4]),
                    "last price": str(dataArrFinal[0][5]),
                    "volume": str(dataArrFinal[0][6]),
                    "change": str(dataArrFinal[0][7]),
                    "bid": str(dataArrFinal[0][8]),
                    "ask": str(dataArrFinal[0][9]),
                }
                stringOutput["data"].append(x)
                obj = stack.objects.filter(username=request.user).first()
                obj.stocks['data'].append(symbolCode)
                obj.save()
                return HttpResponse(json.dumps(stringOutput, indent=4), content_type="application/json")
            except:
                return HttpResponse(json.dumps({"error": "Invalid Symbol"}), content_type="application/json")
        else:
            print(symbol)
            if market == "NSE":
                for share in NSE:
                    if share[10] == symbol:
                        shareId = share[2]
                        break
            elif market == "MCX":
                for share in MCX:
                    if share[3] == symbol:
                        shareId = share[2]
                        break
            elif market == "NFO":
                for share in NFO:
                    if share[3] == symbol:
                        shareId = share[2]
                        break
            elif market == "Forex":
                for share in Forex:
                    if share[3] == symbol:
                        shareId = share[2]
                        break
            userStack = stack.objects.filter(username=request.user.id).first()
            userStack.stocks["data"].remove(shareId)
            userStack.save()
            return HttpResponse(json.dumps({"success": "True"}), content_type="application/json")
    else:
        return HttpResponse(HttpResponse('Invalid API Key', content_type="application/json"))


@csrf_exempt
@login_required
def scriptChanger(request):
    market = request.GET.get('segment')
    if market == "NSE":
        return HttpResponse(json.dumps(stocksNSE), content_type="application/json")
    elif market == "NFO":
        todo = request.GET.get('todo')
        if todo == "expiry":
            script = request.GET.get('script')
            uniq = []
            for share in NFO:
                if share[16] == script and share[15] not in uniq:
                    uniq.append(share[15])
            return HttpResponse(json.dumps(uniq), content_type="application/json")
        elif todo == "strike":
            script = request.GET.get('script')
            expiry = request.GET.get('expiry')
            typeCall = request.GET.get('typeCall')
            uniq = []
            for share in NFO:
                if share[16] == script and share[15] == expiry and share[6] == typeCall and share[7] not in uniq:
                    uniq.append(share[7])
            return HttpResponse(json.dumps(uniq), content_type="application/json")
        elif todo == "add":
            script = request.GET.get('script')
            expiry = request.GET.get('expiry')
            typeCall = request.GET.get('typeCall')
            strike = request.GET.get('strike')
            for share in NFO:
                if share[16] == script and share[15] == expiry and share[6] == typeCall and share[7] == strike:
                    return HttpResponse(json.dumps({"symbol": share[3]}), content_type="application/json")
            return HttpResponse(json.dumps({"error": "Invalid Symbol"}), content_type="application/json")
        else:
            NFOScript = ["AARTIIND", "ABB", "ABBOTINDIA", "ABCAPITAL", "ABFRL", "ACC", "ADANIENT", "ADANIPORTS", "ALKEM", "AMARAJABAT", "AMBUJACEM", "APOLLOHOSP", "APOLLOTYRE", "ASHOKLEY", "ASIANPAINT", "ASTRAL", "ATUL", "AUBANK", "AUROPHARMA", "AXISBANK", "BAJAJ-AUTO", "BAJAJFINSV", "BAJFINANCE", "BALKRISIND", "BALRAMCHIN", "BANDHANBNK", "BANKBARODA", "BANKNIFTY", "BATAINDIA", "BEL", "BERGEPAINT", "BHARATFORG", "BHARTIARTL", "BHEL", "BIOCON", "BOSCHLTD", "BPCL", "BRITANNIA", "BSOFT", "CANBK", "CANFINHOME", "CHAMBLFERT", "CHOLAFIN", "CIPLA", "COALINDIA", "COFORGE", "COLPAL", "CONCOR", "COROMANDEL", "CROMPTON", "CUB", "CUMMINSIND", "DABUR", "DALBHARAT", "DEEPAKNTR", "DELTACORP", "DIVISLAB", "DIXON", "DLF", "DRREDDY", "EICHERMOT", "ESCORTS", "EXIDEIND", "FEDERALBNK", "FINNIFTY", "FSL", "GAIL", "GLENMARK", "GMRINFRA", "GNFC", "GODREJCP", "GODREJPROP", "GRANULES", "GRASIM", "GSPL", "GUJGASLTD", "HAL", "HAVELLS", "HCLTECH", "HDFC", "HDFCAMC", "HDFCBANK", "HDFCLIFE", "HEROMOTOCO", "HINDALCO", "HINDCOPPER", "HINDPETRO", "HINDUNILVR", "HONAUT", "IBULHSGFIN", "ICICIBANK", "ICICIGI", "ICICIPRULI", "IDEA", "IDFC",
                         "IDFCFIRSTB", "IEX", "IGL", "INDHOTEL", "INDIACEM", "INDIAMART", "INDIGO", "INDUSINDBK", "INDUSTOWER", "INFY", "INTELLECT", "IOC", "IPCALAB", "IRCTC", "ITC", "JINDALSTEL", "JKCEMENT", "JSWSTEEL", "JUBLFOOD", "KOTAKBANK", "L&TFH", "LALPATHLAB", "LAURUSLABS", "LICHSGFIN", "LT", "LTI", "LTTS", "LUPIN", "M&M", "M&MFIN", "MANAPPURAM", "MARICO", "MARUTI", "MCDOWELL-N", "MCX", "METROPOLIS", "MFSL", "MGL", "MIDCPNIFTY", "MINDTREE", "MOTHERSON", "MPHASIS", "MRF", "MUTHOOTFIN", "NATIONALUM", "NAUKRI", "NAVINFLUOR", "NESTLEIND", "NIFTY", "NMDC", "NTPC", "OBEROIRLTY", "OFSS", "ONGC", "PAGEIND", "PEL", "PERSISTENT", "PETRONET", "PFC", "PIDILITIND", "PIIND", "PNB", "POLYCAB", "POWERGRID", "PVR", "RAIN", "RAMCOCEM", "RBLBANK", "RECLTD", "RELIANCE", "SAIL", "SBICARD", "SBILIFE", "SBIN", "SHREECEM", "SIEMENS", "SRF", "SRTRANSFIN", "SUNPHARMA", "SUNTV", "SYNGENE", "TATACHEM", "TATACOMM", "TATACONSUM", "TATAMOTORS", "TATAPOWER", "TATASTEEL", "TCS", "TECHM", "TITAN", "TORNTPHARM", "TORNTPOWER", "TRENT", "TVSMOTOR", "UBL", "ULTRACEMCO", "UPL", "VEDL", "VOLTAS", "WHIRLPOOL", "WIPRO", "ZEEL", "ZYDUSLIFE"]
            return HttpResponse(json.dumps(NFOScript), content_type="application/json")
    elif market == "MCX":
        todo = request.GET.get('todo')
        if todo == "expiry":
            script = request.GET.get('script')
            uniq = []
            for share in MCX:
                if share[16] == script and share[15] not in uniq:
                    uniq.append(share[15])
                    break
            return HttpResponse(json.dumps(uniq), content_type="application/json")
        elif todo == "strike":
            script = request.GET.get('script')
            expiry = request.GET.get('expiry')
            typeCall = request.GET.get('typeCall')
            uniq = []
            for share in MCX:
                if share[16] == script and share[15] == expiry and (share[6] == typeCall or share[6] == "" or share[6] == "XX") and share[7] not in uniq:
                    uniq.append(share[7])
                    break
            return HttpResponse(json.dumps(uniq), content_type="application/json")
        elif todo == "add":
            script = request.GET.get('script')
            expiry = request.GET.get('expiry')
            typeCall = request.GET.get('typeCall')
            strike = request.GET.get('strike')
            for share in MCX:
                if share[16] == script and share[15] == expiry and (share[6] == typeCall or share[6] == "" or share[6] == "XX") and share[7] == strike:
                    return HttpResponse(json.dumps({"symbol": share[3]}), content_type="application/json")
            return HttpResponse(json.dumps({"error": "Invalid Symbol"}), content_type="application/json")
        else:
            MCXScript = ["ALUMINIUM", "CARDAMOM", "CHANADEL", "COPPER", "CORIANDER", "COTTON", "CRUDEOIL", "GOLD", "GOLDGUINEA", "GOLDM", "GOLDPETAL", "KAPAS", "LEAD", "MCXBULLDEX",
                         "MCXENRGDEX", "MCXMETLDEX", "MENTHAOIL", "NATURALGAS", "NICKEL", "NICKELAUC", "RUBBER", "SILVER", "SILVERM", "SILVERMIC", "SOYABEAN", "STEELGZB", "WHEAT", "ZINC"]
            return HttpResponse(json.dumps(MCXScript), content_type="application/json")
    elif market == "Forex":
        todo = request.GET.get('todo')
        if todo == "expiry":
            script = request.GET.get('script')
            uniq = []
            for share in Forex:
                if share[16] == script and share[15] not in uniq:
                    uniq.append(share[15])
                    break
            return HttpResponse(json.dumps(uniq), content_type="application/json")
        elif todo == "strike":
            script = request.GET.get('script')
            expiry = request.GET.get('expiry')
            typeCall = request.GET.get('typeCall')
            uniq = []
            for share in Forex:
                if share[16] == script and share[15] == expiry and (share[6] == typeCall or share[6] == "" or share[6] == "XX") and share[7] not in uniq:
                    uniq.append(share[7])
                    break
            return HttpResponse(json.dumps(uniq), content_type="application/json")
        elif todo == "add":
            script = request.GET.get('script')
            expiry = request.GET.get('expiry')
            typeCall = request.GET.get('typeCall')
            strike = request.GET.get('strike')
            for share in Forex:
                if share[16] == script and share[15] == expiry and (share[6] == typeCall or share[6] == "" or share[6] == "XX") and share[7] == strike:
                    return HttpResponse(json.dumps({"symbol": share[3]}), content_type="application/json")
            return HttpResponse(json.dumps({"error": "Invalid Symbol"}), content_type="application/json")
        else:
            ForexScript = ["GBPINR", "USDINR", "JPYINR", "USDJPY",
                           "GBPUSD", "EURINR", "EURUSD", "ONMIBOR"]
            return HttpResponse(json.dumps(ForexScript), content_type="application/json")
    else:
        return HttpResponse(json.dumps({"error": "Invalid Market"}), content_type="application/json")
