from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Document
from .forms import DocumentForm, DocumentStatusForm
from django.http import FileResponse
from django.utils import timezone
from django.http import FileResponse

def is_moderator(user):
    return user.groups.filter(name='moderators').exists()


def docs_home(request):
    return render(request, 'documents/docs_home.html')


@login_required
def document_list(request):
    active_docs = Document.objects.filter(uploaded_by=request.user).exclude(status='archived')
    archived_docs = Document.objects.filter(uploaded_by=request.user, status='archived')
    documents = Document.objects.all()
    return render(request, 'documents/document_list.html', {
        'active_docs': active_docs,
        'archived_docs': archived_docs,
        'documents' : documents,
    })
    # documents = Document.objects.all()
    # return render(request, 'documents/document_list.html', {'documents': documents})


def create(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)  # Обрабатываем данные формы + файл
        form.save()
        return redirect('document_list')  # Перенаправляем после успеха
    else:
        form = DocumentForm()
    return render(request, 'documents/create.html', {'form': form})


@login_required
def download_document(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    file = open(document.file.path, 'rb')
    response = FileResponse(file, as_attachment=True)
    return response



@login_required
@user_passes_test(lambda u: u.is_staff or is_moderator(u))
def update_status(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    if request.method == 'POST':
        form = DocumentStatusForm(request.POST, instance=document)
        if form.is_valid():
            form.save()
    return redirect('document_list')


@login_required
@user_passes_test(lambda u: u.is_staff or is_moderator(u))
def delete_document(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    if request.method == 'POST':
        document.delete()
    return redirect('document_list')


@login_required
@user_passes_test(lambda u: u.is_staff or is_moderator(u))
def archive_document(request, document_id):
    document = get_object_or_404(Document, id=document_id, uploaded_by=request.user)
    document.status = 'archived'
    document.archived_at = timezone.now()
    document.save()
    messages.success(request, 'Документ перемещен в архив')
    return redirect('document_list')

@login_required
@user_passes_test(lambda u: u.is_staff or is_moderator(u))
def restore_document(request, document_id):
    document = get_object_or_404(Document, id=document_id, uploaded_by=request.user)
    document.status = 'pending'
    document.archived_at = None
    document.save()
    messages.success(request, 'Документ восстановлен из архива')
    return redirect('document_list')

