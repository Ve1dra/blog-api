from django.db import models
from authentication.models import User
import uuid
# Create your models here.
class PaymentRecord(models.Model):
    order_id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    email = models.EmailField()
    amount = models.DecimalField(decimal_places=2, max_digits=12)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment_source')