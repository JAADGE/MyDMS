from django.contrib import admin
from .models import Document

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'uploaded_at')
    list_filter = ('status',)
    list_editable = ('status',)
    actions = ['accept_documents', 'reject_documents']

    def accept_documents(self, request, queryset):
        queryset.update(status='accepted')

    def reject_documents(self, request, queryset):
        queryset.update(status='rejected')

    accept_documents.short_description = "Mark selected documents as accepted"
    reject_documents.short_description = "Mark selected documents as rejected"
    
def has_delete_permission(self, request, obj=None):
    # Разрешаем удаление только для суперпользователей или модераторов
    return request.user.is_superuser or request.user.groups.filter(name='Moderators').exists()

def has_change_permission(self, request, obj=None):
     # Разрешаем изменение только для суперпользователей или модераторов
    return request.user.is_superuser or request.user.groups.filter(name='Moderators').exists()
