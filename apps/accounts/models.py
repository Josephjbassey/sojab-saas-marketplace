from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Custom fields can be added here later (e.g., phone, avatar)
    pass
