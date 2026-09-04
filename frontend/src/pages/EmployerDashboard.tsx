import React, { useState, useEffect } from 'react';
import {
  Building2,
  FileCheck2,
  FileWarning,
  UploadCloud,
  ArrowRight,
  ShieldAlert,
  CheckCircle2,
  AlertOctagon,
  TrendingUp,
  Zap,
  BookOpen,
  Send,
  Loader2,
  ChevronRight,
  Scale,
  Award,
  Check,
} from 'lucide-react';
import { MetricCard } from '../components/MetricCard';
import { StatutoryNoticeViewerModal } from '../components/StatutoryNoticeViewerModal';
import { SafeHarbourCertificateModal } from '../components/SafeHarbourCertificateModal';
import { ActiveRole, EmployerComplianceProfile, StatutoryNotice, SafeHarbourCertificate } from '../types';
import { 
  getEmployerComplianceProfile, 
  getComprehensiveExplanation, 
  queryLabourRAG, 
  getEstablishmentNotices, 
  updateNoticeStatus,
  recalibrateCompliance,
  issueSafeHarbourCertificate
} from '../services/api';

interface EmployerDashboardProps {
  onNavigate: (role: ActiveRole) => void;
  onOpenAssistant: () => void;
}

// Animated circular score gauge
const ComplianceGauge: React.FC<{ score: number; delta: number }> = ({ score, delta }) => {
  const radius = 52;
  const circumference = 2 * Math.PI * radius;
  const filled = (score / 100) * circumference;
  const safeHarbourAt = (85 / 100) * circumference;

  const color = score >= 85
    ? '#10b981'   // emerald
    : score >= 60
    ? '#f59e0b'   // amber
    : '#f43f5e';  // rose

  return (
    <div className="flex flex-col items-center gap-3">
      <div className="relative w-36 h-36">
        <svg className="w-full h-full -rotate-90" viewBox="0 0 120 120">
          {/* Track */}
          <circle cx="60" cy="60" r={radius} fill="none" stroke="#1e293b" strokeWidth="10" />
          {/* Safe harbour marker at 85% */}
          <circle
            cx="60" cy="60" r={radius} fill="none"
            stroke="#22d3ee20" strokeWidth="10"
            strokeDasharray={`2 ${circumference - 2}`}
            strokeDashoffset={-safeHarbourAt}
          />
          {/* Score arc */}
          <circle
            cx="60" cy="60" r={radius} fill="none"
            stroke={color} strokeWidth="10" strokeLinecap="round"
            strokeDasharray={`${filled} ${circumference - filled}`}
            style={{ transition: 'stroke-dasharray 1s ease-in-out' }}
          />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className="text-3xl font-extrabold text-white font-mono">{score}</span>
          <span className="text-[10px] text-slate-400 font-mono">/100</span>
        </div>
      </div>
      <div className="text-center space-y-0.5">
        <p className="text-xs font-semibold" style={{ color }}>{score >= 85 ? 'Safe Harbour ✓' : 'Needs Remediation'}</p>
        {delta > 0 && (
          <p className="text-[11px] text-slate-400">
            <span className="text-cyan-400 font-bold">+{delta} pts</span> to safe harbour (85+)
          </p>
        )}
      </div>
    </div>
  );
};

