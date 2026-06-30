from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required.')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('role', User.Role.ADMIN)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None

    # Roles:
    # user - personal account, profile/settings, learning progress, service requests.
    # operator - user request/case processing in future cases-service workflows.
    # editor - content, courses, FAQ, and educational material management.
    # admin - full platform administration and staff access.
    class Role(models.TextChoices):
        USER = 'user', 'User'
        OPERATOR = 'operator', 'Operator'
        EDITOR = 'editor', 'Editor'
        ADMIN = 'admin', 'Admin'

    class AccountType(models.TextChoices):
        ADULT = 'adult', 'Adult account'
        MINOR = 'minor', 'Minor account'

    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=32, blank=True)
    city = models.CharField(max_length=128, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    role = models.CharField(max_length=32, choices=Role.choices, default=Role.USER)
    account_type = models.CharField(max_length=32, choices=AccountType.choices, default=AccountType.ADULT)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class UserSettings(models.Model):
    class InterfaceLanguage(models.TextChoices):
        RU = 'ru', 'Russian'
        KK = 'kk', 'Kazakh'
        EN = 'en', 'English'

    class Theme(models.TextChoices):
        LIGHT = 'light', 'Light'
        DARK = 'dark', 'Dark'
        SYSTEM = 'system', 'System'

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='settings')
    email_notifications = models.BooleanField(default=True)
    push_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)
    interface_language = models.CharField(
        max_length=8,
        choices=InterfaceLanguage.choices,
        default=InterfaceLanguage.RU,
    )
    theme = models.CharField(max_length=16, choices=Theme.choices, default=Theme.LIGHT)

    def __str__(self):
        return f'{self.user.email} settings'
