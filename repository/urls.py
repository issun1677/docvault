from repository import views
from django.urls import path

urlpatterns = [
    path('upload/', views.upload_document, name='upload_document'),
    path('document_list/', views.list_document, name='list_document'),
    path('download/<int:document_id>', views.document_download, name='document_download'),
    path('', views.dashboard, name='dashboard'),
 
]

