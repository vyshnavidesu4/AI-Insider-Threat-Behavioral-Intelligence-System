export type UserRole = 'analyst' | 'manager' | 'admin';

export interface User {
  id: string;
  email: string;
  full_name: string;
  role: UserRole;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface AuthTokens {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
}

export type DepartmentCode =
  | 'RETAIL_BANKING'
  | 'WEALTH_MANAGEMENT'
  | 'TREASURY_OPERATIONS'
  | 'LOAN_ORIGINATION'
  | 'COMPLIANCE_AND_RISK'
  | 'IT_OPERATIONS';

export type RiskTier = 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';

export interface Department {
  id: string;
  code: DepartmentCode;
  name: string;
  description?: string;
  risk_tier: RiskTier;
  data_access_policies: Record<string, any>;
  created_at: string;
  updated_at: string;
}

export type ClearanceLevel = 'STANDARD' | 'CONFIDENTIAL' | 'RESTRICTED' | 'HIGH_RISK';
export type EmploymentStatus = 'ACTIVE' | 'ON_NOTICE' | 'PROBATION' | 'TERMINATED';

export interface Employee {
  id: string;
  employee_number: string;
  department_id: string;
  full_name: string;
  email: string;
  job_title: string;
  clearance_level: ClearanceLevel;
  is_privileged: boolean;
  status: EmploymentStatus;
  hire_date?: string;
  created_at: string;
  updated_at: string;
  department?: Department;
}

export type EventType =
  | 'LOGON'
  | 'LOGOFF'
  | 'FILE_ACCESS'
  | 'USB_TRANSFER'
  | 'EMAIL_SENT'
  | 'DB_QUERY'
  | 'WIRE_TRANSFER_INITIATED'
  | 'PRIVILEGE_CHANGE';

export type SensitivityLevel =
  | 'PUBLIC'
  | 'INTERNAL'
  | 'CONFIDENTIAL'
  | 'RESTRICTED_PII'
  | 'WIRE_TRANSFER';

export interface ActivityEvent {
  id: string;
  employee_id: string;
  timestamp: string;
  event_type: EventType;
  source_ip?: string;
  host_machine?: string;
  target_resource: string;
  sensitivity_level: SensitivityLevel;
  volume_mb: number;
  event_metadata: Record<string, any>;
  is_anomalous: boolean;
  created_at: string;
  updated_at: string;
}

export interface RiskScore {
  id: string;
  employee_id: string;
  calculated_at: string;
  behavioral_anomalies_score: number;       // 35%
  privilege_misuse_score: number;           // 25%
  data_access_violations_score: number;     // 20%
  access_pattern_deviations_score: number;  // 10%
  historical_security_events_score: number; // 10%
  composite_score: number;                  // Final weighted score (0-100)
  risk_factors: Record<string, any>;
  created_at: string;
  updated_at: string;
}

export type AlertSeverity = 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW' | 'INFORMATIONAL';
export type AlertStatus = 'NEW' | 'TRIAGED' | 'ESCALATED' | 'CLOSED_BENIGN' | 'CLOSED_MALICIOUS';

export interface Alert {
  id: string;
  alert_id: string;
  employee_id: string;
  title: string;
  description?: string;
  severity: AlertSeverity;
  status: AlertStatus;
  risk_score_at_trigger: number;
  trigger_reasons: Record<string, any>;
  triggered_at: string;
  triaged_by_user_id?: string;
  triaged_at?: string;
  triage_notes?: string;
  investigation_id?: string;
  created_at: string;
  updated_at: string;
}

export type InvestigationStatus = 'OPEN' | 'IN_PROGRESS' | 'UNDER_REVIEW' | 'RESOLVED' | 'REFERRED_TO_LEGAL';
export type InvestigationPriority = 'P1_URGENT' | 'P2_HIGH' | 'P3_MEDIUM' | 'P4_LOW';

export interface Investigation {
  id: string;
  case_number: string;
  title: string;
  description?: string;
  status: InvestigationStatus;
  priority: InvestigationPriority;
  target_employee_id: string;
  assigned_to_user_id?: string;
  hypothesis?: string;
  timeline_events: Array<Record<string, any>>;
  findings_summary?: string;
  created_at: string;
  updated_at: string;
}
