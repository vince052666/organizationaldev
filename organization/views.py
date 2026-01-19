from django.shortcuts import render
from .models import OrganizationalUnit


def organizational_chart(request):
    """Display organizational chart with 5-layer hierarchy"""
    # Get all organizational units ordered by layer and name
    units = OrganizationalUnit.objects.filter(is_active=True).select_related('parent').order_by('layer', 'name')
    
    # Get top-level units (layer 1)
    top_level_units = units.filter(layer=1)
    
    context = {
        'top_level_units': top_level_units,
        'all_units': units,
    }
    
    return render(request, 'organization/org_chart.html', context)
