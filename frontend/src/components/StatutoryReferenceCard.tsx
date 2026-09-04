import React from 'react';
import { Scale, BookOpen } from 'lucide-react';

interface StatutoryReferenceCardProps {
  statute: string;
  authority: string;
  citationSnippet?: string;
}

export const StatutoryReferenceCard: React.FC<StatutoryReferenceCardProps> = ({
  statute,
  authority,
  citationSnippet,
}) => {
  return (
    <div className="bg-slate-900/80 border border-slate-800 rounded-lg p-3 space-y-1.5">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-1.5 text-xs text-amber-400 font-semibold">
          <Scale className="w-3.5 h-3.5" />
          <span>{statute}</span>
        </div>
        <span className="text-[10px] text-slate-400 bg-slate-800 px-2 py-0.5 rounded font-mono">
          Authoritative Source
        </span>
      </div>
      <p className="text-[11px] text-slate-400 flex items-center gap-1">
        <BookOpen className="w-3 h-3 text-slate-500" />
        Enforcing Authority: <span className="text-slate-300 font-medium">{authority}</span>
      </p>
      {citationSnippet && (
        <p className="text-xs text-slate-300 italic bg-slate-950/60 p-2 rounded border border-slate-850">
          "{citationSnippet}"
        </p>
      )}
    </div>
  );
};
