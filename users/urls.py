from django.urls import include, path, re_path
from users.views import Register, Login, Index, Delete

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('login', Login.as_view(), name='login'),
    path('register', Register.as_view(), name='register'),
    path('delete/<str:login>', Delete.as_view(), name='delete'),
]
