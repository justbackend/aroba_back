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
from utils.utility import clear_users_perms
from . import managers
from utils import choices
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
import utils


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
    phone = models.CharField(_("phone number"), max_length=15, blank=True, validators=[utils.PhoneValidator])
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

    USERNAME_FIELD = 'username'

    objects = managers.UserManager()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        db_table = "users"

    def __str__(self):
        return str(self.username)

    def hashing_password(self):
        if not self.password.startswith("pbkdf2_sha256"):
            self.set_password(self.password)

    def save(self, *args, **kwargs):
        self.hashing_password()
        sum(*args, **kwargs)

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
    API_DYNAMIC_CHOICES = (
        ('1', 'Yes'),
        ('0', 'No'),
    )

    route = models.CharField(_("route"), max_length=50, choices=choices.APIRoutes.choices)
    name = models.CharField(_("name"), max_length=100, )
    dynamic = models.BooleanField(_("dynamic"), default=False)
    method = models.CharField(
        _("method"), max_length=100,
        choices=choices.APIMethods.choices,
        default=choices.APIMethods.GET
    )

    class Meta:
        db_table = "api_routes"

    def __str__(self):
        return f'{self.route}{self.name} {self.method}'

    def format_save_redis(self):
        return dict(dynamic=self.dynamic, )


@receiver(m2m_changed, sender=Role.actions.through)
def role_action_change(sender, instance, **kwargs):
    users = instance.users.all()
    clear_users_perms(users)


@receiver(m2m_changed, sender=Action.apis.through)
def action_apis_change(sender, instance, **kwargs):
    users = instance.users.all()
    clear_users_perms(users)


@receiver(m2m_changed, sender=User.actions.through)
def user_action_change(sender, instance, **kwargs):
    clear_users_perms((instance,))


@receiver(m2m_changed, sender=User.roles.through)
def user_action_change(sender, instance, action, **kwargs):

    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        related_actions = Action.objects.filter(roles__in=instance.roles.all()).distinct()
        instance.actions.set(related_actions)

        clear_users_perms((instance,))

