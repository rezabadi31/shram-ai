import React, { useState, useEffect } from 'react';
import {
  ClipboardList,
  CheckCircle2,
  XCircle,
  AlertOctagon,
  ChevronDown,
  ChevronUp,
  FileCheck2,
  Send,
  ArrowLeft,
  Loader2,
  Shield,
  AlertTriangle,
  BadgeCheck,
  StickyNote,
  Plus,
  Trash2,
} from 'lucide-react';
import { ActiveRole } from '../types';
import { API_BASE } from '../config/api';

// ------ API helpers (inline fallback for demo) ------

async function apiStartSession(establishmentId: string, establishmentName: string): Promise<any> {
  try {
    const res = await fetch(
      `${API_BASE}/inspection/start?establishment_id=${encodeURIComponent(establishmentId)}&establishment_name=${encodeURIComponent(establishmentName)}&inspector_id=INS-OFFICER-42`,
      { method: 'POST' }
    );
    if (!res.ok) throw new Error('start failed');
    return await res.json();
  } catch {
    // Demo fallback session
    return {
      session_id: `INSP-DEMO${Math.random().toString(36).substring(2, 6).toUpperCase()}`,
      establishment_id: establishmentId,
      establishment_name: establishmentName,
      inspector_id: 'INS-OFFICER-42',
      started_at: new Date().toLocaleString('en-IN'),
      status: 'ACTIVE',
      violations_found: 0,
      documents_seized: [],
      field_notes: '',
      violation_docket: [],
      total_penalty_proposed_inr: 0,
      checklist: DEMO_CHECKLIST,
    };
  }
}

