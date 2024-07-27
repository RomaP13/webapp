from django.shortcuts import render


def index(request):
    return render(request, "index.html")


def profile(request):
    user = {
        "username": "test_user",
        "wealth": 1000,
        "gold": 10,
        "silver": 990,
        "photo": "https://via.placeholder.com/150"
    }
    return render(request, "profile.html", {"user": user})
