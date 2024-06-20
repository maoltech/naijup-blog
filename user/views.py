from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer, LoginOutputSerializer
from .models import User
from django.contrib.auth import logout
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
import logging

logger = logging.getLogger(__name__)
class UserSignInView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email_or_username = request.data.get('email')
        password = request.data.get('password')

        if email_or_username is None or password is None:
            return Response({'error': 'Please provide both email/username and password'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email=email_or_username).first() or User.objects.filter(username=email_or_username).first()
            
        if user is None or not user.check_password(password):
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
        token = RefreshToken.for_user(user=user)
        return Response({'token': str(token.access_token), 'data': LoginOutputSerializer(user).data})

class UserSignUpView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                # token, _ = Token.objects.get_or_create(user=user)
                token = RefreshToken.for_user(user=user)
                response = {'token': str(token.access_token), 'data': LoginOutputSerializer(user).data}
                return Response(response, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error saving user: {str(e)}")
            return Response({'error': 'An error occurred during sign up. Please try again.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

class UserSignOutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({'message': 'Successfully logged out'}, status=status.HTTP_200_OK)

class UserDetailsView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class GetUserByUsernameView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

