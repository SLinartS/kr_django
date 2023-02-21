from users.models import User
from django.shortcuts import redirect
from users.actions.user import get_auth_user
from mysqll import constants
import re


class AccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        print('----------- accessInfoRequest', request)
        auth_user = get_auth_user(request)

        if (request.path == '/logout' or request.path == '/login' or request.path == '/register'):
            return self.get_response(request)

        match auth_user.role.id:
            case constants.ROLE_TEACHER_ID:
                array = [
                    '/materials',
                    '/groups',
                    '/upload-material',
                    '/delete',
                    '/download'
                ]
                for path in array:
                    if (re.search(path, request.path)):
                        return self.get_response(request)
                return redirect('/materials')

            case constants.ROLE_STUDENT_ID:
                array = ['/works', '/upload-work', '/download']
                for path in array:
                    if (re.search(path, request.path)):
                        return self.get_response(request)
                return redirect('/works')

            case constants.ROLE_ADMIN_ID:
                return self.get_response(request)

        return self.get_response(request)
        # Code to be executed for each request/response after
        # the view is called.
