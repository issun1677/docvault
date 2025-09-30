from repository import views
from django.urls import path

urlpatterns = [
    path('upload/', views.upload_document, name='upload_document'),
]
