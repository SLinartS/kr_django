from django.urls import path
from users.views import Register, Login, Logout

urlpatterns = [
    path('login', Login.as_view(), name='login'),
    path('register', Register.as_view(), name='register'),
    path('logout', Logout.as_view(), name='logout'),
    # path('delete/<str:login>', Delete.as_view(), name='delete'),
]
