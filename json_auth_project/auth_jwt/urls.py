import django.urls

import auth_jwt.views


app_name = 'auth_jwt'
urlpatterns = [
    django.urls.path(
        'user',
        auth_jwt.views.UserRetrieveUpdateAPIView.as_view(),
    ),
    django.urls.path('users/', auth_jwt.views.RegistrationAPIView.as_view()),
    django.urls.path('users/login/', auth_jwt.views.LoginPIView.as_view()),
]
