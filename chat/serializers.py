from rest_framework import serializers
from .models import ChatEntry

class ChatEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatEntry
        fields = ['id', 'question', 'answer']
