from django.urls import path
from users.views import Register, Login, Logout, AccessCodes

urlpatterns = [
    path('login', Login.as_view(), name='login'),
    path('register', Register.as_view(), name='register'),
    path('logout', Logout.as_view(), name='logout'),
    path('access-codes', AccessCodes.as_view(), name='access-codes'),
    path('generate-code', AccessCodes.as_view(), name='generate-code'),
    # path('delete/<str:login>', Delete.as_view(), name='delete'),
]
