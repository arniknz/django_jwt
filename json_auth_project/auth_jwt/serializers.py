import rest_framework.serializers

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
