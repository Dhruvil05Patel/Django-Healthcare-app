from rest_framework import generics, permissions, serializers
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .serializers import RegisterSerializer


class EmailOrUsernameTokenObtainPairSerializer(TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make username optional and add email as alternate input
        if "username" in self.fields:
            self.fields["username"].required = False
        self.fields["email"] = serializers.EmailField(required=False)

    def validate(self, attrs):
        username = attrs.get("username")
        email = attrs.get("email")
        if not username and email:
            attrs["username"] = email
        if not attrs.get("username"):
            raise serializers.ValidationError({"email": "Email or username is required."})
        return super().validate(attrs)


class JWTLoginView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]
    serializer_class = EmailOrUsernameTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            "user": serializer.data,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }, status=201)


class JWTRefreshView(TokenRefreshView):
    permission_classes = [permissions.AllowAny]
