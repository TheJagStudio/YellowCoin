from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from user.models import UserAccount
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .models import tradeEdit, userEdit, autoSquare


@csrf_exempt
@login_required
def trade_edit(request):
    current_user = request.user
    if current_user.is_superuser:
        if request.method == 'POST':
            type = request.POST.get('type')
            from_date = request.POST.get('from')
            to_date = request.POST.get('to')
            #segment = request.POST.get('Segment')
            #script = request.POST.get('Script')
            Master = request.POST.get('Master')
            Broker = request.POST.get('Broker')
            query = tradeEdit.objects.all()
            data = {'data': []}
            for row in query:
                data['data'].append({"Action": row.tType, "Client": row.client, "Symbol": row.symbol, "Order_Type": row.order_type, "Lot": row.lot,
                                    "Qty": row.qty, "Order_Price": row.order_price, "Deleted_By": row.Deleted_by, "user_ip": row.userIp, "o_time": str(row.oTime), "d_time": str(row.dTime)})
            return HttpResponse(json.dumps(data), content_type="application/json")

        masters = UserAccount.objects.filter(
            Account_Type__contains="Master").all()
        brokers = UserAccount.objects.filter(
            Account_Type__contains="Broker").all()
        return render(request, 'log_trade_edit.html', {'current_user': current_user, 'masters': masters, 'brokers': brokers})
    else:
        user_account = UserAccount.objects.filter(user=current_user).first()
        if user_account.Account_Type == "User":
            givenUser = "False"
        else:
            givenUser = "True"
        if request.method == 'POST':
            type = request.POST.get('type')
            from_date = request.POST.get('from')
            to_date = request.POST.get('to')
            #segment = request.POST.get('Segment')
            #script = request.POST.get('Script')
            Master = request.POST.get('Master')
            Broker = request.POST.get('Broker')
            query = tradeEdit.objects.all()
            data = {'data': []}
            for row in query:
                data['data'].append({"Action": row.tType, "Client": row.client, "Symbol": row.symbol, "Order_Type": row.order_type, "Lot": row.lot,
                                    "Qty": row.qty, "Order_Price": row.order_price, "Deleted_By": row.Deleted_by, "user_ip": row.userIp, "o_time": str(row.oTime), "d_time": str(row.dTime)})
            return HttpResponse(json.dumps(data), content_type="application/json")
        masters = UserAccount.objects.filter(
            Account_Type__contains="Master").all()
        brokers = UserAccount.objects.filter(
            Account_Type__contains="Broker").all()
        return render(request, 'user_log_trade_edit.html', {'current_user': current_user, 'givenUser': givenUser, 'masters': masters, 'brokers': brokers})


@ csrf_exempt
@ login_required
def user_log(request):
    current_user = request.user
    if current_user.is_superuser:
        if request.method == 'POST':
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            from_date = body['fromDate']
            to_date = body['toDate']
            print(from_date, to_date)
            query = userEdit.objects.filter(
                dTime__range=[from_date, to_date]).all()
            data = {'data': []}
            for row in query:
                data['data'].append({"Action": row.action, "userCode": row.userCode,
                                    "userIp": "", "d_time": str(row.dTime)})
            return HttpResponse(json.dumps(data), content_type="application/json")
        return render(request, 'log_user_log.html', {'current_user': current_user})
    else:
        user_account = UserAccount.objects.filter(user=current_user).first()
        if user_account.Account_Type == "User":
            givenUser = "False"
        else:
            givenUser = "True"
        return render(request, 'log_user_log.html', {'current_user': current_user, 'givenUser': givenUser})


@login_required
def auto(request):
    current_user = request.user
    if current_user.is_superuser:
        return render(request, 'log_auto.html', {'current_user': current_user})


@login_required
def cross_log(request):
    current_user = request.user
    if current_user.is_superuser:
        return render(request, 'log_cross.html', {'current_user': current_user})


@login_required
def rejection_log(request):
    current_user = request.user
    if current_user.is_superuser:
        return render(request, 'log_rejection.html', {'current_user': current_user})
    else:
        user_account = UserAccount.objects.filter(user=current_user).first()
        if user_account.Account_Type == "User":
            givenUser = "False"
        else:
            givenUser = "True"
        return render(request, 'user_log_rejection.html', {'current_user': current_user, 'givenUser': givenUser})
