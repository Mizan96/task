from django.contrib.auth.models import User
from rest_framework import serializers

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['email'] = user.email

        return token

def get_tokens_for_user(user):
    token = MyTokenObtainPairSerializer()
    refresh = token.get_token(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserSignUpSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name','username', 'email', 'password', 'token']
        extra_kwargs = {'password': {'write_only': True}}
        
    def get_token(self, user):
        token = get_tokens_for_user(user)
        return token
    
        
    
    