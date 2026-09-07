"""Initial database schema for regional bank insider threat intelligence

Revision ID: 0001_initial_schema
Revises: 
Create Date: 2026-09-07 16:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '0001_initial_schema'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Users table
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('email', sa.String(length=255), nullable=False, unique=True),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('full_name', sa.String(length=255), nullable=False),
        sa.Column('role', sa.Enum('analyst', 'manager', 'admin', name='user_role_enum'), nullable=False, server_default='analyst'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_role'), 'users', ['role'], unique=False)

    # 2. Departments table
    op.create_table(
        'departments',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('code', sa.Enum('RETAIL_BANKING', 'WEALTH_MANAGEMENT', 'TREASURY_OPERATIONS', 'LOAN_ORIGINATION', 'COMPLIANCE_AND_RISK', 'IT_OPERATIONS', name='department_code_enum'), nullable=False, unique=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.String(length=500), nullable=True),
        sa.Column('risk_tier', sa.Enum('LOW', 'MEDIUM', 'HIGH', 'CRITICAL', name='department_risk_tier_enum'), nullable=False, server_default='MEDIUM'),
        sa.Column('data_access_policies', postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default='{}'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(op.f('ix_departments_code'), 'departments', ['code'], unique=True)
    op.create_index(op.f('ix_departments_id'), 'departments', ['id'], unique=False)

    # 3. Employees table
    op.create_table(
        'employees',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('employee_number', sa.String(length=50), nullable=False, unique=True),
        sa.Column('department_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('departments.id', ondelete='RESTRICT'), nullable=False),
        sa.Column('full_name', sa.String(length=255), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False, unique=True),
        sa.Column('job_title', sa.String(length=255), nullable=False),
        sa.Column('clearance_level', sa.Enum('STANDARD', 'CONFIDENTIAL', 'RESTRICTED', 'HIGH_RISK', name='clearance_level_enum'), nullable=False, server_default='STANDARD'),
        sa.Column('is_privileged', sa.Boolean(), nullable=False, server_default=sa.text('false')),
        sa.Column('status', sa.Enum('ACTIVE', 'ON_NOTICE', 'PROBATION', 'TERMINATED', name='employment_status_enum'), nullable=False, server_default='ACTIVE'),
        sa.Column('hire_date', sa.Date(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(op.f('ix_employees_department_id'), 'employees', ['department_id'], unique=False)
    op.create_index(op.f('ix_employees_email'), 'employees', ['email'], unique=True)
    op.create_index(op.f('ix_employees_employee_number'), 'employees', ['employee_number'], unique=True)
    op.create_index(op.f('ix_employees_id'), 'employees', ['id'], unique=False)
    op.create_index(op.f('ix_employees_status'), 'employees', ['status'], unique=False)

    # 4. Activity Events table
    op.create_table(
        'activity_events',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('employee_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('employees.id', ondelete='CASCADE'), nullable=False),
        sa.Column('timestamp', sa.DateTime(timezone=True), nullable=False),
        sa.Column('event_type', sa.Enum('LOGON', 'LOGOFF', 'FILE_ACCESS', 'USB_TRANSFER', 'EMAIL_SENT', 'DB_QUERY', 'WIRE_TRANSFER_INITIATED', 'PRIVILEGE_CHANGE', name='event_type_enum'), nullable=False),
        sa.Column('source_ip', sa.String(length=45), nullable=True),
        sa.Column('host_machine', sa.String(length=100), nullable=True),
        sa.Column('target_resource', sa.String(length=500), nullable=False),
        sa.Column('sensitivity_level', sa.Enum('PUBLIC', 'INTERNAL', 'CONFIDENTIAL', 'RESTRICTED_PII', 'WIRE_TRANSFER', name='sensitivity_level_enum'), nullable=False, server_default='INTERNAL'),
        sa.Column('volume_mb', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('metadata', postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default='{}'),
        sa.Column('is_anomalous', sa.Boolean(), nullable=False, server_default=sa.text('false')),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(op.f('ix_activity_events_employee_id'), 'activity_events', ['employee_id'], unique=False)
    op.create_index(op.f('ix_activity_events_id'), 'activity_events', ['id'], unique=False)
    op.create_index(op.f('ix_activity_events_timestamp'), 'activity_events', ['timestamp'], unique=False)
    op.create_index(op.f('ix_activity_events_event_type'), 'activity_events', ['event_type'], unique=False)
    op.create_index(op.f('ix_activity_events_is_anomalous'), 'activity_events', ['is_anomalous'], unique=False)
    op.create_index('ix_activity_events_emp_time', 'activity_events', ['employee_id', 'timestamp'])
    op.create_index('ix_activity_events_type_time', 'activity_events', ['event_type', 'timestamp'])

    # 5. Behavior Baselines table
    op.create_table(
        'behavior_baselines',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('employee_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('employees.id', ondelete='CASCADE'), nullable=False),
        sa.Column('metric_name', sa.String(length=100), nullable=False),
        sa.Column('mean_value', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('std_dev', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('p95_value', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('window_start', sa.DateTime(timezone=True), nullable=False),
        sa.Column('window_end', sa.DateTime(timezone=True), nullable=False),
        sa.Column('calculated_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('distribution_params', postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default='{}'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(op.f('ix_behavior_baselines_employee_id'), 'behavior_baselines', ['employee_id'], unique=False)
    op.create_index(op.f('ix_behavior_baselines_id'), 'behavior_baselines', ['id'], unique=False)
    op.create_index(op.f('ix_behavior_baselines_metric_name'), 'behavior_baselines', ['metric_name'], unique=False)
    op.create_index(op.f('ix_behavior_baselines_calculated_at'), 'behavior_baselines', ['calculated_at'], unique=False)
    op.create_index('ix_behavior_baselines_emp_metric', 'behavior_baselines', ['employee_id', 'metric_name'])

    # 6. Risk Scores table (with the 5 explicit component columns)
    op.create_table(
        'risk_scores',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('employee_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('employees.id', ondelete='CASCADE'), nullable=False),
        sa.Column('calculated_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('behavioral_anomalies_score', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('privilege_misuse_score', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('data_access_violations_score', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('access_pattern_deviations_score', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('historical_security_events_score', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('composite_score', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('risk_factors', postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default='{}'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(op.f('ix_risk_scores_employee_id'), 'risk_scores', ['employee_id'], unique=False)
    op.create_index(op.f('ix_risk_scores_id'), 'risk_scores', ['id'], unique=False)
    op.create_index(op.f('ix_risk_scores_calculated_at'), 'risk_scores', ['calculated_at'], unique=False)
    op.create_index(op.f('ix_risk_scores_composite_score'), 'risk_scores', ['composite_score'], unique=False)
    op.create_index('ix_risk_scores_emp_calculated', 'risk_scores', ['employee_id', 'calculated_at'])

    # 7. Investigations table
    op.create_table(
        'investigations',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('case_number', sa.String(length=50), nullable=False, unique=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('status', sa.Enum('OPEN', 'IN_PROGRESS', 'UNDER_REVIEW', 'RESOLVED', 'REFERRED_TO_LEGAL', name='investigation_status_enum'), nullable=False, server_default='OPEN'),
        sa.Column('priority', sa.Enum('P1_URGENT', 'P2_HIGH', 'P3_MEDIUM', 'P4_LOW', name='investigation_priority_enum'), nullable=False, server_default='P2_HIGH'),
        sa.Column('target_employee_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('employees.id', ondelete='RESTRICT'), nullable=False),
        sa.Column('assigned_to_user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True),
        sa.Column('hypothesis', sa.Text(), nullable=True),
        sa.Column('timeline_events', postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default='[]'),
        sa.Column('findings_summary', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(op.f('ix_investigations_case_number'), 'investigations', ['case_number'], unique=True)
    op.create_index(op.f('ix_investigations_id'), 'investigations', ['id'], unique=False)
    op.create_index(op.f('ix_investigations_status'), 'investigations', ['status'], unique=False)
    op.create_index(op.f('ix_investigations_target_employee_id'), 'investigations', ['target_employee_id'], unique=False)
    op.create_index(op.f('ix_investigations_assigned_to_user_id'), 'investigations', ['assigned_to_user_id'], unique=False)
    op.create_index('ix_investigations_status_priority', 'investigations', ['status', 'priority'])

    # 8. Alerts table
    op.create_table(
        'alerts',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('alert_id', sa.String(length=50), nullable=False, unique=True),
        sa.Column('employee_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('employees.id', ondelete='CASCADE'), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.String(length=1000), nullable=True),
        sa.Column('severity', sa.Enum('CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'INFORMATIONAL', name='alert_severity_enum'), nullable=False, server_default='MEDIUM'),
        sa.Column('status', sa.Enum('NEW', 'TRIAGED', 'ESCALATED', 'CLOSED_BENIGN', 'CLOSED_MALICIOUS', name='alert_status_enum'), nullable=False, server_default='NEW'),
        sa.Column('risk_score_at_trigger', sa.Float(), nullable=False),
        sa.Column('trigger_reasons', postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default='{}'),
        sa.Column('triggered_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('triaged_by_user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True),
        sa.Column('triaged_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('triage_notes', sa.String(length=1000), nullable=True),
        sa.Column('investigation_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('investigations.id', ondelete='SET NULL'), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(op.f('ix_alerts_alert_id'), 'alerts', ['alert_id'], unique=True)
    op.create_index(op.f('ix_alerts_employee_id'), 'alerts', ['employee_id'], unique=False)
    op.create_index(op.f('ix_alerts_id'), 'alerts', ['id'], unique=False)
    op.create_index(op.f('ix_alerts_severity'), 'alerts', ['severity'], unique=False)
    op.create_index(op.f('ix_alerts_status'), 'alerts', ['status'], unique=False)
    op.create_index(op.f('ix_alerts_triggered_at'), 'alerts', ['triggered_at'], unique=False)
    op.create_index(op.f('ix_alerts_investigation_id'), 'alerts', ['investigation_id'], unique=False)
    op.create_index('ix_alerts_severity_status', 'alerts', ['severity', 'status'])


def downgrade() -> None:
    op.drop_table('alerts')
    op.drop_table('investigations')
    op.drop_table('risk_scores')
    op.drop_table('behavior_baselines')
    op.drop_table('activity_events')
    op.drop_table('employees')
    op.drop_table('departments')
    op.drop_table('users')
    
    op.execute('DROP TYPE IF EXISTS alert_status_enum')
    op.execute('DROP TYPE IF EXISTS alert_severity_enum')
    op.execute('DROP TYPE IF EXISTS investigation_priority_enum')
    op.execute('DROP TYPE IF EXISTS investigation_status_enum')
    op.execute('DROP TYPE IF EXISTS sensitivity_level_enum')
    op.execute('DROP TYPE IF EXISTS event_type_enum')
    op.execute('DROP TYPE IF EXISTS employment_status_enum')
    op.execute('DROP TYPE IF EXISTS clearance_level_enum')
    op.execute('DROP TYPE IF EXISTS department_risk_tier_enum')
    op.execute('DROP TYPE IF EXISTS department_code_enum')
    op.execute('DROP TYPE IF EXISTS user_role_enum')