export const EmployerDashboard: React.FC<EmployerDashboardProps> = ({ onNavigate, onOpenAssistant }) => {
  const [profile, setProfile] = useState<EmployerComplianceProfile | null>(null);
  const [remediation, setRemediation] = useState<any | null>(null);
  const [ragQuery, setRagQuery] = useState('');
  const [ragAnswer, setRagAnswer] = useState<string | null>(null);
  const [isRagLoading, setIsRagLoading] = useState(false);
  const [pendingNotices, setPendingNotices] = useState<StatutoryNotice[]>([]);
  const [selectedNotice, setSelectedNotice] = useState<StatutoryNotice | null>(null);
  const [isNoticeModalOpen, setIsNoticeModalOpen] = useState(false);
  const [curedActions, setCuredActions] = useState<string[]>([]);
  const [isRecalibrating, setIsRecalibrating] = useState(false);
  const [certificate, setCertificate] = useState<SafeHarbourCertificate | null>(null);
  const [isCertModalOpen, setIsCertModalOpen] = useState(false);
  const [isClaimingCert, setIsClaimingCert] = useState(false);

  useEffect(() => {
    getEmployerComplianceProfile("EST-001").then(setProfile).catch(console.error);
    getComprehensiveExplanation("EST-001").then(setRemediation).catch(console.error);
    getEstablishmentNotices("EST-001").then(setPendingNotices).catch(console.error);

    const params = new URLSearchParams(window.location.search);
    if (params.get('cert') === 'true') {
      issueSafeHarbourCertificate("EST-001").then(cert => {
        setCertificate(cert);
        setIsCertModalOpen(true);
      }).catch(console.error);
    }
  }, []);

  const handleCureAction = async (actionId: string) => {
    if (curedActions.includes(actionId)) return;
    setIsRecalibrating(true);
    const updated = [...curedActions, actionId];
    setCuredActions(updated);
    try {
      const res = await recalibrateCompliance("EST-001", updated);
      if (profile) {
        setProfile({
          ...profile,
          voluntary_compliance_score: res.recalibrated_score,
          score_delta_to_safe_harbour: res.score_delta_to_safe_harbour,
          total_penalty_exposure_inr: res.residual_penalty_exposure_inr,
        });
      }
    } catch (e) {
      console.error(e);
    } finally {
      setIsRecalibrating(false);
    }
  };

  const handleClaimCertificate = async () => {
    setIsClaimingCert(true);
    try {
      const cert = await issueSafeHarbourCertificate("EST-001");
      setCertificate(cert);
      setIsCertModalOpen(true);
    } catch (e) {
      console.error(e);
    } finally {
      setIsClaimingCert(false);
    }
  };

  const handleRagQuery = async (q: string) => {
    setIsRagLoading(true);
    setRagQuery(q);
    try {
      const res = await queryLabourRAG(q);
      setRagAnswer(res.answer || res.response || "Please refer to the AI compliance assistant for a detailed response.");
    } catch {
      setRagAnswer("Please refer to the AI compliance assistant for a detailed response.");
    } finally {
      setIsRagLoading(false);
    }
  };

  const chipQueries = [
    "What documents must I file this quarter?",
    "How can I reduce my compliance risk score?",
    "What is the safe harbour rule under Code on Wages?",
    "What are the penalties for minimum wage violations?",
  ];

  const p = profile;

  return (
    <div className="space-y-8">

      {/* Header Profile Bar */}
      <div className="glass-panel p-6 rounded-2xl border border-slate-800 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="flex items-center gap-4">
          <div className="w-14 h-14 rounded-xl bg-gradient-to-br from-amber-500 to-amber-700 flex items-center justify-center shadow-lg shadow-amber-500/10">
            <Building2 className="w-7 h-7 text-white" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-xl sm:text-2xl font-bold text-white">{p?.establishment_name || "ABC Industries Ltd."}</h1>
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700">
                LIN: {p?.lin || "1928374650"}
              </span>
            </div>
            <p className="text-xs text-slate-400 mt-1">
              Registration: <span className="font-mono text-slate-300">{p?.registration_number || "MH-PUN-EST-001"}</span> • {p?.jurisdiction || "Central Sphere"}
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={handleClaimCertificate}
            className="flex items-center gap-1.5 px-3 py-2.5 rounded-xl bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white font-semibold text-xs transition shadow-md shadow-emerald-500/20 cursor-pointer"
          >
            <Award className="w-4 h-4" />
            <span>Safe Harbour Certificate</span>
          </button>
          <button
            onClick={() => onNavigate('upload')}
            className="flex items-center gap-2 px-4 py-2.5 rounded-xl bg-amber-500 hover:bg-amber-400 text-slate-950 font-semibold text-xs transition shadow-md shadow-amber-500/20 cursor-pointer"
          >
            <UploadCloud className="w-4 h-4" />
            <span>Submit Registers</span>
          </button>
          <button
            onClick={onOpenAssistant}
            className="flex items-center gap-1.5 px-3 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs border border-slate-700 transition cursor-pointer"
          >
            <span>Ask Compliance AI</span>
          </button>
        </div>
      </div>

      {/* Safe Harbour Eligible / Active Banner */}
      {(p?.voluntary_compliance_score ?? 48) >= 85 && (
        <div className="p-4 rounded-2xl bg-gradient-to-r from-emerald-950/70 via-slate-900 to-cyan-950/60 border border-emerald-500/40 flex flex-col sm:flex-row sm:items-center justify-between gap-3 shadow-xl animate-fadeIn">
          <div className="flex items-center gap-3">
            <div className="p-2.5 rounded-xl bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 shrink-0">
              <Award className="w-6 h-6" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h3 className="text-sm font-bold text-white">
                  Safe Harbour Voluntary Compliance Status Achieved! ({p?.voluntary_compliance_score}/100)
                </h3>
                <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-bold border border-emerald-500/30">
                  180-DAY IMMUNITY
                </span>
              </div>
              <p className="text-xs text-slate-300">
                Statutory self-audit requirements fulfilled. Establishment is protected from automated inspection selection under Code on Wages §56 and Social Security Code §138.
              </p>
            </div>
          </div>
          <button
            onClick={handleClaimCertificate}
            disabled={isClaimingCert}
            className="px-4 py-2 rounded-xl bg-gradient-to-r from-emerald-500 to-teal-500 hover:from-emerald-400 hover:to-teal-400 text-slate-950 font-bold text-xs transition shrink-0 cursor-pointer shadow-md shadow-emerald-500/20 flex items-center gap-1.5"
          >
            <Award className="w-4 h-4" />
            <span>{isClaimingCert ? 'Issuing Certificate...' : 'View Official Safe Harbour Certificate (Form SH-01)'}</span>
          </button>
        </div>
      )}

      {/* Statutory Show Cause Notice Action Alert Banner */}
      {pendingNotices.length > 0 && (
        <div className="p-4 rounded-2xl bg-gradient-to-r from-amber-950/60 via-slate-900 to-rose-950/50 border border-amber-500/40 flex flex-col sm:flex-row sm:items-center justify-between gap-3 shadow-xl">
          <div className="flex items-center gap-3">
            <div className="p-2.5 rounded-xl bg-amber-500/20 text-amber-400 border border-amber-500/30 shrink-0">
              <Scale className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h3 className="text-sm font-bold text-white">
                  Formal Statutory Notice Received ({pendingNotices[0].notice_number})
                </h3>
                <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-rose-500/20 text-rose-300 font-bold border border-rose-500/30">
                  {pendingNotices[0].status}
                </span>
              </div>
              <p className="text-xs text-slate-300">
                Action required on or before <strong className="text-amber-400 font-mono">{pendingNotices[0].response_deadline}</strong>. Cure violations or apply for Sec 56 compounding.
              </p>
            </div>
          </div>
          <button
            onClick={() => {
              setSelectedNotice(pendingNotices[0]);
              setIsNoticeModalOpen(true);
            }}
            className="px-4 py-2 rounded-xl bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold text-xs transition shrink-0 cursor-pointer shadow-md shadow-amber-500/20"
          >
            View Notice & Respond
          </button>
        </div>
      )}

      {/* Metrics Row */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <MetricCard
          label="ML Risk Score (XGBoost)"
          value={`${p?.ml_risk_score ?? 84.5} / 100`}
          subtext={`${p?.priority_class ?? 'HIGH'} Priority — Top 8% Risk`}
          icon={ShieldAlert}
          variant="danger"
        />
        <MetricCard
          label="Voluntary Compliance Score"
          value={`${p?.voluntary_compliance_score ?? 48} / 100`}
          subtext={`+${p?.score_delta_to_safe_harbour ?? 37} pts to safe harbour`}
          icon={TrendingUp}
          variant="warning"
        />
        <MetricCard
          label="Missing Statutory Filings"
          value={p?.missing_filings_count ?? 3}
          subtext="1 Overdue • 2 Approaching deadline"
          icon={FileWarning}
          variant="danger"
        />
        <MetricCard
          label="Statutory Penalty Exposure"
          value={`₹${((p?.total_penalty_exposure_inr ?? 320000) / 100000).toFixed(1)}L`}
          subtext="Maximum potential exposure"
          icon={AlertOctagon}
          variant="danger"
        />
      </div>

      {/* Main 3-column grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">

        {/* Left 2 Cols */}
        <div className="lg:col-span-2 space-y-6">

          {/* Compliance Score Gauge + Penalty Exposure Side-by-Side */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">

            {/* Score Gauge */}
            <div className="glass-panel p-6 rounded-2xl border border-slate-800 flex flex-col items-center gap-4">
              <div className="w-full flex items-center justify-between">
                <h2 className="text-sm font-bold text-white">Compliance Score Gauge</h2>
                <span className="text-[10px] font-mono text-cyan-400 bg-cyan-500/10 px-2 py-0.5 rounded border border-cyan-500/20">
                  Safe Harbour @ 85+
                </span>
              </div>
              <ComplianceGauge
                score={p?.voluntary_compliance_score ?? 48}
                delta={p?.score_delta_to_safe_harbour ?? 37}
              />
              <p className="text-[11px] text-slate-400 text-center leading-relaxed">
                Establishments scoring <strong className="text-white">85+</strong> are deprioritized by the ML risk classifier and reduce inspection probability.
              </p>
            </div>

            {/* Penalty Exposure Calculator */}
            <div className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-4">
              <div className="flex items-center justify-between">
                <h2 className="text-sm font-bold text-white flex items-center gap-2">
                  <AlertOctagon className="w-4 h-4 text-rose-400" />
                  Penalty Exposure Calculator
                </h2>
                <span className="text-[10px] font-mono text-rose-300 bg-rose-500/10 px-2 py-0.5 rounded border border-rose-500/20">
                  Max Risk
                </span>
              </div>
              <div className="space-y-2">
                {(p?.penalty_exposures ?? []).filter(pe => pe.applicable).map((pe, idx) => (
                  <div key={idx} className="flex items-start justify-between p-2.5 rounded-lg bg-slate-950 border border-rose-500/10 text-xs gap-2">
                    <div className="flex-1 min-w-0">
                      <p className="font-mono text-[10px] text-rose-300">{pe.section}</p>
                      <p className="text-slate-400 text-[11px] truncate">{pe.violation_description}</p>
                    </div>
                    <span className="text-rose-400 font-mono font-bold shrink-0">₹{(pe.maximum_fine_inr / 1000).toFixed(0)}K</span>
                  </div>
                ))}
              </div>
              <div className="pt-2 border-t border-slate-800 flex items-center justify-between">
                <span className="text-xs text-slate-400">Total Maximum Exposure:</span>
                <span className="text-sm font-extrabold text-rose-400 font-mono">
                  ₹{((p?.total_penalty_exposure_inr ?? 320000) / 100000).toFixed(1)}L
                </span>
              </div>
            </div>
          </div>

          {/* AI Remediation Advisory Panel */}
          {remediation?.employer_remediation && (
            <div className="glass-panel p-6 rounded-2xl border border-emerald-500/20 bg-emerald-950/5 space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <h2 className="text-sm font-bold text-emerald-300 flex items-center gap-2">
                    <Zap className="w-4 h-4" />
                    AI Remediation Advisory
                  </h2>
                  <p className="text-xs text-slate-400 mt-0.5">
                    Generated by Phase 21 Generative Explanation Engine — grounded in verified statutory citations
                  </p>
                </div>
                <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-300 border border-emerald-500/30 font-bold">
                  ₹{(remediation.employer_remediation.total_estimated_arrears_inr / 1000).toFixed(1)}K Arrears
                </span>
              </div>

              <p className="text-xs text-slate-300 leading-relaxed">
                {remediation.employer_remediation.advisory_summary}
              </p>

              <div className="space-y-2">
                {remediation.employer_remediation.remediation_steps.map((step: any) => (
                  <div key={step.step_number} className="flex items-start gap-3 p-3 rounded-xl bg-slate-900/60 border border-emerald-500/10">
                    <span className="w-6 h-6 rounded-full bg-emerald-500/20 text-emerald-300 text-[11px] font-bold flex items-center justify-center shrink-0 font-mono">
                      {step.step_number}
                    </span>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center justify-between gap-2">
                        <p className="text-xs font-semibold text-emerald-200">{step.action}</p>
                        <span className="text-[10px] font-mono text-amber-300 bg-amber-500/10 px-1.5 py-0.5 rounded shrink-0">{step.deadline}</span>
                      </div>
                      <p className="text-[11px] text-slate-400 mt-0.5">{step.statutory_cure}</p>
                      {step.estimated_financial_arrears && step.estimated_financial_arrears !== "₹0" && (
                        <p className="text-[11px] font-mono font-bold text-emerald-400">{step.estimated_financial_arrears}</p>
                      )}
                    </div>
                  </div>
                ))}
              </div>

              <div className="p-3 rounded-xl bg-blue-950/30 border border-blue-500/20 text-xs text-blue-200">
                <span className="font-bold text-blue-300">⚖️ Safe Harbour: </span>
                {remediation.employer_remediation.safe_harbour_guidelines}
              </div>
            </div>
          )}

          {/* Corrective Actions */}
          <div className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-sm font-bold text-white flex items-center gap-2">
                  <ShieldAlert className="w-4 h-4 text-amber-400" />
                  Immediate Corrective Actions
                </h2>
                <p className="text-xs text-slate-400 mt-0.5">
                  Resolve before statutory inspector queue selection
                </p>
              </div>
              <span className="text-xs font-mono text-amber-400 bg-amber-500/10 px-2 py-0.5 rounded border border-amber-500/20">
                {(p?.corrective_actions ?? []).length} Pending
              </span>
            </div>

            <div className="space-y-3">
              {(p?.corrective_actions ?? []).map((item, idx) => {
                const actionId = `ACT-00${idx + 1}`;
                const isCured = curedActions.includes(actionId);
                return (
                  <div 
                    key={idx} 
                    className={`p-4 rounded-xl border transition space-y-2 ${
                      isCured 
                        ? 'bg-emerald-950/20 border-emerald-500/40' 
                        : 'bg-slate-900/70 border-slate-800'
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <span className={`text-xs font-semibold flex items-center gap-1.5 ${isCured ? 'text-emerald-300' : 'text-rose-300'}`}>
                        {isCured ? (
                          <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
                        ) : (
                          <span className="w-1.5 h-1.5 rounded-full bg-rose-400 shrink-0" />
                        )}
                        {item.issue}
                      </span>
                      <div className="flex items-center gap-2">
                        {isCured && (
                          <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
                            CURED ✓
                          </span>
                        )}
                        <span className={`text-[10px] font-mono font-bold px-2 py-0.5 rounded border shrink-0 ${
                          item.priority === 'CRITICAL' 
                            ? 'bg-rose-500/20 text-rose-300 border-rose-500/30' 
                            : item.priority === 'HIGH' 
                            ? 'bg-amber-500/20 text-amber-300 border-amber-500/30' 
                            : 'bg-slate-800 text-slate-400 border-slate-700'
                        }`}>
                          {item.priority}
                        </span>
                      </div>
                    </div>
                    <p className="text-xs text-slate-400 leading-relaxed">
                      <strong className="text-slate-300">Action:</strong> {item.recommended_action}
                    </p>
                    <div className="flex flex-col sm:flex-row sm:items-center justify-between pt-2 border-t border-slate-800/60 text-[11px] gap-2">
                      <span className="text-amber-400 font-mono">{item.statutory_ref}</span>
                      <div className="flex items-center gap-3">
                        {item.estimated_arrears_inr > 0 && (
                          <span className="text-emerald-400 font-mono font-bold">₹{item.estimated_arrears_inr.toLocaleString('en-IN')}</span>
                        )}
                        <span className="text-slate-500">{item.deadline}</span>
                        {!isCured ? (
                          <button
                            onClick={() => handleCureAction(actionId)}
                            disabled={isRecalibrating}
                            className="px-3 py-1 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs flex items-center gap-1 transition cursor-pointer shadow-sm shadow-emerald-600/30 disabled:opacity-50"
                          >
                            <Check className="w-3.5 h-3.5" />
                            <span>{isRecalibrating ? 'Recalibrating...' : 'Cure & Recalibrate'}</span>
                          </button>
                        ) : (
                          <span className="text-emerald-400 font-semibold text-xs flex items-center gap-1">
                            <span>Remediated</span>
                          </span>
                        )}
                        <button
                          onClick={() => onNavigate('upload')}
                          className="text-blue-400 hover:text-blue-300 font-medium flex items-center gap-1 cursor-pointer"
                        >
                          <span>Proof</span>
                          <ArrowRight className="w-3 h-3" />
                        </button>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Register Submissions */}
          <div className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-sm font-bold text-white flex items-center gap-2">
                  <FileCheck2 className="w-4 h-4 text-emerald-400" />
                  Statutory Register Submissions
                </h2>
                <p className="text-xs text-slate-400 mt-0.5">
                  Audit results from Document AI and deterministic rule engine
                </p>
              </div>
              <button
                onClick={() => onNavigate('upload')}
                className="text-xs text-blue-400 hover:text-blue-300 font-medium cursor-pointer"
              >
                + New Upload
              </button>
            </div>

            <div className="space-y-2.5">
              {(p?.register_statuses ?? []).map((reg, idx) => {
                const hasIssues = reg.issues_count > 0;
                const badgeClass = hasIssues
                  ? "text-rose-400 bg-rose-500/10 border-rose-500/20"
                  : reg.audit_badge === "Compliant" || reg.audit_badge === "Reconciled"
                  ? "text-emerald-400 bg-emerald-500/10 border-emerald-500/20"
                  : "text-blue-400 bg-blue-500/10 border-blue-500/20";
                return (
                  <div key={idx} className="flex items-center justify-between p-3 rounded-xl bg-slate-900/60 border border-slate-800 text-xs">
                    <div className="space-y-0.5">
                      <p className="font-semibold text-slate-200">{reg.name}</p>
                      <p className="text-[11px] text-slate-500 font-mono">Last processed: {reg.last_processed}</p>
                    </div>
                    <div className="flex items-center gap-3">
                      <span className={`text-[11px] px-2 py-0.5 rounded border font-mono ${badgeClass}`}>
                        {reg.audit_badge}
                      </span>
                      <span className="text-slate-400 text-[11px] hidden sm:inline">{reg.status}</span>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

        </div>

        {/* Right 1 Col: RAG Counsellor + Missing Docs + Safe Harbour Banner */}
        <div className="space-y-6">

          {/* AI Compliance Counsellor */}
          <div className="glass-panel p-5 rounded-2xl border border-indigo-500/30 bg-indigo-950/10 space-y-4">
            <div className="flex items-center gap-2">
              <BookOpen className="w-4 h-4 text-indigo-400" />
              <h2 className="text-sm font-bold text-indigo-200">AI Compliance Counsellor</h2>
            </div>
            <p className="text-[11px] text-slate-400">
              Ask any labour law compliance question — powered by the ShramAI RAG Engine.
            </p>

            {/* Quick chip queries */}
            <div className="flex flex-col gap-2">
              {chipQueries.map((q, idx) => (
                <button
                  key={idx}
                  onClick={() => handleRagQuery(q)}
                  className="text-left text-[11px] text-indigo-300 hover:text-white px-3 py-2 rounded-lg bg-indigo-950/40 border border-indigo-500/20 hover:bg-indigo-500/20 transition flex items-center gap-2 cursor-pointer"
                >
                  <ChevronRight className="w-3 h-3 shrink-0" />
                  {q}
                </button>
              ))}
            </div>

            {/* Custom query input */}
            <div className="flex gap-2">
              <input
                type="text"
                placeholder="Ask a custom question..."
                value={ragQuery}
                onChange={e => setRagQuery(e.target.value)}
                onKeyDown={e => e.key === 'Enter' && ragQuery.trim() && handleRagQuery(ragQuery)}
                className="flex-1 px-3 py-1.5 rounded-lg bg-slate-950 border border-slate-800 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-indigo-500"
              />
              <button
                onClick={() => ragQuery.trim() && handleRagQuery(ragQuery)}
                disabled={isRagLoading}
                className="px-3 py-1.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold flex items-center gap-1 transition cursor-pointer disabled:opacity-50"
              >
                {isRagLoading ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <Send className="w-3.5 h-3.5" />}
              </button>
            </div>

            {/* RAG Answer */}
            {ragAnswer && (
              <div className="p-3 rounded-xl bg-slate-900 border border-indigo-500/20 text-xs text-slate-300 leading-relaxed space-y-1">
                <p className="text-[10px] font-mono text-indigo-400 font-bold uppercase">RAG Response</p>
                <p>{ragAnswer}</p>
              </div>
            )}
          </div>

          {/* Missing Documents */}
          <div className="glass-panel p-5 rounded-2xl border border-slate-800 space-y-4">
            <div className="flex items-center justify-between">
              <h2 className="text-sm font-bold text-white flex items-center gap-2">
                <FileWarning className="w-4 h-4 text-rose-400" />
                Missing Statutory Documents
              </h2>
              <span className="text-xs font-mono text-rose-400 bg-rose-500/10 px-2 py-0.5 rounded border border-rose-500/20">
                Action Required
              </span>
            </div>

            <div className="space-y-2.5">
              {[
                { title: "Quarterly Safety Committee Audit Minutes", code: "OSHWC Code 2020", deadline: "Overdue by 14 days", severity: "HIGH" },
                { title: "Maternity Benefit Register (Form G)", code: "Social Security Code 2020", deadline: "Due in 6 days", severity: "MEDIUM" },
                { title: "Overtime Hours Authorization Register", code: "Code on Wages 2019", deadline: "Due in 12 days", severity: "MEDIUM" },
              ].map((m, idx) => (
                <div key={idx} className="p-3 rounded-xl bg-slate-900/60 border border-slate-800 space-y-1.5">
                  <div className="flex items-center justify-between">
                    <p className="font-semibold text-xs text-slate-200">{m.title}</p>
                    <span className="text-[10px] font-mono text-rose-400 bg-rose-500/15 px-1.5 py-0.5 rounded shrink-0 ml-2">
                      {m.severity}
                    </span>
                  </div>
                  <p className="text-[11px] text-amber-400 font-mono">{m.code}</p>
                  <p className="text-[11px] text-slate-400">{m.deadline}</p>
                </div>
              ))}
            </div>

            <button
              onClick={() => onNavigate('upload')}
              className="w-full py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 text-xs font-semibold transition cursor-pointer"
            >
              Resolve Missing Filings
            </button>
          </div>

          {/* Safe Harbour Banner */}
          <div className="p-5 rounded-2xl bg-gradient-to-br from-indigo-950/40 via-slate-900 to-blue-950/40 border border-indigo-500/30 space-y-3">
            <div className="flex items-center gap-2 text-indigo-300 font-semibold text-xs">
              <CheckCircle2 className="w-4 h-4 text-indigo-400" />
              <span>Proactive Compliance Benefit</span>
            </div>
            <p className="text-xs text-slate-300 leading-relaxed">
              Establishments that maintain a score above <strong className="text-white">85/100</strong> are automatically deprioritized by the ML risk classifier for routine inspections.
            </p>
            <div className="pt-2 border-t border-indigo-500/20 flex items-center justify-between text-[11px] text-indigo-300">
              <span>Current: <strong className="font-mono text-white">{p?.voluntary_compliance_score ?? 48}</strong></span>
              <span>Target: <strong className="font-mono text-emerald-400">85+</strong></span>
            </div>
          </div>

        </div>
      </div>

      {/* Statutory Notice Viewer Modal (Employer Mode) */}
      <StatutoryNoticeViewerModal
        notice={selectedNotice}
        isOpen={isNoticeModalOpen}
        onClose={() => setIsNoticeModalOpen(false)}
        onUpdateStatus={async (noticeId, status, notes) => {
          const updated = await updateNoticeStatus(noticeId, status, notes);
          setSelectedNotice(updated);
          setPendingNotices(prev => prev.map(n => n.notice_id === noticeId ? updated : n));
        }}
        isEmployerRole={true}
      />

      {/* Safe Harbour Certificate Viewer Modal */}
      <SafeHarbourCertificateModal
        certificate={certificate}
        isOpen={isCertModalOpen}
        onClose={() => setIsCertModalOpen(false)}
      />
    </div>
  );
};
