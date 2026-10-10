from rest_framework import serializers
from authentication.models import User
import datetime
from django.core.validators import RegexValidator


nigerian_phone_regex = RegexValidator(
    regex=r'^(?:\+234|0)(?:7[0-1]|8[0-1]|9[0-1])\d{8}$',
    message="Enter a valid Nigerian phone number starting with +234 or 0."
)


class SignupSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(
        validators=[nigerian_phone_regex],
        max_length=14,
    )
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'phone', 'password', 'dob', 'is_active', 'is_staff', 'is_superuser')

    def validate(self, attrs):
        """attrs is the parameter that holds the all key - value in the field's variable"""
        phone_number = attrs["phone"]

        if len(phone_number) not in (11, 14):
            raise serializers.ValidationError("Phone number must be 11 or 14 characters long")
        try:
            int(phone_number[1:])
        except:
            raise serializers.ValidationError("Phone number must be numbers only")

        username = attrs["username"]
        if username.strip().lower() == 'string':
            raise serializers.ValidationError("Username default must be changed!")

        dob = attrs.get("dob")
        if dob:
            today = datetime.date.today()
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            if age < 18:
                raise serializers.ValidationError("Sorry! You must be at least 18 years old.")

        password = attrs["password"]
        if len(password) < 8:
            raise serializers.ValidationError("Password must be exactly 8 characters long")
        return attrs

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})