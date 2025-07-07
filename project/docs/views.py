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
    return user.groups.filter(name__in=['moderators', 'moderator']).exists()


def docs_home(request):
    return render(request, 'documents/docs_home.html')


@login_required
def document_list(request):
    active_docs = Document.objects.exclude(status='archived').order_by('-uploaded_at')
    archived_docs = Document.objects.filter(status='archived').order_by('-archived_at')
    documents = Document.objects.all()
    return render(request, 'documents/document_list.html', {
        'active_docs': active_docs,
        'archived_docs': archived_docs,
        'can_edit': is_moderator(request.user),  # Флаг для проверки прав в шаблоне
        'documents': documents
    })


@login_required
@user_passes_test(lambda u: u.is_staff or is_moderator(u))
def create(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.uploaded_by = request.user
            doc.save()
            return redirect('document_list')
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

# @login_required
# @user_passes_test(lambda u: u.is_staff or is_moderator(u))
# def update_status(request, document_id):
#     document = get_object_or_404(Document, id=document_id)
#     if request.method == 'POST':
#         status = request.POST.get('status')
#         if new_status in dict(Document.STATUS_CHOICES):
#             document.status = new_status
#             document.save()
#             messages.success(request, 'Статус документа обновлен')
#     return redirect('document_list')


@login_required
@user_passes_test(lambda u: u.is_staff or is_moderator(u))
def delete_document(request, document_id):
    document = get_object_or_404(Document, id=document_id)
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
    document.status = 'review'
    document.archived_at = None
    document.save()
    return redirect('document_list')

