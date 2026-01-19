from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Mission(models.Model):
    """Organization's mission statement"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


class Vision(models.Model):
    """Organization's vision statement"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    target_year = models.IntegerField(help_text="Target year for achieving this vision")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


class KPI(models.Model):
    """Key Performance Indicators"""
    FREQUENCY_CHOICES = [
        ('DAILY', 'Daily'),
        ('WEEKLY', 'Weekly'),
        ('MONTHLY', 'Monthly'),
        ('QUARTERLY', 'Quarterly'),
        ('ANNUAL', 'Annual'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    target_value = models.DecimalField(max_digits=10, decimal_places=2)
    unit_of_measure = models.CharField(max_length=50, help_text="e.g., %, count, currency")
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, default='MONTHLY')
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE, related_name='kpis', null=True, blank=True)
    vision = models.ForeignKey(Vision, on_delete=models.CASCADE, related_name='kpis', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = "KPI"
        verbose_name_plural = "KPIs"
    
    def __str__(self):
        return self.name


class KPITracking(models.Model):
    """Track actual KPI values over time"""
    kpi = models.ForeignKey(KPI, on_delete=models.CASCADE, related_name='tracking')
    actual_value = models.DecimalField(max_digits=10, decimal_places=2)
    tracking_date = models.DateField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-tracking_date']
        verbose_name = "KPI Tracking"
        verbose_name_plural = "KPI Tracking"
    
    def __str__(self):
        return f"{self.kpi.name} - {self.tracking_date}"
    
    @property
    def achievement_percentage(self):
        """Calculate achievement percentage against target"""
        if self.kpi.target_value > 0:
            return (self.actual_value / self.kpi.target_value) * 100
        return 0
