import rest_framework.serializers
import django.contrib.auth

import auth_jwt.models


class RegistrationSerializer(rest_framework.serializers.ModelSerializer):
    password = rest_framework.serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
    )
    token = rest_framework.serializers.CharField(
        max_length=255,
        read_only=True,
    )

    class Meta:
        model = auth_jwt.models.User
        fields = ['email', 'username' 'password', 'token']

    def create(self, validated_data):
        return auth_jwt.models.User.objects.create_user(validated_data)


class LoginSerializer(rest_framework.serializers.Serializer):
    email = rest_framework.serializers.CharField(
        max_length=255,
    )
    username = rest_framework.serializers.CharField(
        max_length=255,
        read_only=True,
    )
    password = rest_framework.serializers.CharField(
        max_length=128,
        write_only=True,
    )
    token = rest_framework.serializers.CharField(
        max_length=255,
        read_only=True,
    )

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
            raise rest_framework.serializers.ValidationError(
                'Email is required'
            )

        if password is None:
            raise rest_framework.serializers.ValidationError(
                'Password is required'
            )

        user = django.contrib.auth.authenticate(
            username=email,
            password=password,
        )
        if user is None:
            raise rest_framework.serializers.ValidationError(
                'User not found'
            )

        if not user.is_active:
            raise rest_framework.serializers.ValidationError(
                'This user has been deactivated'
            )

        return {
            'email': user.email,
            'username': user.username,
            'token': user.token,
        }


class UserSerializer(rest_framework.serializers.ModelSerializer):
    password = rest_framework.serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
    )

    class Meta:
        model = auth_jwt.models.User
        fields = ['email', 'username' 'password', 'token']

        read_only_field = ('token',)

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for key, value in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        instance.save()
        return instance
