import React from 'react';
import { AlertTriangle, Filter, Search } from 'lucide-react';
import { DenseTable, Column } from '../components/common/Table';
import { SeverityBadge, StatusBadge } from '../components/common/Badge';
import { RiskScoreBadge } from '../components/common/RiskScoreBadge';

interface AlertItem {
  id: string;
  alert_id: string;
  triggered_at: string;
  employee_id: string;
  employee_name: string;
  department: string;
  title: string;
  severity: 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW' | 'INFORMATIONAL';
  status: 'NEW' | 'TRIAGED' | 'ESCALATED' | 'CLOSED_BENIGN' | 'CLOSED_MALICIOUS';
  risk_score: number;
}

const SAMPLE_ALERTS: AlertItem[] = [
  {
    id: '1',
    alert_id: 'ALT-2026-00481',
    triggered_at: '2026-09-07 15:42:19',
    employee_id: 'EMP-TREAS-894',
    employee_name: 'Marcus Vance',
    department: 'TREASURY_OPERATIONS',
    title: 'High-Value SWIFT Transfer Queue Extraction without Dual-Control Key',
    severity: 'CRITICAL',
    status: 'NEW',
    risk_score: 94,
  },
  {
    id: '2',
    alert_id: 'ALT-2026-00479',
    triggered_at: '2026-09-07 14:18:04',
    employee_id: 'EMP-WEALTH-302',
    employee_name: 'Elena Rostova',
    department: 'WEALTH_MANAGEMENT',
    title: 'Bulk Export of Confidential Client Portfolio Valuations (1.4k records)',
    severity: 'CRITICAL',
    status: 'ESCALATED',
    risk_score: 88,
  },
  {
    id: '3',
    alert_id: 'ALT-2026-00472',
    triggered_at: '2026-09-07 13:05:44',
    employee_id: 'EMP-ITOPS-118',
    employee_name: 'David Chen',
    department: 'IT_OPERATIONS',
    title: 'Off-Hours Privilege Escalation: Added Self to Core Banking DBA Group',
    severity: 'HIGH',
    status: 'TRIAGED',
    risk_score: 82,
  },
  {
    id: '4',
    alert_id: 'ALT-2026-00465',
    triggered_at: '2026-09-07 11:22:30',
    employee_id: 'EMP-LOAN-542',
    employee_name: 'Sarah Jenkins',
    department: 'LOAN_ORIGINATION',
    title: 'Anomalous Query Rate on Declined Commercial Credit Files',
    severity: 'MEDIUM',
    status: 'NEW',
    risk_score: 68,
  },
];

export const Alerts: React.FC = () => {
  const columns: Column<AlertItem>[] = [
    {
      header: 'ALERT ID',
      accessor: (r) => <span className="font-semibold text-slate-300">{r.alert_id}</span>,
      width: '130px',
    },
    {
      header: 'TRIGGERED AT',
      accessor: (r) => <span className="text-socText-muted">{r.triggered_at}</span>,
      width: '160px',
    },
    {
      header: 'SEVERITY',
      accessor: (r) => <SeverityBadge severity={r.severity} />,
      width: '90px',
    },
    {
      header: 'RISK SCORE',
      accessor: (r) => <RiskScoreBadge score={r.risk_score} showLabel size="sm" />,
      width: '100px',
    },
    {
      header: 'EMPLOYEE / DEPT',
      accessor: (r) => (
        <div>
          <div className="text-slate-200 font-medium">{r.employee_name}</div>
          <div className="text-socText-muted text-2xs">{r.employee_id} • {r.department}</div>
        </div>
      ),
      width: '220px',
    },
    {
      header: 'DESCRIPTION',
      accessor: (r) => <span className="text-slate-300">{r.title}</span>,
    },
    {
      header: 'STATUS',
      accessor: (r) => <StatusBadge status={r.status} />,
      width: '120px',
    },
  ];

  return (
    <div className="space-y-3">
      {/* Search & Filter Toolbar */}
      <div className="bg-soc-panel border border-soc-border p-2 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="relative">
            <Search className="w-3.5 h-3.5 absolute left-2.5 top-2 text-socText-muted" />
            <input
              type="text"
              placeholder="Filter by Alert ID, Employee, Dept, or Trigger..."
              className="bg-soc-bg border border-soc-border pl-8 pr-3 py-1 text-xs font-mono-dense text-slate-200 focus:outline-none focus:border-soc-borderFocus rounded-sm w-80"
            />
          </div>
          <button className="flex items-center gap-1.5 px-2.5 py-1 bg-soc-elevated border border-soc-border text-xs font-mono-dense text-slate-300 hover:text-slate-100 rounded-sm">
            <Filter className="w-3.5 h-3.5 text-socText-muted" />
            <span>SEVERITY: ALL</span>
          </button>
        </div>
        <div className="text-2xs font-mono-dense text-socText-muted">
          SHOWING 4 OF 4 UNRESOLVED ALERTS
        </div>
      </div>

      {/* Dense Alerts Table */}
      <div className="soc-panel">
        <div className="soc-panel-header">
          <div className="flex items-center gap-2">
            <AlertTriangle className="w-3.5 h-3.5 text-amber-400" />
            <span className="font-mono-dense uppercase">ACTIVE INCIDENT & ALERT QUEUE</span>
          </div>
          <span className="text-2xs font-mono-dense text-socText-muted">ACTION REQUIRED</span>
        </div>
        <DenseTable
          columns={columns}
          data={SAMPLE_ALERTS}
          keyExtractor={(r) => r.id}
          onRowClick={(r) => console.log('Triage alert:', r.alert_id)}
        />
      </div>
    </div>
  );
};
