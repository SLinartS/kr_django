from django.db import models


class Role(models.Model):
    title = models.CharField(max_length=20)
    alias = models.CharField(max_length=20)


class User(models.Model):
    login = models.CharField(max_length=30)
    password = models.CharField(max_length=60)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    patronymic = models.CharField(max_length=50, null=True)
    session_id = models.CharField(max_length=30, null=True)
    role = models.ForeignKey(Role, on_delete=models.PROTECT)
