import React from 'react';
import { clsx } from 'clsx';
import { AlertSeverity, AlertStatus, RiskTier } from '../../types';

interface BadgeProps {
  children: React.ReactNode;
  variant?: 'critical' | 'high' | 'medium' | 'low' | 'benign' | 'info' | 'neutral';
  className?: string;
  size?: 'xs' | 'sm';
}

export const Badge: React.FC<BadgeProps> = ({
  children,
  variant = 'neutral',
  className,
  size = 'xs',
}) => {
  const variantStyles = {
    critical: 'bg-threat-criticalBg border-threat-criticalBorder text-threat-criticalText',
    high: 'bg-threat-highBg border-threat-highBorder text-threat-highText',
    medium: 'bg-threat-mediumBg border-threat-mediumBorder text-threat-mediumText',
    low: 'bg-threat-lowBg border-threat-lowBorder text-threat-lowText',
    benign: 'bg-threat-benignBg border-threat-benignBorder text-threat-benignText',
    info: 'bg-threat-infoBg border-threat-infoBorder text-threat-infoText',
    neutral: 'bg-soc-subtle border-soc-border text-socText-secondary',
  };

  const sizeStyles = {
    xs: 'text-2xs px-1.5 py-0.5',
    sm: 'text-xs px-2 py-0.5',
  };

  return (
    <span
      className={clsx(
        'inline-flex items-center font-mono-dense font-medium border uppercase tracking-wider rounded-sm',
        variantStyles[variant],
        sizeStyles[size],
        className
      )}
    >
      {children}
    </span>
  );
};

export const SeverityBadge: React.FC<{ severity: AlertSeverity }> = ({ severity }) => {
  const map: Record<AlertSeverity, 'critical' | 'high' | 'medium' | 'low' | 'info'> = {
    CRITICAL: 'critical',
    HIGH: 'high',
    MEDIUM: 'medium',
    LOW: 'low',
    INFORMATIONAL: 'info',
  };
  return <Badge variant={map[severity]}>{severity}</Badge>;
};

export const StatusBadge: React.FC<{ status: AlertStatus }> = ({ status }) => {
  const map: Record<AlertStatus, 'critical' | 'high' | 'medium' | 'low' | 'benign'> = {
    NEW: 'critical',
    ESCALATED: 'high',
    TRIAGED: 'medium',
    CLOSED_MALICIOUS: 'critical',
    CLOSED_BENIGN: 'benign',
  };
  return <Badge variant={map[status]}>{status.replace('_', ' ')}</Badge>;
};

export const DepartmentBadge: React.FC<{ code: string }> = ({ code }) => {
  return (
    <span className="inline-flex items-center text-2xs font-mono-dense text-slate-300 bg-soc-elevated px-1.5 py-0.5 border border-soc-border rounded-sm">
      {code.replace('_', ' ')}
    </span>
  );
};
