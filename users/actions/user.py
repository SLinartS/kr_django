from users.models import User


def get_auth_user(request: object) -> User:
    user_login = request.COOKIES.get('user_login')
    return User.objects.filter(login=user_login)[0] if User.objects.filter(login=user_login) else False