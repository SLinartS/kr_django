from django.db import models


class Role(models.Model):
    title = models.CharField(max_length=20)
    alias = models.CharField(max_length=20)

class AccessCode(models.Model):
    code = models.CharField(max_length=20)
    role = models.ForeignKey(Role, on_delete=models.PROTECT)

class User(models.Model):
    login = models.CharField(max_length=20)
    password = models.CharField(max_length=40)
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    patronymic = models.CharField(max_length=30, null=True)
    session_id = models.CharField(max_length=20, null=True)
    role = models.ForeignKey(Role, on_delete=models.PROTECT)