async function apiSubmitSession(payload: any): Promise<any> {
  try {
    const res = await fetch(`${API_BASE}/inspection/submit`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error('submit failed');
    return await res.json();
  } catch {
    const violations = payload.checklist.filter((i: any) => ['HIGH', 'CRITICAL', 'MEDIUM'].includes(i.severity));
    const penaltyMap: Record<string, number> = { CRITICAL: 50000, HIGH: 20000, MEDIUM: 10000, LOW: 5000, NONE: 0 };
    const docket = violations.map((v: any) => ({
      violation_id: `VIO-${Math.random().toString(36).substring(2, 8).toUpperCase()}`,
      code_section: v.statutory_ref,
      description: v.finding || v.description,
      evidence_collected: payload.documents_seized,
      suggested_penalty_inr: penaltyMap[v.severity] || 10000,
      severity: v.severity,
    }));
    return {
      session_id: payload.session_id,
      status: 'SUBMITTED',
      violations_found: docket.length,
      total_penalty_proposed_inr: docket.reduce((s: number, d: any) => s + d.suggested_penalty_inr, 0),
      violation_docket: docket,
      report_ref: `RPT-${Math.random().toString(36).substring(2, 10).toUpperCase()}`,
      timestamp: new Date().toLocaleString('en-IN'),
    };
  }
}

const DEMO_CHECKLIST = [
  { item_id: 'WR-01', category: 'Wage Registers', description: 'Verify Form B Wage Register is maintained for all workers with correct minimum wage entries', statutory_ref: 'Code on Wages 2019 — Section 6, Form B', is_verified: false, finding: null, severity: 'NONE' },
  { item_id: 'WR-02', category: 'Wage Registers', description: 'Verify overtime wage entries are at 2x regular rate and recorded in OT authorization column', statutory_ref: 'Code on Wages 2019 — Section 14', is_verified: false, finding: null, severity: 'NONE' },
  { item_id: 'ATT-01', category: 'Attendance Records', description: 'Verify Form D Attendance Muster Roll headcount matches wage register headcount', statutory_ref: 'Code on Wages 2019 — Section 50, Form D', is_verified: false, finding: null, severity: 'NONE' },
  { item_id: 'ATT-02', category: 'Attendance Records', description: 'Cross-check biometric turnstile logs or gate register against muster roll entries', statutory_ref: 'Code on Wages 2019 — Section 50', is_verified: false, finding: null, severity: 'NONE' },
  { item_id: 'PAY-01', category: 'Payment Evidence', description: 'Verify bank UTR payment scroll matches wage register disbursement amounts', statutory_ref: 'Code on Wages 2019 — Section 6(3)', is_verified: false, finding: null, severity: 'NONE' },
  { item_id: 'SAF-01', category: 'Safety Compliance', description: 'Verify Safety Committee is constituted and composition order is displayed on factory board', statutory_ref: 'OSHWC Code 2020 — Section 23', is_verified: false, finding: null, severity: 'NONE' },
  { item_id: 'SAF-02', category: 'Safety Compliance', description: 'Inspect machinery inspection logbook (pressing shop / hazardous areas) signed by Safety Officer', statutory_ref: 'OSHWC Code 2020 — Section 28', is_verified: false, finding: null, severity: 'NONE' },
  { item_id: 'SOC-01', category: 'Social Security', description: 'Verify ESIC registration and contribution challan for current quarter', statutory_ref: 'Social Security Code 2020 — Section 28', is_verified: false, finding: null, severity: 'NONE' },
  { item_id: 'SOC-02', category: 'Social Security', description: 'Verify EPF/EPS contribution statement is filed and deposited within prescribed date', statutory_ref: 'Social Security Code 2020 — Section 16', is_verified: false, finding: null, severity: 'NONE' },
  { item_id: 'EMP-01', category: 'Employee Records', description: 'Verify Form A Employee Register with all mandatory fields (Name, DOJ, Designation, Aadhaar reference)', statutory_ref: 'Code on Wages 2019 — Section 50, Form A', is_verified: false, finding: null, severity: 'NONE' },
];

const SEVERITY_OPTIONS = ['NONE', 'LOW', 'MEDIUM', 'HIGH', 'CRITICAL'] as const;
type Severity = typeof SEVERITY_OPTIONS[number];

const severityStyle: Record<Severity, string> = {
  NONE: 'bg-slate-800 text-slate-400 border-slate-700',
  LOW: 'bg-blue-500/15 text-blue-300 border-blue-500/30',
  MEDIUM: 'bg-amber-500/15 text-amber-300 border-amber-500/30',
  HIGH: 'bg-orange-500/15 text-orange-300 border-orange-500/30',
  CRITICAL: 'bg-rose-500/15 text-rose-300 border-rose-500/30',
};

const CATEGORY_ICON: Record<string, React.ReactNode> = {
  'Wage Registers': <ClipboardList className="w-3.5 h-3.5 text-blue-400" />,
  'Attendance Records': <FileCheck2 className="w-3.5 h-3.5 text-cyan-400" />,
  'Payment Evidence': <BadgeCheck className="w-3.5 h-3.5 text-emerald-400" />,
  'Safety Compliance': <Shield className="w-3.5 h-3.5 text-amber-400" />,
  'Social Security': <AlertTriangle className="w-3.5 h-3.5 text-purple-400" />,
  'Employee Records': <ClipboardList className="w-3.5 h-3.5 text-slate-400" />,
};

interface InspectionWorkflowProps {
  establishmentId: string;
  establishmentName: string;
  onBack: () => void;
  onNavigate?: (role: ActiveRole) => void;
}

export const InspectionWorkflow: React.FC<InspectionWorkflowProps> = ({
  establishmentId,
  establishmentName,
  onBack,
}) => {
  const [session, setSession] = useState<any | null>(null);
  const [checklist, setChecklist] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [report, setReport] = useState<any | null>(null);
  const [expandedItems, setExpandedItems] = useState<Set<string>>(new Set());
  const [fieldNotes, setFieldNotes] = useState('');
  const [seizedDocs, setSeizedDocs] = useState<string[]>([]);
  const [newDoc, setNewDoc] = useState('');
  const [activeCategory, setActiveCategory] = useState<string>('ALL');

  useEffect(() => {
    apiStartSession(establishmentId, establishmentName).then(s => {
      setSession(s);
      setChecklist(s.checklist.map((i: any) => ({ ...i })));
      setIsLoading(false);
    });
  }, [establishmentId, establishmentName]);

  const categories = ['ALL', ...Array.from(new Set(checklist.map(i => i.category)))];
  const filteredChecklist = activeCategory === 'ALL' ? checklist : checklist.filter(i => i.category === activeCategory);

  const verifiedCount = checklist.filter(i => i.is_verified).length;
  const violationCount = checklist.filter(i => ['MEDIUM', 'HIGH', 'CRITICAL'].includes(i.severity)).length;
  const progress = checklist.length > 0 ? Math.round((verifiedCount / checklist.length) * 100) : 0;

  const updateItem = (itemId: string, patch: Partial<any>) => {
    setChecklist(prev => prev.map(i => i.item_id === itemId ? { ...i, ...patch } : i));
  };

  const toggleExpand = (itemId: string) => {
    setExpandedItems(prev => {
      const next = new Set(prev);
      next.has(itemId) ? next.delete(itemId) : next.add(itemId);
      return next;
    });
  };

  const handleSubmit = async () => {
    setIsSubmitting(true);
    try {
      const result = await apiSubmitSession({
        session_id: session.session_id,
        establishment_id: establishmentId,
        inspector_id: 'INS-OFFICER-42',
        checklist,
        documents_seized: seizedDocs,
        field_notes: fieldNotes,
      });
      setReport(result);
    } finally {
      setIsSubmitting(false);
    }
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-64">
        <div className="text-center space-y-3">
          <Loader2 className="w-8 h-8 animate-spin text-blue-400 mx-auto" />
          <p className="text-xs text-slate-400">Initializing inspection session…</p>
        </div>
      </div>
    );
  }

  // ── REPORT VIEW ──────────────────────────────────────────────────
  if (report) {
    const PENALTY_COLOR: Record<string, string> = {
      CRITICAL: 'text-rose-300',
      HIGH: 'text-orange-300',
      MEDIUM: 'text-amber-300',
    };
    return (
      <div className="space-y-6">
        {/* Report Banner */}
        <div className="glass-panel p-6 rounded-2xl border border-emerald-500/30 bg-emerald-950/10 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2">
              <CheckCircle2 className="w-5 h-5 text-emerald-400" />
              <h1 className="text-lg font-extrabold text-white">Inspection Report Submitted</h1>
            </div>
            <p className="text-xs text-slate-400 mt-1">
              Session: <span className="font-mono text-slate-200">{report.session_id}</span> • Ref: <span className="font-mono text-emerald-300">{report.report_ref}</span>
            </p>
          </div>
          <button
            onClick={onBack}
            className="flex items-center gap-2 px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs border border-slate-700 transition cursor-pointer"
          >
            <ArrowLeft className="w-3.5 h-3.5" />
            Back to Queue
          </button>
        </div>

        {/* Summary Metrics */}
        <div className="grid grid-cols-2 sm:grid-cols-3 gap-4">
          {[
            { label: 'Violations Found', value: report.violations_found, color: report.violations_found > 0 ? 'text-rose-400' : 'text-emerald-400' },
            { label: 'Total Penalty Proposed', value: `₹${(report.total_penalty_proposed_inr / 1000).toFixed(0)}K`, color: 'text-amber-400' },
            { label: 'Documents Seized', value: seizedDocs.length, color: 'text-blue-400' },
          ].map((m, idx) => (
            <div key={idx} className="glass-panel p-4 rounded-2xl border border-slate-800 text-center space-y-1">
              <p className={`text-2xl font-extrabold font-mono ${m.color}`}>{m.value}</p>
              <p className="text-[11px] text-slate-400">{m.label}</p>
            </div>
          ))}
        </div>

        {/* Violation Docket */}
        {report.violation_docket.length > 0 && (
          <div className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-4">
            <h2 className="text-sm font-bold text-rose-300 flex items-center gap-2">
              <AlertOctagon className="w-4 h-4" />
              Violation Docket — {report.violation_docket.length} Violations
            </h2>
            <div className="space-y-3">
              {report.violation_docket.map((v: any) => (
                <div key={v.violation_id} className="p-4 rounded-xl bg-rose-950/10 border border-rose-500/20 space-y-2">
                  <div className="flex items-center justify-between gap-2">
                    <span className="font-mono text-[10px] text-rose-300">{v.violation_id} — {v.code_section}</span>
                    <div className="flex items-center gap-2 shrink-0">
                      <span className={`text-[10px] font-mono font-bold px-2 py-0.5 rounded border ${severityStyle[v.severity as Severity]}`}>
                        {v.severity}
                      </span>
                      <span className={`text-xs font-mono font-bold ${PENALTY_COLOR[v.severity] || 'text-slate-300'}`}>
                        ₹{(v.suggested_penalty_inr / 1000).toFixed(0)}K
                      </span>
                    </div>
                  </div>
                  <p className="text-xs text-slate-300">{v.description}</p>
                  {v.evidence_collected?.length > 0 && (
                    <p className="text-[11px] text-slate-500">Evidence: {v.evidence_collected.join(', ')}</p>
                  )}
                </div>
              ))}
            </div>
            <div className="pt-3 border-t border-slate-800 flex items-center justify-between">
              <span className="text-xs text-slate-400">Total Penalty Proposed:</span>
              <span className="text-base font-extrabold text-rose-400 font-mono">
                ₹{report.total_penalty_proposed_inr.toLocaleString('en-IN')}
              </span>
            </div>
          </div>
        )}

        {/* Field Notes */}
        {fieldNotes && (
          <div className="glass-panel p-5 rounded-2xl border border-slate-800 space-y-2">
            <h2 className="text-xs font-bold text-slate-300 flex items-center gap-2"><StickyNote className="w-3.5 h-3.5 text-amber-400" /> Inspector Field Notes</h2>
            <p className="text-xs text-slate-400 leading-relaxed">{fieldNotes}</p>
          </div>
        )}
      </div>
    );
  }

  // ── ACTIVE SESSION VIEW ──────────────────────────────────────────
  return (
    <div className="space-y-6">

      {/* Session Header */}
      <div className="glass-panel p-5 rounded-2xl border border-slate-800 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div className="flex items-center gap-3">
          <button
            onClick={onBack}
            className="p-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 transition cursor-pointer"
          >
            <ArrowLeft className="w-4 h-4" />
          </button>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-base font-extrabold text-white">Field Inspection Workflow</h1>
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-blue-500/20 text-blue-300 border border-blue-500/30 font-bold">
                {session?.session_id}
              </span>
            </div>
            <p className="text-xs text-slate-400 mt-0.5">
              {establishmentName} • Inspector: <span className="font-mono text-slate-300">INS-OFFICER-42</span> • Started: {session?.started_at}
            </p>
          </div>
        </div>

        {/* Progress Badge */}
        <div className="flex items-center gap-3 shrink-0">
          <div className="text-center">
            <p className="text-xs font-mono font-bold text-white">{verifiedCount}/{checklist.length}</p>
            <p className="text-[10px] text-slate-500">Items Checked</p>
          </div>
          <div className="text-center">
            <p className="text-xs font-mono font-bold text-rose-400">{violationCount}</p>
            <p className="text-[10px] text-slate-500">Violations</p>
          </div>
        </div>
      </div>

      {/* Progress Bar */}
      <div className="space-y-1.5">
        <div className="flex items-center justify-between text-[11px] text-slate-400">
          <span>Inspection Progress</span>
          <span className="font-mono font-bold text-white">{progress}%</span>
        </div>
        <div className="h-2 bg-slate-900 rounded-full border border-slate-800 overflow-hidden">
          <div
            className="h-full rounded-full bg-gradient-to-r from-blue-600 to-indigo-500 transition-all duration-500"
            style={{ width: `${progress}%` }}
          />
        </div>
      </div>

      {/* Category Filter Pills */}
      <div className="flex flex-wrap gap-2">
        {categories.map(cat => (
          <button
            key={cat}
            onClick={() => setActiveCategory(cat)}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-semibold border transition cursor-pointer ${
              activeCategory === cat
                ? 'bg-blue-600 text-white border-blue-500 shadow-md'
                : 'bg-slate-900 text-slate-400 border-slate-800 hover:text-slate-200'
            }`}
          >
            {cat !== 'ALL' && CATEGORY_ICON[cat]}
            {cat}
          </button>
        ))}
      </div>

      {/* Checklist Items */}
      <div className="space-y-3">
        {filteredChecklist.map(item => {
          const isExpanded = expandedItems.has(item.item_id);
          const isVerified = item.is_verified;
          const severity = item.severity as Severity;

          return (
            <div
              key={item.item_id}
              className={`glass-panel rounded-2xl border transition ${
                severity === 'CRITICAL' ? 'border-rose-500/40' :
                severity === 'HIGH' ? 'border-orange-500/30' :
                severity === 'MEDIUM' ? 'border-amber-500/20' :
                isVerified ? 'border-emerald-500/20' : 'border-slate-800'
              }`}
            >
              {/* Item Header Row */}
              <div
                className="p-4 flex items-start gap-3 cursor-pointer select-none"
                onClick={() => toggleExpand(item.item_id)}
              >
                {/* Verify Toggle */}
                <button
                  onClick={e => { e.stopPropagation(); updateItem(item.item_id, { is_verified: !isVerified }); }}
                  className="mt-0.5 shrink-0 cursor-pointer"
                >
                  {isVerified
                    ? <CheckCircle2 className="w-5 h-5 text-emerald-400" />
                    : <XCircle className="w-5 h-5 text-slate-600 hover:text-slate-400 transition" />
                  }
                </button>

                {/* Content */}
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 flex-wrap">
                    {CATEGORY_ICON[item.category]}
                    <span className="text-[10px] font-mono text-slate-500">{item.item_id}</span>
                    <span className={`text-[10px] font-mono px-1.5 py-0.5 rounded border font-bold ${severityStyle[severity]}`}>
                      {severity}
                    </span>
                  </div>
                  <p className={`text-xs mt-1 leading-relaxed ${isVerified ? 'text-slate-300' : 'text-slate-200'}`}>
                    {item.description}
                  </p>
                  <p className="text-[10px] font-mono text-blue-400/70 mt-0.5">{item.statutory_ref}</p>
                </div>

                {/* Expand toggle */}
                <div className="shrink-0 text-slate-500">
                  {isExpanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                </div>
              </div>

              {/* Expanded: Finding + Severity */}
              {isExpanded && (
                <div className="px-4 pb-4 space-y-3 border-t border-slate-800/60 pt-3">
                  {/* Severity selector */}
                  <div className="space-y-1">
                    <p className="text-[10px] font-mono text-slate-500 uppercase tracking-wider">Finding Severity</p>
                    <div className="flex flex-wrap gap-1.5">
                      {SEVERITY_OPTIONS.map(sev => (
                        <button
                          key={sev}
                          onClick={() => updateItem(item.item_id, { severity: sev })}
                          className={`text-[10px] font-mono px-2 py-1 rounded border font-bold transition cursor-pointer ${
                            severity === sev ? severityStyle[sev] : 'bg-slate-900 text-slate-500 border-slate-800 hover:text-slate-300'
                          }`}
                        >
                          {sev}
                        </button>
                      ))}
                    </div>
                  </div>
                  {/* Finding textarea */}
                  <div className="space-y-1">
                    <p className="text-[10px] font-mono text-slate-500 uppercase tracking-wider">Finding / Evidence Description</p>
                    <textarea
                      rows={2}
                      placeholder="Describe the specific finding, e.g. 'Form B shows ₹340 shortfall for 3 workers on Shift B…'"
                      value={item.finding || ''}
                      onChange={e => updateItem(item.item_id, { finding: e.target.value })}
                      className="w-full px-3 py-2 rounded-lg bg-slate-950 border border-slate-800 text-xs text-slate-200 placeholder-slate-600 focus:outline-none focus:border-blue-500 resize-none"
                    />
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Documents Seized */}
      <div className="glass-panel p-5 rounded-2xl border border-slate-800 space-y-3">
        <h2 className="text-xs font-bold text-amber-300 flex items-center gap-2 uppercase tracking-wider font-mono">
          <FileCheck2 className="w-3.5 h-3.5" /> Documents Seized On-Site
        </h2>
        <div className="flex gap-2">
          <input
            type="text"
            placeholder="e.g. Form B Register Oct 2024"
            value={newDoc}
            onChange={e => setNewDoc(e.target.value)}
            onKeyDown={e => {
              if (e.key === 'Enter' && newDoc.trim()) {
                setSeizedDocs(prev => [...prev, newDoc.trim()]);
                setNewDoc('');
              }
            }}
            className="flex-1 px-3 py-1.5 rounded-lg bg-slate-950 border border-slate-800 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-amber-500"
          />
          <button
            onClick={() => { if (newDoc.trim()) { setSeizedDocs(prev => [...prev, newDoc.trim()]); setNewDoc(''); } }}
            className="px-3 py-1.5 rounded-lg bg-amber-600 hover:bg-amber-500 text-white text-xs font-semibold flex items-center gap-1 cursor-pointer"
          >
            <Plus className="w-3.5 h-3.5" />
          </button>
        </div>
        {seizedDocs.length > 0 ? (
          <div className="space-y-1.5">
            {seizedDocs.map((doc, idx) => (
              <div key={idx} className="flex items-center justify-between p-2.5 rounded-lg bg-slate-950 border border-amber-500/15 text-xs text-slate-300">
                <span className="flex items-center gap-2">
                  <FileCheck2 className="w-3.5 h-3.5 text-amber-400 shrink-0" />
                  {doc}
                </span>
                <button onClick={() => setSeizedDocs(prev => prev.filter((_, i) => i !== idx))} className="text-slate-600 hover:text-rose-400 cursor-pointer">
                  <Trash2 className="w-3.5 h-3.5" />
                </button>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-[11px] text-slate-600 italic">No documents added yet. Type above and press Enter or +.</p>
        )}
      </div>

      {/* Field Notes */}
      <div className="glass-panel p-5 rounded-2xl border border-slate-800 space-y-3">
        <h2 className="text-xs font-bold text-slate-300 flex items-center gap-2 uppercase tracking-wider font-mono">
          <StickyNote className="w-3.5 h-3.5 text-amber-400" /> Inspector Field Notes
        </h2>
        <textarea
          rows={4}
          placeholder="Record any additional on-site observations, worker statements, management responses, or contextual notes…"
          value={fieldNotes}
          onChange={e => setFieldNotes(e.target.value)}
          className="w-full px-3 py-2.5 rounded-lg bg-slate-950 border border-slate-800 text-xs text-slate-200 placeholder-slate-600 focus:outline-none focus:border-blue-500 resize-none leading-relaxed"
        />
      </div>

      {/* Submit Button */}
      <div className="flex items-center justify-between py-2">
        <p className="text-xs text-slate-400">
          <span className="text-white font-semibold">{verifiedCount}</span> of {checklist.length} items verified •{' '}
          <span className={violationCount > 0 ? 'text-rose-400 font-semibold' : 'text-emerald-400 font-semibold'}>
            {violationCount} violation{violationCount !== 1 ? 's' : ''} found
          </span>
        </p>
        <button
          onClick={handleSubmit}
          disabled={isSubmitting || verifiedCount === 0}
          className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white text-xs font-bold shadow-lg shadow-blue-500/20 transition cursor-pointer disabled:opacity-50"
        >
          {isSubmitting
            ? <><Loader2 className="w-3.5 h-3.5 animate-spin" /> Submitting…</>
            : <><Send className="w-3.5 h-3.5" /> Submit Inspection Report</>
          }
        </button>
      </div>

    </div>
  );
};
