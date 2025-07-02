from django.urls import path
from . import views
from .views import document_list, update_status, delete_document, download_document
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
path('', views.docs_home,name='docs'),
path('create', views.create,name='create'),
path('list', views.document_list, name='document_list'),
path('update_status/<int:document_id>/', update_status, name='update_status'),
path('delete_document/<int:document_id>/', delete_document, name='delete_document'),
path('download/<int:document_id>/', download_document, name='download_document')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
