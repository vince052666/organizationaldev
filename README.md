# Organizational Development Automation System

A comprehensive Django-based system for automating organizational mission, vision, KPIs, structure, projects, activities, programs, procurement, and expenditures.

## Features

### 1. Mission, Vision, and KPIs Module
- **Mission Management**: Define and track organizational mission statements
- **Vision Management**: Set long-term vision with target years
- **KPI Tracking**: 
  - Define Key Performance Indicators aligned with mission and vision
  - Track KPI values over time (daily, weekly, monthly, quarterly, annual)
  - Automatic calculation of achievement percentages

### 2. Organizational Structure Module
- **5-Layer Hierarchical Structure**: Generic database design supporting up to 5 layers of organization
  - Layer 1: Top Level (e.g., Company/Organization)
  - Layer 2: Divisions
  - Layer 3: Departments
  - Layer 4: Teams
  - Layer 5: Sub-Teams
- **Organizational Units**: Each unit includes:
  - Unique code and name
  - Parent-child relationships
  - Leadership information (head name, title)
  - Contact details
  - Automatic validation of hierarchy rules
- **Position Management**: Define positions within each organizational unit
- **Organizational Chart Support**: Built-in methods for traversing hierarchy

### 3. Project Management Module
- **Programs**: Strategic programs aligned with mission and vision
- **Projects**: 
  - Aligned with KPIs and organizational goals
  - Status tracking (Planning, In Progress, On Hold, Completed, Cancelled)
  - Priority levels (Low, Medium, High, Critical)
  - Budget tracking with utilization calculations
  - Progress percentage tracking
- **Activities**: Tasks within projects with status, assignments, and time tracking
- **Milestones**: Track project milestones and achievements

### 4. Finance Management Module
- **Budget Management**:
  - Annual, quarterly, or monthly budgets for organizational units
  - Automatic calculation of remaining budget and utilization percentage
- **Procurement**:
  - Procurement requests and orders
  - Status tracking (Requested, Approved, Ordered, Received, Cancelled)
  - Types: Goods, Services, Works, Consultancy
  - Link to projects and organizational units
- **Expense Tracking**:
  - Comprehensive expense categories
  - Link expenses to budgets, projects, and procurements
  - Approval and payment tracking
- **Bookkeeping (Ledger)**:
  - Double-entry accounting support
  - Account types: Asset, Liability, Equity, Revenue, Expense
  - Debit and credit entries
  - Reference tracking to expenses and other transactions

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/vince052666/organizationaldev.git
cd organizationaldev
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run database migrations:
```bash
python manage.py migrate
```

4. Create a superuser for admin access:
```bash
python manage.py createsuperuser
```

5. Run the development server:
```bash
python manage.py runserver
```

6. Access the admin interface:
```
http://127.0.0.1:8000/admin/
```

## Usage

### Admin Interface

The system provides a comprehensive Django admin interface for managing all modules:

1. **Mission & Vision**: `/admin/mission_vision/`
   - Create and manage mission statements
   - Define vision with target years
   - Set up KPIs and track their values

2. **Organization**: `/admin/organization/`
   - Create organizational units (5-layer hierarchy)
   - Define positions within units

3. **Projects**: `/admin/projects/`
   - Create programs aligned with mission/vision
   - Manage projects linked to KPIs
   - Track activities and milestones

4. **Finance**: `/admin/finance/`
   - Set budgets for organizational units
   - Manage procurement processes
   - Track expenses and payments
   - Maintain ledger entries

### Data Model Relationships

```
Mission/Vision
    ├── KPIs
    │   ├── KPI Tracking (time series)
    │   └── Projects (many-to-many)
    └── Programs

Organizational Units (5-layer hierarchy)
    ├── Positions
    ├── Budgets
    ├── Programs
    ├── Projects
    ├── Procurements
    ├── Expenses
    └── Ledger Entries

Projects
    ├── Activities
    ├── Milestones
    ├── Expenses
    └── Procurements
```

## Database Schema Highlights

### Organizational Structure (5 Layers)
The system enforces strict hierarchical rules:
- Layer 1 units have no parent
- Each child must be exactly one layer below its parent
- Maximum 5 layers supported
- Built-in methods for traversing ancestors and descendants

### KPI Alignment
Projects can be linked to multiple KPIs, enabling:
- Tracking of project contributions to organizational goals
- Performance measurement against targets
- Automatic calculation of achievement percentages

### Financial Integration
Complete financial tracking with:
- Budget allocation and monitoring
- Procurement lifecycle management
- Expense tracking with approval workflows
- Basic double-entry bookkeeping

## Development

### Project Structure
```
organizationaldev/
├── manage.py
├── requirements.txt
├── orgdev/              # Main project settings
├── mission_vision/      # Mission, Vision, KPI app
├── organization/        # Organizational structure app
├── projects/            # Project management app
└── finance/             # Financial management app
```

### Adding Custom Features

The modular design allows easy extension:
1. Each app is independent with its own models, admin, and views
2. Models use Django's ORM for database abstraction
3. Admin interfaces are customizable
4. Foreign key relationships enable cross-module integration

## Technologies Used

- **Django 4.2+**: Web framework
- **SQLite**: Database (default, can be changed to PostgreSQL/MySQL)
- **Python 3.8+**: Programming language

## Future Enhancements

Potential additions:
- REST API for external integrations
- Dashboard with charts and visualizations
- Document management system
- User role-based permissions
- Workflow automation
- Reporting and analytics
- Email notifications
- Calendar integration

## License

This project is provided as-is for organizational development automation.

## Support

For issues or questions, please open an issue on the GitHub repository. 
