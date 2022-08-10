from django.db import models
from django.contrib.auth.models import User


class stack(models.Model):
    stocks = models.JSONField()
    username = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.username.username


class cashEntry(models.Model):
    id = models.AutoField(primary_key=True)
    accountCode = models.CharField(max_length=50)
    accountName = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    tType = models.CharField(max_length=50)
    amount = models.FloatField(default=0.00)
    remark = models.CharField(max_length=500)
    username = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.username.username


class depositeEntry(models.Model):
    id = models.AutoField(primary_key=True)
    accountCode = models.CharField(max_length=50)
    accountName = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    tType = models.CharField(max_length=50)
    amount = models.FloatField(default=0.00)
    remark = models.CharField(max_length=500)
    username = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.username.username


class jvEntry(models.Model):
    id = models.AutoField(primary_key=True)
    accountCode = models.CharField(max_length=50)
    accountName = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    tType = models.CharField(max_length=50)
    amount = models.FloatField(default=0.00)
    remark = models.CharField(max_length=500)
    username = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.username.username

