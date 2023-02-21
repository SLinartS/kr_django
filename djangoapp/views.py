from django.views import View
from django.shortcuts import render, redirect, HttpResponse
from users.models import User, Role
from djangoapp.models import Group, File, FileType
from users.actions.user import get_auth_user
from djangoapp.services.file import delete_file, load_file
from mysqll.config import ERROR_PAGE_URL, FILES_DIR
from mysqll.constants import FILETYPE_MATERIAL_ID, FILETYPE_WORK_ID, ROLE_TEACHER_ID
import mimetypes
from utils.utils import generate_file_url
from os import path
import json


class Redirect(View):

    def get(self, request):
        return redirect('/groups')


class Materials(View):
    template_name = 'djangoapp/materials.html'

    def get(self, request):
        auth_user = get_auth_user(request)
        files = File.objects.filter(type=FileType.objects.get(
            id=FILETYPE_MATERIAL_ID), teacher=User.objects.get(id=auth_user.id))

        groups = Group.objects.filter(users__id=auth_user.id)

        user_name = auth_user.name[:1] + '.'
        user_patronymic = auth_user.patronymic[:1] + '.'

        return render(request, self.template_name, context={
            'auth_user': auth_user,
            'user_name': user_name,
            'user_patronymic': user_patronymic,
            'groups': groups,
            'files': files,
        })


class Groups(View):
    template_name = 'djangoapp/groups.html'

    def get(self, request):
        group_id = request.GET.get('group')
        auth_user = get_auth_user(request)
        if (group_id):
            # Получаем юзеров, которые находятся в той же группе
            # что и текущий пользователь (преподаватель)
            users_from_auth_user_group = User.objects.filter(
                group__in=Group.objects.filter(users__id=auth_user.id))
            # Получаем работы найденных студентов
            works_of_users = File.objects.filter(
                type=FileType.objects.get(id=FILETYPE_WORK_ID),
                author__in=users_from_auth_user_group)
            # Получаем только те файлы, авторы которых принадлежат
            # выбранной в данной момент группе
            files = works_of_users.filter(author__in=User.objects.filter(
                group__id=group_id), teacher=auth_user)
        else:
            files = File.objects.filter(
                type=FileType.objects.get(id=FILETYPE_WORK_ID))
        groups = Group.objects.filter(users__id=auth_user.id)

        user_name = auth_user.name[:1] + '.'
        user_patronymic = auth_user.patronymic[:1] + '.'

        return render(request, self.template_name, context={
            'auth_user': auth_user,
            'user_name': user_name,
            'user_patronymic': user_patronymic,
            'groups': groups,
            'files': files,
        })


class Works(View):
    template_name = 'djangoapp/works.html'

    def get(self, request):
        teacher_id = request.GET.get('teacher')
        auth_user = get_auth_user(request)
        if (teacher_id):
            files_materials = File.objects.filter(
                type=FileType.objects.get(id=FILETYPE_MATERIAL_ID),
                author=User.objects.get(id=teacher_id))
            files_works = File.objects.filter(
                type=FileType.objects.get(id=FILETYPE_WORK_ID),
                teacher__in=User.objects.filter(id=teacher_id),
                author__in=User.objects.filter(id=auth_user.id)
            )
        else:
            files_materials = File.objects.filter(
                type=FileType.objects.get(id=FILETYPE_MATERIAL_ID))
            files_works = []
        users = User.objects.filter(role=Role.objects.get(id=ROLE_TEACHER_ID))

        download_access = User.objects.filter(group__in=Group.objects.filter(users__id=auth_user.id),
                                              role=Role.objects.get(
                                                  id=ROLE_TEACHER_ID),
                                              id=teacher_id
                                              )
        # access_teachers_array = []
        # for teacher in access_teachers:
        #     access_teachers_array.append({'id': teacher.id})
        # access_teachers = json.dumps(access_teachers_array)

        # print(access_teachers)
        return render(request, self.template_name, context={
            'auth_user': auth_user,
            'users': users,
            'files_materials': files_materials,
            'files_works': files_works,
            'download_access': not download_access,
            'teacher_id': teacher_id
        })


class Delete(View):
    template_name = 'djangoapp/groups.html'

    def post(self, request, id):
        try:
            delete_file(id)
            return redirect(request.META.get('HTTP_REFERER')) if request.META.get('HTTP_REFERER') else redirect('/')
        except Exception as e:
            return render(request, ERROR_PAGE_URL, context={'error': e})


class UploadWork(View):
    template_name = 'djangoapp/works.html'

    def post(self, request, teacher_id):
        files = request.FILES.getlist('work')
        for file in files:
            auth_user = get_auth_user(request)
            random_url = generate_file_url() + path.splitext(file.name)[-1]
            load_file(file, random_url)

            File.objects.create(title=file.name, url=random_url,
                                author=auth_user, teacher=User.objects.get(id=teacher_id), type=FileType.objects.get(id=FILETYPE_WORK_ID))
        return redirect(request.META.get('HTTP_REFERER')) if request.META.get('HTTP_REFERER') else redirect('/')


class UploadMaterial(View):
    template_name = 'djangoapp/materials.html'

    def post(self, request):
        file = request.FILES['material']
        title = request.POST['title']
        if (title):
            title = title.strip()
        if (not title):
            title = file.name.strip()

        auth_user = get_auth_user(request)
        random_url = generate_file_url() + path.splitext(file.name)[-1]

        load_file(file, random_url)

        File.objects.create(title=title, url=random_url,
                            author=auth_user, teacher=auth_user, type=FileType.objects.get(id=FILETYPE_MATERIAL_ID))
        return redirect(request.META.get('HTTP_REFERER')) if request.META.get('HTTP_REFERER') else redirect('/')


class Download(View):
    template_name = 'djangoapp/groups.html'

    def get(self, request, url):
        filepath = FILES_DIR / url
        file_from_db = File.objects.get(url=url)
        mime_type, _ = mimetypes.guess_type(filepath)
        with open(filepath, 'rb') as file:
            response = HttpResponse(file, content_type=mime_type)
            response['Content-Disposition'] = "attachment; filename=" + \
                file_from_db.title

            return response
