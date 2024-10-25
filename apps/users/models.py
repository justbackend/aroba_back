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
        Create and save a user with the given username, and password.
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

    objects = UserManager()

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
        modules (ManyToManyField): Modules associated with the role.

    Methods:
        __str__(): Returns the name of the role.
    """

    name = models.CharField(_("name"), max_length=150, unique=True)
    modules = models.ManyToManyField('Module', related_name='roles', blank=True)

    class Meta:
        db_table = "roles"

    def __str__(self):
        return self.name


class Module(BaseModel):
    """
    Model representing application modules to which roles can be assigned.

    Attributes:
        name (str): Unique name of the module.
        apis (ManyToManyField): API routes associated with the module.

    Methods:
        __str__(): Returns the name of the module.
    """

    name = models.CharField(_("name"), max_length=150, unique=True)
    apis = models.ManyToManyField('APIRoute', related_name='modules', blank=True)

    class Meta:
        db_table = "modules"

    def __str__(self):
        return self.name


class APIRoute(models.Model):
    """
    Model representing API routes available in the application.

    Attributes:
        route (str): The actual API route.
        name (str): Descriptive name of the API route.
        dynamic (str): Indicates whether the route is dynamic (Yes/No).
        method (str): HTTP method used for the route (GET, POST, etc.).

    Methods:
        __str__(): Returns a string representation of the API route.
    """

    API_DYNAMIC_CHOICES = (
        ('1', 'Yes'),
        ('0', 'No'),
    )

    route = models.CharField(_("route"), max_length=50, choices=choices.APIRoutes.choices)
    name = models.CharField(_("name"), max_length=100, null=True, blank=True)
    dynamic = models.CharField(_("dynamic"), choices=API_DYNAMIC_CHOICES)
    method = models.CharField(
        _("method"), max_length=100,
        choices=choices.APIMethods.choices,
        default=choices.APIMethods.GET


    )

    def __str__(self):
        return f'{self.route}{self.name} {self.method}'
