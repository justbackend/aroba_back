from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import UserManager as DjangoUserManager
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken

from apps.common.models import BaseModel
from utils import choices


class UserManager(DjangoUserManager):
    def _create_user(self, username, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError("The given username must be set")

        username = User.normalize_username(username)
        user = self.model(username=username, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    username = models.CharField(max_length=50, unique=True, verbose_name='Username')

    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    roles = models.ManyToManyField('Role', blank=True, related_name='users')

    USERNAME_FIELD = 'username'

    objects = UserManager()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        db_table = "users"

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return dict(refresh=str(refresh), accsess=str(refresh.access_token))

    def __str__(self):
        return str(self.username)


class Role(BaseModel):
    name = models.CharField(_("name"), max_length=150, unique=True)
    modules = models.ManyToManyField('Module', related_name='roles', blank=True)

    class Meta:
        db_table = "roles"

    def __str__(self):
        return self.name


class Module(BaseModel):
    name = models.CharField(_("name"), max_length=150, unique=True)
    apis = models.ManyToManyField('APIRoute', related_name='modules', blank=True)

    class Meta:
        db_table = "modules"

    def __str__(self):
        return self.name


class APIRoute(models.Model):
    API_METHOD_CHOICES = (
        ('POST', 'POST'),
        ('GET', 'GET'),
        ('PUT', 'PUT'),
        ('DELETE', 'DELETE'),
        ('PATCH', 'PATCH'),
    )

    route = models.CharField(_("route"), max_length=50, choices=choices.API_ROUTE_CHOICES)
    name = models.CharField(_("name"), max_length=100, )
    dynamic = models.CharField(_("dynamic"), choices=choices.API_DYNAMIC_CHOICES)
    method = models.CharField(
        _("method"), max_length=100,
        choices=choices.APIMethod.choices,
        default=choices.APIMethod.GET
    )

    def __str__(self):
        return f'{self.route}{self.name} {self.method}'
