from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)

class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    roles = models.ManyToManyField(Role, related_name="users")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email

    def has_role(self, role_name):
        return self.roles.filter(name=role_name).exists()


