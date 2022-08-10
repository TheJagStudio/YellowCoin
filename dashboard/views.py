from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from user.models import UserAccount


@login_required
def dashboard(request):
    current_user = request.user
    if current_user.is_superuser:
        accounts = UserAccount.objects.all()
        count = [0, 0, 0]
        for account in accounts:
            if "Master" in account.Account_Type:
                count[0] += 1
            if "Broker" in account.Account_Type:
                count[1] += 1
            if "User" in account.Account_Type:
                count[2] += 1
        return render(request, 'dashboard_trades.html', {'current_user': current_user, 'count': count})
    else:
        user_account = UserAccount.objects.filter(user=current_user).first()
        if user_account.Account_Type == "User":
            givenUser = "False"
        else:
            givenUser = "True"
        accounts = UserAccount.objects.all()
        count = [0, 0, 0]
        for account in accounts:
            if "Master" in account.Account_Type:
                count[0] += 1
            if "Broker" in account.Account_Type:
                count[1] += 1
            if "User" in account.Account_Type:
                count[2] += 1
        return render(request, 'user_dashboard_trades.html', {'current_user': current_user, 'givenUser': givenUser, 'count': count})


@login_required
def trade_entry(request):
    current_user = request.user
    if current_user.is_superuser:
        return render(request, 'dashboard_trade_entry.html', {'current_user': current_user})


@login_required
def exected_order(request):
    current_user = request.user
    if current_user.is_superuser:
        return render(request, 'dashboard_executed_orders.html', {'current_user': current_user})


@login_required
def running_orders(request):
    current_user = request.user
    if current_user.is_superuser:
        return render(request, 'dashboard_running_orders.html', {'current_user': current_user})


@login_required
def summary_reports(request):
    current_user = request.user
    if current_user.is_superuser:
        return render(request, 'dashboard_summary_report.html', {'current_user': current_user})


@login_required
def M2M(request):
    current_user = request.user
    if current_user.is_superuser:
        return render(request, 'dashboard_m2m.html', {'current_user': current_user})


@login_required
def user(request):
    current_user = request.user
    if current_user.is_superuser:
        return render(request, 'dashboard_user.html', {'current_user': current_user})
