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
            try:
                user = User.objects.get(
                    login=user_login, session_id=session_id)
                if (user):
                    response = self.get_response(request)
                    return response
                if (request.path != '/register'):
                    return redirect('/register')

            except:
                if (request.path != '/register'):
                    return redirect('/register')
                response = self.get_response(request)
                return response

        response = self.get_response(request)
        return response

        # Code to be executed for each request/response after
        # the view is called.
