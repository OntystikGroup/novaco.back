from django.contrib.auth import authenticate
from rest_framework import serializers
from customAuth.models import User


class LoginUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)
    tokens = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'password' ,'tokens', 'is_staff']

    def get_tokens(self, obj):
        user = User.objects.get(username=obj.username)
        return user.tokens

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if password is None:
            raise serializers.ValidationError("Password is required")

        if username is None:
            raise serializers.ValidationError("Username is required")

        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError('A user with this username and password was not found.')

        if not user.is_active:
            raise serializers.ValidationError('This user is not currently activated.')

        return user


class RegisterUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)

    class Meta:
        model = User
        fields = ['id', 'username', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data['username'],
                                        password=validated_data['password'])
        return user

    def validate(self, attrs):
        is_user_exists = User.objects.filter(username=attrs['username']).exists()
        if is_user_exists:
            raise serializers.ValidationError("User exists")
        return attrs


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField(max_length=255)


class LoggedUserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField(max_length=255)
    tokens = serializers.SerializerMethodField()
    is_staff = serializers.BooleanField()

    class Meta:
        model = User

    def get_tokens(self, obj):
        return obj.get('tokens')
