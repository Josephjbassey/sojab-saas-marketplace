from django.db import models
from django.conf import settings
from django.utils.text import slugify
from apps.common.models import BaseModel

class Organization(BaseModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='owned_organizations',
        null=True,
        blank=True
    )
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Membership(BaseModel):
    ROLE_OWNER = 'owner'
    ROLE_ADMIN = 'admin'
    ROLE_MEMBER = 'member'
    ROLE_GUEST = 'guest'

    ROLE_CHOICES = [
        (ROLE_OWNER, 'Owner'),
        (ROLE_ADMIN, 'Admin'),
        (ROLE_MEMBER, 'Member'),
        (ROLE_GUEST, 'Guest'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='memberships'
    )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='memberships'
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=ROLE_MEMBER
    )

    class Meta:
        unique_together = ('user', 'organization')

    def __str__(self):
        return f"{self.user.email} in {self.organization.name} ({self.role})"

    @property
    def is_owner(self):
        return self.role == self.ROLE_OWNER

    @property
    def is_admin(self):
        return self.role == self.ROLE_ADMIN

    @property
    def is_member(self):
        return self.role == self.ROLE_MEMBER

    @property
    def is_guest(self):
        return self.role == self.ROLE_GUEST
