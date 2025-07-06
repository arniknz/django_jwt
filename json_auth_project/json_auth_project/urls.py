import django.contrib
import django.urls

urlpatterns = [
    django.urls.path(
        'admin/',
        django.contrib.admin.site.urls,
    ),
    django.urls.path(
        'api/',
        django.urls.include('auth_jwt.urls', namespace='auth_jwt'),
    ),
]
