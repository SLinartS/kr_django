from users.models import User
from django.shortcuts import redirect


class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        print('----------- infoRequest', request)
        user_login = request.COOKIES.get('user_login')
        session_id = request.COOKIES.get('session_id')

        if (user_login and session_id):
            users = User.objects.filter(
                login=user_login, session_id=session_id)
            if (users and users[0]):
                if (request.path not in ['/login', '/register']):
                    return self.get_response(request)
                return redirect(request.META.get('HTTP_REFERER')) if request.META.get('HTTP_REFERER') else redirect('/')
            else:
                if (request.path in ['/login', '/register']):
                    return self.get_response(request)
        if (request.path != '/login'):
            return redirect('/login')
        return self.get_response(request)
        # Code to be executed for each request/response after
        # the view is called.
