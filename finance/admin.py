from django.contrib import admin
from .models import Budget, Procurement, Expense, LedgerEntry


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ['organizational_unit', 'fiscal_year', 'period', 'allocated_amount', 'spent_amount', 'remaining_display', 'utilization_display']
    list_filter = ['fiscal_year', 'period', 'organizational_unit']
    search_fields = ['organizational_unit__name', 'description']
    readonly_fields = ['created_at', 'updated_at', 'remaining_display', 'utilization_display']
    
    def remaining_display(self, obj):
        return f"${obj.remaining_amount:,.2f}"
    remaining_display.short_description = "Remaining"
    
    def utilization_display(self, obj):
        return f"{obj.utilization_percentage:.2f}%"
    utilization_display.short_description = "Utilization %"


@admin.register(Procurement)
class ProcurementAdmin(admin.ModelAdmin):
    list_display = ['procurement_number', 'procurement_type', 'organizational_unit', 'vendor', 'estimated_cost', 'status', 'request_date']
    list_filter = ['status', 'procurement_type', 'organizational_unit']
    search_fields = ['procurement_number', 'description', 'vendor']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'request_date'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('procurement_number', 'procurement_type', 'description', 'vendor')
        }),
        ('Organization & Project', {
            'fields': ('organizational_unit', 'project')
        }),
        ('Financial', {
            'fields': ('estimated_cost', 'actual_cost')
        }),
        ('Status & Dates', {
            'fields': ('status', 'request_date', 'required_by_date', 'approval_date', 'order_date', 'received_date')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['expense_number', 'category', 'organizational_unit', 'amount', 'expense_date', 'approved', 'paid']
    list_filter = ['category', 'approved', 'paid', 'organizational_unit']
    search_fields = ['expense_number', 'description', 'payee']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'expense_date'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('expense_number', 'category', 'description', 'amount')
        }),
        ('Organization & References', {
            'fields': ('organizational_unit', 'project', 'procurement', 'budget')
        }),
        ('Payment Details', {
            'fields': ('expense_date', 'payee', 'receipt_number', 'approved', 'paid', 'payment_date')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(LedgerEntry)
class LedgerEntryAdmin(admin.ModelAdmin):
    list_display = ['entry_number', 'entry_date', 'account_type', 'account_name', 'entry_type', 'amount', 'organizational_unit']
    list_filter = ['entry_type', 'account_type', 'organizational_unit']
    search_fields = ['entry_number', 'account_name', 'description', 'reference_number']
    readonly_fields = ['created_at']
    date_hierarchy = 'entry_date'
