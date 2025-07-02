from django.contrib import admin
from .models import Document

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'uploaded_at')
    list_filter = ('status',)
    actions = ['accept_documents', 'reject_documents', 'delete_documents']

    def accept_documents(self, request, queryset):
        queryset.update(status='accepted')

    def reject_documents(self, request, queryset):
        queryset.update(status='rejected')

    def delete_documents(self, request, queryset):
        queryset.update(status='deleted')

    accept_documents.short_description = "Mark selected documents as accepted"
    reject_documents.short_description = "Mark selected documents as rejected"
    delete_documents.short_description = "Mark selected documents as deleted"