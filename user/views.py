from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import UserAccount
from django.contrib.auth.models import User
from accounts.models import stack
from log.models import userEdit
from datetime import datetime


@login_required
def adduser(request):
    current_user = request.user
    user_account = UserAccount.objects.filter(user=current_user).first()
    allAccountTypes = ["Master One", "Master Two", "Master Three", "Master Four",
                       "Master Five", "Master Six", "Master Seven", "Broker", "Tele Master", "User"]
    accountTypes = []
    x = 0
    for accounts in allAccountTypes:
        if accounts == user_account.Account_Type or x == 1:
            if x == 1:
                accountTypes.append(accounts)
            x = 1
    if user_account.Account_Type != "User":
        if (request.method == 'POST'):
            Username = request.POST.get('Username')
            Password = request.POST.get('Password')

            newDefualtUser = User.objects.create_user(Username, '', Password)
            newDefualtUser.save()
            Account_Code = request.POST.get('Account_Code')
            Account_Name = request.POST.get('Account_Name')
            Account_Type = request.POST.get('inputGroupSelect01')
            Partnership = request.POST.get('Partnership')
            Remarks = request.POST.get('Remarks')
            request.session['MCX'] = {"Brokerage Details": [
            ], "Margin Details": [], "Other Details": []}
            request.session['NSE'] = {"Brokerage Details": [
            ], "Margin Details": [], "Other Details": []}
            request.session['FOREX'] = {"Brokerage Details": [
            ], "Margin Details": [], "Other Details": []}
            print(request.session['MCX'],
                  request.session['NSE'], request.session['FOREX'])
            request.session['segments'] = {"segments": []}
            MCX = request.POST.get('flexRadioDefault1')
            NSE = request.POST.get('flexRadioDefault2')
            FOREX = request.POST.get('flexRadioDefault3')
            if MCX == "checked":
                mcx_bd_userchoice = request.POST.get('mcx_bd_userchoice')
                print(mcx_bd_userchoice)
                if mcx_bd_userchoice != "select_id":
                    copyUser = UserAccount.objects.filter(
                        user=request.user).first()
                    request.session['MCX']["Brokerage Details"] = copyUser.MCX["Brokerage Details"]
                else:
                    mcx_bd_type = request.POST.get('mcx_bd_type')
                    mcx_bd_script = request.POST.get('mcx_bd_script')
                    mcx_bd_delivery = request.POST.get('mcx_bd_delivery')
                    mcx_bd_intradaycom = request.POST.get('mcx_bd_intradaycom')
                    request.session['MCX']["Brokerage Details"] = [
                        mcx_bd_type, mcx_bd_script, mcx_bd_delivery, mcx_bd_intradaycom]

                mcx_md_userchoice = request.POST.get('mcx_md_userchoice')
                print(mcx_md_userchoice)
                if mcx_md_userchoice != "select_id":
                    copyUser = UserAccount.objects.filter(
                        user=request.user).first()
                    request.session['MCX']["Margin Details"] = copyUser.MCX["Margin Details"]
                else:
                    mcx_md_type = request.POST.get('mcx_md_type')
                    mcx_md_totallotwise = request.POST.get(
                        'mcx_md_totallotwise')
                    mcx_md_script = request.POST.get('mcx_md_script')
                    mcx_md_maxorder = request.POST.get('mcx_md_maxorder')
                    mcx_md_positionlimit = request.POST.get(
                        'mcx_md_positionlimit')
                    request.session['MCX']["Margin Details"] = [
                        mcx_md_type, mcx_md_totallotwise, mcx_md_script, mcx_md_maxorder, mcx_md_positionlimit]

                mcx_od_userchoice = request.POST.get('mcx_od_userchoice')
                if mcx_od_userchoice != "select_id":
                    copyUser = UserAccount.objects.filter(
                        user=request.user).first()
                    request.session['MCX']["Other Details"] = copyUser.MCX["Other Details"]
                else:
                    mcx_od_type = request.POST.get('mcx_od_type')
                    mcx_od_allowscripts = request.POST.get(
                        'mcx_od_allowscripts')
                    mcx_od_noofscripts = request.POST.get('mcx_od_noofscripts')
                    request.session['MCX']["Other Details"] = [
                        mcx_od_type, mcx_od_allowscripts, mcx_od_noofscripts]

                request.session['segments']["segments"].append("MCX")
                print(request.session['segments']["segments"])
                print(request.session['MCX'])

            elif NSE == "checked":
                nse_bd_userchoice = request.POST.get('nse_bd_userchoice')
                if nse_bd_userchoice != "select_id":
                    copyUser = UserAccount.objects.filter(
                        user=request.user).first()
                    request.session['NSE']["Brokerage Details"] = copyUser.NSE["Brokerage Details"]
                else:
                    nse_bd_minscriptrate = request.POST.get(
                        'nse_bd_minscriptrate')
                    nse_bd_script = request.POST.get('nse_bd_script')
                    nse_bd_deliverycommision = request.POST.get(
                        'nse_bd_deliverycommision')
                    nse_bd_intradaycommision = request.POST.get(
                        'nse_bd_intradaycommision')
                    request.session['NSE']["Brokerage Details"] = [
                        nse_bd_minscriptrate, nse_bd_script, nse_bd_deliverycommision, nse_bd_intradaycommision]

                nse_md_userchoice = request.POST.get('nse_md_userchoice')
                if nse_md_userchoice != "select_id":
                    copyUser = UserAccount.objects.filter(
                        user=request.user).first()
                    request.session['NSE']["Margin Details"] = copyUser.NSE["Margin Details"]
                else:
                    nse_md_type = request.POST.get('mcx_md_type')
                    nse_md_totallotwise = request.POST.get(
                        'nse_md_totallotwise')
                    nse_md_script = request.POST.get('nse_md_script')
                    nse_md_maxorder = request.POST.get('nse_md_maxorder')
                    nse_md_positionlimit = request.POST.get(
                        'nse_md_positionlimit')
                    nse_md_nqv = request.POST.get('nse_md_nqv')
                    request.session['NSE']["Margin Details"] = [
                        nse_md_type, nse_md_totallotwise, nse_md_script, nse_md_maxorder, nse_md_positionlimit, nse_md_nqv]

                nse_od_userchoice = request.POST.get('nse_od_userchoice')
                if nse_od_userchoice != "select_id":
                    copyUser = UserAccount.objects.filter(
                        user=request.user).first()
                    request.session['NSE']["Other Details"] = copyUser.NSE["Other Details"]
                else:
                    nse_od_type = request.POST.get('nse_od_type')
                    nse_od_allowscripts = request.POST.get(
                        'nse_od_allowscripts')
                    nse_od_noofscripts = request.POST.get('nse_od_noofscripts')
                    nse_od_minratescriptblock = request.POST.get(
                        'nse_od_minratescriptblock')
                    request.session['NSE']["Other Details"] = [
                        nse_od_type, nse_od_allowscripts, nse_od_noofscripts, nse_od_minratescriptblock]

                request.session['segments']["segments"].append("NSE")
                print(request.session['segments']["segments"])
                print(request.session['NSE'])

            elif FOREX == "checked":
                forex_bd_userchoice = request.POST.get('forex_bd_userchoice')
                if forex_bd_userchoice != "select_id":
                    copyUser = UserAccount.objects.filter(
                        user=request.user).first()
                    request.session['FOREX']["Brokerage Details"] = copyUser.FOREX["Brokerage Details"]
                else:
                    forex_bd_type = request.POST.get('forex_bd_type')
                    forex_bd_symbol = request.POST.get('forex_bd_symbol')
                    forex_bd_deliverycom = request.POST.get(
                        'forex_bd_deliverycom')
                    forex_bd_intradaycom = request.POST.get(
                        'forex_bd_intradaycom')
                    request.session['FOREX']["Brokerage Details"] = [
                        forex_bd_type, forex_bd_symbol, forex_bd_deliverycom, forex_bd_intradaycom]

                forex_md_userchoice = request.POST.get('forex_md_userchoice')
                if forex_md_userchoice != "select_id":
                    copyUser = UserAccount.objects.filter(
                        user=request.user).first()
                    request.session['FOREX']["Margin Details"] = copyUser.FOREX["Margin Details"]
                else:
                    forex_md_type = request.POST.get('forex_md_type')
                    forex_md_totallotwise = request.POST.get(
                        'forex_md_totallotwise')
                    forex_md_symbol = request.POST.get('forex_md_symbol')
                    forex_md_maxorder = request.POST.get('forex_md_maxorder')
                    forex_md_positionlimit = request.POST.get(
                        'forex_md_positionlimit')
                    request.session['FOREX']["Margin Details"] = [
                        forex_md_type, forex_md_totallotwise, forex_md_symbol, forex_md_maxorder, forex_md_positionlimit]

                forex_od_userchoice = request.POST.get('forex_od_userchoice')
                if forex_od_userchoice != "select_id":
                    copyUser = UserAccount.objects.filter(
                        user=request.user).first()
                    request.session['FOREX']["Other Details"] = copyUser.FOREX["Other Details"]
                else:
                    forex_od_type = request.POST.get('nse_od_type')
                    forex_od_allowsymbol = request.POST.get(
                        'forex_od_allowsymbol')
                    forex_od_noofsymbol = request.POST.get(
                        'forex_od_noofsymbol')
                    request.session['FOREX']["Other Details"] = [
                        forex_od_type, forex_od_allowsymbol, forex_od_noofsymbol]

                request.session['segments']["segments"].append("FOREX")
                print(request.session['segments']["segments"])
                print(request.session['FOREX'])

            if request.POST.get('inlineRadioOptions') == "Yes":
                order_bt_hl = True
            else:
                order_bt_hl = False
            if request.POST.get('Apply Auto Square') == "Yes":
                apply_auto_square = True
            else:
                apply_auto_square = False
            if request.POST.get('Intra Day Auto Square') == "Yes":
                Intra_Day_Auto_Square = True
            else:
                Intra_Day_Auto_Square = False
            if request.POST.get('Only Position SquareOff') == "Yes":
                Only_Position_SquareOff = True
            else:
                Only_Position_SquareOff = False
            if request.POST.get('M2M') == "Yes":
                M2M_Linked_with_Ledger = True
            else:
                M2M_Linked_with_Ledger = False
            if request.POST.get('Band Script Allow') == "Yes":
                Band_Script_Allow = True
            else:
                Band_Script_Allow = False
            alertper = request.POST.get('alertper')
            if(alertper == ""):
                alertper = 0
            M2MPL = request.POST.get('M2MPL')
            if(M2MPL == ""):
                M2MPL = 0
            Balance = request.POST.get('Balance')
            if(Balance == ""):
                Balance = 100000
            print(order_bt_hl, apply_auto_square, Intra_Day_Auto_Square, Only_Position_SquareOff,
                  M2M_Linked_with_Ledger, Band_Script_Allow, alertper, M2MPL, Balance)
            newEntry = userEdit(
                userCode=Account_Code, action="Created", userIp="", dTime=datetime.now())
            newEntry.save()
            newUser = UserAccount(Account_Code=Account_Code, Account_Name=Account_Name, Account_Type=Account_Type, Partnership=Partnership, Remarks=Remarks, creator=current_user.username, segments=request.session['segments'], MCX=request.session['MCX'], NSE=request.session['NSE'],
                                  FOREX=request.session['FOREX'], Between_HighLow=order_bt_hl, Auto_Square=apply_auto_square, Day_AutoSquare=Intra_Day_Auto_Square, Position_SquareOff=Only_Position_SquareOff, Linked_with_Ledger=M2M_Linked_with_Ledger, Band_Script_Allow=Band_Script_Allow, Alert=alertper, M2M_PL=M2MPL, Balance=Balance, user=newDefualtUser)
            newUser.save()
            print(newUser)

        allUser = User.objects.all()
        allUserNames = []
        if current_user.is_superuser:
            accountTypes = ["Master One", "Master Two", "Master Three", "Master Four",
                            "Master Five", "Master Six", "Master Seven", "Broker", "Tele Master", "User"]
        print(accountTypes)

        for user in allUser:
            allUserNames.append(user.username)
        return render(request, 'create_user.html', {'current_user': current_user, "accountTypes": accountTypes, "users": allUserNames})


@login_required
def user_list(request):
    current_user = request.user
    user_account = UserAccount.objects.filter(user=current_user).first()
    if user_account.Account_Type != "User":
        user_list = UserAccount.objects.filter(
            creator=current_user.username).all()
        return render(request, 'user_list.html', {'current_user': current_user, 'user_list': user_list})
