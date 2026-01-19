from django.contrib import admin
from .models import Mission, Vision, KPI, KPITracking


@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'created_at', 'updated_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Vision)
class VisionAdmin(admin.ModelAdmin):
    list_display = ['title', 'target_year', 'is_active', 'created_at']
    list_filter = ['is_active', 'target_year']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(KPI)
class KPIAdmin(admin.ModelAdmin):
    list_display = ['name', 'target_value', 'unit_of_measure', 'frequency', 'is_active']
    list_filter = ['frequency', 'is_active', 'mission', 'vision']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    filter_horizontal = []


@admin.register(KPITracking)
class KPITrackingAdmin(admin.ModelAdmin):
    list_display = ['kpi', 'actual_value', 'tracking_date', 'achievement_percentage']
    list_filter = ['tracking_date', 'kpi']
    search_fields = ['kpi__name', 'notes']
    readonly_fields = ['created_at', 'achievement_percentage']
    date_hierarchy = 'tracking_date'
    
    def achievement_percentage(self, obj):
        return f"{obj.achievement_percentage:.2f}%"
    achievement_percentage.short_description = "Achievement %"
