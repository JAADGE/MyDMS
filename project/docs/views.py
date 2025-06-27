from django.shortcuts import render
from .models import Document


def docs_home(request):
    return render(request, 'docs/docs_home.html')
