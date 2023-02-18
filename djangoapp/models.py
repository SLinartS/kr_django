from django.db import models
from users.models import User


class FileType(models.Model):
    type = models.CharField(max_length=20)


class File(models.Model):
    title = models.CharField(max_length=150)
    url = models.CharField(max_length=255)
    author = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='file_authors_set')
    teacher = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='file_teachers_set')
    type = models.ForeignKey(FileType, on_delete=models.PROTECT)


class Group(models.Model):
    title = models.CharField(max_length=50)
    users = models.ManyToManyField(User)
