from rest_framework.response import Response
from rest_framework import generics, status
from django.contrib.auth import authenticate
from authentication.models import User
from authentication.serializers import SignupSerializer, LoginSerializer
from rest_framework.throttling import UserRateThrottle

# Create your views here.

class SignupView(generics.GenericAPIView):
    serializer_class = SignupSerializer
    throttle_classes = [UserRateThrottle]

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        phone = serializer.validated_data['phone']
        dob = serializer.validated_data['dob']

        email_exists = User.objects.filter(email=email).exists()
        if email_exists:
            return Response({"message": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)
        phone_exists = User.objects.filter(phone=phone).exists()
        if phone_exists:
            return Response({"message": "Phone already exists"}, status=status.HTTP_400_BAD_REQUEST)
        username_exists = User.objects.filter(username=username).exists()
        if username_exists:
            return Response({"message": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username,
                                        password=password,
                                        email=email,
                                        phone=phone,
                                        dob=dob)
        user.set_password(password)
        user.save()
        return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    throttle_classes = [UserRateThrottle]

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        username_exists = User.objects.filter(username=username).exists()
        if not username_exists:
            return Response({"message": "INVALID CREDENTIALS"}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        if user is None:
            return Response({"message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                "id": str(user.id),
                "username": str(user.username),
                "email": str(user.email),
                "phone": user.phone,
                "dob": user.dob,
                "token": user.token(),
            }, status=status.HTTP_200_OK)
