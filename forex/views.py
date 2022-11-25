from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from user.models import UserAccount
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json


@login_required
def forex_wacthlist(request):
    current_user = request.user
    if current_user.is_superuser:
        symbol = ["GBPINR", "USDINR", "JPYINR", "USDJPY",
                  "GBPUSD", "EURINR", "EURUSD", "ONMIBOR"]
        return render(request, 'forex_watchlist.html', {'current_user': current_user, 'symbols': symbol})
    else:
        user_account = UserAccount.objects.filter(user=current_user).first()
        if user_account.Account_Type == "User":
            givenUser = "False"
        else:
            givenUser = "True"
        return render(request, 'user_forex_watchlist.html', {'current_user': current_user, 'givenUser': givenUser})


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
