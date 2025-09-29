

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.db.models import Q


# Create your models here.



class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password,  role="unverified"):
        if not (email, username, password):
            raise ValueError("Не все данные были переданы")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, role = role)
        user.set_password(password)
        user.save()
        return user

class User(AbstractBaseUser):

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=Q(role='unverified') | Q(role='verified') | Q(role='admin') | Q(role='superadmin'),
                name='role_valid_values'
            )
        ]
    username = models.CharField(unique=True, max_length=30)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, default="unverified")
    date_joined = models.DateTimeField(auto_now_add=True)
    verification_token = models.UUIDField(default=None, editable=False, null=True, unique=True)
    verification_token_created = models.DateTimeField(default=None, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email

    def has_role(self, role_name):
        return self.role == role_name

    @property
    def is_staff(self):
        return self.role in ["admin", "superadmin"]

    def has_perm(self, perm, obj=None):
        return self.role in ['admin', 'superadmin']

    def has_module_perms(self, app_label):
        return self.role in ['admin', 'superadmin']

    objects = CustomUserManager()



