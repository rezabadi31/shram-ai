import React from 'react';
import { CheckCircle2, Circle, Loader2 } from 'lucide-react';

export interface ProgressStep {
  label: string;
  status: 'complete' | 'current' | 'upcoming';
}

interface ProgressBarProps {
  steps: ProgressStep[];
}

export const ProgressBar: React.FC<ProgressBarProps> = ({ steps }) => {
  return (
    <div className="w-full py-3">
      <div className="grid grid-cols-1 sm:grid-cols-5 gap-2">
        {steps.map((step, idx) => {
          const isComplete = step.status === 'complete';
          const isCurrent = step.status === 'current';

          return (
            <div
              key={idx}
              className={`flex items-center gap-2 p-2.5 rounded-lg border text-xs font-medium transition ${
                isComplete
                  ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-300'
                  : isCurrent
                  ? 'bg-blue-500/15 border-blue-500/40 text-blue-200 ring-1 ring-blue-500/30'
                  : 'bg-slate-900/40 border-slate-800/80 text-slate-500'
              }`}
            >
              {isComplete ? (
                <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
              ) : isCurrent ? (
                <Loader2 className="w-4 h-4 text-blue-400 animate-spin shrink-0" />
              ) : (
                <Circle className="w-4 h-4 text-slate-600 shrink-0" />
              )}
              <span className="truncate">{step.label}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
};
