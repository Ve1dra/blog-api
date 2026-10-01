from rest_framework import serializers
from authentication.models import User
import datetime

class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'phone', 'password', 'dob', 'is_active', 'is_staff', 'is_superuser')

    def validate(self, attrs):
        """attrs is the parameter that holds the all key - value in the field's variable"""
        phone = attrs["phone"]
        if not phone.startswith('+234'):
            raise serializers.ValidationError("Phone number must start with +234")
        if len(phone) != 14:
            raise serializers.ValidationError("Phone number must be exactly 14 characters long")
        try:
            int(phone[1:])
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