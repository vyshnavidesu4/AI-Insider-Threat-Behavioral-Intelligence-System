"""Seed initial SOC accounts, bank departments, employees, and sample alerts into the database."""
import os
import sys

# Ensure backend root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from datetime import datetime, timezone, date
from app.core.database import SessionLocal, Base, engine
from app.core.security import get_password_hash
from app.models.user import User, UserRole
from app.models.department import Department, DepartmentCode, RiskTier
from app.models.employee import Employee, ClearanceLevel, EmploymentStatus
from app.models.risk_score import RiskScore
from app.models.alert import Alert, AlertSeverity, AlertStatus


def seed_database():
    print("[*] Creating database tables if not existing...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # 1. Seed SOC Users
        print("[*] Seeding SOC Users...")
        users_data = [
            {
                "email": "analyst@regionalbank.com",
                "password": "AnalystPassword123!",
                "full_name": "Alex Mercer (Senior Analyst)",
                "role": UserRole.ANALYST,
            },
            {
                "email": "manager@regionalbank.com",
                "password": "ManagerPassword123!",
                "full_name": "Sarah Connor (SOC Manager)",
                "role": UserRole.MANAGER,
            },
            {
                "email": "admin@regionalbank.com",
                "password": "AdminPassword123!",
                "full_name": "Root Administrator",
                "role": UserRole.ADMIN,
            },
        ]

        for u in users_data:
            existing = db.query(User).filter(User.email == u["email"]).first()
            if not existing:
                user = User(
                    email=u["email"],
                    hashed_password=get_password_hash(u["password"]),
                    full_name=u["full_name"],
                    role=u["role"],
                    is_active=True,
                )
                db.add(user)
                print(f"  + Created user: {u['email']} [{u['role'].value}]")

        db.commit()

        # 2. Seed 6 Regional Bank Departments
        print("[*] Seeding 6 Regional Bank Departments...")
        depts_data = [
            (DepartmentCode.TREASURY_OPERATIONS, "Treasury Operations", RiskTier.CRITICAL, "High-value wire transfers, liquidity management, SWIFT terminals"),
            (DepartmentCode.WEALTH_MANAGEMENT, "Wealth Management", RiskTier.HIGH, "Ultra-HNW accounts, private client trusts, portfolio management"),
            (DepartmentCode.IT_OPERATIONS, "IT Operations", RiskTier.HIGH, "Core banking database infrastructure, sysadmin privileges, network access"),
            (DepartmentCode.LOAN_ORIGINATION, "Loan Origination", RiskTier.MEDIUM, "Commercial & retail underwriting, credit assessment, SSN / PII verification"),
            (DepartmentCode.RETAIL_BANKING, "Retail Banking", RiskTier.LOW, "Branch operations, head tellers, customer depository accounts"),
            (DepartmentCode.COMPLIANCE_AND_RISK, "Compliance & Risk", RiskTier.LOW, "AML monitoring, regulatory audit files, fraud reporting"),
        ]

        created_depts = {}
        for code, name, tier, desc in depts_data:
            dept = db.query(Department).filter(Department.code == code).first()
            if not dept:
                dept = Department(
                    code=code,
                    name=name,
                    risk_tier=tier,
                    description=desc,
                    data_access_policies={"authorized_hours": "08:00-18:00", "wire_limit_usd": 1000000},
                )
                db.add(dept)
                db.flush()
                print(f"  + Created department: {name} [{tier.value}]")
            created_depts[code] = dept

        db.commit()

        # 3. Seed Sample Employees
        print("[*] Seeding Bank Employees...")
        emp_data = [
            ("EMP-TREAS-894", DepartmentCode.TREASURY_OPERATIONS, "Marcus Vance", "m.vance@regionalbank.com", "Senior Settlement Officer", ClearanceLevel.HIGH_RISK, True, 94.0),
            ("EMP-WEALTH-302", DepartmentCode.WEALTH_MANAGEMENT, "Elena Rostova", "e.rostova@regionalbank.com", "Portfolio Manager - Ultra HNW", ClearanceLevel.CONFIDENTIAL, False, 88.0),
            ("EMP-ITOPS-118", DepartmentCode.IT_OPERATIONS, "David Chen", "d.chen@regionalbank.com", "Lead Database Administrator", ClearanceLevel.HIGH_RISK, True, 82.0),
            ("EMP-LOAN-542", DepartmentCode.LOAN_ORIGINATION, "Sarah Jenkins", "s.jenkins@regionalbank.com", "Commercial Underwriter", ClearanceLevel.STANDARD, False, 68.0),
            ("EMP-RET-109", DepartmentCode.RETAIL_BANKING, "Arthur Pendelton", "a.pendelton@regionalbank.com", "Branch Head Teller", ClearanceLevel.STANDARD, False, 18.0),
        ]

        for emp_num, d_code, name, email, title, clearance, is_priv, composite_score in emp_data:
            emp = db.query(Employee).filter(Employee.employee_number == emp_num).first()
            if not emp:
                emp = Employee(
                    employee_number=emp_num,
                    department_id=created_depts[d_code].id,
                    full_name=name,
                    email=email,
                    job_title=title,
                    clearance_level=clearance,
                    is_privileged=is_priv,
                    status=EmploymentStatus.ACTIVE,
                    hire_date=date(2022, 5, 12),
                )
                db.add(emp)
                db.flush()
                print(f"  + Created employee: {name} ({emp_num})")

                # Add risk score
                risk = RiskScore(
                    employee_id=emp.id,
                    calculated_at=datetime.now(timezone.utc),
                    behavioral_anomalies_score=composite_score * 0.95,
                    privilege_misuse_score=composite_score * 0.9,
                    data_access_violations_score=composite_score * 0.85,
                    access_pattern_deviations_score=composite_score * 0.7,
                    historical_security_events_score=composite_score * 0.6,
                    composite_score=composite_score,
                    risk_factors={"top_drivers": ["Unusual off-hours volume", "Access to non-department files"]},
                )
                db.add(risk)

        db.commit()
        print("\n[✓] Database seeding complete! Ready for local SOC operations.")

    except Exception as e:
        db.rollback()
        print(f"[!] Error seeding database: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
