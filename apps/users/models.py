__all__ = (
    'Permission',
    'Module',
    'User',
    'Role',
)

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Permission, ContentType as BaseContentType
from django.core.cache import cache
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken

from apps.common.models import BaseModel
from utils.choices import *
from utils.validators import PhoneValidator
from . import managers


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    """
    Custom user model that supports username authentication.

    Attributes:
        username (str): Unique identifier for the user.
        first_name (str): User's first name.
        last_name (str): User's last name.
        date_joined (datetime): Timestamp of when the user joined.
        roles (ManyToManyField): Roles assigned to the user for permissions.
        is_staff (bool): Indicates if the user can access the admin site.
        is_active (bool): Indicates if the user is active or disabled.

    Methods:
        tokens(): Generates JWT tokens for the user.
    """

    username = models.CharField(max_length=50, unique=True, verbose_name='Username')
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    photo = models.ImageField(upload_to='users/', blank=True, verbose_name='Photo')
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    roles = models.ManyToManyField('Role', blank=True, related_name='users')
    actions = models.ManyToManyField('Action', blank=True, related_name='users', verbose_name=_('Actions'))
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

    phone = models.CharField(
        _("phone number"),
        max_length=15,
        blank=True,
        validators=[PhoneValidator()],
        null=True,
    )

    USERNAME_FIELD = 'username'

    objects = managers.UserManager()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        db_table = "users"

    @classmethod
    def profile_data(cls, user_id):
        data = cache.get(f'user_profile_{user_id}')
        if data is None:
            user = cls.objects.filter(pk=user_id).first()
            data = dict(
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
                photo=str(user.photo.url),
                phone=user.phone,
            )
            cache.set(f'user_profile_{user_id}', data)
        return data

    def __str__(self):
        return str(self.username)

    def hashing_password(self):
        if self.password and not self.password.startswith("pbkdf2_sha256"):
            self.set_password(self.password)

    def save(self, *args, **kwargs):
        self.hashing_password()
        super(User, self).save(*args, **kwargs)

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return dict(refresh=str(refresh), access=str(refresh.access_token))


class Role(BaseModel):
    """
    Model representing user roles within the application.

    Attributes:
        name (str): Unique name of the role.
        actions (ManyToManyField): Modules associated with the role.

    Methods:
        __str__(): Returns the name of the role.
    """

    name = models.CharField(_("name"), max_length=150, unique=True)
    actions = models.ManyToManyField('Action', blank=True, related_name='roles')

    class Meta:
        db_table = "roles"

    def __str__(self):
        return self.name


class Module(models.Model):
    name = models.CharField(_("name"), max_length=150, )

    class Meta:
        db_table = "modules"


class Action(models.Model):
    module = models.ForeignKey('Module', on_delete=models.CASCADE, related_name="actions")
    name = models.CharField(_("name"), max_length=150)
    apis = models.ManyToManyField(
        'APIRoute', blank=True, related_name='actions', verbose_name='APIs'
    )

    class Meta:
        db_table = "module_actions"


class APIRoute(models.Model):
    route = models.CharField(_("route"), max_length=50, choices=APIRoutes.choices)
    name = models.CharField(_("name"), max_length=100, )
    dynamic = models.BooleanField(_("dynamic"), default=False)
    method = models.CharField(
        _("method"), max_length=100,
        choices=APIMethods.choices,
        default=APIMethods.GET
    )

    class Meta:
        db_table = "api_routes"

    def __str__(self):
        return f'{self.route}{self.name} {self.method}'
