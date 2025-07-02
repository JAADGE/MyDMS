from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import Document
from .forms import DocumentForm


def docs_home(request):
    return render(request, 'documents/docs_home.html')


def create(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)  # Обрабатываем данные формы + файл
        form.save()
        return redirect('document_list')  # Перенаправляем после успеха
    else:
        form = DocumentForm()
    return render(request, 'documents/create.html', {'form': form})


def document_list(request):
    documents = Document.objects.all()
    return render(request, 'documents/document_list.html', {'documents': documents})