from django.http import HttpRequest

def user_context(request: HttpRequest):
    return {
        "cur_user": request.user
    }
