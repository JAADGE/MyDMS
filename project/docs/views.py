from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from .models import Document
from .forms import DocumentForm
from .forms import DocumentStatusForm
from . import forms


def is_moderator(user):
    return user.groups.filter(name='moderators' or 'Moderators').exists()


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


# @login_required
# def document_list(request):
#     documents = Document.objects.all()
#     return render(request, 'documents/document_list.html', {'documents': documents, 'status_form': DocumentStatusForm()})



@login_required
@user_passes_test(lambda u: u.is_staff or u.is_moderator(u))
def update_status(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    if request.method == 'POST':
        form = DocumentStatusForm(request.POST, instance=document)
        if form.is_valid():
            form.save()
    return redirect('document_list')


@login_required
@user_passes_test(lambda u: u.is_staff or u.is_moderator(u))
def delete_document(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    if request.method == 'POST':
        document.delete()
    return redirect('document_list')


@login_required
def document_list(request):
    documents = Document.objects.all()
    return render(request, 'documents/document_list.html', {'documents': documents})