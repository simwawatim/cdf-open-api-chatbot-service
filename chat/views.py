# views.py
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import status
from chat.response import send_response
from chat.serializers import ChatInputSerializer

class ChatAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        serializer = ChatInputSerializer(data=request.data)

        if not serializer.is_valid():
            errors = serializer.errors
            if "message" in errors:
                error_msg = errors["message"][0] 
            else:
                error_msg = "Validation error"

            return send_response(
                status="fail",
                message=f"'message' field error: {error_msg}",
                data=None,
                status_code=400,
                http_status=status.HTTP_400_BAD_REQUEST
            )

        user_message = serializer.validated_data["message"]

        ai_reply = f"I received your message: {user_message}"

        return send_response(
            status="success",
            message="Response generated successfully",
            data={"reply": ai_reply},
            status_code=200,
            http_status=status.HTTP_200_OK
        )
