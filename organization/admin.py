from django.contrib import admin
from .models import OrganizationalUnit, Position


@admin.register(OrganizationalUnit)
class OrganizationalUnitAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'layer', 'parent', 'head_name', 'is_active']
    list_filter = ['layer', 'is_active']
    search_fields = ['name', 'code', 'head_name']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'code', 'layer', 'parent', 'description', 'is_active')
        }),
        ('Leadership', {
            'fields': ('head_name', 'head_title')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('parent')


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ['title', 'organizational_unit', 'level', 'is_active']
    list_filter = ['is_active', 'level', 'organizational_unit']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']
