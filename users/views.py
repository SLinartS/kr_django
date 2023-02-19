from django.views import View
from django.shortcuts import render, redirect
from users.models import User, Role
from utils.utils import generate_session_id
from users.actions.user import get_auth_user
from mysqll.config import ERROR_PAGE_URL
from mysqll.constants import ROLE_TEACHER_ID, ROLE_STUDENT_ID

TOKEN_LIFE_TIME = 60 * 60


class Register(View):
    template_name = 'users/register.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        login = request.POST.get('login')
        password = request.POST.get('password')
        name = request.POST.get('password')
        surname = request.POST.get('password')
        patronymic = request.POST.get('patronymic')

        if (login and password and name and surname and patronymic):
            session_id = generate_session_id()
            new_user = User.objects.create(
                login=login, password=password, name=name, surname=surname, patronymic=patronymic, session_id=session_id, role=Role.objects.get(id=ROLE_TEACHER_ID))
            if (new_user):
                response = redirect('/groups')
                response.set_cookie('user_login', login, TOKEN_LIFE_TIME)
                response.set_cookie('session_id', session_id, TOKEN_LIFE_TIME)
                return response
        return render(request, self.template_name, context={'errors': 'Ошибка заполнения полей'})


class Login(View):
    template_name = 'users/login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        login = request.POST.get('login')
        password = request.POST.get('password')

        if (login and password):
            user = User.objects.filter(login=login, password=password)
            if (user):
                session_id = generate_session_id()
                user.update(session_id=session_id)
                response = redirect('/groups')
                response.set_cookie('user_login', login, TOKEN_LIFE_TIME)
                response.set_cookie('session_id', session_id, TOKEN_LIFE_TIME)
                return response
        return render(request, self.template_name, context={'errors': 'Неверный логин или пароль'})


class Logout(View):
    template_name = 'users'

    def get(self, request):
        try:
            user = get_auth_user(request)
            if (user):
                user.session_id=None
                user.save()
                return redirect('/login')
        except ValueError:
            return render(request, ERROR_PAGE_URL, contenx={'error': 'Ошибка выхода из аккаунта'})


class Delete(View):
    template_name = 'index.html'

    def post(self, request, login):
        if (login):
            User.objects.filter(login=login).delete()
        return redirect('/groups')
