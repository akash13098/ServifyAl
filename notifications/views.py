from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Notification

class NotificationListAPIView(APIView):

    def get(self, request):
        notifications = Notification.objects.filter(user=request.user).order_by('-created_at')

        data = [
            {
                "title": n.title,
                "message": n.message,
                "is_read": n.is_read
            }
            for n in notifications
        ]

        return Response(data)