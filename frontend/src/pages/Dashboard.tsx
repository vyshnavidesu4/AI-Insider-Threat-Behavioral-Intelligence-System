import React from 'react';
import {
  ShieldAlert,
  Users,
  Activity,
  ArrowUpRight,
  TrendingUp,
  Flame,
  Clock,
  Building2,
} from 'lucide-react';
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';
import { DenseTable, Column } from '../components/common/Table';
import { SeverityBadge, StatusBadge, DepartmentBadge } from '../components/common/Badge';
import { RiskScoreBadge } from '../components/common/RiskScoreBadge';

// Sample mock threat alerts tailored to regional banking operations
const MOCK_CRITICAL_ALERTS = [
  {
    id: '1',
    alert_id: 'ALT-2026-00481',
    timestamp: '2026-09-07 15:42:19',
    employee_name: 'Marcus Vance',
    employee_id: 'EMP-TREAS-894',
    department: 'TREASURY_OPERATIONS',
    event_type: 'WIRE_TRANSFER_INITIATED',
    details: 'Attempted $4.2M after-hours swift queue export without secondary dual-control key',
    risk_score: 94,
    severity: 'CRITICAL' as const,
    status: 'NEW' as const,
  },
  {
    id: '2',
    alert_id: 'ALT-2026-00479',
    timestamp: '2026-09-07 14:18:04',
    employee_name: 'Elena Rostova',
    employee_id: 'EMP-WEALTH-302',
    department: 'WEALTH_MANAGEMENT',
    event_type: 'FILE_ACCESS',
    details: 'Bulk download: 1,420 High-Net-Worth client KYC dossiers to external portable storage',
    risk_score: 88,
    severity: 'CRITICAL' as const,
    status: 'ESCALATED' as const,
  },
  {
    id: '3',
    alert_id: 'ALT-2026-00472',
    timestamp: '2026-09-07 13:05:44',
    employee_name: 'David Chen',
    employee_id: 'EMP-ITOPS-118',
    department: 'IT_OPERATIONS',
    event_type: 'PRIVILEGE_CHANGE',
    details: 'Unauthorized elevation of service principal to Global Core Banking schema admin',
    risk_score: 82,
    severity: 'HIGH' as const,
    status: 'TRIAGED' as const,
  },
  {
    id: '4',
    alert_id: 'ALT-2026-00465',
    timestamp: '2026-09-07 11:22:30',
    employee_name: 'Sarah Jenkins',
    employee_id: 'EMP-LOAN-542',
    department: 'LOAN_ORIGINATION',
    event_type: 'DB_QUERY',
    details: 'Off-schedule extraction of rejected commercial credit scores & SSNs',
    risk_score: 68,
    severity: 'MEDIUM' as const,
    status: 'NEW' as const,
  },
];

const TELEMETRY_STREAM = [
  { time: '08:00', normal: 1240, anomalous: 4 },
  { time: '10:00', normal: 2890, anomalous: 12 },
  { time: '12:00', normal: 2450, anomalous: 8 },
  { time: '14:00', normal: 3120, anomalous: 28 },
  { time: '16:00', normal: 2980, anomalous: 45 },
  { time: '18:00', normal: 1100, anomalous: 34 },
  { time: '20:00', normal: 420, anomalous: 19 },
];

const DEPARTMENT_RISK_MATRIX = [
  { code: 'TREASURY_OPERATIONS', name: 'Treasury Operations', risk_tier: 'CRITICAL', avg_score: 74.2, active_alerts: 4, baseline_deviation: '+38%' },
  { code: 'WEALTH_MANAGEMENT', name: 'Wealth Management', risk_tier: 'HIGH', avg_score: 62.8, active_alerts: 3, baseline_deviation: '+21%' },
  { code: 'IT_OPERATIONS', name: 'IT Operations', risk_tier: 'HIGH', avg_score: 58.4, active_alerts: 2, baseline_deviation: '+14%' },
  { code: 'LOAN_ORIGINATION', name: 'Loan Origination', risk_tier: 'MEDIUM', avg_score: 34.1, active_alerts: 1, baseline_deviation: '+4%' },
  { code: 'RETAIL_BANKING', name: 'Retail Banking', risk_tier: 'LOW', avg_score: 18.5, active_alerts: 0, baseline_deviation: '-2%' },
  { code: 'COMPLIANCE_AND_RISK', name: 'Compliance & Risk', risk_tier: 'LOW', avg_score: 12.0, active_alerts: 0, baseline_deviation: '-8%' },
];

