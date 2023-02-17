from users.models import User

def get_all():
  users = User.objects.all()
  return users