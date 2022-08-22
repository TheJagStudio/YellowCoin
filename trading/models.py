from django.db import models
from django.contrib.auth.models import User


class trades(models.Model):
    id = models.AutoField(primary_key=True)
    time = models.DateTimeField(auto_now_add=True)
    market = models.CharField(max_length=100)
    script = models.CharField(max_length=100)
    bs = models.CharField(max_length=100)
    orderType = models.CharField(max_length=100)
    lot = models.IntegerField()
    qty = models.IntegerField()
    orderPrice = models.FloatField()
    status = models.CharField(max_length=100)
    oTime = models.DateTimeField(auto_now_add=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id) + " | " + self.user_id.username + " | " + self.script + " | " + self.time.strftime('%Y-%m-%d')
