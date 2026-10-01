import requests
from rest_framework.response import Response
from rest_framework import generics
from .serializers import PaymentInitSerializer
from .models import PaymentRecord
from rest_framework import permissions
from rest_framework import throttling
from datetime import datetime
from decouple import config

# Create your views here.
class PaymentInitViews(generics.GenericAPIView):
    serializer_class = PaymentInitSerializer
    queryset = PaymentRecord.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [throttling.UserRateThrottle]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        ref = f"test-{str(datetime.now())}".replace(" ", "").replace(":", "")
        if serializer.is_valid():
            amount_in_kobo = int(serializer.validated_data.get("amount") * 100)
            email = serializer.validated_data.get("email")
            channels = ['card', 'bank', 'bank_transfer', 'apple_pay', 'google_pay']
            gateway_url = 'https://api.paystack.co/transaction/initialize'
            header ={
                "Authorization" : f"Bearer {config("PAYSTACK_SECRET_KEY")}",
                "content_type": "application/json"
            }
            payload = {
                "email": email,
                "amount": amount_in_kobo,
                "channels": channels,
                "ref":ref,
            }
            try:
                response = requests.post(url=gateway_url, headers=header, json=payload)
                resp_data = response.json()
                payment_url = resp_data["data"]["authorization_url"]
                return Response({
                    "payment_url" : payment_url,
                    "reference": resp_data["data"]["reference"]
                }, status=200)
            except requests.exceptions.RequestException as e:
                return Response({"error": "Gateway connection failed"}, status=503)
        return Response(serializer.errors, status=400)