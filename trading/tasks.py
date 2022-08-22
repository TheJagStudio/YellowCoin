from celery import shared_task
from .views import dataB
from channels.layers import get_channel_layer
import asyncio
import json


@shared_task(bind=True)
def update_data(self, stocks):
    temp = dataB(stocks)
    channel_layer = get_channel_layer()
    print(channel_layer)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(channel_layer.group_send("stock_track", {
        'type': 'send_stock_update',
        'message': temp,
    }))
    return 'Task completed'