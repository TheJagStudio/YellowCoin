from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from user.models import UserAccount

# Create your views here.


@login_required
def track_report(request):
    current_user = request.user
    if request.method == 'POST':
        return render(request, 'reportPdf.html', {'current_user': current_user})
    if current_user.is_superuser:
        return render(request, 'report_track.html', {'current_user': current_user})


@login_required
def ledge_report(request):
    current_user = request.user
    if current_user.is_superuser:
        return render(request, 'report_ledge.html', {'current_user': current_user})
    else:
        user_account = UserAccount.objects.filter(user=current_user).first()
        if user_account.Account_Type == "User":
            givenUser = "False"
        else:
            givenUser = "True"
        return render(request, 'user_report_ledge.html', {'current_user': current_user, 'givenUser': givenUser})


@login_required
def deposit_report(request):
    current_user = request.user
    if current_user.is_superuser:
        return render(request, 'report_deposit.html', {'current_user': current_user})
    else:
        user_account = UserAccount.objects.filter(user=current_user).first()
        if user_account.Account_Type == "User":
            givenUser = "False"
        else:
            givenUser = "True"
        return render(request, 'user_report_deposit.html', {'current_user': current_user, 'givenUser': givenUser})


@login_required
def trail_report(request):
    current_user = request.user
    if current_user.is_superuser:
        return render(request, 'report_trail.html', {'current_user': current_user})


@login_required
def client_report(request):
    current_user = request.user
    if current_user.is_superuser:
        return render(request, 'report_client.html', {'current_user': current_user})
