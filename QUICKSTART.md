# Quick Start Guide

This guide will help you get the Organizational Development Automation System up and running quickly.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/vince052666/organizationaldev.git
cd organizationaldev
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Database Migrations

```bash
python manage.py migrate
```

### 4. Create a Superuser Account

```bash
python manage.py createsuperuser
```

Follow the prompts to create your admin account. Example:
- Username: admin
- Email: admin@example.com
- Password: (choose a secure password)

### 5. Load Sample Data (Optional)

To explore the system with pre-populated data:

```bash
python manage.py create_sample_data
```

This creates:
- 1 Mission and 1 Vision
- 3 KPIs with tracking data
- 10 Organizational Units (demonstrating 5-layer hierarchy)
- 2 Positions
- 1 Program and 2 Projects with KPI alignments
- 2 Activities and 2 Milestones
- 2 Budgets
- 2 Procurements
- 2 Expenses
- 2 Ledger Entries

### 6. Start the Development Server

```bash
python manage.py runserver
```

### 7. Access the System

Open your browser and navigate to:
- Admin Interface: http://127.0.0.1:8000/admin/
- Organizational Chart: http://127.0.0.1:8000/organization/chart/

Login with the superuser credentials you created in step 4.

## Using the System

### Mission, Vision & KPIs

1. Navigate to **Mission_Vision** section in the admin
2. Click **Missions** to add your organization's mission statement
3. Click **Visions** to define your long-term vision with target year
4. Click **KPIs** to create Key Performance Indicators
   - Link KPIs to Mission and/or Vision
   - Set target values and frequency
5. Click **KPI Tracking** to record actual values over time
   - Achievement percentages are calculated automatically

### Organizational Structure

1. Navigate to **Organization** section
2. Click **Organizational Units** to start building your structure
3. **Layer 1** units (top level) must have no parent
4. Each subsequent layer (2-5) must have a parent from the layer above
5. Add leadership information, contact details, and descriptions
6. View the visual chart at: http://127.0.0.1:8000/organization/chart/

**Example 5-Layer Structure:**
```
Layer 1: Company
└── Layer 2: Division
    └── Layer 3: Department
        └── Layer 4: Team
            └── Layer 5: Sub-Team
```

### Project Management

1. Navigate to **Projects** section
2. Create **Programs** aligned with Mission/Vision
3. Create **Projects** within programs:
   - Link to organizational units
   - Assign to one or more KPIs (many-to-many)
   - Set status, priority, budget
   - Track progress percentage
4. Add **Activities** to break down project work
5. Set **Milestones** to track key achievements

### Financial Management

1. Navigate to **Finance** section
2. **Budgets**: Create annual/quarterly/monthly budgets for organizational units
   - System automatically calculates remaining budget and utilization %
3. **Procurements**: Track procurement requests and orders
   - Link to projects if applicable
   - Track through status: Requested → Approved → Ordered → Received
4. **Expenses**: Record all expenses
   - Link to budgets, projects, and procurements
   - Track approval and payment status
5. **Ledger Entries**: Maintain double-entry bookkeeping
   - Record debits and credits
   - Link to expenses for traceability

## Key Features to Explore

### Automatic Calculations

- **KPI Achievement %**: Automatically calculated as (actual/target) × 100
- **Budget Utilization %**: Automatically calculated as (spent/allocated) × 100
- **Project Budget Utilization**: Automatically calculated as (actual_cost/budget) × 100

### Relationships and Filtering

- **Projects ↔ KPIs**: Many-to-many relationship shows which projects contribute to which KPIs
- **Projects → Programs → Mission/Vision**: Full alignment chain
- **Expenses → Budget/Project/Procurement**: Track where money goes
- **Filter by**: Status, Priority, Organizational Unit, Date ranges

### Hierarchical Navigation

- **Organizational Units**: Get ancestors, descendants, and full path
- **5-Layer Validation**: System enforces strict parent-child layer rules
- **Visual Chart**: See the complete organizational structure

## Common Tasks

### Adding a New Department

1. Go to Organization → Organizational Units
2. Click "Add Organizational Unit"
3. Fill in details:
   - Name and Code
   - Select appropriate Layer (1-5)
   - Select Parent unit (must be from layer above)
   - Add head name, title, and contact info
4. Save

### Creating a Project Aligned to KPIs

1. Go to Projects → Projects
2. Click "Add Project"
3. Fill in basic info and select organizational unit
4. In the "Alignment" section, select relevant KPIs
5. Set budget, dates, and status
6. Save

### Tracking an Expense

1. Go to Finance → Expenses
2. Click "Add Expense"
3. Select organizational unit and category
4. Link to budget (and project/procurement if applicable)
5. Enter amount, payee, and date
6. Mark as approved/paid when complete
7. Save

## Tips and Best Practices

1. **Start with Mission/Vision**: Define these first before creating KPIs
2. **Build Structure Top-Down**: Create Layer 1 first, then Layer 2, etc.
3. **Link Projects to KPIs**: This enables performance tracking
4. **Use Programs**: Group related projects under programs
5. **Track Regularly**: Update KPI tracking and project progress frequently
6. **Budget Control**: Link expenses to budgets for better financial oversight

## Troubleshooting

### "Units without a parent must be at Layer 1"
- Solution: Either add a parent unit or change layer to 1

### "Child unit must be exactly one layer below parent unit"
- Solution: If parent is Layer 2, child must be Layer 3

### Cannot create user/access admin
- Solution: Run `python manage.py createsuperuser` to create an admin account

### Database errors after changes
- Solution: Run `python manage.py migrate` to apply database changes

## Next Steps

- Customize the models to fit your specific needs
- Add more organizational units and projects
- Set up regular KPI tracking
- Generate reports and analytics (future enhancement)
- Add user roles and permissions (future enhancement)

## Support

For issues or questions:
1. Check the README.md for detailed documentation
2. Review the model code in each app's models.py
3. Open an issue on GitHub

## Production Deployment

For production use:
1. Change `DEBUG = False` in settings.py
2. Set a secure `SECRET_KEY`
3. Configure `ALLOWED_HOSTS`
4. Use PostgreSQL or MySQL instead of SQLite
5. Set up proper authentication and user permissions
6. Use a production WSGI server (gunicorn, uwsgi)
7. Configure static files serving
8. Enable HTTPS

Enjoy managing your organization! 🚀
