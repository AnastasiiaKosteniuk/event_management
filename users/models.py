from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """Custom user model that uses email as the unique identifier."""
    email = models.EmailField(unique=True)
