from django.contrib import admin
from .models import Document
from django.contrib.auth.models import Group
from django.utils import timezone
from django import forms



class DocumentAdminForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = '__all__'
        
    def clean(self):
        """Дополнительная валидация данных в админке"""
        cleaned_data = super().clean()
        if cleaned_data.get('status') == 'archived' and not cleaned_data.get('archived_at'):
            cleaned_data['archived_at'] = timezone.now()
        return cleaned_data
    

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    form = DocumentAdminForm
    list_display = ('title', 'status', 'uploaded_by', 'uploaded_at', 'archived_status')
    list_filter = ('status', 'uploaded_at', 'uploaded_by')
    search_fields = ('title', 'uploaded_by__username')
    list_editable = ('status',)
    list_per_page = 25
    date_hierarchy = 'uploaded_at'
    readonly_fields = ('uploaded_at',)
    fieldsets = (
        (None, {
            'fields': ('title', 'file', 'status')
        }),
        ('Дополнительная информация', {
            'fields': ('uploaded_by', 'uploaded_at', 'archived_at'),
            'classes': ('collapse',)
        }),
    )
    actions = ['approve_documents', 'reject_documents', 'archive_documents', 'restore_from_archive']

    # Права доступа
    def has_add_permission(self, request):
        """Кто может добавлять документы"""
        return request.user.is_superuser or request.user.groups.filter(name__in=['managers']).exists()

    def has_change_permission(self, request, obj=None):
        """Кто может изменять документы"""
        if request.user.is_superuser:
            return True
        if request.user.groups.filter(name__in=['moderators', 'managers']).exists():
            # Модераторы могут менять только документы на рассмотрении
            return obj is None or obj.status == 'review'
        return False

    def has_delete_permission(self, request, obj=None):
        """Кто может удалять документы"""
        return request.user.is_superuser

    def get_queryset(self, request):
        """Фильтрация документов в зависимости от прав"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.groups.filter(name='managers').exists():
            return qs
        return qs.filter(status='review')  # Модераторы видят только на рассмотрении

    # Кастомные действия
    def approve_documents(self, request, queryset):
        """Массовое утверждение документов"""
        updated = queryset.update(status='accepted')
        self.message_user(request, f"{updated} документов утверждено")
    approve_documents.short_description = "Утвердить выбранные"

    def reject_documents(self, request, queryset):
        """Массовое отклонение документов"""
        updated = queryset.update(status='rejected')
        self.message_user(request, f"{updated} документов отклонено")
    reject_documents.short_description = "Отклонить выбранные"

    def archive_documents(self, request, queryset):
        """Массовое архивирование"""
        updated = queryset.update(status='archived', archived_at=timezone.now())
        self.message_user(request, f"{updated} документов архивировано")
    archive_documents.short_description = "Архивировать выбранные"

    def restore_from_archive(self, request, queryset):
        """Восстановление из архива"""
        updated = queryset.update(status='review', archived_at=None)
        self.message_user(request, f"{updated} документов восстановлено")
    restore_from_archive.short_description = "Восстановить из архива"

    # Вспомогательные методы
    def archived_status(self, obj):
        """Кастомная колонка в списке"""
        return bool(obj.archived_at)
    archived_status.boolean = True
    archived_status.short_description = "В архиве?"

    def save_model(self, request, obj, form, change):
        """Автоматическая установка пользователя при создании"""
        if not obj.pk:
            obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)

# Настройка отображения групп пользователей
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_permissions')
    filter_horizontal = ('permissions',)
    
    def display_permissions(self, obj):
        return ", ".join([p.name for p in obj.permissions.all()])
    display_permissions.short_description = "Права"

admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)