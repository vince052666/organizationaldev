"""
Management command to create sample data for demonstrating the system.
Run with: python manage.py create_sample_data
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal

from mission_vision.models import Mission, Vision, KPI, KPITracking
from organization.models import OrganizationalUnit, Position
from projects.models import Program, Project, Activity, Milestone
from finance.models import Budget, Procurement, Expense, LedgerEntry


class Command(BaseCommand):
    help = 'Creates sample data for the organizational development system'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Creating sample data...'))
        
        # Clear existing data (optional)
        self.stdout.write('Clearing existing data...')
        Mission.objects.all().delete()
        Vision.objects.all().delete()
        OrganizationalUnit.objects.all().delete()
        
        # Create Mission and Vision
        self.stdout.write('Creating Mission and Vision...')
        mission = Mission.objects.create(
            title="Deliver Excellence in Service",
            description="To provide high-quality services that meet and exceed stakeholder expectations while maintaining operational efficiency.",
            is_active=True
        )
        
        vision = Vision.objects.create(
            title="Be the Leading Organization by 2030",
            description="To become the leading organization in our sector by 2030, recognized for innovation, quality, and social impact.",
            target_year=2030,
            is_active=True
        )
        
        # Create KPIs
        self.stdout.write('Creating KPIs...')
        kpi1 = KPI.objects.create(
            name="Customer Satisfaction Rate",
            description="Percentage of satisfied customers",
            target_value=Decimal('90.00'),
            unit_of_measure="%",
            frequency="MONTHLY",
            mission=mission,
            vision=vision,
            is_active=True
        )
        
        kpi2 = KPI.objects.create(
            name="Project Delivery On-Time Rate",
            description="Percentage of projects delivered on time",
            target_value=Decimal('85.00'),
            unit_of_measure="%",
            frequency="QUARTERLY",
            mission=mission,
            is_active=True
        )
        
        kpi3 = KPI.objects.create(
            name="Budget Efficiency",
            description="Percentage of budget utilized efficiently",
            target_value=Decimal('95.00'),
            unit_of_measure="%",
            frequency="ANNUAL",
            vision=vision,
            is_active=True
        )
        
        # Create KPI Tracking data
        self.stdout.write('Creating KPI tracking data...')
        for i in range(3):
            KPITracking.objects.create(
                kpi=kpi1,
                actual_value=Decimal('87.50') + Decimal(i),
                tracking_date=datetime.now().date() - timedelta(days=30*i),
                notes=f"Month {i+1} tracking"
            )
        
        # Create 5-layer Organizational Structure
        self.stdout.write('Creating 5-layer organizational structure...')
        
        # Layer 1: Company
        company = OrganizationalUnit.objects.create(
            name="Acme Corporation",
            code="ACME",
            layer=1,
            description="Top-level organization",
            head_name="John Smith",
            head_title="CEO",
            email="ceo@acme.com",
            phone="+1-555-0100",
            is_active=True
        )
        
        # Layer 2: Divisions
        operations_div = OrganizationalUnit.objects.create(
            name="Operations Division",
            code="OPS",
            layer=2,
            parent=company,
            description="Handles all operational activities",
            head_name="Jane Doe",
            head_title="VP of Operations",
            email="jane.doe@acme.com",
            is_active=True
        )
        
        finance_div = OrganizationalUnit.objects.create(
            name="Finance Division",
            code="FIN",
            layer=2,
            parent=company,
            description="Financial management and accounting",
            head_name="Robert Johnson",
            head_title="CFO",
            email="robert.j@acme.com",
            is_active=True
        )
        
        # Layer 3: Departments
        it_dept = OrganizationalUnit.objects.create(
            name="IT Department",
            code="IT",
            layer=3,
            parent=operations_div,
            description="Information Technology services",
            head_name="Alice Williams",
            head_title="IT Director",
            email="alice.w@acme.com",
            is_active=True
        )
        
        hr_dept = OrganizationalUnit.objects.create(
            name="Human Resources Department",
            code="HR",
            layer=3,
            parent=operations_div,
            description="Human resources management",
            head_name="Michael Brown",
            head_title="HR Director",
            email="michael.b@acme.com",
            is_active=True
        )
        
        accounting_dept = OrganizationalUnit.objects.create(
            name="Accounting Department",
            code="ACC",
            layer=3,
            parent=finance_div,
            description="Financial accounting and reporting",
            head_name="Sarah Davis",
            head_title="Accounting Manager",
            email="sarah.d@acme.com",
            is_active=True
        )
        
        # Layer 4: Teams
        dev_team = OrganizationalUnit.objects.create(
            name="Development Team",
            code="DEV",
            layer=4,
            parent=it_dept,
            description="Software development team",
            head_name="David Miller",
            head_title="Dev Team Lead",
            email="david.m@acme.com",
            is_active=True
        )
        
        support_team = OrganizationalUnit.objects.create(
            name="IT Support Team",
            code="SUPPORT",
            layer=4,
            parent=it_dept,
            description="Technical support team",
            head_name="Emily Wilson",
            head_title="Support Manager",
            email="emily.w@acme.com",
            is_active=True
        )
        
        # Layer 5: Sub-Teams
        frontend_team = OrganizationalUnit.objects.create(
            name="Frontend Development Sub-Team",
            code="FRONTEND",
            layer=5,
            parent=dev_team,
            description="Frontend specialists",
            head_name="Chris Anderson",
            head_title="Frontend Lead",
            email="chris.a@acme.com",
            is_active=True
        )
        
        backend_team = OrganizationalUnit.objects.create(
            name="Backend Development Sub-Team",
            code="BACKEND",
            layer=5,
            parent=dev_team,
            description="Backend specialists",
            head_name="Lisa Taylor",
            head_title="Backend Lead",
            email="lisa.t@acme.com",
            is_active=True
        )
        
        # Create Positions
        self.stdout.write('Creating positions...')
        Position.objects.create(
            title="Senior Software Engineer",
            organizational_unit=dev_team,
            description="Develop and maintain software applications",
            level="Senior",
            required_qualifications="BS in Computer Science, 5+ years experience",
            is_active=True
        )
        
        Position.objects.create(
            title="IT Support Specialist",
            organizational_unit=support_team,
            description="Provide technical support to users",
            level="Mid",
            required_qualifications="Experience with help desk systems",
            is_active=True
        )
        
        # Create Program
        self.stdout.write('Creating program...')
        program = Program.objects.create(
            name="Digital Transformation Program",
            code="DTP-2024",
            description="Modernize IT infrastructure and processes",
            mission=mission,
            vision=vision,
            organizational_unit=it_dept,
            start_date=datetime.now().date(),
            end_date=datetime.now().date() + timedelta(days=365),
            budget=Decimal('500000.00'),
            is_active=True
        )
        
        # Create Projects
        self.stdout.write('Creating projects...')
        project1 = Project.objects.create(
            name="ERP System Implementation",
            code="ERP-001",
            description="Implement new enterprise resource planning system",
            program=program,
            organizational_unit=it_dept,
            status="IN_PROGRESS",
            priority="HIGH",
            start_date=datetime.now().date(),
            end_date=datetime.now().date() + timedelta(days=180),
            budget=Decimal('200000.00'),
            actual_cost=Decimal('75000.00'),
            progress_percentage=40
        )
        project1.kpis.add(kpi2, kpi3)
        
        project2 = Project.objects.create(
            name="Website Redesign",
            code="WEB-001",
            description="Redesign company website with modern UI/UX",
            program=program,
            organizational_unit=frontend_team,
            status="PLANNING",
            priority="MEDIUM",
            start_date=datetime.now().date() + timedelta(days=30),
            end_date=datetime.now().date() + timedelta(days=150),
            budget=Decimal('75000.00'),
            actual_cost=Decimal('0.00'),
            progress_percentage=0
        )
        project2.kpis.add(kpi1)
        
        # Create Activities
        self.stdout.write('Creating activities...')
        Activity.objects.create(
            project=project1,
            name="Requirements Gathering",
            description="Collect and document system requirements",
            assigned_to="Sarah Davis",
            status="COMPLETED",
            start_date=datetime.now().date() - timedelta(days=30),
            end_date=datetime.now().date() - timedelta(days=20),
            estimated_hours=Decimal('80.00'),
            actual_hours=Decimal('85.00')
        )
        
        Activity.objects.create(
            project=project1,
            name="System Configuration",
            description="Configure ERP system modules",
            assigned_to="Development Team",
            status="IN_PROGRESS",
            start_date=datetime.now().date() - timedelta(days=10),
            end_date=datetime.now().date() + timedelta(days=60),
            estimated_hours=Decimal('240.00'),
            actual_hours=Decimal('80.00')
        )
        
        # Create Milestones
        self.stdout.write('Creating milestones...')
        Milestone.objects.create(
            project=project1,
            name="Requirements Approval",
            description="Requirements document approved by stakeholders",
            target_date=datetime.now().date() - timedelta(days=15),
            achieved=True,
            achieved_date=datetime.now().date() - timedelta(days=15)
        )
        
        Milestone.objects.create(
            project=project1,
            name="System Go-Live",
            description="ERP system launched in production",
            target_date=datetime.now().date() + timedelta(days=150),
            achieved=False
        )
        
        # Create Budgets
        self.stdout.write('Creating budgets...')
        Budget.objects.create(
            organizational_unit=it_dept,
            fiscal_year=2024,
            period="ANNUAL",
            period_number=1,
            allocated_amount=Decimal('1000000.00'),
            spent_amount=Decimal('450000.00'),
            description="IT Department annual budget for 2024"
        )
        
        Budget.objects.create(
            organizational_unit=finance_div,
            fiscal_year=2024,
            period="QUARTERLY",
            period_number=1,
            allocated_amount=Decimal('250000.00'),
            spent_amount=Decimal('180000.00'),
            description="Finance Division Q1 budget"
        )
        
        # Create Procurements
        self.stdout.write('Creating procurements...')
        procurement1 = Procurement.objects.create(
            procurement_number="PR-2024-001",
            organizational_unit=it_dept,
            project=project1,
            procurement_type="GOODS",
            description="Server hardware for ERP system",
            vendor="Tech Solutions Inc.",
            estimated_cost=Decimal('50000.00'),
            actual_cost=Decimal('48500.00'),
            status="RECEIVED",
            request_date=datetime.now().date() - timedelta(days=60),
            required_by_date=datetime.now().date() - timedelta(days=30),
            approval_date=datetime.now().date() - timedelta(days=55),
            order_date=datetime.now().date() - timedelta(days=50),
            received_date=datetime.now().date() - timedelta(days=35)
        )
        
        procurement2 = Procurement.objects.create(
            procurement_number="PR-2024-002",
            organizational_unit=it_dept,
            project=project1,
            procurement_type="SERVICES",
            description="ERP implementation consulting services",
            vendor="Business Consultants LLC",
            estimated_cost=Decimal('120000.00'),
            status="APPROVED",
            request_date=datetime.now().date() - timedelta(days=45),
            required_by_date=datetime.now().date() + timedelta(days=30),
            approval_date=datetime.now().date() - timedelta(days=40)
        )
        
        # Create Expenses
        self.stdout.write('Creating expenses...')
        expense1 = Expense.objects.create(
            expense_number="EXP-2024-001",
            organizational_unit=it_dept,
            project=project1,
            procurement=procurement1,
            category="EQUIPMENT",
            description="Payment for server hardware",
            amount=Decimal('48500.00'),
            expense_date=datetime.now().date() - timedelta(days=30),
            payee="Tech Solutions Inc.",
            receipt_number="INV-2024-5678",
            approved=True,
            paid=True,
            payment_date=datetime.now().date() - timedelta(days=25)
        )
        
        expense2 = Expense.objects.create(
            expense_number="EXP-2024-002",
            organizational_unit=it_dept,
            category="UTILITIES",
            description="Internet service for Q1",
            amount=Decimal('3500.00'),
            expense_date=datetime.now().date() - timedelta(days=15),
            payee="Internet Provider Co.",
            receipt_number="INV-2024-9012",
            approved=True,
            paid=False
        )
        
        # Create Ledger Entries
        self.stdout.write('Creating ledger entries...')
        LedgerEntry.objects.create(
            entry_number="LE-2024-001",
            entry_date=datetime.now().date() - timedelta(days=30),
            account_type="EXPENSE",
            account_name="Equipment Expenses",
            entry_type="DEBIT",
            amount=Decimal('48500.00'),
            description="Server hardware purchase",
            reference_number="EXP-2024-001",
            organizational_unit=it_dept,
            expense=expense1
        )
        
        LedgerEntry.objects.create(
            entry_number="LE-2024-002",
            entry_date=datetime.now().date() - timedelta(days=30),
            account_type="ASSET",
            account_name="Cash",
            entry_type="CREDIT",
            amount=Decimal('48500.00'),
            description="Payment for server hardware",
            reference_number="EXP-2024-001",
            organizational_unit=it_dept,
            expense=expense1
        )
        
        self.stdout.write(self.style.SUCCESS('\nSample data created successfully!'))
        self.stdout.write(self.style.SUCCESS('\nSummary:'))
        self.stdout.write(f'  - Missions: {Mission.objects.count()}')
        self.stdout.write(f'  - Visions: {Vision.objects.count()}')
        self.stdout.write(f'  - KPIs: {KPI.objects.count()}')
        self.stdout.write(f'  - KPI Tracking: {KPITracking.objects.count()}')
        self.stdout.write(f'  - Organizational Units: {OrganizationalUnit.objects.count()} (5-layer structure)')
        self.stdout.write(f'  - Positions: {Position.objects.count()}')
        self.stdout.write(f'  - Programs: {Program.objects.count()}')
        self.stdout.write(f'  - Projects: {Project.objects.count()}')
        self.stdout.write(f'  - Activities: {Activity.objects.count()}')
        self.stdout.write(f'  - Milestones: {Milestone.objects.count()}')
        self.stdout.write(f'  - Budgets: {Budget.objects.count()}')
        self.stdout.write(f'  - Procurements: {Procurement.objects.count()}')
        self.stdout.write(f'  - Expenses: {Expense.objects.count()}')
        self.stdout.write(f'  - Ledger Entries: {LedgerEntry.objects.count()}')
        self.stdout.write(self.style.SUCCESS('\nYou can now log in to the admin interface to explore the data!'))
