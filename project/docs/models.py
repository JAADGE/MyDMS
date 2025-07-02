from django.db import models
from django.contrib.auth.models import User

class Document(models.Model):
    STATUS_CHOICES = [
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('deleted', 'Deleted'),
    ]

    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='documents/')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Документ"
        verbose_name_plural = "Документы"

    
# class ApprovalRoute(models.Model):
#     document = models.ForeignKey(Document, on_delete=models.CASCADE)
#     approver = models.ForeignKey(User, on_delete=models.CASCADE)
#     comment = models.TextField(blank=True)
#     is_approved = models.BooleanField(default=False)
#     date_approved = models.DateTimeField(null=True, blank=True)
    
#     def __str__(self):
#         return self.title