export const Dashboard: React.FC = () => {
  const alertColumns: Column<(typeof MOCK_CRITICAL_ALERTS)[0]>[] = [
    {
      header: 'ALERT ID',
      accessor: (r) => <span className="text-slate-300 font-semibold">{r.alert_id}</span>,
      width: '130px',
    },
    {
      header: 'TIMESTAMP',
      accessor: (r) => <span className="text-socText-muted">{r.timestamp}</span>,
      width: '160px',
    },
    {
      header: 'SEV',
      accessor: (r) => <SeverityBadge severity={r.severity} />,
      width: '90px',
    },
    {
      header: 'RISK SCORE',
      accessor: (r) => <RiskScoreBadge score={r.risk_score} showLabel size="sm" />,
      width: '100px',
    },
    {
      header: 'SUBJECT / DEPT',
      accessor: (r) => (
        <div className="flex flex-col">
          <span className="text-slate-200 font-sans font-medium text-xs">{r.employee_name}</span>
          <span className="text-socText-muted text-2xs font-mono-dense">{r.employee_id} • {r.department}</span>
        </div>
      ),
      width: '220px',
    },
    {
      header: 'DETECTED BEHAVIOR / HEURISTIC',
      accessor: (r) => <span className="text-slate-300">{r.details}</span>,
    },
    {
      header: 'STATUS',
      accessor: (r) => <StatusBadge status={r.status} />,
      width: '110px',
    },
  ];

  return (
    <div className="space-y-3">
      {/* Top Operational Metrics Ribbon */}
      <div className="grid grid-cols-4 gap-2">
        <div className="bg-soc-panel border border-soc-border p-3 flex items-center justify-between">
          <div>
            <div className="text-2xs font-mono-dense text-socText-muted uppercase">
              CRITICAL ANOMALIES (24H)
            </div>
            <div className="text-xl font-mono-dense font-bold text-threat-criticalText mt-0.5">
              12 <span className="text-xs font-normal text-slate-400">/ 142 TOTAL</span>
            </div>
          </div>
          <Flame className="w-5 h-5 text-red-500 opacity-80" />
        </div>

        <div className="bg-soc-panel border border-soc-border p-3 flex items-center justify-between">
          <div>
            <div className="text-2xs font-mono-dense text-socText-muted uppercase">
              HIGH-RISK INSIDERS
            </div>
            <div className="text-xl font-mono-dense font-bold text-threat-highText mt-0.5">
              8 <span className="text-xs font-normal text-slate-400">PERSONNEL</span>
            </div>
          </div>
          <ShieldAlert className="w-5 h-5 text-amber-500 opacity-80" />
        </div>

        <div className="bg-soc-panel border border-soc-border p-3 flex items-center justify-between">
          <div>
            <div className="text-2xs font-mono-dense text-socText-muted uppercase">
              BANK STAFF MONITORED
            </div>
            <div className="text-xl font-mono-dense font-bold text-slate-100 mt-0.5">
              840 <span className="text-xs font-normal text-slate-400">ACCOUNTS</span>
            </div>
          </div>
          <Users className="w-5 h-5 text-slate-400 opacity-80" />
        </div>

        <div className="bg-soc-panel border border-soc-border p-3 flex items-center justify-between">
          <div>
            <div className="text-2xs font-mono-dense text-socText-muted uppercase">
              TELEMETRY INGEST RATE
            </div>
            <div className="text-xl font-mono-dense font-bold text-emerald-400 mt-0.5">
              14.2K <span className="text-xs font-normal text-slate-400">EVT/HR</span>
            </div>
          </div>
          <Activity className="w-5 h-5 text-emerald-500 opacity-80" />
        </div>
      </div>

      {/* Main Grid: Priority Threat Stream & Department Risk Matrix */}
      <div className="grid grid-cols-3 gap-3">
        {/* Left 2 Cols: Priority Threat Stream */}
        <div className="col-span-2 space-y-3">
          <div className="soc-panel">
            <div className="soc-panel-header">
              <div className="flex items-center gap-2">
                <ShieldAlert className="w-3.5 h-3.5 text-red-400" />
                <span className="font-mono-dense uppercase">ACTIVE BEHAVIORAL THREAT QUEUE</span>
              </div>
              <span className="text-2xs font-mono-dense text-socText-muted">REFRESHED: LIVE</span>
            </div>
            <DenseTable
              columns={alertColumns}
              data={MOCK_CRITICAL_ALERTS}
              keyExtractor={(r) => r.id}
            />
          </div>

          {/* Telemetry Chart */}
          <div className="soc-panel p-3">
            <div className="flex items-center justify-between mb-2">
              <div className="text-xs font-mono-dense font-bold text-slate-200 uppercase">
                TELEMETRY INGESTION & ANOMALOUS ACTIVITY PEAKS (24H)
              </div>
              <div className="flex items-center gap-3 text-2xs font-mono-dense">
                <span className="flex items-center gap-1 text-slate-400">
                  <span className="w-2 h-2 bg-slate-600 rounded-sm inline-block" /> Normal Events
                </span>
                <span className="flex items-center gap-1 text-red-400">
                  <span className="w-2 h-2 bg-red-600 rounded-sm inline-block" /> Anomalous Spike
                </span>
              </div>
            </div>
            <div className="h-44 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={TELEMETRY_STREAM} margin={{ top: 5, right: 10, left: -20, bottom: 0 }}>
                  <XAxis dataKey="time" stroke="#475569" tick={{ fill: '#64748b', fontSize: 10, fontFamily: 'JetBrains Mono' }} />
                  <YAxis stroke="#475569" tick={{ fill: '#64748b', fontSize: 10, fontFamily: 'JetBrains Mono' }} />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: '#0f172a',
                      borderColor: '#334155',
                      fontSize: '11px',
                      fontFamily: 'JetBrains Mono',
                    }}
                  />
                  <Area type="monotone" dataKey="normal" stroke="#475569" fill="#1e293b" fillOpacity={0.6} />
                  <Area type="monotone" dataKey="anomalous" stroke="#dc2626" fill="#7f1d1d" fillOpacity={0.8} />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>

        {/* Right Col: Regional Bank Department Matrix */}
        <div className="space-y-3">
          <div className="soc-panel">
            <div className="soc-panel-header">
              <div className="flex items-center gap-2">
                <Building2 className="w-3.5 h-3.5 text-slate-400" />
                <span className="font-mono-dense uppercase">DEPARTMENT RISK MATRIX</span>
              </div>
              <span className="text-2xs font-mono-dense text-socText-muted">6 ENTITIES</span>
            </div>
            <div className="divide-y divide-soc-borderMuted">
              {DEPARTMENT_RISK_MATRIX.map((dept) => (
                <div key={dept.code} className="p-2.5 hover:bg-soc-subtle transition-colors flex items-center justify-between">
                  <div>
                    <div className="text-xs font-semibold text-slate-200">{dept.name}</div>
                    <div className="flex items-center gap-2 mt-1 text-2xs font-mono-dense text-socText-muted">
                      <span>DEVIATION: <strong className={dept.baseline_deviation.startsWith('+') ? 'text-amber-400' : 'text-emerald-400'}>{dept.baseline_deviation}</strong></span>
                      <span>•</span>
                      <span>ALERTS: {dept.active_alerts}</span>
                    </div>
                  </div>
                  <RiskScoreBadge score={dept.avg_score} size="sm" />
                </div>
              ))}
            </div>
          </div>

          {/* 5-Factor Risk Weighting Spec Reference */}
          <div className="soc-panel p-3 space-y-2">
            <div className="text-2xs font-mono-dense text-slate-400 uppercase font-bold border-b border-soc-borderMuted pb-1">
              WEIGHTED THREAT ENGINE HEURISTICS
            </div>
            <div className="space-y-1.5 text-2xs font-mono-dense">
              <div className="flex justify-between text-slate-300">
                <span>Behavioral Anomalies:</span>
                <strong className="text-slate-100">35%</strong>
              </div>
              <div className="flex justify-between text-slate-300">
                <span>Privilege Misuse:</span>
                <strong className="text-slate-100">25%</strong>
              </div>
              <div className="flex justify-between text-slate-300">
                <span>Data Access Violations:</span>
                <strong className="text-slate-100">20%</strong>
              </div>
              <div className="flex justify-between text-slate-300">
                <span>Access Pattern Deviations:</span>
                <strong className="text-slate-100">10%</strong>
              </div>
              <div className="flex justify-between text-slate-300">
                <span>Historical Security Events:</span>
                <strong className="text-slate-100">10%</strong>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
