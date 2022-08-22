from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from user.models import UserAccount
from django.http import HttpResponse
import finnhub
import requests
from django.views.decorators.csrf import csrf_exempt
import json

exchanges = ['oanda', 'fxcm', 'forex.com', 'pepperstone', 'icmtrader',
             'fxpro', 'pepperstoneuk', 'ic markets', 'fxpig']


def get_api_key():
    headers = {
        'Cookie': 'token=cai5jiaad3i7auh4kegg'
    }
    response = requests.request(
        "GET", "https://finnhub.io/api/edit?type=sandboxApiKey", headers=headers)
    return response.json()["sandboxApiKey"]


finnhub_client = finnhub.Client(api_key=get_api_key())
dataForex = finnhub_client.forex_symbols('OANDA')


@login_required
def forex_wacthlist(request):
    current_user = request.user
    if current_user.is_superuser:
        symbols = []
        for data in dataForex:
            symbols.append(data['displaySymbol'])
        return render(request, 'forex_watchlist.html', {'current_user': current_user, 'symbols': symbols})
    else:
        user_account = UserAccount.objects.filter(user=current_user).first()
        if user_account.Account_Type == "User":
            givenUser = "False"
        else:
            givenUser = "True"
        return render(request, 'user_forex_watchlist.html', {'current_user': current_user, 'givenUser': givenUser})


@csrf_exempt
def forex_data(request):
    symbol = request.GET.get('symbol')
    print(symbol)
    data = finnhub_client.forex_rates(base=symbol.split("/")[0])
    data = data['quote'][symbol.split("/")[1]]
    return HttpResponse(json.dumps({"data": data}, indent=4), content_type="application/json")


@login_required
def forex_trades(request):
    current_user = request.user
    if current_user.is_superuser:
        return render(request, 'forex_trades.html', {'current_user': current_user})
    else:
        user_account = UserAccount.objects.filter(user=current_user).first()
        if user_account.Account_Type == "User":
            givenUser = "False"
        else:
            givenUser = "True"
        return render(request, 'user_forex_trades.html', {'current_user': current_user, 'givenUser': givenUser})


@login_required
def forex_portfolio(request):
    current_user = request.user
    if current_user.is_superuser:
        return render(request, 'forex_portfolio.html', {'current_user': current_user})
    else:
        user_account = UserAccount.objects.filter(user=current_user).first()
        if user_account.Account_Type == "User":
            givenUser = "False"
        else:
            givenUser = "True"
        return render(request, 'user_forex_portfolio.html', {'current_user': current_user, 'givenUser': givenUser})


@login_required
def forex_margin(request):
    current_user = request.user
    if current_user.is_superuser:
        return render(request, 'forex_margin.html', {'current_user': current_user})
