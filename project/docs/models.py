from django.db import models
from django.contrib.auth.models import User
from django.contrib import auth

class Document(models.Model):
    STATUS_CHOICES = [
        ('accepted', 'Утвердить'),
        ('rejected', 'Отклонить'),
        ('rework', 'На доработке'),
        ('review', 'на рассмотрении'),
        ('archived', 'В архиве'),
    ]

    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='documents/')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='review')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    archived_at = models.DateTimeField(null=True, blank=True)


    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Документ"
        verbose_name_plural = "Документы"

    
