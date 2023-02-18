from djangoapp.models import File, FileType
from mysqll.config import FILES_DIR
from os import remove


def load_file(formFile, random_url):
    fileUrl = FILES_DIR / random_url
    with open(fileUrl, 'wb+') as file:
        file.write(formFile.read())


def delete_file(id: int):
    file = File.objects.get(id=id)
    fileUrl = FILES_DIR / file.url
    remove(fileUrl)
    file.delete()
