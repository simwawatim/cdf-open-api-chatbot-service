from django.urls import path
from chat.views import ChatAPIView

urlpatterns = [
    path("chat/", ChatAPIView.as_view()),
]
