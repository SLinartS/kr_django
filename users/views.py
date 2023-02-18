from django.views import View
from django.shortcuts import render, redirect
from users.models import User
from utils.utils import generate_session_id

TOKEN_LIFE_TIME = 60


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
                login=login, password=password, name=name, surname=surname, patronymic=patronymic, session_id=session_id, role=1)
            if (new_user):
                response = redirect('/')
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
                response = redirect('/')
                response.set_cookie('user_login', login, TOKEN_LIFE_TIME)
                response.set_cookie('session_id', session_id, TOKEN_LIFE_TIME)
                return response
        return render(request, self.template_name, context={'errors': 'Неверный логин или пароль'})


class Delete(View):
    template_name = 'index.html'

    def post(self, request, login):
        if (login):
            User.objects.filter(login=login).delete()
        return redirect('/')


class Index(View):
    template_name = 'index.html'

    def get(self, request):
        users = User.objects.all()
        return render(request, self.template_name, context={'users': users})
