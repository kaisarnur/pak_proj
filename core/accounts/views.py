from rest_framework import generics, status, permissions, viewsets
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts import messages
from accounts.models import User, Profile
from accounts.serializers import (
    RegisterSerializer, LoginSerializer, LogoutSerializer, UserDetailSerializer,
    ProfileSerializer
)


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    @staticmethod
    def get_access_token(serializer):
        tokens = serializer.data.get('tokens', None)
        token = tokens.get('access', None)
        return token

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DeleteAccountView(APIView):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):  # noqa
        request.user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LoginApiView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserDetailView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserDetailSerializer

    def get(self, request):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status.HTTP_200_OK)


class ProfileViewSet(viewsets.GenericViewSet):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [FormParser, MultiPartParser]

    def retrieve(self, request):
        try:
            serializer = self.serializer_class(request.user.profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response({'error': messages.PROFILE_DOES_NOT_EXISTS},
                            status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request):
        try:
            serializer = self.serializer_class(request.user.profile, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except Profile.DoesNotExist:
            return Response({'error': messages.PROFILE_DOES_NOT_EXISTS},
                            status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request):
        try:
            instance = request.user.profile
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Profile.DoesNotExist:
            return Response({'error': messages.PROFILE_DOES_NOT_EXISTS},
                            status=status.HTTP_404_NOT_FOUND)
