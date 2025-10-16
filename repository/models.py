from django.db import models
from django.contrib.auth.models import User



class Document(models.Model):
    file = models.FileField(upload_to='uploads/%Y/%m/%d/')
    original_file_name = models.CharField(max_length=250)
    file_size = models.BigIntegerField()  # stores size in bytes
    mime_type = models.CharField(max_length=100)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')
      

    def __str__(self):
        return self.original_file_name


