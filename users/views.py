from django.views import View
from django.shortcuts import render, redirect
from users.models import User, Role
from utils.utils import generate_session_id
from users.actions.user import get_auth_user
from mysqll.config import ERROR_PAGE_URL
from mysqll.constants import ROLE_TEACHER_ID, ROLE_STUDENT_ID
from helpers.validator import Validator

TOKEN_LIFE_TIME = 60 * 60


class Register(View):
    template_name = 'users/register.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        login = request.POST.get('login')
        password = request.POST.get('password')
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        patronymic = request.POST.get('patronymic')

        login_errors = Validator(login).not_empty(
        ).min_length(6).max_length(20).valid_login().errors
        password_errors = Validator(
            password).not_empty().min_length(6).max_length(40).valid_password().errors
        name_errors = Validator(name).not_empty(
        ).max_length(25).valid_characters().errors
        surname_errors = Validator(
            surname).not_empty().max_length(25).valid_characters().errors
        patronymic_errors = Validator(
            patronymic).not_empty().max_length(25).valid_characters().errors

        if (not (login_errors or password_errors or name_errors or surname_errors or patronymic_errors)):
            session_id = generate_session_id()
            if (not User.objects.filter(login=login)):
                new_user = User.objects.create(
                    login=login, password=password, name=name, surname=surname, patronymic=patronymic, session_id=session_id, role=Role.objects.get(id=ROLE_TEACHER_ID))
                if (new_user):
                    response = redirect('/groups')
                    response.set_cookie('user_login', login, TOKEN_LIFE_TIME)
                    response.set_cookie('session_id', session_id, TOKEN_LIFE_TIME)
                    return response
            else:
                login_errors.append('Пользователь с таким логином уже существует')
        return render(request, self.template_name,
                      context={'errors': {
                          'login': login_errors,
                          'password': password_errors,
                          'name': name_errors,
                          'surname': surname_errors,
                          'patronymic': patronymic_errors
                      }})


class Login(View):
    template_name = 'users/login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        login = request.POST.get('login')
        password = request.POST.get('password')

        if (login and password):
            user = User.objects.filter(login__regex=rf'{login}', password__regex=rf'{password}')
            print(user)
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
                user.session_id = None
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
