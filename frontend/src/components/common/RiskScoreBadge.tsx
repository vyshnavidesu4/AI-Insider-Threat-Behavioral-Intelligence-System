import React from 'react';
import { clsx } from 'clsx';

interface RiskScoreBadgeProps {
  score: number;
  showLabel?: boolean;
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

export const RiskScoreBadge: React.FC<RiskScoreBadgeProps> = ({
  score,
  showLabel = false,
  size = 'md',
  className,
}) => {
  const normalized = Math.max(0, Math.min(100, Math.round(score)));

  let colorClasses = 'bg-threat-benignBg border-threat-benignBorder text-threat-benignText';
  let tierLabel = 'LOW';

  if (normalized >= 80) {
    colorClasses = 'bg-threat-criticalBg border-threat-criticalBorder text-threat-criticalText';
    tierLabel = 'CRITICAL';
  } else if (normalized >= 60) {
    colorClasses = 'bg-threat-highBg border-threat-highBorder text-threat-highText';
    tierLabel = 'HIGH';
  } else if (normalized >= 40) {
    colorClasses = 'bg-threat-mediumBg border-threat-mediumBorder text-threat-mediumText';
    tierLabel = 'MED';
  } else if (normalized >= 20) {
    colorClasses = 'bg-threat-lowBg border-threat-lowBorder text-threat-lowText';
    tierLabel = 'LOW';
  }

  const sizeClasses = {
    sm: 'text-2xs px-1.5 py-0.2',
    md: 'text-xs px-2 py-0.5 font-bold',
    lg: 'text-sm px-2.5 py-1 font-bold',
  };

  return (
    <div className={clsx('inline-flex items-center gap-1 font-mono-dense border rounded-sm', colorClasses, sizeClasses[size], className)}>
      <span>{normalized.toString().padStart(2, '0')}</span>
      {showLabel && <span className="text-2xs opacity-75">[{tierLabel}]</span>}
    </div>
  );
};
