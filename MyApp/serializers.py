
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

from MyApp.models import User, FriendRequest


class EditUserSerializer(serializers.Serializer):
    user_full_name = serializers.CharField(required=True)


class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = '__all__'


class AccRejRequestSerializer(serializers.Serializer):
    requestid = serializers.CharField(required=True)
    requeststatus = serializers.ChoiceField(choices=(('accept', 'accept'),
                                                      ('reject','reject')))



class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'user_full_name')
        extra_kwargs = {
            'user_full_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            user_full_name=validated_data['user_full_name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user

