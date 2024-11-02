from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager as DjangoUserManager, AbstractBaseUser
from django.contrib.contenttypes.models import ContentTypeManager as DjangoContentTypeManager


class UserManager(DjangoUserManager):
    def _create_user(self, username, password, **extra_fields):
        """
        Create and save a user with the given username, and password.
        """
        if not username:
            raise ValueError("The given username must be set")

        username = AbstractBaseUser.normalize_username(username)
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

    def get_queryset(self):
        return super().get_queryset().order_by('-id')


class ModuleManager(DjangoContentTypeManager):

    def get_queryset(self):
        return super().get_queryset().filter(extended__isnull=False)
