from django.views import View
from django.shortcuts import render, redirect
from users.services.user import get_all
from users.models import User
from django.http import HttpResponseRedirect, HttpResponse
import random
import string


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
            session_id = ''.join(random.choice(
                string.ascii_letters + string.punctuation) for x in range(15))
            new_user = User.objects.create(
                login=login, password=password, name=name, surname=surname, patronymic=patronymic, session_id=session_id)
            if (new_user):
                response = redirect('/')
                response.set_cookie('user_login', login, 30)
                response.set_cookie('session_id', session_id, 30)
                return response
        else:
            return render(request, self.template_name, context={'errors': 'Ошибка заполнения полей'})


class Login(View):
    template_name = 'users/login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        return redirect('/')

class Delete(View):
    template_name = 'index.html'

    def post(self, request, login):
        if (login):
            User.objects.filter(login=login).delete()
        return redirect('/')


class Index(View):
    template_name = 'index.html'

    def get(self, request):
        return render(request, self.template_name, context={'users': get_all()})
