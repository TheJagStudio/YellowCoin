from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import stack, cashEntry, depositeEntry, jvEntry
from django.contrib.auth.models import User
from user.models import UserAccount
# import db.session


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ('You have been logged in!'))
            if stack.objects.filter(username=request.user).exists():
                return redirect('/dashboard')
            else:
                print("New stack created for" + request.user.username)
                newstack = stack(username=request.user, stocks={"data": []})
                newstack.save()
                print(newstack)
                return redirect('/dashboard')
        else:
            messages.success(request, ('Error logging in - please try again.'))
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')


@login_required
def logout_user(request):
    logout(request)
    messages.success(request, ('You have been logged out!'))
    return redirect('accounts:login_user')


@login_required
def cash_ledge(request):
    current_user = request.user
    if current_user.is_superuser:
        return render(request, 'account_ledge.html', {'current_user': current_user})


@login_required
def cash_entry(request):
    current_user = request.user
    if request.method == 'POST':
        transaction_type = request.POST.get('type')
        accountCode = request.POST.get('accountCode')
        accountName = request.POST.get('accountName')
        tDate = request.POST.get('tDate')
        amount = request.POST.get('amount')
        remarks = request.POST.get('remarks')
        submit = request.POST.get('submit')
        users = User.objects.all()
        if submit == "Save":
            vid = request.POST.get('Vid')
            if vid == "":
                vid = None
            upEntry = cashEntry.objects.filter(id=vid).first()
            if upEntry == None:
                newEntry = cashEntry(accountCode=accountCode, accountName=accountName, date=tDate, tType=transaction_type,
                                     amount=amount, remark=remarks, username=request.user)
                newEntry.save()
            else:
                upEntry.accountCode = accountCode
                upEntry.accountName = accountName
                upEntry.date = tDate
                upEntry.tType = transaction_type
                upEntry.amount = amount
                upEntry.remark = remarks
                upEntry.username = request.user
                upEntry.save()

        else:
            delEntry = cashEntry.objects.filter(accountCode=accountCode, accountName=accountName, date=tDate,
                                                tType=transaction_type, amount=amount, remark=remarks, username=request.user).first()
            delEntry.delete()

    if current_user.is_superuser:
        users = User.objects.all()
        entries = cashEntry.objects.all()
        userAcc = UserAccount.objects.filter(user=current_user).first()
        balance = userAcc.Balance
        return render(request, 'account_entry.html', {'current_user': current_user, 'users': users, 'entries': entries, 'balance': balance})
    else:
        user_account = UserAccount.objects.filter(user=current_user).first()
        if user_account.Account_Type == "User":
            givenUser = "False"
        else:
            givenUser = "True"
        entries = cashEntry.objects.filter(username=current_user)
        return render(request, 'account_entry.html', {'current_user': current_user, 'users': users, 'givenUser': givenUser, 'entries': entries})


@login_required
def deposit_entry(request):
    current_user = request.user
    if request.method == 'POST':
        transaction_type = request.POST.get('type')
        accountCode = request.POST.get('accountCode')
        accountName = request.POST.get('accountName')
        tDate = request.POST.get('tDate')
        amount = request.POST.get('amount')
        remarks = request.POST.get('remarks')
        submit = request.POST.get('submit')
        users = User.objects.all()
        if submit == "Save":
            vid = request.POST.get('Vid')
            if vid == "":
                vid = None
            upEntry = depositeEntry.objects.filter(id=vid).first()
            if upEntry == None:
                newEntry = depositeEntry(accountCode=accountCode, accountName=accountName, date=tDate, tType=transaction_type,
                                         amount=amount, remark=remarks, username=request.user)
                newEntry.save()
            else:
                upEntry.accountCode = accountCode
                upEntry.accountName = accountName
                upEntry.date = tDate
                upEntry.tType = transaction_type
                upEntry.amount = amount
                upEntry.remark = remarks
                upEntry.username = request.user
                upEntry.save()
        else:
            delEntry = depositeEntry.objects.filter(accountCode=accountCode, accountName=accountName, date=tDate,
                                                    tType=transaction_type, amount=amount, remark=remarks, username=request.user).first()
            delEntry.delete()

    if current_user.is_superuser:
        users = User.objects.all()
        entries = depositeEntry.objects.all()
        userAcc = UserAccount.objects.filter(user=current_user).first()
        balance = userAcc.Balance
        return render(request, 'account_deposit.html', {'current_user': current_user, 'users': users, 'entries': entries, 'balance': balance})
    else:
        user_account = UserAccount.objects.filter(user=current_user).first()
        if user_account.Account_Type == "User":
            givenUser = "False"
        else:
            givenUser = "True"
        entries = depositeEntry.objects.filter(username=current_user)
        return render(request, 'account_deposit.html', {'current_user': current_user, 'users': users, 'givenUser': givenUser, 'entries': entries})


@login_required
def jv(request):
    current_user = request.user
    if request.method == 'POST':
        transaction_type = request.POST.get('type')
        accountCode = request.POST.get('accountCode')
        accountName = request.POST.get('accountName')
        tDate = request.POST.get('tDate')
        amount = request.POST.get('amount')
        remarks = request.POST.get('remarks')
        submit = request.POST.get('submit')
        users = User.objects.all()
        if submit == "Save":
            vid = request.POST.get('Vid')
            if vid == "":
                vid = None
            upEntry = jvEntry.objects.filter(id=vid).first()
            if upEntry == None:
                newEntry = jvEntry(accountCode=accountCode, accountName=accountName, date=tDate, tType=transaction_type,
                                   amount=amount, remark=remarks, username=request.user)
                newEntry.save()
            else:
                upEntry.accountCode = accountCode
                upEntry.accountName = accountName
                upEntry.date = tDate
                upEntry.tType = transaction_type
                upEntry.amount = amount
                upEntry.remark = remarks
                upEntry.username = request.user
                upEntry.save()

        else:
            delEntry = jvEntry.objects.filter(accountCode=accountCode, accountName=accountName, date=tDate,
                                              tType=transaction_type, amount=amount, remark=remarks, username=request.user).first()
            delEntry.delete()

    if current_user.is_superuser:
        users = User.objects.all()
        entries = jvEntry.objects.all()
        userAcc = UserAccount.objects.filter(user=current_user).first()
        balance = userAcc.Balance
        return render(request, 'account_jv.html', {'current_user': current_user, 'users': users, 'entries': entries, 'balance': balance})
    else:
        user_account = UserAccount.objects.filter(user=current_user).first()
        if user_account.Account_Type == "User":
            givenUser = "False"
        else:
            givenUser = "True"
        entries = jvEntry.objects.filter(username=current_user)
        return render(request, 'account_jv.html', {'current_user': current_user, 'users': users, 'givenUser': givenUser, 'entries': entries})


@login_required
def jv_broker(request):
    current_user = request.user

    if current_user.is_superuser:
        brokers = UserAccount.objects.filter(Account_Type="Broker").all()
        return render(request, 'account_jv_broker.html', {'current_user': current_user, 'brokers': brokers})


@login_required
def jv_broker_delete(request):
    current_user = request.user
    if current_user.is_superuser:
        return render(request, 'account_jv_broker_delete.html', {'current_user': current_user})


@login_required
def valan(request):
    current_user = request.user
    if current_user.is_superuser:
        return render(request, 'account_valan.html', {'current_user': current_user})
