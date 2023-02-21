import base64
import json

from django.http import JsonResponse
from .models import Notification


def notification(request):
    index = request.GET.get('idx', None)
    message = request.GET.get('msg', None)
    sensor_data = request.GET.get('data', None)
    if None in (index, message, sensor_data):
        return JsonResponse({}, status=400)
    notif = Notification.objects.create(event_index=index, event_message=message,
                                        event_sensor_data=json.loads(base64.urlsafe_b64decode(sensor_data).decode()))
    return JsonResponse({'created_object_index': notif.event_index}, status=201)
