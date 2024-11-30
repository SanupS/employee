from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    groups = models.ManyToManyField(
        Group,
        related_name="customuser_groups",  # Custom related_name to avoid conflicts
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_permissions",  # Custom related_name to avoid conflicts
        blank=True
    )

    def __str__(self):
        return self.username
    
    from django.db import models

class Form(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



class FormField(models.Model):
    label = models.CharField(max_length=100)
    field_type = models.CharField(max_length=50)  # e.g., 'text', 'number', etc.

    def __str__(self):
        return self.label

class Employee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


    

