from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    telegram_id = models.CharField(max_length=100, unique=True)
    silver = models.PositiveIntegerField(default=1000)
    gold = models.PositiveIntegerField(default=0)
    photo = models.URLField(blank=True, null=True)
    auth_token = models.CharField(max_length=255, blank=True, null=True)

    def get_wealth(self):
        return (
            self.silver + self.gold * 1
        )
