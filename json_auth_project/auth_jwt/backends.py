import jwt
import django.conf
import rest_framework.authentication
import rest_framework.exceptions
import auth_jwt.models


class JWTAuth(rest_framework.authentication.BaseAuthentication):
    authentication_header_prefix = 'Token'

    def authenticate(self, request):
        request.user = None

        auth_header = rest_framework.authentication.get_authorization_header(
            request,
        ).split()
        auth_header_prefix = self.authentication_header_prefix.lower()

        if not auth_header or len(auth_header) == 1 or len(auth_header) > 2:
            return None

        prefix = auth_header[0].decode('utf-8')
        token = auth_header[1].decode('utf-8')

        if prefix.lower() != auth_header_prefix:
            return None

        return self._authenticate_creditals(request, token)

    def _authenticate_creditals(self, request, token):
        try:
            payload = jwt.decode(token, django.conf.settings.SECRET_KEY)
        except Exception:
            rest_framework.exceptions.AuthenticationFailed(
                'Error: Unable to decode token.',
            )

        try:
            user = auth_jwt.models.User.objects.get(pk=payload['id'])
        except auth_jwt.models.User.DoesNotExist:
            rest_framework.exceptions.AuthenticationFailed(
                'Error: User does not exist for this token',
            )

        if not user.is_active:
            rest_framework.exceptions.AuthenticationFailed(
                'Error: User is not active.',
            )

        return (user, token)
