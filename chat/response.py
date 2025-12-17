from rest_framework.response import Response

def send_response(*, status, message, data=None, status_code=200, http_status=200):
    return Response(
        {
            "status": status,
            "message": message,
            "data": data,
            "status_code": status_code,
            "http_status": http_status
        },
        status=http_status
    )
