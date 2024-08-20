from django.contrib.auth.models import User
from rest_framework import serializers

from django.contrib.auth.hashers import make_password

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
    
    
class UserSerializer(serializers.ModelSerializer):
    url =  serializers.Hyperlink
    class Meta:
        model = User
        fields = ['url','id', 'first_name', 'last_name', 'email', 'username', 'password']
        
    def create(self, validated_data):
        user = User(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
        
    
    