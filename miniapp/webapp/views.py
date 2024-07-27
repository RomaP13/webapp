from django.contrib.auth import get_user_model, login
from django.http import HttpRequest, HttpResponse
from django.http.response import Http404
from django.shortcuts import render

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
    return render(request, "index.html", {"users": users})


def profile(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated:
        raise Http404("User not authenticated")
    return render(request, "profile.html")
