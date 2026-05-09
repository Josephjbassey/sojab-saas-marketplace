from django.db import models
from apps.common.models import BaseModel
from apps.organizations.models import Organization

class Client(BaseModel):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='clients')
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return self.name
