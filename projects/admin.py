from django.contrib import admin
from .models import Program, Project, Activity, Milestone


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'organizational_unit', 'start_date', 'end_date', 'budget', 'is_active']
    list_filter = ['is_active', 'organizational_unit', 'start_date']
    search_fields = ['name', 'code', 'description']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'start_date'


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'status', 'priority', 'organizational_unit', 'progress_percentage', 'budget_utilization_display']
    list_filter = ['status', 'priority', 'organizational_unit', 'program']
    search_fields = ['name', 'code', 'description']
    readonly_fields = ['created_at', 'updated_at', 'budget_utilization_display']
    filter_horizontal = ['kpis']
    date_hierarchy = 'start_date'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'code', 'description', 'program', 'organizational_unit')
        }),
        ('Alignment', {
            'fields': ('kpis',)
        }),
        ('Status & Priority', {
            'fields': ('status', 'priority', 'progress_percentage')
        }),
        ('Timeline', {
            'fields': ('start_date', 'end_date')
        }),
        ('Budget', {
            'fields': ('budget', 'actual_cost', 'budget_utilization_display')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def budget_utilization_display(self, obj):
        return f"{obj.budget_utilization:.2f}%"
    budget_utilization_display.short_description = "Budget Utilization"


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['name', 'project', 'status', 'assigned_to', 'start_date', 'end_date']
    list_filter = ['status', 'project']
    search_fields = ['name', 'description', 'assigned_to']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'start_date'


@admin.register(Milestone)
class MilestoneAdmin(admin.ModelAdmin):
    list_display = ['name', 'project', 'target_date', 'achieved', 'achieved_date']
    list_filter = ['achieved', 'project']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at']
    date_hierarchy = 'target_date'
