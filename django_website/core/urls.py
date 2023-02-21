from django.urls import path

from .views import notification

urlpatterns = [
    path('notification/', notification, name='notification'),
]
