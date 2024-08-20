from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from api_app.serializers import UserSignUpSerializer, UserSerializer
from rest_framework import status

from django.contrib.auth.hashers import make_password

from rest_framework.response import Response

from rest_framework import viewsets

@api_view(['POST'])
def registration(request):
    if request.method == 'POST':
        data = request.data
        try: 
            user = User.objects.create(
                first_name = data['first_name'],
                last_name = data['last_name'],
                username = data['username'],
                email = data['email'],
                password = make_password(data['password'])
            )
            serializer = UserSignUpSerializer(user, many=False)
            return Response(serializer.data['token'])
        except:
            message = {'detail': 'User with this email already exists'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        


class UserAPI(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    