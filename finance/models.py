from django.db import models
from organization.models import OrganizationalUnit
from projects.models import Project


class Budget(models.Model):
    """Annual or periodic budgets for organizational units"""
    PERIOD_CHOICES = [
        ('ANNUAL', 'Annual'),
        ('QUARTERLY', 'Quarterly'),
        ('MONTHLY', 'Monthly'),
    ]
    
    organizational_unit = models.ForeignKey(
        OrganizationalUnit,
        on_delete=models.CASCADE,
        related_name='budgets'
    )
    fiscal_year = models.IntegerField()
    period = models.CharField(max_length=20, choices=PERIOD_CHOICES, default='ANNUAL')
    period_number = models.IntegerField(default=1, help_text="Quarter or month number within fiscal year")
    allocated_amount = models.DecimalField(max_digits=15, decimal_places=2)
    spent_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-fiscal_year', 'organizational_unit']
        unique_together = ['organizational_unit', 'fiscal_year', 'period', 'period_number']
    
    def __str__(self):
        return f"{self.organizational_unit.name} - FY{self.fiscal_year} {self.period}"
    
    @property
    def remaining_amount(self):
        """Calculate remaining budget"""
        return self.allocated_amount - self.spent_amount
    
    @property
    def utilization_percentage(self):
        """Calculate budget utilization percentage"""
        if self.allocated_amount > 0:
            return (self.spent_amount / self.allocated_amount) * 100
        return 0


class Procurement(models.Model):
    """Procurement requests and orders"""
    STATUS_CHOICES = [
        ('REQUESTED', 'Requested'),
        ('APPROVED', 'Approved'),
        ('ORDERED', 'Ordered'),
        ('RECEIVED', 'Received'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    PROCUREMENT_TYPE_CHOICES = [
        ('GOODS', 'Goods'),
        ('SERVICES', 'Services'),
        ('WORKS', 'Works'),
        ('CONSULTANCY', 'Consultancy'),
    ]
    
    procurement_number = models.CharField(max_length=50, unique=True)
    organizational_unit = models.ForeignKey(
        OrganizationalUnit,
        on_delete=models.CASCADE,
        related_name='procurements'
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='procurements'
    )
    procurement_type = models.CharField(max_length=20, choices=PROCUREMENT_TYPE_CHOICES)
    description = models.TextField()
    vendor = models.CharField(max_length=200, blank=True)
    estimated_cost = models.DecimalField(max_digits=15, decimal_places=2)
    actual_cost = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='REQUESTED')
    request_date = models.DateField()
    required_by_date = models.DateField()
    approval_date = models.DateField(null=True, blank=True)
    order_date = models.DateField(null=True, blank=True)
    received_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-request_date']
    
    def __str__(self):
        return f"{self.procurement_number} - {self.description[:50]}"


class Expense(models.Model):
    """Track expenses and expenditures"""
    EXPENSE_CATEGORY_CHOICES = [
        ('SALARIES', 'Salaries & Wages'),
        ('EQUIPMENT', 'Equipment'),
        ('SUPPLIES', 'Supplies'),
        ('TRAVEL', 'Travel'),
        ('UTILITIES', 'Utilities'),
        ('RENT', 'Rent'),
        ('SERVICES', 'Services'),
        ('MAINTENANCE', 'Maintenance'),
        ('TRAINING', 'Training'),
        ('OTHER', 'Other'),
    ]
    
    expense_number = models.CharField(max_length=50, unique=True)
    organizational_unit = models.ForeignKey(
        OrganizationalUnit,
        on_delete=models.CASCADE,
        related_name='expenses'
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='expenses'
    )
    procurement = models.ForeignKey(
        Procurement,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='expenses'
    )
    budget = models.ForeignKey(
        Budget,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='expenses'
    )
    category = models.CharField(max_length=20, choices=EXPENSE_CATEGORY_CHOICES)
    description = models.TextField()
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    expense_date = models.DateField()
    payee = models.CharField(max_length=200)
    receipt_number = models.CharField(max_length=100, blank=True)
    approved = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    payment_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-expense_date']
    
    def __str__(self):
        return f"{self.expense_number} - {self.description[:50]}"


class LedgerEntry(models.Model):
    """Basic bookkeeping ledger for double-entry accounting"""
    ENTRY_TYPE_CHOICES = [
        ('DEBIT', 'Debit'),
        ('CREDIT', 'Credit'),
    ]
    
    ACCOUNT_TYPE_CHOICES = [
        ('ASSET', 'Asset'),
        ('LIABILITY', 'Liability'),
        ('EQUITY', 'Equity'),
        ('REVENUE', 'Revenue'),
        ('EXPENSE', 'Expense'),
    ]
    
    entry_number = models.CharField(max_length=50, unique=True)
    entry_date = models.DateField()
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPE_CHOICES)
    account_name = models.CharField(max_length=200)
    entry_type = models.CharField(max_length=10, choices=ENTRY_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    description = models.TextField()
    reference_number = models.CharField(max_length=100, blank=True, help_text="Reference to expense, procurement, etc.")
    organizational_unit = models.ForeignKey(
        OrganizationalUnit,
        on_delete=models.CASCADE,
        related_name='ledger_entries'
    )
    expense = models.ForeignKey(
        Expense,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ledger_entries'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-entry_date', 'entry_number']
        verbose_name_plural = "Ledger Entries"
    
    def __str__(self):
        return f"{self.entry_number} - {self.entry_type} {self.amount}"
