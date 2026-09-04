import React from 'react';

interface RiskBadgeProps {
  category: 'HIGH' | 'MEDIUM' | 'LOW' | string;
  score?: number;
  size?: 'sm' | 'md' | 'lg';
}

export const RiskBadge: React.FC<RiskBadgeProps> = ({ category, score, size = 'md' }) => {
  const cat = category.toUpperCase();

  const styles = {
    HIGH: 'bg-rose-500/15 text-rose-300 border-rose-500/30',
    MEDIUM: 'bg-amber-500/15 text-amber-300 border-amber-500/30',
    LOW: 'bg-emerald-500/15 text-emerald-300 border-emerald-500/30',
  }[cat] || 'bg-slate-700/30 text-slate-300 border-slate-600';

  const dotColor = {
    HIGH: 'bg-rose-400 animate-pulse',
    MEDIUM: 'bg-amber-400',
    LOW: 'bg-emerald-400',
  }[cat] || 'bg-slate-400';

  const sizeClasses = {
    sm: 'text-[10px] px-2 py-0.5 gap-1.5',
    md: 'text-xs px-2.5 py-1 gap-2',
    lg: 'text-sm px-3.5 py-1.5 gap-2.5 font-bold',
  }[size];

  return (
    <span className={`inline-flex items-center font-semibold rounded-full border ${styles} ${sizeClasses}`}>
      <span className={`w-2 h-2 rounded-full ${dotColor}`} />
      <span>{cat} RISK</span>
      {score !== undefined && (
        <span className="font-mono opacity-80">({score})</span>
      )}
    </span>
  );
};
