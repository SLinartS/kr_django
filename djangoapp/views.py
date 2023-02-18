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
        return render(request, self.template_name, context={
            'auth_user': auth_user,
            'groups': groups,
            'files': files,
        })


class Groups(View):
    template_name = 'djangoapp/groups.html'

    def get(self, request):
        group_id = request.GET.get('group')
        auth_user = get_auth_user(request)
        if (group_id):
            files = File.objects.filter(
                type=FileType.objects.get(id=FILETYPE_WORK_ID),
                author__in=User.objects.filter(group__in=Group.objects.filter(users__id=auth_user.id))).filter(author__in=User.objects.filter(group__id=group_id))
        else:
            files = File.objects.filter(
                type=FileType.objects.get(id=FILETYPE_WORK_ID))
        groups = Group.objects.all()
        return render(request, self.template_name, context={
            'auth_user': auth_user,
            'groups': groups,
            'files': files,
        })


class Works(View):
    template_name = 'djangoapp/works.html'

    def get(self, request):
        teacher_id = request.GET.get('teacher')
        auth_user = get_auth_user(request)
        if (teacher_id):
            files = File.objects.filter(
                type=FileType.objects.get(id=FILETYPE_MATERIAL_ID),
                author=User.objects.get(id=teacher_id))
        else:
            files = File.objects.filter(
                type=FileType.objects.get(id=FILETYPE_WORK_ID))
        users = User.objects.filter(role=Role.objects.get(id=ROLE_TEACHER_ID))
        return render(request, self.template_name, context={
            'auth_user': auth_user,
            'users': users,
            'files': files,
            'teacher_id': teacher_id
        })


class Delete(View):
    template_name = 'djangoapp/groups.html'

    def post(self, request, id):
        try:
            delete_file(id)
            return redirect('/groups')
        except Exception as e:
            return render(request, ERROR_PAGE_URL, context={'error': e})


class UploadWork(View):
    template_name = 'djangoapp/works.html'

    def post(self, request, teacher_id):
        file = request.FILES['work']
        auth_user = get_auth_user(request)
        random_url = generate_file_url()
        load_file(file, random_url)

        File.objects.create(title=file.name, url=random_url,
                            author=auth_user, teacher=User.objects.get(id=teacher_id), type=FileType.objects.get(id=FILETYPE_WORK_ID))
        return redirect('works')


class UploadMaterial(View):
    template_name = 'djangoapp/materials.html'

    def post(self, request):
        file = request.FILES['material']
        auth_user = get_auth_user(request)
        random_url = generate_file_url() + path.splitext(file.name)[-1]

        load_file(file, random_url)

        File.objects.create(title=file.name, url=random_url,
                            author=auth_user, teacher=auth_user, type=FileType.objects.get(id=FILETYPE_MATERIAL_ID))
        return redirect('materials')


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
