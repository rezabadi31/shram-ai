import React from 'react';
import { LucideIcon } from 'lucide-react';

interface MetricCardProps {
  label: string;
  value: string | number;
  subtext?: string;
  icon: LucideIcon;
  variant?: 'default' | 'danger' | 'warning' | 'success';
}

export const MetricCard: React.FC<MetricCardProps> = ({
  label,
  value,
  subtext,
  icon: Icon,
  variant = 'default',
}) => {
  const iconColors = {
    default: 'text-blue-400 bg-blue-500/10 border-blue-500/20',
    danger: 'text-rose-400 bg-rose-500/10 border-rose-500/20',
    warning: 'text-amber-400 bg-amber-500/10 border-amber-500/20',
    success: 'text-emerald-400 bg-emerald-500/10 border-emerald-500/20',
  }[variant];

  return (
    <div className="glass-panel p-5 rounded-xl border border-slate-800 transition hover:border-slate-700 flex flex-col justify-between">
      <div className="flex items-center justify-between">
        <span className="text-xs text-slate-400 font-medium tracking-wide">{label}</span>
        <div className={`p-2 rounded-lg border ${iconColors}`}>
          <Icon className="w-4 h-4" />
        </div>
      </div>
      <div className="mt-3">
        <div className="text-2xl sm:text-3xl font-extrabold tracking-tight text-white font-mono">
          {value}
        </div>
        {subtext && (
          <p className="text-[11px] text-slate-400 mt-1 font-medium">{subtext}</p>
        )}
      </div>
    </div>
  );
};
