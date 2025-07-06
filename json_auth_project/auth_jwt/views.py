import rest_framework
import rest_framework.status
import rest_framework.views
import rest_framework.permissions
import rest_framework.response
import rest_framework.generics

import auth_jwt.serializers
import auth_jwt.renderers


class RegistrationAPIView(rest_framework.views.APIView):
    permission_classes = (rest_framework.permissions.AllowAny,)
    serializer_class = auth_jwt.serializers.RegistrationSerializer
    renderer_classes = (auth_jwt.renderers.UserJSONRenderer,)

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return rest_framework.response.Response(
            serializer.data,
            status=rest_framework.status.HTTP_201_CREATED,
        )


class LoginPIView(rest_framework.views.APIView):
    permission_classes = (rest_framework.permissions.AllowAny,)
    serializer_class = auth_jwt.serializers.LoginSerializer
    renderer_classes = (auth_jwt.renderers.UserJSONRenderer,)

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return rest_framework.response.Response(
            serializer.data,
            status=rest_framework.status.HTTP_200_OK,
        )


class UserRetrieveUpdateAPIView(rest_framework.generics.RetrieveAPIView):
    permission_classes = (rest_framework.permissions.IsAuthenticated,)
    renderer_classes = (auth_jwt.renderers.UserJSONRenderer,)
    serializer_class = auth_jwt.serializers.UserSerializer

    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)
        return rest_framework.response.Response(
            serializer.data,
            status=rest_framework.status.HTTP_200_OK,
        )

    def update(self, request, *args, **kwargs):
        serializer_data = request.data.get('user', {})
        serializer = self.serializer_class(
            request.user,
            data=serializer_data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return rest_framework.response.Response(
            serializer.data,
            status=rest_framework.status.HTTP_200_OK,
        )
