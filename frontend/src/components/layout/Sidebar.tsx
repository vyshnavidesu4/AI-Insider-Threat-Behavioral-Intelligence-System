import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  AlertTriangle,
  Users,
  FolderLock,
  FileSpreadsheet,
  Settings,
} from 'lucide-react';
import { clsx } from 'clsx';

export const Sidebar: React.FC = () => {
  const navItems = [
    { to: '/', label: 'SOC Overview', icon: LayoutDashboard, exact: true },
    { to: '/alerts', label: 'Triage Alerts', icon: AlertTriangle, badge: '5 ACTIVE' },
    { to: '/employees', label: 'Employee Dossiers', icon: Users },
    { to: '/investigations', label: 'Case Management', icon: FolderLock },
  ];

  return (
    <aside className="w-52 bg-soc-panel border-r border-soc-border flex flex-col justify-between select-none">
      <div className="py-2">
        <div className="px-3 py-1.5 text-2xs font-mono-dense text-socText-muted uppercase tracking-wider">
          Threat Monitoring
        </div>
        <nav className="space-y-0.5 px-1.5">
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.exact}
              className={({ isActive }) =>
                clsx(
                  'flex items-center justify-between px-2.5 py-1.5 text-xs font-mono-dense rounded-sm transition-colors',
                  isActive
                    ? 'bg-soc-elevated text-slate-100 border border-soc-border font-medium'
                    : 'text-socText-secondary hover:text-slate-200 hover:bg-soc-subtle border border-transparent'
                )
              }
            >
              <div className="flex items-center gap-2">
                <item.icon className="w-3.5 h-3.5 text-socText-muted" />
                <span>{item.label}</span>
              </div>
              {item.badge && (
                <span className="text-2xs font-mono-dense bg-threat-criticalBg text-threat-criticalText border border-threat-criticalBorder px-1 py-0.2 rounded-sm">
                  {item.badge}
                </span>
              )}
            </NavLink>
          ))}
        </nav>
      </div>

      {/* Scope Footer */}
      <div className="p-3 border-t border-soc-border text-2xs font-mono-dense text-socText-muted space-y-1 bg-soc-bg/50">
        <div className="text-slate-300 font-semibold">TARGET INSTITUTION:</div>
        <div>REGIONAL BANK CORP</div>
        <div className="text-slate-500">6 MONITORED DEPTS</div>
      </div>
    </aside>
  );
};
