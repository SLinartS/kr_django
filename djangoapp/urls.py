from django.urls import path
from djangoapp.views import Materials, Groups, Works, Download, UploadWork, UploadMaterial, Delete, Redirect

urlpatterns = [
    path('', Redirect.as_view(), name='main'),
    path('groups', Groups.as_view(), name='groups'),
    path('materials', Materials.as_view(), name='materials'),
    path('works', Works.as_view(), name='works'),
    path('delete/<str:id>', Delete.as_view(), name='delete'),
    path('download/<str:url>', Download.as_view(), name='download'),
    path('upload-material', UploadMaterial.as_view(), name='upload-material'),
    path('upload-work/<str:teacher_id>', UploadWork.as_view(), name='upload-work'),
]
