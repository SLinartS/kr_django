from mysqll import constants
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from users.models import User


def get_user_redirect(user: User) -> HttpResponseRedirect:
    match user.role.id:
        case constants.ROLE_TEACHER_ID:
            return redirect('/materials')
        case constants.ROLE_STUDENT_ID:
            return redirect('/works')
        case constants.ROLE_ADMIN_ID:
            return redirect('/access-codes')
