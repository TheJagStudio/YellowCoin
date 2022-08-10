from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from pytz import timezone
# from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yellowcoin.settings')

app = Celery('yellowcoin')
app.conf.enable_utc = False
app.conf.update(timezone = 'Asia/Kolkata')

app.config_from_object(settings, namespace='CELERY')
stocksA = ["INTC:NASDAQ","AAPL:NASDAQ","MSFT:NASDAQ","GOOG:NASDAQ","AMZN:NASDAQ","ITC:NSE","IDEA:NSE","YESBANK:NSE","BHEL:NSE","RELIANCE:NSE","TCS:NSE","HDFC:NSE","ICICIBANK:NSE","MARUTI:NSE","WIPRO:NSE"]
app.conf.beat_schedule = {
    # 'every-10-seconds': {
    #     'task': 'trading.tasks.update_data',
    #     'schedule': 10,
    #     'args': (stocksA,)
    # }
}

app.autodiscover_tasks()
@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))