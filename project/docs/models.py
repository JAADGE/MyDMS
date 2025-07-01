from django.db import models
from django.contrib.auth.models import User

class Document(models.Model):
    # STATUS_CHOICES = [
    # ('draft', 'Черновик'),
    # ('review', 'На согласовании'),
    # ('approved', 'Утвержден'),
    # ('rejected', 'Отклонен'),
    # ]
        
    title = models.CharField(max_length=100, verbose_name="Название документа")
    file = models.FileField(upload_to='documents/', verbose_name="Файл")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата загрузки")
    # author = models.ForeignKey(User, on_delete=models.CASCADE)
    # status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    

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