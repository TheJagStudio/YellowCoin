from django.db import models
from django.contrib.auth.models import User
# add json field
from django.contrib.postgres.fields import JSONField


class UserAccount(models.Model):
    id = models.AutoField(primary_key=True)
    Account_Code = models.CharField(max_length=50)
    Account_Name = models.CharField(max_length=50)
    Account_Type = models.CharField(max_length=100)
    Partnership = models.CharField(max_length=100, default="5")
    Remarks = models.CharField(max_length=100)
    creator = models.CharField(max_length=100, default="admin")
    segments = models.JSONField(default={"segments": []})
    MCX = models.JSONField(default={"Brokerage Details": [],
                                    "Margin Details": [], "Other Details": []})
    NSE = models.JSONField(default={"Brokerage Details": [],
                                    "Margin Details": [], "Other Details": []})
    FOREX = models.JSONField(default={"Brokerage Details": [],
                                      "Margin Details": [], "Other Details": []})
    Between_HighLow = models.BooleanField(default=True)
    Auto_Square = models.BooleanField(default=True)
    Day_AutoSquare = models.BooleanField(default=True)
    Position_SquareOff = models.BooleanField(default=True)
    Linked_with_Ledger = models.BooleanField(default=True)
    Band_Script_Allow = models.BooleanField(default=True)
    Alert = models.FloatField(default=0.0)
    M2M_PL = models.IntegerField(default=0)
    Balance = models.IntegerField(default=100000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
