from django.contrib.auth.models import User
from rest_framework import exceptions, status
from rest_framework.generics import (
    CreateAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    get_object_or_404,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ldn_central_app.authentication import JWTAuthentication, generate_access_token

from .models import Gym
from .serializers import GymSerializer, UserSerializer


class GymListCreateView(ListCreateAPIView):
    serializer_class = GymSerializer
    queryset = Gym.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


class GymRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = GymSerializer
    queryset = Gym.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


class RegistrationCreateView(CreateAPIView):
    serializer_class = UserSerializer


class SessionCreateView(APIView):
    """
    This is the login post method.
    """

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = get_object_or_404(User, username=username)
        if not user.check_password(password):
            raise exceptions.AuthenticationFailed(
                "Incorrect Password", code=status.HTTP_401_UNAUTHORIZED
            )
        # temp token will be replaced
        token = generate_access_token(user)
        response = Response()
        response.set_cookie(key="jwt", value=token, httponly=True)
        response.data = {"jwt": token}
        return response


class SessionRetrieveDestroyView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    """
    Gets current user based on cookie session created
    authentication_classes will also update request with an authenticated
    user e.g request.user
    """

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response({"data": serializer.data})

    def delete(self, request):
        response = Response()
        response.delete_cookie(key="jwt")
        response.data = {"message": "Logged out"}
        return response
