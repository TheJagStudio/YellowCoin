from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class tradeEdit(models.Model):
    tType = models.CharField(max_length=50)
    client = models.CharField(max_length=50)
    symbol = models.CharField(max_length=50)
    order_type = models.CharField(max_length=50)
    market = models.CharField(max_length=50)
    lot = models.IntegerField()
    qty = models.IntegerField()
    order_price = models.IntegerField()
    Deleted_by = models.CharField(max_length=50)
    userIp = models.CharField(max_length=50)
    oTime = models.DateField(auto_now_add=True)
    dTime = models.DateField()

    def __str__(self):
        return self.tType + " | " + self.client + " | " + self.symbol + " | " + self.order_type + " | " + self.Deleted_by


class userEdit(models.Model):
    userCode = models.CharField(max_length=50)
    action = models.CharField(max_length=50)
    userIp = models.CharField(max_length=50)
    dTime = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.userCode + " | " + self.action + " | " + str(self.dTime)


class autoSquare(models.Model):
    tTime = models.DateField()
    client = models.CharField(max_length=50)
    amount = models.CharField(max_length=50)

    def __str__(self):
        return self.tTime + " | " + self.client + " | " + self.amount
