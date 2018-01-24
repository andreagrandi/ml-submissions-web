from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model


UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=UserModel.objects.all())]
            )
    username = serializers.CharField(
            validators=[UniqueValidator(queryset=UserModel.objects.all())]
            )
    password = serializers.CharField(min_length=8)

    def create(self, validated_data):
        user = UserModel.objects.create_user(
            uswername=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'])
        return user

    class Meta:
        model = UserModel
        fields = ('id', 'username', 'email', 'password')
