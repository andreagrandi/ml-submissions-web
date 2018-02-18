from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model
from .models import Submission


UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=UserModel.objects.all())]
            )
    username = serializers.CharField(
            validators=[UniqueValidator(queryset=UserModel.objects.all())]
            )
    password = serializers.CharField(min_length=8, write_only=True)

    def create(self, validated_data):
        user = UserModel.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            full_name=validated_data['full_name'])
        return user

    class Meta:
        model = UserModel
        fields = ('id', 'username', 'email', 'password', 'full_name')


class SubmissionSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Submission
        fields = ('created', 'datafile', 'owner', 'score')
