__all__ = (
    'Permission',
    'Module',
    'User',
    'Role',
)
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Permission, ContentType as BaseContentType
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken

from apps.common.models import BaseModel
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
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    roles = models.ManyToManyField('Role', blank=True, related_name='users')
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

    USERNAME_FIELD = 'username'

    objects = managers.UserManager()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        db_table = "users"

    def __str__(self):
        return str(self.username)

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return dict(refresh=str(refresh), accsess=str(refresh.access_token))


class Role(BaseModel):
    """
    Model representing user roles within the application.

    Attributes:
        name (str): Unique name of the role.
        permissions (ManyToManyField): Modules associated with the role.

    Methods:
        __str__(): Returns the name of the role.
    """

    name = models.CharField(_("name"), max_length=150, unique=True)
    permissions = models.ManyToManyField(
        Permission, blank=True, related_name='roles', verbose_name='Permissions'
    )

    class Meta:
        db_table = "roles"

    def __str__(self):
        return self.name


class ExtendedModule(models.Model):
    """
    The ExtendedModule model is designed to add additional fields to Django's default ContentType model.

       Attributes:
       content_type (OneToOneField): A field linking to Django's ContentType model, establishing a one-to-one
       relationship. custom (BooleanField): Indicates whether the ContentType entry is custom-defined,
       with True signifying custom content.
    """
    content_type = models.OneToOneField(BaseContentType, on_delete=models.CASCADE, related_name="extended")
    custom = models.BooleanField(default=False, verbose_name='Custom type')

    class Meta:
        db_table = "extended_content_types"


class Module(BaseContentType):
    objects = managers.ModuleManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not hasattr(self, 'extended'):
            ExtendedModule.objects.create(content_type=self, custom=True)
