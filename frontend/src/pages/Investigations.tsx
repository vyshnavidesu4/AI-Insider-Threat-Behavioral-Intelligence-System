import React from 'react';
import { FolderLock, Plus, Search } from 'lucide-react';
import { DenseTable, Column } from '../components/common/Table';
import { Badge } from '../components/common/Badge';

interface CaseItem {
  id: string;
  case_number: string;
  title: string;
  target_employee: string;
  assigned_analyst: string;
  status: 'OPEN' | 'IN_PROGRESS' | 'UNDER_REVIEW' | 'RESOLVED' | 'REFERRED_TO_LEGAL';
  priority: 'P1_URGENT' | 'P2_HIGH' | 'P3_MEDIUM' | 'P4_LOW';
  created_at: string;
}

const SAMPLE_CASES: CaseItem[] = [
  {
    id: '1',
    case_number: 'INV-2026-0089',
    title: 'Off-Hours Wire Transfer Sequence Anomaly ($4.2M Swift Route)',
    target_employee: 'Marcus Vance (EMP-TREAS-894)',
    assigned_analyst: 'analyst@regionalbank.com',
    status: 'IN_PROGRESS',
    priority: 'P1_URGENT',
    created_at: '2026-09-07 15:50',
  },
  {
    id: '2',
    case_number: 'INV-2026-0085',
    title: 'Unauthorized HNW Client Portfolio Extraction Prior to Resignation Notice',
    target_employee: 'Elena Rostova (EMP-WEALTH-302)',
    assigned_analyst: 'manager@regionalbank.com',
    status: 'UNDER_REVIEW',
    priority: 'P2_HIGH',
    created_at: '2026-09-07 14:30',
  },
];

export const Investigations: React.FC = () => {
  const columns: Column<CaseItem>[] = [
    {
      header: 'CASE #',
      accessor: (r) => <span className="font-semibold text-slate-300">{r.case_number}</span>,
      width: '140px',
    },
    {
      header: 'CREATED',
      accessor: (r) => <span className="text-socText-muted">{r.created_at}</span>,
      width: '150px',
    },
    {
      header: 'PRIORITY',
      accessor: (r) => (
        <Badge variant={r.priority === 'P1_URGENT' ? 'critical' : 'high'}>
          {r.priority.replace('_', ' ')}
        </Badge>
      ),
      width: '120px',
    },
    {
      header: 'CASE TITLE',
      accessor: (r) => <span className="text-slate-200 font-medium">{r.title}</span>,
    },
    {
      header: 'TARGET SUBJECT',
      accessor: (r) => <span className="text-slate-300">{r.target_employee}</span>,
      width: '240px',
    },
    {
      header: 'ASSIGNED ANALYST',
      accessor: (r) => <span className="text-socText-muted text-2xs">{r.assigned_analyst}</span>,
      width: '200px',
    },
    {
      header: 'STATUS',
      accessor: (r) => (
        <Badge variant={r.status === 'IN_PROGRESS' ? 'high' : 'medium'}>
          {r.status.replace('_', ' ')}
        </Badge>
      ),
      width: '130px',
    },
  ];

  return (
    <div className="space-y-3">
      {/* Action Toolbar */}
      <div className="bg-soc-panel border border-soc-border p-2 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="relative">
            <Search className="w-3.5 h-3.5 absolute left-2.5 top-2 text-socText-muted" />
            <input
              type="text"
              placeholder="Search case files, hypotheses, evidence..."
              className="bg-soc-bg border border-soc-border pl-8 pr-3 py-1 text-xs font-mono-dense text-slate-200 focus:outline-none focus:border-soc-borderFocus rounded-sm w-80"
            />
          </div>
        </div>
        <button className="flex items-center gap-1.5 px-3 py-1 bg-soc-elevated hover:bg-slate-700 text-slate-100 border border-soc-border text-xs font-mono-dense font-bold uppercase rounded-sm transition-colors">
          <Plus className="w-3.5 h-3.5 text-emerald-400" />
          <span>INITIALIZE CASE FILE</span>
        </button>
      </div>

      <div className="soc-panel">
        <div className="soc-panel-header">
          <div className="flex items-center gap-2">
            <FolderLock className="w-3.5 h-3.5 text-slate-300" />
            <span className="font-mono-dense uppercase">INSIDER THREAT INVESTIGATION DOSSIERS</span>
          </div>
          <span className="text-2xs font-mono-dense text-socText-muted">2 ACTIVE CASES</span>
        </div>
        <DenseTable
          columns={columns}
          data={SAMPLE_CASES}
          keyExtractor={(r) => r.id}
          onRowClick={(r) => console.log('Open case file:', r.case_number)}
        />
      </div>
    </div>
  );
};
