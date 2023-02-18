from django.urls import path
from users.views import Register, Login, Delete

urlpatterns = [
    path('login', Login.as_view(), name='login'),
    path('register', Register.as_view(), name='register'),
    # path('delete/<str:login>', Delete.as_view(), name='delete'),
]
