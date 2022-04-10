from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, password, **extra_fields):
        user = self.model(**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(password, **extra_fields)

    def create_superuser(self, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(password, **extra_fields)


class User(AbstractUser):
    first_name = None
    last_name = None

    POSITION_CHOICES = (
        ('0', 'General Director'),
        ('1', 'Main Manager'),
        ('2', 'Middle Manager'),
        ('3', 'Lower Middle Manager'),
        ('4', 'Lower Manager'),
    )

    full_name = models.CharField(max_length=255, null=True, verbose_name='full name')
    position = models.CharField(max_length=30, null=True, choices=POSITION_CHOICES, verbose_name='position')
    head_manager = models.ForeignKey('self', null=True, on_delete=models.CASCADE, verbose_name='head_manager')
    hiring_date = models.DateField(null=True, auto_now_add=True)
    salary = models.IntegerField(null=True, verbose_name='salary')
    salary_information = models.IntegerField(null=True, verbose_name='salary information')

    objects = UserManager()
