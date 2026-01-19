# System Architecture Documentation

## Overview

The Organizational Development Automation System is built using Django's Model-View-Template (MVT) architecture, with a focus on modular design and clear separation of concerns.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     Django Application                       │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Mission    │  │Organization  │  │   Projects   │      │
│  │   Vision     │  │  Structure   │  │  Management  │      │
│  │     KPI      │  │              │  │              │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
│         │                  │                  │              │
│         └──────────────────┼──────────────────┘              │
│                            │                                 │
│                   ┌────────▼─────────┐                      │
│                   │     Finance      │                      │
│                   │   Management     │                      │
│                   └──────────────────┘                      │
│                                                               │
├─────────────────────────────────────────────────────────────┤
│                   Django ORM (Models)                        │
├─────────────────────────────────────────────────────────────┤
│                   SQLite Database                            │
│              (PostgreSQL/MySQL in production)                │
└─────────────────────────────────────────────────────────────┘
```

## Module Architecture

### 1. Mission Vision Module (`mission_vision/`)

**Purpose**: Manage organizational mission, vision, and KPIs

**Models**:
- `Mission`: Organization's mission statement
- `Vision`: Long-term vision with target year
- `KPI`: Key Performance Indicators
- `KPITracking`: Time-series tracking of KPI values

**Key Features**:
- Automatic achievement percentage calculation
- Frequency-based tracking (daily, weekly, monthly, quarterly, annual)
- Many-to-one relationships with Mission/Vision

**Relationships**:
```
Mission ─┬─→ KPI ─→ KPITracking
         │
Vision ──┘
```

### 2. Organization Module (`organization/`)

**Purpose**: Manage 5-layer organizational hierarchy

**Models**:
- `OrganizationalUnit`: Recursive hierarchical structure (5 layers)
- `Position`: Positions within organizational units

**Key Features**:
- Self-referencing foreign key for parent-child relationships
- Validation ensuring strict 5-layer hierarchy
- Methods for traversing ancestors and descendants
- Full path generation for display

**Hierarchy Rules**:
1. Layer 1 units must have no parent (top level)
2. Layer 2-5 units must have a parent from the layer above
3. Child must be exactly one layer below parent
4. Maximum 5 layers enforced

**Data Structure**:
```python
OrganizationalUnit {
    id: Primary Key
    name: String
    code: String (unique)
    layer: Integer (1-5)
    parent: ForeignKey (self)
    # ... other fields
}
```

**Tree Traversal Methods**:
- `get_ancestors()`: Returns list of parent units up to root
- `get_descendants()`: Returns all child units recursively
- `get_full_path()`: Returns hierarchical path string

### 3. Projects Module (`projects/`)

**Purpose**: Manage programs, projects, activities, and milestones

**Models**:
- `Program`: Strategic programs aligned with mission/vision
- `Project`: Projects with KPI alignment
- `Activity`: Tasks within projects
- `Milestone`: Project milestones

**Key Features**:
- Many-to-many relationship between Projects and KPIs
- Status and priority tracking
- Budget utilization calculation
- Progress percentage tracking

**Relationships**:
```
Mission/Vision ─→ Program ─→ Project ←─ KPI (M2M)
                              │
                              ├─→ Activity
                              └─→ Milestone
```

**Project-KPI Alignment**:
- Projects can be linked to multiple KPIs
- Enables tracking of project contributions to organizational goals
- Filters available in admin for KPI-based project views

### 4. Finance Module (`finance/`)

**Purpose**: Comprehensive financial management

**Models**:
- `Budget`: Periodic budgets for organizational units
- `Procurement`: Procurement lifecycle management
- `Expense`: Expense tracking and approval
- `LedgerEntry`: Double-entry bookkeeping

**Key Features**:
- Automatic budget utilization calculation
- Expense linking to projects, procurements, and budgets
- Basic double-entry accounting
- Status-based workflows

**Relationships**:
```
OrganizationalUnit ─┬─→ Budget ←────┐
                    │                │
                    ├─→ Procurement ─┤
                    │                │
                    ├─→ Expense ─────┤
                    │                │
                    └─→ LedgerEntry ─┘
                    
Project ────────────────→ Expense
                          │
                          └─→ LedgerEntry
```

## Database Schema

### Key Relationships

```sql
-- Mission/Vision to KPIs (One-to-Many)
KPI.mission_id → Mission.id
KPI.vision_id → Vision.id

-- KPI to Tracking (One-to-Many)
KPITracking.kpi_id → KPI.id

-- Organizational Units (Self-referencing)
OrganizationalUnit.parent_id → OrganizationalUnit.id

-- Projects to KPIs (Many-to-Many)
project_kpis.project_id → Project.id
project_kpis.kpi_id → KPI.id

-- Programs to Projects (One-to-Many)
Project.program_id → Program.id

-- Projects to Activities/Milestones (One-to-Many)
Activity.project_id → Project.id
Milestone.project_id → Project.id

-- Finance to Organizational Units (Many-to-One)
Budget.organizational_unit_id → OrganizationalUnit.id
Procurement.organizational_unit_id → OrganizationalUnit.id
Expense.organizational_unit_id → OrganizationalUnit.id
LedgerEntry.organizational_unit_id → OrganizationalUnit.id

