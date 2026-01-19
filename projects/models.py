from django.db import models
from mission_vision.models import KPI, Mission, Vision
from organization.models import OrganizationalUnit


class Program(models.Model):
    """Strategic programs aligned with organizational goals"""
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    mission = models.ForeignKey(Mission, on_delete=models.SET_NULL, null=True, blank=True, related_name='programs')
    vision = models.ForeignKey(Vision, on_delete=models.SET_NULL, null=True, blank=True, related_name='programs')
    organizational_unit = models.ForeignKey(
        OrganizationalUnit,
        on_delete=models.CASCADE,
        related_name='programs'
    )
    start_date = models.DateField()
    end_date = models.DateField()
    budget = models.DecimalField(max_digits=15, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Project(models.Model):
    """Projects aligned with KPIs and organizational goals"""
    STATUS_CHOICES = [
        ('PLANNING', 'Planning'),
        ('IN_PROGRESS', 'In Progress'),
        ('ON_HOLD', 'On Hold'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('CRITICAL', 'Critical'),
    ]
    
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='projects', null=True, blank=True)
    organizational_unit = models.ForeignKey(
        OrganizationalUnit,
        on_delete=models.CASCADE,
        related_name='projects'
    )
    kpis = models.ManyToManyField(KPI, related_name='projects', blank=True, help_text="KPIs this project contributes to")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PLANNING')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='MEDIUM')
    start_date = models.DateField()
    end_date = models.DateField()
    budget = models.DecimalField(max_digits=15, decimal_places=2)
    actual_cost = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    progress_percentage = models.IntegerField(default=0, help_text="Project completion percentage (0-100)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-priority', 'start_date']
    
    def __str__(self):
        return self.name
    
    @property
    def budget_utilization(self):
        """Calculate budget utilization percentage"""
        if self.budget > 0:
            return (self.actual_cost / self.budget) * 100
        return 0


class Activity(models.Model):
    """Activities within projects"""
    STATUS_CHOICES = [
        ('NOT_STARTED', 'Not Started'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('BLOCKED', 'Blocked'),
    ]
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='activities')
    name = models.CharField(max_length=200)
    description = models.TextField()
    assigned_to = models.CharField(max_length=200, blank=True, help_text="Person or team assigned")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NOT_STARTED')
    start_date = models.DateField()
    end_date = models.DateField()
    estimated_hours = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    actual_hours = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['start_date']
        verbose_name_plural = "Activities"
    
    def __str__(self):
        return f"{self.project.name} - {self.name}"


class Milestone(models.Model):
    """Project milestones"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='milestones')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    target_date = models.DateField()
    achieved = models.BooleanField(default=False)
    achieved_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['target_date']
    
    def __str__(self):
        return f"{self.project.name} - {self.name}"
