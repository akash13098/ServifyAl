from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Booking, Payment
from .services import create_booking
from providers.models import Provider, ProviderService

class CreateBookingAPIView(APIView):

    def post(self, request):
        user = request.user

        provider_id = request.data.get('provider_id')
        service_id = request.data.get('service_id')
        scheduled_time = request.data.get('scheduled_time')
        address = request.data.get('address')

        provider = Provider.objects.get(id=provider_id)
        service = ProviderService.objects.get(id=service_id)

        booking = create_booking(
            user,
            provider,
            service,
            scheduled_time,
            address
        )

        return Response({"booking_id": booking.id}, status=status.HTTP_201_CREATED)
    
    
    
class AcceptBookingAPIView(APIView):
    
    def post(self, request, booking_id):
        provider = request.user.provider

        booking = Booking.objects.get(id=booking_id)

        accept_booking(booking, provider)

        return Response({"message": "Booking accepted"})
    
    
class StartServiceAPIView(APIView):
    
    def post(self, request, booking_id):
        provider = request.user.provider

        booking = Booking.objects.get(id=booking_id)

        start_service(booking, provider)

        return Response({"message": "Service started"})
    
    
class CompleteServiceAPIView(APIView):
    
    def post(self, request, booking_id):
        provider = request.user.provider

        booking = Booking.objects.get(id=booking_id)

        complete_service(booking, provider)

        return Response({"message": "Service completed"})
    
class CancelBookingAPIView(APIView):
    
    def post(self, request, booking_id):
        user = request.user

        booking = Booking.objects.get(id=booking_id)

        cancel_booking(booking, user)

        return Response({"message": "Booking cancelled"})
    
class CreateReviewAPIView(APIView):
    
    def post(self, request, booking_id):
        user = request.user

        rating = request.data.get('rating')
        comment = request.data.get('comment')

        booking = Booking.objects.get(id=booking_id)

        create_review(booking, user, rating, comment)

        return Response({"message": "Review submitted"})
    
    
class CreatePaymentAPIView(APIView):
    
    def post(self, request, booking_id):
        booking = Booking.objects.get(id=booking_id)

        payment = create_payment_order(booking)

        return Response({
            "order_id": payment.razorpay_order_id,
            "amount": payment.amount
        })
        
        
class VerifyPaymentAPIView(APIView):
    
    def post(self, request):
        order_id = request.data.get("order_id")
        payment_id = request.data.get("payment_id")

        payment = Payment.objects.get(razorpay_order_id=order_id)

        verify_payment(payment, payment_id)

        return Response({"message": "Payment successful"})