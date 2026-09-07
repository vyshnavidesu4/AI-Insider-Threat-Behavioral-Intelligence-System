import React from 'react';
import { Users, Search, ShieldCheck } from 'lucide-react';
import { DenseTable, Column } from '../components/common/Table';
import { Badge, DepartmentBadge } from '../components/common/Badge';
import { RiskScoreBadge } from '../components/common/RiskScoreBadge';

interface EmployeeItem {
  id: string;
  employee_number: string;
  full_name: string;
  email: string;
  department: string;
  job_title: string;
  clearance_level: string;
  is_privileged: boolean;
  status: string;
  composite_score: number;
}

const SAMPLE_EMPLOYEES: EmployeeItem[] = [
  {
    id: '1',
    employee_number: 'EMP-TREAS-894',
    full_name: 'Marcus Vance',
    email: 'm.vance@regionalbank.com',
    department: 'TREASURY_OPERATIONS',
    job_title: 'Senior Settlement Officer',
    clearance_level: 'HIGH_RISK',
    is_privileged: true,
    status: 'ACTIVE',
    composite_score: 94,
  },
  {
    id: '2',
    employee_number: 'EMP-WEALTH-302',
    full_name: 'Elena Rostova',
    email: 'e.rostova@regionalbank.com',
    department: 'WEALTH_MANAGEMENT',
    job_title: 'Portfolio Manager - Ultra HNW',
    clearance_level: 'CONFIDENTIAL',
    is_privileged: false,
    status: 'ON_NOTICE',
    composite_score: 88,
  },
  {
    id: '3',
    employee_number: 'EMP-ITOPS-118',
    full_name: 'David Chen',
    email: 'd.chen@regionalbank.com',
    department: 'IT_OPERATIONS',
    job_title: 'Lead Database Administrator',
    clearance_level: 'HIGH_RISK',
    is_privileged: true,
    status: 'ACTIVE',
    composite_score: 82,
  },
  {
    id: '4',
    employee_number: 'EMP-LOAN-542',
    full_name: 'Sarah Jenkins',
    email: 's.jenkins@regionalbank.com',
    department: 'LOAN_ORIGINATION',
    job_title: 'Commercial Underwriter',
    clearance_level: 'STANDARD',
    is_privileged: false,
    status: 'ACTIVE',
    composite_score: 68,
  },
  {
    id: '5',
    employee_number: 'EMP-RET-109',
    full_name: 'Arthur Pendelton',
    email: 'a.pendelton@regionalbank.com',
    department: 'RETAIL_BANKING',
    job_title: 'Branch Head Teller',
    clearance_level: 'STANDARD',
    is_privileged: false,
    status: 'ACTIVE',
    composite_score: 18,
  },
];

export const Employees: React.FC = () => {
  const columns: Column<EmployeeItem>[] = [
    {
      header: 'EMP ID',
      accessor: (r) => <span className="font-semibold text-slate-300">{r.employee_number}</span>,
      width: '130px',
    },
    {
      header: 'NAME & EMAIL',
      accessor: (r) => (
        <div>
          <div className="text-slate-200 font-medium">{r.full_name}</div>
          <div className="text-socText-muted text-2xs">{r.email}</div>
        </div>
      ),
      width: '220px',
    },
    {
      header: 'DEPARTMENT',
      accessor: (r) => <DepartmentBadge code={r.department} />,
      width: '180px',
    },
    {
      header: 'ROLE / TITLE',
      accessor: (r) => <span className="text-slate-300">{r.job_title}</span>,
      width: '200px',
    },
    {
      header: 'CLEARANCE',
      accessor: (r) => (
        <Badge
          variant={
            r.clearance_level === 'HIGH_RISK'
              ? 'critical'
              : r.clearance_level === 'CONFIDENTIAL'
              ? 'high'
              : 'neutral'
          }
        >
          {r.clearance_level}
        </Badge>
      ),
      width: '120px',
    },
    {
      header: 'PRIVILEGE',
      accessor: (r) =>
        r.is_privileged ? (
          <span className="text-2xs font-mono-dense text-amber-400 font-bold">[PRIVILEGED]</span>
        ) : (
          <span className="text-2xs font-mono-dense text-slate-500">STANDARD</span>
        ),
      width: '110px',
    },
    {
      header: 'COMPOSITE RISK',
      accessor: (r) => <RiskScoreBadge score={r.composite_score} showLabel size="sm" />,
      width: '120px',
    },
  ];

  return (
    <div className="space-y-3">
      {/* Search Toolbar */}
      <div className="bg-soc-panel border border-soc-border p-2 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="relative">
            <Search className="w-3.5 h-3.5 absolute left-2.5 top-2 text-socText-muted" />
            <input
              type="text"
              placeholder="Search by Employee ID, Name, Department..."
              className="bg-soc-bg border border-soc-border pl-8 pr-3 py-1 text-xs font-mono-dense text-slate-200 focus:outline-none focus:border-soc-borderFocus rounded-sm w-80"
            />
          </div>
        </div>
        <div className="text-2xs font-mono-dense text-socText-muted">
          INDEXED: 840 BANK PERSONNEL DOSSIERS
        </div>
      </div>

      <div className="soc-panel">
        <div className="soc-panel-header">
          <div className="flex items-center gap-2">
            <Users className="w-3.5 h-3.5 text-slate-300" />
            <span className="font-mono-dense uppercase">EMPLOYEE BEHAVIORAL DOSSIERS</span>
          </div>
          <span className="text-2xs font-mono-dense text-socText-muted">SCORED VIA 5-FACTOR MATRIX</span>
        </div>
        <DenseTable
          columns={columns}
          data={SAMPLE_EMPLOYEES}
          keyExtractor={(r) => r.id}
          onRowClick={(r) => console.log('Open dossier:', r.employee_number)}
        />
      </div>
    </div>
  );
};
