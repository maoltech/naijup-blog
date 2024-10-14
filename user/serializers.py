from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'bio', 'first_name', 'last_name', 'profile_picture', 'is_author']
        extra_kwargs = {
            'password': {'write_only': True}, 
            'profile_picture': {'required': False},
            'is_author': {'required': False},
            'last_name': {'required': False},
            'first_name': {'required': False},
            'bio': {'required': False}
            }

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
class LoginOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'bio', 'first_name', 'last_name', 'profile_picture', 'is_author', 'created_at', 'updated_at', 'is_author']
        extra_kwargs = {'password': {'write_only': True}}
