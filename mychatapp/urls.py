from django.urls import path
from mychatapp.views import index,detail, sentMessages, receiveMessage, chatNotification

urlpatterns = [
    path("", index, name="index"),
    path("friend/<str:pk>", detail, name="detail"),
    path("sent_msg/<str:pk>", sentMessages, name="sentMessages"),
    path("rec_msg/<str:pk>", receiveMessage, name="rec_msg"),
    path("notification/", chatNotification, name="notification"),
]