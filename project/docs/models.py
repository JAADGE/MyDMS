from django.db import models
from django.contrib.auth.models import User

class Document(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('review', 'На согласовании'),
        ('approved', 'Утвержден'),
        ('rejected', 'Отклонен'),
    ]
    
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='documents/')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)

class ApprovalRoute(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    approver = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(blank=True)
    is_approved = models.BooleanField(default=False)
    date_approved = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.title