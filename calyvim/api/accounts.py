from django.contrib.auth import login
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers

from calyvim.models import User


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=False)
    full_name = serializers.CharField(required=False)
    password = serializers.CharField(required=True)


class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            # Log the request
            return Response(
                data={"errors": serializer.errors, "detail": "Invalid data entered."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = serializer.validated_data
        user: User = User.objects.filter(username=data.get("username")).first()
        if not user:
            return Response(
                data={"detail": "Either username or password entered is incorrect."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        if not user.check_password(data.get("password")):
            return Response(
                data={"detail": "Either username or password entered is incorrect."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        login(request, user)
        return Response(data={"detail": "Login success!"}, status=status.HTTP_200_OK)


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            # Log the request
            return Response(
                data={"errors": serializer.errors, "detail": "Invalid data entered."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        data = serializer.validated_data
        password = data.pop("password")
        user: User = User(**data)
        user.set_password(password)
        user.save()
        # Send user verification email
        login(request, user)
        return Response(
            data={"detail": "Your account has been created."},
            status=status.HTTP_201_CREATED,
        )


class UsernameCheckAPIView(APIView):
    def get(self, request):
        username = request.query_params.get("username")
        if not username:
            return Response(
                data={"detail": "Please provide username."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        username_available = not User.objects.filter(username=username).exists()
        return Response(
            data={"username_available": username_available}, status=status.HTTP_200_OK
        )