-- Finance Internal Relationships
Expense.procurement_id → Procurement.id
Expense.budget_id → Budget.id
LedgerEntry.expense_id → Expense.id
```

## Data Flow

### 1. Strategic Planning Flow

```
Mission/Vision → KPIs → Projects → Activities/Milestones
                 ↓
           KPI Tracking (time-series data)
```

### 2. Organizational Flow

```
Layer 1 (Company)
    ↓
Layer 2 (Division)
    ↓
Layer 3 (Department)
    ↓
Layer 4 (Team)
    ↓
Layer 5 (Sub-Team)
```

### 3. Financial Flow

```
Budget Allocation → Procurement Request → Expense → Ledger Entry
                         ↓
                    Project Costs
                         ↓
                 Budget Utilization
```

## Design Patterns

### 1. Recursive Hierarchical Structure

The `OrganizationalUnit` model uses self-referencing foreign keys to create a tree structure:

```python
parent = models.ForeignKey('self', on_delete=models.CASCADE, ...)
```

This enables:
- Unlimited depth (constrained to 5 layers via validation)
- Parent-child navigation
- Ancestor/descendant queries

### 2. Many-to-Many with Through Models

Projects-KPIs relationship allows:
- A project to contribute to multiple KPIs
- A KPI to be tracked by multiple projects
- Easy filtering and reporting

### 3. Calculated Properties

Models use `@property` decorators for computed fields:

```python
@property
def budget_utilization(self):
    if self.budget > 0:
        return (self.actual_cost / self.budget) * 100
    return 0
```

Benefits:
- No database storage needed
- Always up-to-date
- Can be displayed in admin

### 4. Status-Based Workflows

Multiple models use status fields for workflow management:
- Projects: Planning → In Progress → Completed
- Procurements: Requested → Approved → Ordered → Received
- Expenses: Approval → Payment workflows

## Admin Interface Customization

### List Display Optimization

```python
list_display = ['name', 'status', 'calculated_field']
```

### Filtering and Search

```python
list_filter = ['status', 'priority', 'organizational_unit']
search_fields = ['name', 'code', 'description']
```

### Fieldsets for Organization

```python
fieldsets = (
    ('Basic Information', {...}),
    ('Relationships', {...}),
    ('Timestamps', {...}),
)
```

## Security Considerations

### Input Validation

1. **Model Validation**: `clean()` methods enforce business rules
2. **Database Constraints**: Unique constraints on codes
3. **Foreign Key Protection**: CASCADE and SET_NULL appropriately

### Data Integrity

1. **Hierarchical Validation**: Prevents invalid organizational structures
2. **Date Validation**: Ensures end_date > start_date
3. **Decimal Fields**: Proper precision for financial data

### Future Enhancements

1. **User Authentication**: Django's built-in auth with custom permissions
2. **Row-Level Security**: Users can only see their organizational unit data
3. **Audit Trail**: Track all changes with timestamps and user info
4. **API Security**: Token-based authentication for REST API

## Performance Considerations

### Query Optimization

1. **Select Related**: Used in admin for foreign key lookups
```python
def get_queryset(self, request):
    return super().get_queryset(request).select_related('parent')
```

2. **Prefetch Related**: For many-to-many relationships
3. **Database Indexing**: Automatic on foreign keys and unique fields

### Scalability

1. **Database Choice**: SQLite for development, PostgreSQL/MySQL for production
2. **Caching**: Django's caching framework can be added
3. **Pagination**: Admin automatically paginates large result sets
4. **Asynchronous Tasks**: Celery can be added for long-running operations

## Testing Strategy

### Unit Tests

- Model validation logic
- Calculated properties
- Hierarchy traversal methods

### Integration Tests

- Admin interface functionality
- Form validation
- Filter and search operations

### Example Test Structure

```python
from django.test import TestCase
from organization.models import OrganizationalUnit

class OrganizationalUnitTests(TestCase):
    def test_layer_validation(self):
        # Test that layer 2 units require a parent
        ...
```

## Deployment Architecture

### Development

```
Django Dev Server (manage.py runserver)
    ↓
SQLite Database
```

### Production

```
Load Balancer
    ↓
Web Server (Nginx)
    ↓
WSGI Server (Gunicorn)
    ↓
Django Application
    ↓
PostgreSQL Database
```

## API Extension Points

For future REST API implementation using Django REST Framework:

```python
# Serializers for each model
class ProjectSerializer(serializers.ModelSerializer):
    budget_utilization = serializers.ReadOnlyField()
    
# ViewSets for CRUD operations
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
```

## Maintenance and Monitoring

### Database Migrations

```bash
python manage.py makemigrations  # Create migrations
python manage.py migrate         # Apply migrations
```

### Data Management

```bash
python manage.py create_sample_data  # Load sample data
python manage.py dumpdata > backup.json  # Backup
python manage.py loaddata backup.json    # Restore
```

### Monitoring Points

1. Database query performance
2. Admin response times
3. Model validation errors
4. Budget utilization alerts
5. KPI achievement tracking

## Conclusion

This architecture provides:
- **Modularity**: Independent apps that can be enhanced separately
- **Scalability**: Database-agnostic design for growth
- **Maintainability**: Clear separation of concerns
- **Extensibility**: Easy to add new features and relationships
- **Performance**: Optimized queries and calculated fields
