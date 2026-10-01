from rest_framework import serializers
from .models import PaymentRecord
import uuid
class PaymentInitSerializer(serializers.Serializer):
    class Meta:
        model = PaymentRecord
        field = ['order_id', 'amount', 'email']


