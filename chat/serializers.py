# serializers.py
from rest_framework import serializers

class ChatInputSerializer(serializers.Serializer):
    message = serializers.CharField(
        required=True,
        allow_blank=False, 
        max_length=2000
    )
