from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import json
# import csrf
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from user.models import UserAccount
import csv
from accounts.models import stack
from trading.views import ApiF

MCX = []
NSE = []
NFO = []
MCXS = []
NSES = []
NFOS = []
with open("static/all_Symbols.csv", 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        if row[11] == "MCX":
            MCX.append(row)
            MCXS.append(row[2])
        elif row[11] == "NSE" and row[3] != "":
            NSE.append(row)
            NSES.append(row[3])
        elif row[11] == "NFO" and row[3] != "":
            NFO.append(row)
            NFOS.append(row[3])


@csrf_exempt
def login_user(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    username = body['username']
    password = body['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        userType = UserAccount.objects.filter(
            user=request.user).first().Account_Type
        stringOutput = {'status': 'success', 'message': 'Login successful', "name": request.user.username,
                        "type": userType}
        return HttpResponse(json.dumps(stringOutput, indent=4), content_type="application/json")
    else:
        return HttpResponse(json.dumps({"success": "False"}, indent=4), content_type="application/json")


@csrf_exempt
def segmentData(request):
    data = {"NSE": NSES, "NFO": NFOS, "MCX": MCXS}
    return HttpResponse(json.dumps(data, indent=4), content_type="application/json")
