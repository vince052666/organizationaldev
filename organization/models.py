from django.db import models
from django.core.exceptions import ValidationError


class OrganizationalUnit(models.Model):
    """
    Generic organizational structure supporting up to 5 layers of hierarchy.
    Example: Company > Division > Department > Team > Sub-Team
    """
    LAYER_CHOICES = [
        (1, 'Layer 1 - Top Level'),
        (2, 'Layer 2'),
        (3, 'Layer 3'),
        (4, 'Layer 4'),
        (5, 'Layer 5 - Bottom Level'),
    ]
    
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50, unique=True, help_text="Unique identifier code")
    layer = models.IntegerField(choices=LAYER_CHOICES, default=1)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        help_text="Parent organizational unit"
    )
    description = models.TextField(blank=True)
    head_name = models.CharField(max_length=200, blank=True, help_text="Name of the unit head")
    head_title = models.CharField(max_length=100, blank=True, help_text="Title of the unit head")
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['layer', 'name']
        verbose_name = "Organizational Unit"
        verbose_name_plural = "Organizational Units"
    
    def __str__(self):
        return f"{self.name} (Layer {self.layer})"
    
    def clean(self):
        """Validate organizational hierarchy rules"""
        if self.parent:
            # Child layer must be greater than parent layer
            if self.layer <= self.parent.layer:
                raise ValidationError("Child unit must be at a lower layer than parent unit")
            # Child layer must be exactly one level below parent (enforcing strict hierarchy)
            if self.layer != self.parent.layer + 1:
                raise ValidationError("Child unit must be exactly one layer below parent unit")
        else:
            # Top-level units must be layer 1
            if self.layer != 1:
                raise ValidationError("Units without a parent must be at Layer 1")
        
        # Cannot exceed 5 layers
        if self.layer > 5:
            raise ValidationError("Cannot exceed 5 layers of organization")
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    def get_ancestors(self):
        """Get all ancestor units up to the root"""
        ancestors = []
        current = self.parent
        while current:
            ancestors.append(current)
            current = current.parent
        return ancestors
    
    def get_descendants(self):
        """Get all descendant units recursively"""
        descendants = []
        for child in self.children.all():
            descendants.append(child)
            descendants.extend(child.get_descendants())
        return descendants
    
    def get_full_path(self):
        """Get the full hierarchical path"""
        path = [self.name]
        current = self.parent
        while current:
            path.insert(0, current.name)
            current = current.parent
        return " > ".join(path)


class Position(models.Model):
    """Positions within organizational units"""
    title = models.CharField(max_length=200)
    organizational_unit = models.ForeignKey(
        OrganizationalUnit,
        on_delete=models.CASCADE,
        related_name='positions'
    )
    description = models.TextField(blank=True)
    level = models.CharField(max_length=50, blank=True, help_text="Job level or grade")
    required_qualifications = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['organizational_unit', 'title']
    
    def __str__(self):
        return f"{self.title} - {self.organizational_unit.name}"
