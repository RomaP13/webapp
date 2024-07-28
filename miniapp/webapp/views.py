from django.contrib.auth import get_user_model, login
from django.db import models
from django.http import HttpRequest, HttpResponse
from django.http.response import Http404
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

from .forms import BuyGoldForm, SellGoldForm
from .models import Gold

User = get_user_model()


def index(request: HttpRequest) -> HttpResponse:
    auth_token = request.GET.get("auth_token")
    if auth_token:
        try:
            user = User.objects.get(auth_token=auth_token)
            user.backend = "django.contrib.auth.backends.ModelBackend"
            login(request, user)
        except User.DoesNotExist:
            raise Http404("Invalid token")

    users = User.objects.all()
    gold_instance = Gold.get_gold_instance()
    total_gold = gold_instance.total_gold
    gold_price = Gold.get_current_price()

    context = {
        "users": users,
        "total_gold": total_gold,
        "gold_price": gold_price,
    }

    return render(request, "index.html", context)


def profile(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated:
        raise Http404("User not authenticated")

    return render(
        request,
        "profile.html",
        {
            "user": request.user,
        },
    )


@csrf_exempt
def buy_sell_gold(request):
    if request.method == "POST" and request.user.is_authenticated:
        user = request.user
        amount = int(request.POST.get("amount"))
        action = request.POST.get("action")
        success = True

        if action == "buy":
            success = Gold.buy_gold(user, amount)
        elif action == "sell":
            success = Gold.sell_gold(user, amount)

        if success:
            user.save()
    return redirect("index")
