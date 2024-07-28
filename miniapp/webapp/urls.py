from django.urls import path
from .views import index, profile, buy_sell_gold

urlpatterns = [
    path("", index, name="index"),
    path("profile/", profile, name="profile"),
    path("buy_sell_gold/", buy_sell_gold, name="buy_sell_gold"),
]
