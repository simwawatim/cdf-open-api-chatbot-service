from django.urls import path
from .views import ChatAPIView, ChatEntryListCreateAPIView

urlpatterns = [
    path("chat-api/", ChatAPIView.as_view(), name="chat-api"),
    path('qa/', ChatEntryListCreateAPIView.as_view(), name='chatentry-list-create'),

]
