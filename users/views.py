from django.views import View
from django.shortcuts import render, redirect
from users.models import User, Role, AccessCode
from utils.utils import generate_session_id, generate_access_code
from users.actions.user import get_auth_user
from mysqll.config import ERROR_PAGE_URL
from helpers.validator import Validator
from users.services.user import get_user_redirect

TOKEN_LIFE_TIME = 60 * 60


class Register(View):
    template_name = 'users/register.html'

    def get(self, request):
        code = request.GET.get('code')
        return render(request, self.template_name, context={'code': code})

    def post(self, request):
        access_codes = AccessCode.objects.filter(code=request.POST.get('code'))
        if (not AccessCode.objects.filter(code=access_codes[0].code) if access_codes else True):
            return render(request, self.template_name,
                          context={'errors': {
                              'login': ['Отсутствует валидный токен доступа'],
                          }})

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
        ).max_length(30).valid_characters().errors
        surname_errors = Validator(
            surname).not_empty().max_length(30).valid_characters().errors
        patronymic_errors = Validator(
            patronymic).not_empty().max_length(30).valid_characters().errors

        if (not (login_errors or password_errors or name_errors or surname_errors or patronymic_errors)):
            session_id = generate_session_id()
            if (not User.objects.filter(login=login)):
                new_user = User.objects.create(
                    login=login, password=password, name=name, surname=surname, patronymic=patronymic, session_id=session_id, role=access_codes[0].role)
                if (new_user):
                    AccessCode.objects.filter(
                        code=access_codes[0].code).delete()

                    response = get_user_redirect(new_user)
                    response.set_cookie('user_login', login, TOKEN_LIFE_TIME)
                    response.set_cookie(
                        'session_id', session_id, TOKEN_LIFE_TIME)
                    return response
            else:
                login_errors.append(
                    'Пользователь с таким логином уже существует')
        print('--------=====================', access_codes[0].code)
        return render(request, self.template_name,
                      context={
                          'errors': {
                              'login': login_errors,
                              'password': password_errors,
                              'name': name_errors,
                              'surname': surname_errors,
                              'patronymic': patronymic_errors,
                          },
                          'code': access_codes[0].code})


class Login(View):
    template_name = 'users/login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        login = request.POST.get('login')
        password = request.POST.get('password')

        if (login and password):
            users = User.objects.filter(
                login__regex=rf'{login}', password__regex=rf'{password}')
            if (users):
                session_id = generate_session_id()
                users[0].session_id = session_id
                users[0].save()

                response = get_user_redirect(users[0])
                response.set_cookie('user_login', login, TOKEN_LIFE_TIME)
                response.set_cookie('session_id', session_id, TOKEN_LIFE_TIME)
                return response
        return render(request, self.template_name, context={'errors': 'Неверный логин или пароль'})


class Logout(View):
    template_name = 'users'

    def get(self, request):
        user = get_auth_user(request)
        if (user):
            user.session_id = None
            user.save()
            return redirect('/login')
        return render(request, ERROR_PAGE_URL, context={'error': 'Ошибка выхода из аккаунта'})


class AccessCodes(View):
    template_name = 'users/access-codes.html'

    def get(self, request):
        access_codes = AccessCode.objects.all()
        domain = request.get_host()
        roles = Role.objects.all()
        return render(request,
                      self.template_name,
                      context={
                          'access_codes': access_codes,
                          'domain': domain,
                          'roles': roles
                      })

    def post(self, request):
        role = request.POST.get('role')
        access_code = generate_access_code();

        AccessCode.objects.create(code=access_code, role=Role.objects.get(title=role))

        return redirect('/access-codes')


class Delete(View):
    template_name = 'index.html'

    def post(self, request, login):
        if (login):
            User.objects.filter(login=login).delete()
        return redirect('/groups')
