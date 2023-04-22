from django.contrib import auth
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from accounts import messages
from accounts.models import User, Profile


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, min_length=6, write_only=True)
    tokens = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'tokens']

    def create(self, validated_data):
        self.user = get_user_model().objects.create_user(**validated_data)
        self.user.save()
        return self.user

    def get_tokens(self, obj):
        user = get_user_model().objects.get(email=self.user.email)

        return {
            'access': user.tokens()['access'],
            'refresh': user.tokens()['refresh'],
        }


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = get_user_model().objects.get(email=obj['email'])

        return {
            'access': user.tokens()['access'],
            'refresh': user.tokens()['refresh']
        }

    class Meta:
        model = User
        fields = ['email', 'password', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        user = auth.authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed('Вы ввели неправильный логин или пароль!')
        if not user.is_active:
            raise AuthenticationFailed('Аккаунт отключен, обратитесь к администратору')
        return super().validate(attrs)


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(
        error_messages={'blank': messages.ENTER_REFRESH_TOKEN}
    )

    default_error_messages = {'bad_token': messages.TEXT_UNAUTHORIZED}

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')


class UserDetailSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField

    class Meta:
        model = get_user_model()
        fields = [
            'id', 'is_superuser', 'is_staff', 'is_active', 'email', 'created_at', 'updated_at'
        ]


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['name', 'avatar', 'created_at', 'updated_at']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)
