import jwt

import datetime
import django.conf
import django.contrib.auth.models
import django.db.models


class UserManager(django.contrib.auth.models.BaseUserManager):
    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError('User must have username')
        if email is None:
            raise TypeError('User must have email')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):
        if password is None:
            raise TypeError('Superuser must have password')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(
    django.contrib.auth.models.AbstractBaseUser,
    django.contrib.auth.models.PermissionsMixin,
):
    username = django.db.models.CharField(
        db_index=True,
        max_length=255,
        unique=True,
    )
    email = django.db.models.EmailField(
        db_index=True,
        unique=True,
    )
    is_active = django.db.models.BooleanField(
        default=True,
    )
    is_staff = django.db.models.BooleanField(
        default=False,
    )
    created_at = django.db.models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = django.db.models.DateTimeField(
        auto_now=True,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def token(self):
        return self._generate_jwt_token()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def _generate_jwt_token(self):
        dt = datetime.datetime.now() + datetime.timedelta(days=1)

        token = jwt.encode(
            {
                'id': self.pk,
                'exp': int(dt.strftime('%s')),
            },
            django.conf.settings.SECRET_KEY, algorithm='HS256',
        )

        return token
