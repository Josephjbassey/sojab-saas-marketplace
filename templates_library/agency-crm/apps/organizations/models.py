from django.db import models
from django.conf import settings
from apps.common.models import BaseModel

class Organization(BaseModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Membership(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, default='member')

    class Meta:
        unique_together = ('user', 'organization')
