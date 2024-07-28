from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    telegram_id = models.CharField(max_length=100, unique=True)
    silver = models.PositiveIntegerField(default=1000)
    gold = models.PositiveIntegerField(default=0)
    photo = models.URLField(blank=True, null=True)
    auth_token = models.CharField(max_length=255, blank=True, null=True)

    def get_wealth(self):
        gold_price = Gold.get_current_price()
        return self.silver + self.gold * gold_price


class Gold(models.Model):
    MIN_PRICE = 0.5
    MAX_PRICE = 100

    total_gold = models.PositiveIntegerField(default=1000000000)
    gold_price = models.FloatField(default=1.0)

    @classmethod
    def get_gold_instance(cls):
        gold_instance = cls.objects.first()
        if not gold_instance:
            gold_instance = cls.objects.create()
        return gold_instance

    @classmethod
    def get_current_price(cls):
        gold_instance = cls.get_gold_instance()
        return gold_instance.gold_price

    @classmethod
    def buy_gold(cls, user, amount):
        gold_instance = cls.get_gold_instance()
        total_cost = amount * gold_instance.gold_price
        if user.silver >= total_cost:
            # Updating the amount of gold and silver the user has
            user.gold += amount
            user.silver -= total_cost

            # Update gold price based on bounding curve
            gold_instance.gold_price = min(
                max(gold_instance.gold_price * 1.1, cls.MIN_PRICE),
                cls.MAX_PRICE,
            )

            print(
                f"Bought {amount} gold for {total_cost:.2f} silver. New price: {gold_instance.gold_price:.2f}"
            )
            user.save()
            gold_instance.save()
            return True
        return False

    @classmethod
    def sell_gold(cls, user, amount):
        gold_instance = cls.get_gold_instance()
        total_earned = amount * gold_instance.gold_price
        if user.gold >= amount:
            # Updating the amount of gold and silver the user has
            user.gold -= amount
            user.silver += total_earned

            # Update gold price based on bounding curve
            gold_instance.gold_price = max(
                min(gold_instance.gold_price / 1.1, cls.MAX_PRICE),
                cls.MIN_PRICE,
            )

            print(
                f"Sold {amount} gold for {total_earned:.2f} silver. New price: {gold_instance.gold_price:.2f}"
            )
            user.save()
            gold_instance.save()
            return True
        return False
