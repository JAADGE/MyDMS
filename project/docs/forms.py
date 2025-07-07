from django import forms
from .models import Document

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'file']
        widgets = {
            'file': forms.FileInput(attrs={
                'accept': '.pdf,.doc,.docx,.xls,.xlsx'
            })
        }
        
        
class DocumentStatusForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['status']