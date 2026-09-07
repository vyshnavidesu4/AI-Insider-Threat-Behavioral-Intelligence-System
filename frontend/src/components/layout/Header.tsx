import React from 'react';
import { Shield, Activity, Bell, LogOut, User } from 'lucide-react';
import { useAuth } from '../../hooks/useAuth';
import { Badge } from '../common/Badge';

export const Header: React.FC = () => {
  const { user, logout } = useAuth();

  return (
    <header className="h-10 bg-soc-panel border-b border-soc-border px-4 flex items-center justify-between select-none z-20">
      {/* Brand & System Node Status */}
      <div className="flex items-center gap-3">
        <div className="flex items-center gap-1.5 font-bold tracking-wider text-xs text-slate-100">
          <Shield className="w-4 h-4 text-emerald-500" />
          <span className="font-mono-dense uppercase tracking-widest text-slate-200">
            SENTINEL // BANK-SOC
          </span>
        </div>
        <div className="h-3 w-[1px] bg-soc-border" />
        <div className="flex items-center gap-1.5 text-2xs font-mono-dense text-emerald-400">
          <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
          <span>INGESTION: ACTIVE (6 REGIONS)</span>
        </div>
      </div>

      {/* Operator Session & Role Actions */}
      <div className="flex items-center gap-4 text-xs">
        {user && (
          <div className="flex items-center gap-2">
            <div className="flex items-center gap-1 text-socText-secondary font-mono-dense text-2xs">
              <User className="w-3.5 h-3.5 text-socText-muted" />
              <span>{user.email}</span>
            </div>
            <Badge
              variant={
                user.role === 'admin'
                  ? 'critical'
                  : user.role === 'manager'
                  ? 'high'
                  : 'low'
              }
            >
              ROLE: {user.role}
            </Badge>
            <button
              onClick={logout}
              title="Terminate Session"
              className="p-1 hover:bg-soc-elevated text-socText-muted hover:text-red-400 border border-transparent hover:border-soc-border rounded-sm transition-colors"
            >
              <LogOut className="w-3.5 h-3.5" />
            </button>
          </div>
        )}
      </div>
    </header>
  );
};
