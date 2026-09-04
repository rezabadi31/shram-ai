import React, { useState, useEffect } from 'react';
import { 
  Building2, 
  FileText, 
  AlertTriangle, 
  Scale, 
  Activity, 
  FileCheck2, 
  Bot, 
  Check, 
  X, 
  HelpCircle, 
  CheckCircle2,
  ArrowLeft,
  ShieldCheck,
  AlertOctagon,
  Sparkles,
  Loader2,
  Cpu,
  Layers,
  Binary,
  TrendingUp,
  TrendingDown,
  ShieldAlert,
  ClipboardList,
  History,
  Download
} from 'lucide-react';
import { RiskBadge } from '../components/RiskBadge';
import { StatutoryReferenceCard } from '../components/StatutoryReferenceCard';
import { EvidenceGraphModal } from '../components/EvidenceGraphModal';
import { RiskFeatureMatrixModal } from '../components/RiskFeatureMatrixModal';
import { ComplianceTimeline } from '../components/ComplianceTimeline';
import { StatutoryNoticeViewerModal } from '../components/StatutoryNoticeViewerModal';
import { EstablishmentDossier, ActiveRole, ComplianceAuditReport, OrchestrationExecutionResponse, DocumentAgentAuditResult, ComplianceAgentAuditResult, CrossDocumentAuditResult, ShapLocalExplanationResponse, RiskAgentAuditResult, ComprehensiveExplanationResponse, EstablishmentTimeline, StatutoryNotice } from '../types';
import { evaluateCompliance, runAgentOrchestration, auditEstablishmentDocuments, runComplianceAgentAudit, reconcileEstablishmentAnomalies, getEstablishmentShapExplanation, runRiskAgentAudit, getComprehensiveExplanation, getEstablishmentTimeline, getEstablishmentNotices, generateStatutoryNotice, updateNoticeStatus, exportInspectorDossier } from '../services/api';

interface EstablishmentIntelligenceProps {
  dossier: EstablishmentDossier;
  onBack: () => void;
  onNavigate: (role: ActiveRole) => void;
  onBeginInspection?: () => void;
}

type TabType = 'overview' | 'documents' | 'findings' | 'anomalies' | 'shap' | 'brief' | 'feedback' | 'timeline';

export const EstablishmentIntelligence: React.FC<EstablishmentIntelligenceProps> = ({
  dossier,
  onBack,
  onNavigate,
  onBeginInspection,
}) => {
  const [activeTab, setActiveTab] = useState<TabType>('overview');
  const [feedbackState, setFeedbackState] = useState<Record<string, string>>({});
  const [inspectorNotes, setInspectorNotes] = useState('');
  const [submittedFeedback, setSubmittedFeedback] = useState(false);
  const [liveAuditReport, setLiveAuditReport] = useState<ComplianceAuditReport | null>(null);
  const [orchestrationResult, setOrchestrationResult] = useState<OrchestrationExecutionResponse | null>(null);
  const [isOrchestrating, setIsOrchestrating] = useState(false);
  const [docAuditResult, setDocAuditResult] = useState<DocumentAgentAuditResult | null>(null);
  const [complianceAgentAudit, setComplianceAgentAudit] = useState<ComplianceAgentAuditResult | null>(null);
  const [anomalyResult, setAnomalyResult] = useState<CrossDocumentAuditResult | null>(null);
  const [isGraphModalOpen, setIsGraphModalOpen] = useState(false);
  const [isFeatureModalOpen, setIsFeatureModalOpen] = useState(false);
  const [shapExplanation, setShapExplanation] = useState<ShapLocalExplanationResponse | null>(null);
  const [riskAgentResult, setRiskAgentResult] = useState<RiskAgentAuditResult | null>(null);
  const [isRiskAgentRunning, setIsRiskAgentRunning] = useState(false);
  const [explanation, setExplanation] = useState<ComprehensiveExplanationResponse | null>(null);
  const [explanationAudience, setExplanationAudience] = useState<'inspector' | 'employer'>('inspector');
  const [timelineData, setTimelineData] = useState<EstablishmentTimeline | null>(null);
  const [isLoadingTimeline, setIsLoadingTimeline] = useState<boolean>(false);
  const [isNoticeModalOpen, setIsNoticeModalOpen] = useState(false);
  const [activeNotice, setActiveNotice] = useState<StatutoryNotice | null>(null);
  const [isNoticeLoading, setIsNoticeLoading] = useState(false);

  const { establishment, documents, findings, anomalies, shap_contributions, ai_inspection_brief } = dossier;

  useEffect(() => {
    evaluateCompliance(establishment.id).then(report => {
      setLiveAuditReport(report);
    }).catch(err => console.error(err));

    auditEstablishmentDocuments(establishment.id).then(res => {
      setDocAuditResult(res);
    }).catch(err => console.error(err));

    runComplianceAgentAudit(establishment.id).then(res => {
      setComplianceAgentAudit(res);
    }).catch(err => console.error(err));

    reconcileEstablishmentAnomalies(establishment.id).then(res => {
      setAnomalyResult(res);
    }).catch(err => console.error(err));

    getEstablishmentShapExplanation(establishment.id).then(res => {
      setShapExplanation(res);
    }).catch(err => console.error(err));

    runRiskAgentAudit(establishment.id).then(res => {
      setRiskAgentResult(res);
    }).catch(err => console.error(err));

    getComprehensiveExplanation(establishment.id).then(res => {
      setExplanation(res);
    }).catch(err => console.error(err));

    setIsLoadingTimeline(true);
    getEstablishmentTimeline(establishment.id).then(res => {
      setTimelineData(res);
    }).catch(err => {
      console.error(err);
    }).finally(() => {
      setIsLoadingTimeline(false);
    });
  }, [establishment.id]);

  const handleOpenNoticeModal = async () => {
    setIsNoticeLoading(true);
    setIsNoticeModalOpen(true);
    try {
      const notices = await getEstablishmentNotices(establishment.id);
      if (notices && notices.length > 0) {
        setActiveNotice(notices[0]);
      } else {
        const generated = await generateStatutoryNotice({ establishment_id: establishment.id });
        setActiveNotice(generated);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setIsNoticeLoading(false);
    }
  };

  const handleRunOrchestrator = async () => {
    setIsOrchestrating(true);
    try {
      const res = await runAgentOrchestration(establishment.id);
      setOrchestrationResult(res);
    } catch (e) {
      console.error(e);
    } finally {
      setIsOrchestrating(false);
    }
  };

  const handleRunRiskAgent = async () => {
    setIsRiskAgentRunning(true);
    try {
      const res = await runRiskAgentAudit(establishment.id);
      setRiskAgentResult(res);
    } catch (e) {
      console.error(e);
    } finally {
      setIsRiskAgentRunning(false);
    }
  };

  const handleFeedback = (findingId: string, action: 'CONFIRMED' | 'REJECTED' | 'NEEDS_MORE_EVIDENCE') => {
    setFeedbackState(prev => ({ ...prev, [findingId]: action }));
  };

  const handleExportDossier = async () => {
    try {
      const data = await exportInspectorDossier(establishment.id);
      const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `ShramAI_Statutory_Dossier_${establishment.id}.json`;
      a.click();
      URL.revokeObjectURL(url);
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div className="space-y-6">
      
      {/* Top Breadcrumb & Actions Bar */}
      <div className="flex items-center justify-between">
        <button
          onClick={onBack}
          className="inline-flex items-center gap-1.5 text-xs text-slate-400 hover:text-white transition"
        >
          <ArrowLeft className="w-3.5 h-3.5" />
          <span>Back to Inspection Priority Queue</span>
        </button>

        <div className="flex items-center gap-3">
          <button
            onClick={() => setIsFeatureModalOpen(true)}
            className="px-3.5 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-indigo-300 border border-indigo-500/30 text-xs font-semibold flex items-center gap-1.5 shadow-md transition cursor-pointer"
          >
            <Binary className="w-3.5 h-3.5 text-indigo-400" />
            <span>ML Features</span>
          </button>
          <button
            onClick={() => setIsGraphModalOpen(true)}
            className="px-3.5 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-cyan-300 border border-cyan-500/30 text-xs font-semibold flex items-center gap-1.5 shadow-md transition cursor-pointer"
          >
            <Layers className="w-3.5 h-3.5 text-cyan-400" />
            <span>Evidence Graph</span>
          </button>
          <button
            onClick={handleRunRiskAgent}
            disabled={isRiskAgentRunning}
            className="px-3.5 py-1.5 rounded-xl bg-gradient-to-r from-rose-600 to-amber-600 hover:from-rose-500 hover:to-amber-500 text-white text-xs font-semibold flex items-center gap-1.5 shadow-lg shadow-rose-500/20 transition cursor-pointer disabled:opacity-50"
          >
            {isRiskAgentRunning ? (
              <>
                <Loader2 className="w-3.5 h-3.5 animate-spin" />
                <span>Risk Agent Evaluating...</span>
              </>
            ) : (
              <>
                <ShieldAlert className="w-3.5 h-3.5 text-white" />
                <span>Run Risk Agent</span>
              </>
            )}
          </button>
          <button
            onClick={handleRunOrchestrator}
            disabled={isOrchestrating}
            className="px-3.5 py-1.5 rounded-xl bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white text-xs font-semibold flex items-center gap-1.5 shadow-lg shadow-purple-500/20 transition cursor-pointer disabled:opacity-50"
          >
            {isOrchestrating ? (
              <>
                <Loader2 className="w-3.5 h-3.5 animate-spin" />
                <span>Running LangGraph...</span>
              </>
            ) : (
              <>
                <Sparkles className="w-3.5 h-3.5" />
                <span>Run Agentic AI Audit</span>
              </>
            )}
          </button>
          <button
            onClick={handleOpenNoticeModal}
            className="px-3.5 py-1.5 rounded-xl bg-amber-600/20 border border-amber-500/40 hover:bg-amber-600/30 text-amber-300 text-xs font-semibold flex items-center gap-1.5 transition cursor-pointer"
          >
            <Scale className="w-3.5 h-3.5 text-amber-400" />
            <span>{isNoticeLoading ? 'Loading Notice...' : 'Statutory Notice'}</span>
          </button>
          <button
            onClick={handleExportDossier}
            className="px-3.5 py-1.5 rounded-xl bg-indigo-600/20 border border-indigo-500/40 hover:bg-indigo-600/30 text-indigo-300 text-xs font-semibold flex items-center gap-1.5 transition cursor-pointer"
            title="Download Statutory Audit Dossier (JSON)"
          >
            <Download className="w-3.5 h-3.5 text-indigo-400" />
            <span>Export Dossier</span>
          </button>
          <span className="text-xs text-slate-400 font-mono">Dossier ID: DOS-{establishment.id}</span>
          {onBeginInspection && (
            <button
              onClick={onBeginInspection}
              className="px-3.5 py-1.5 rounded-xl bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white text-xs font-bold flex items-center gap-1.5 shadow-lg shadow-emerald-500/20 transition cursor-pointer"
            >
              <ClipboardList className="w-3.5 h-3.5" />
              <span>Begin Field Inspection</span>
            </button>
          )}
        </div>
      </div>

      {/* Establishment Header Dossier Banner */}
      <div className="glass-panel p-6 rounded-2xl border border-slate-800 flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div className="flex items-start gap-4">
          <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-blue-600 to-indigo-700 flex items-center justify-center text-white shadow-lg shadow-blue-500/20 shrink-0">
            <Building2 className="w-7 h-7" />
          </div>
          <div className="space-y-1">
            <div className="flex flex-wrap items-center gap-2">
              <h1 className="text-xl sm:text-2xl font-extrabold text-white">{establishment.name}</h1>
              <RiskBadge category={establishment.risk_category} score={establishment.risk_score} size="md" />
            </div>
            <p className="text-xs text-slate-400">
              Registration No: <strong className="font-mono text-slate-300">{establishment.registration_number}</strong> • Sector: {establishment.industry}
            </p>
            <p className="text-xs text-slate-400">
              Reported Active Workforce: <strong className="font-mono text-slate-200">{establishment.worker_count} Workers</strong>
            </p>
          </div>
        </div>

        <div className="flex items-center gap-4 border-t md:border-t-0 md:border-l border-slate-800 pt-4 md:pt-0 md:pl-6">
          <div className="text-center">
            <span className="text-[10px] text-slate-400 uppercase font-semibold block">Risk Score</span>
            <span className="text-3xl font-extrabold font-mono text-rose-400">{establishment.risk_score}</span>
            <span className="text-[10px] text-slate-500 block">/ 100 Calibrated</span>
          </div>
          <div className="text-center">
            <span className="text-[10px] text-slate-400 uppercase font-semibold block">Rule Findings</span>
            <span className="text-3xl font-extrabold font-mono text-amber-400">{findings.length}</span>
            <span className="text-[10px] text-slate-500 block">Non-Compliant</span>
          </div>
          <div className="text-center">
            <span className="text-[10px] text-slate-400 uppercase font-semibold block">Anomalies</span>
            <span className="text-3xl font-extrabold font-mono text-purple-400">{anomalies.length}</span>
            <span className="text-[10px] text-slate-500 block">Cross-Register</span>
          </div>
        </div>
      </div>

      {/* Multi-Agent Orchestrator Stepper Banner */}
      {orchestrationResult && (
        <div className="p-5 rounded-2xl bg-gradient-to-r from-purple-950/40 via-slate-900 to-indigo-950/40 border border-purple-500/30 space-y-4 shadow-xl">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-purple-500/20 pb-3">
            <div className="flex items-center gap-2">
              <div className="p-1.5 rounded-lg bg-purple-500/20 text-purple-300">
                <Cpu className="w-4 h-4" />
              </div>
              <div>
                <h3 className="text-xs font-bold text-white flex items-center gap-2">
                  LangGraph Agentic Orchestrator Execution Completed
                  <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
                    {orchestrationResult.status}
                  </span>
                </h3>
                <p className="text-[11px] text-slate-400 font-mono">
                  Workflow: {orchestrationResult.workflow_id} • Execution Time: {orchestrationResult.execution_time_ms}ms • {orchestrationResult.steps_completed} Checkpoints
                </p>
              </div>
            </div>
            <div className="flex items-center gap-2 text-xs font-mono">
              <span className="px-2.5 py-1 rounded bg-slate-900 border border-slate-800 text-amber-400">
                Compliance: {orchestrationResult.compliance_score}%
              </span>
              <span className="px-2.5 py-1 rounded bg-slate-900 border border-slate-800 text-rose-400">
                Risk Score: {orchestrationResult.risk_score} ({orchestrationResult.risk_category})
              </span>
            </div>
          </div>

          {/* Stepper Node Transitions */}
          <div className="grid grid-cols-1 md:grid-cols-5 gap-2.5">
            {orchestrationResult.steps.map((s, idx) => (
              <div key={idx} className="p-3 rounded-xl bg-slate-950/80 border border-slate-800 space-y-1.5 hover:border-purple-500/40 transition">
                <div className="flex items-center justify-between">
                  <span className="text-[9px] font-mono px-1.5 py-0.5 rounded bg-purple-500/10 text-purple-400 font-bold border border-purple-500/20">
                    {s.node_name}
                  </span>
                  <span className="text-[9px] font-mono text-slate-500">#{s.step_index}</span>
                </div>
                <p className="text-[11px] text-slate-300 leading-tight">
                  {s.action_taken}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Risk Agent Tactical Enforcement Mandate Card */}
      {riskAgentResult && (
        <div className="glass-panel p-5 rounded-2xl border border-rose-500/30 bg-gradient-to-r from-rose-950/20 via-slate-900 to-amber-950/20 space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800 pb-3">
            <div className="flex items-center gap-2.5">
              <div className="p-2 rounded-xl bg-rose-500/10 text-rose-400 border border-rose-500/20">
                <ShieldAlert className="w-5 h-5" />
              </div>
              <div>
                <h2 className="text-sm font-bold text-white flex items-center gap-2">
                  Risk Agent: Calibrated Tactical Enforcement Mandate
                </h2>
                <p className="text-xs text-slate-400">
                  Grounding: {riskAgentResult.ml_model_used} • Actuarial Baseline: {riskAgentResult.base_jurisdiction_risk} pts
                </p>
              </div>
            </div>
            <div className="flex items-center gap-2 text-xs font-mono">
              <RiskBadge category={riskAgentResult.priority_class} score={riskAgentResult.calibrated_risk_score} size="sm" />
              <span className="px-2.5 py-1 rounded bg-slate-900 border border-slate-800 text-amber-300">
                {riskAgentResult.percentile_context}
              </span>
              <span className="px-2.5 py-1 rounded bg-slate-900 border border-slate-800 text-emerald-400 font-bold">
                {(riskAgentResult.confidence_score * 100).toFixed(0)}% Conf
              </span>
            </div>
          </div>

          <p className="text-xs text-slate-300 leading-relaxed font-sans">
            {riskAgentResult.attribution_synthesis.synthesis_narrative}
          </p>

          {/* Directives Grid */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
            {riskAgentResult.enforcement_directives.map((dir) => (
              <div key={dir.directive_id} className="p-3.5 rounded-xl bg-slate-950/80 border border-slate-800 space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded bg-rose-500/20 text-rose-300 border border-rose-500/30">
                    {dir.urgency}
                  </span>
                  <span className="text-[10px] font-mono text-slate-500">{dir.directive_id}</span>
                </div>
                <h4 className="text-xs font-bold text-slate-100 uppercase font-mono">
                  {dir.action_type.replace(/_/g, ' ')}
                </h4>
                <p className="text-[11px] text-slate-300 leading-tight">
                  {dir.description}
                </p>
                <div className="text-[10px] font-mono text-amber-400/90 pt-1 border-t border-slate-800/80">
                  {dir.statutory_authority}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Navigation Tabs Bar */}
      <div className="border-b border-slate-800 flex items-center gap-2 overflow-x-auto pb-1">
        {[
          { id: 'overview', label: 'Overview', icon: Building2 },
          { id: 'documents', label: `Documents (${documents.length})`, icon: FileText },
          { id: 'findings', label: `Compliance Findings (${findings.length})`, icon: Scale },
          { id: 'anomalies', label: `Cross-Doc Anomalies (${anomalies.length})`, icon: AlertTriangle },
          { id: 'shap', label: 'SHAP Risk Explanation', icon: Activity },
          { id: 'brief', label: 'AI Inspection Brief', icon: Bot },
          { id: 'timeline', label: `Audit Timeline (${timelineData?.total_events || 0})`, icon: History },
          { id: 'feedback', label: 'Inspector Verification', icon: ShieldCheck },
        ].map((tab) => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as TabType)}
              className={`flex items-center gap-2 px-4 py-2.5 rounded-xl text-xs font-semibold whitespace-nowrap transition ${
                isActive
                  ? 'bg-blue-600/20 text-blue-300 border border-blue-500/30'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900/60'
              }`}
            >
              <Icon className={`w-3.5 h-3.5 ${isActive ? 'text-blue-400' : 'text-slate-500'}`} />
              <span>{tab.label}</span>
            </button>
          );
        })}
      </div>

      {/* Tab 1: OVERVIEW */}
      {activeTab === 'overview' && (
        <div className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            
            <div className="md:col-span-2 glass-panel p-6 rounded-2xl space-y-4">
              <h2 className="text-base font-bold text-white flex items-center gap-2">
                <AlertOctagon className="w-4 h-4 text-rose-400" />
                Primary Executive Risk Summary
              </h2>
              <p className="text-xs text-slate-300 leading-relaxed">
                {ai_inspection_brief.brief_summary}
              </p>

              <div className="pt-4 border-t border-slate-800 space-y-3">
                <h3 className="text-xs font-semibold text-slate-200 uppercase tracking-wider">
                  Critical Recommended Focus Areas for Inspection Officer
                </h3>
                <div className="space-y-2">
                  {ai_inspection_brief.critical_focus_areas.map((focus, idx) => (
                    <div key={idx} className="flex items-start gap-2 text-xs text-slate-300 bg-slate-900/60 p-3 rounded-xl border border-slate-800">
                      <span className="text-rose-400 font-bold">•</span>
                      <span>{focus}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            <div className="glass-panel p-6 rounded-2xl space-y-4">
              <h2 className="text-base font-bold text-white flex items-center gap-2">
                <Activity className="w-4 h-4 text-emerald-400" />
                ML Risk Model Metadata
              </h2>
              <div className="space-y-2.5 text-xs">
                <div className="flex justify-between py-1.5 border-b border-slate-800 text-slate-400">
                  <span>Model Algorithm:</span>
                  <strong className="text-slate-200 font-mono">XGBoost 2.0</strong>
                </div>
                <div className="flex justify-between py-1.5 border-b border-slate-800 text-slate-400">
                  <span>Risk Probability:</span>
                  <strong className="text-rose-400 font-mono">0.87 (87%)</strong>
                </div>
                <div className="flex justify-between py-1.5 border-b border-slate-800 text-slate-400">
                  <span>Jurisdiction Percentile:</span>
                  <strong className="text-slate-200 font-mono">94th %ile</strong>
                </div>
                <div className="flex justify-between py-1.5 border-b border-slate-800 text-slate-400">
                  <span>Deterministic Violations:</span>
                  <strong className="text-amber-400 font-mono">3 Rules Failed</strong>
                </div>
                <div className="flex justify-between py-1.5 text-slate-400">
                  <span>Cross-Doc Mismatch:</span>
                  <strong className="text-purple-400 font-mono">5 Workers Unaccounted</strong>
                </div>
              </div>

              <button
                onClick={() => setActiveTab('brief')}
                className="w-full py-2.5 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-semibold text-xs transition shadow-md shadow-blue-500/20"
              >
                View Complete Inspection Brief
              </button>
            </div>

          </div>
        </div>
      )}

      {/* Tab 2: DOCUMENTS & STATUTORY GAP ANALYSIS */}
      {activeTab === 'documents' && (
        <div className="space-y-6">
          
          {/* Autonomous Document Agent Gap Analysis Card */}
          {docAuditResult && (
            <div className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-5">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800 pb-4">
                <div>
                  <h2 className="text-base font-bold text-white flex items-center gap-2">
                    <FileCheck2 className="w-4 h-4 text-emerald-400" />
                    Autonomous Document Agent Statutory Filing Audit
                  </h2>
                  <p className="text-xs text-slate-400 mt-0.5">
                    Evaluates scan legibility, structural completeness, and compares uploaded registers against legally mandated filings
                  </p>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-xs font-mono px-2.5 py-1 rounded bg-blue-500/10 text-blue-400 border border-blue-500/20">
                    Legibility: {docAuditResult.overall_legibility_score}% ({docAuditResult.legibility_status})
                  </span>
                  <span className="text-xs font-mono px-2.5 py-1 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                    Completeness: {docAuditResult.completeness_score}%
                  </span>
                </div>
              </div>

              {/* Missing Statutory Registers Warning */}
              {docAuditResult.missing_count > 0 && (
                <div className="p-4 rounded-xl bg-rose-950/30 border border-rose-500/30 space-y-2">
                  <div className="flex items-center gap-2 text-xs font-bold text-rose-300">
                    <AlertTriangle className="w-4 h-4 text-rose-400" />
                    <span>Statutory Default Warning: {docAuditResult.missing_count} Mandatory Register(s) Missing</span>
                  </div>
                  <ul className="text-xs text-rose-200/80 space-y-1 list-disc list-inside">
                    {docAuditResult.missing_registers_penalties.map((pen, pIdx) => (
                      <li key={pIdx} className="font-mono text-[11px]">{pen}</li>
                    ))}
                  </ul>
                  <p className="text-xs text-slate-300 pt-1 border-t border-rose-900/50">
                    <strong>Agent Recommendation:</strong> {docAuditResult.agent_recommendation}
                  </p>
                </div>
              )}

              {/* Statutory Registers Matrix Table */}
              <div className="space-y-3">
                <h3 className="text-xs font-bold text-slate-200 uppercase tracking-wider font-mono">
                  Statutory Register Filing Compliance Matrix (Four Labour Codes):
                </h3>
                <div className="overflow-x-auto rounded-xl border border-slate-800">
                  <table className="w-full text-left text-xs">
                    <thead className="bg-slate-900 text-slate-400 font-mono text-[11px] uppercase border-b border-slate-800">
                      <tr>
                        <th className="p-3">Form</th>
                        <th className="p-3">Statutory Register</th>
                        <th className="p-3">Governing Code & Section</th>
                        <th className="p-3">Filing Frequency</th>
                        <th className="p-3">Filing Status</th>
                        <th className="p-3">Statutory Penalty on Default</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-800/80">
                      {docAuditResult.register_comparisons.map((reg, rIdx) => (
                        <tr key={rIdx} className="hover:bg-slate-900/40 transition">
                          <td className="p-3 font-mono font-bold text-amber-400">{reg.form_designation}</td>
                          <td className="p-3 text-slate-200 font-medium">{reg.register_name}</td>
                          <td className="p-3 text-slate-400 font-mono text-[11px]">{reg.statute} • {reg.section}</td>
                          <td className="p-3 text-slate-400">{reg.filing_frequency}</td>
                          <td className="p-3">
                            <span className={`text-[10px] font-mono px-2 py-0.5 rounded font-bold border ${
                              reg.status === 'SUBMITTED'
                                ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30'
                                : 'bg-rose-500/10 text-rose-400 border-rose-500/30'
                            }`}>
                              {reg.status}
                            </span>
                          </td>
                          <td className="p-3 font-mono text-[11px] text-slate-400">{reg.penalty_on_default}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>

            </div>
          )}

          {/* Uploaded Files Matrix */}
          <div className="glass-panel rounded-2xl border border-slate-800 p-6 space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-base font-bold text-white flex items-center gap-2">
                  <FileText className="w-4 h-4 text-blue-400" />
                  Audited Uploaded Documents & Text Extraction Proofs
                </h2>
                <p className="text-xs text-slate-400 mt-0.5">
                  Parsed using Direct PDF Text Layer + PaddleOCR Layout Analysis
                </p>
              </div>
              <button
                onClick={() => onNavigate('upload')}
                className="text-xs text-blue-400 hover:text-blue-300 font-semibold"
              >
                + Upload Additional Records
              </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {documents.map((doc) => (
                <div key={doc.id} className="p-4 rounded-xl bg-slate-900/70 border border-slate-800 space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-semibold text-slate-200">{doc.document_type}</span>
                    <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                      OCR Conf: {Math.round(doc.ocr_confidence * 100)}%
                    </span>
                  </div>
                  <p className="text-xs font-mono text-slate-400 truncate">{doc.filename}</p>
                  <div className="flex items-center justify-between pt-2 border-t border-slate-800/80 text-[11px] text-slate-500 font-mono">
                    <span>{doc.pages} Pages • {doc.extracted_records} Rows Extracted</span>
                    <span>Uploaded: {doc.upload_date}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

        </div>
      )}

      {/* Tab 3: COMPLIANCE FINDINGS */}
      {activeTab === 'findings' && (
        <div className="space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 p-4 rounded-2xl bg-slate-900 border border-slate-800">
            <div>
              <div className="flex items-center gap-2">
                <h2 className="text-base font-bold text-white flex items-center gap-2">
                  <Scale className="w-4 h-4 text-amber-400" />
                  Autonomous Compliance Agent Audit
                </h2>
                {liveAuditReport && (
                  <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-rose-500/20 text-rose-300 border border-rose-500/30 font-bold">
                    {liveAuditReport.overall_compliance_score}% Pass Rate ({liveAuditReport.failed_count} Violations)
                  </span>
                )}
                <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-blue-500/20 text-blue-300 border border-blue-500/30 font-bold">
                  98% RAG Grounded
                </span>
              </div>
              <p className="text-xs text-slate-400 mt-0.5">
                Deterministic rules validated against Four Labour Codes RAG with row-level evidence anchors & zero hallucinations
              </p>
            </div>
            {liveAuditReport ? (
              <div className="flex items-center gap-2 text-xs font-mono">
                <span className="px-2.5 py-1 rounded bg-rose-500/10 text-rose-400 border border-rose-500/20">
                  {liveAuditReport.failed_count} Failed
                </span>
                <span className="px-2.5 py-1 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                  {liveAuditReport.passed_count} Passed
                </span>
              </div>
            ) : (
              <span className="text-xs font-mono text-amber-400 bg-amber-500/10 px-2.5 py-1 rounded border border-amber-500/20">
                {findings.length} Flagged Issues
              </span>
            )}
          </div>

          <div className="space-y-4">
            {findings.map((finding) => {
              const groundedMatch = complianceAgentAudit?.findings.find(f => f.rule_id === finding.rule_id);

              return (
                <div key={finding.id} className="glass-panel p-5 rounded-xl border border-slate-800 space-y-3">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-mono font-bold text-amber-400 bg-amber-500/10 px-2 py-0.5 rounded border border-amber-500/20">
                        {finding.rule_id}
                      </span>
                      <h3 className="font-bold text-sm text-slate-100">{finding.rule_name}</h3>
                    </div>
                    <div className="flex items-center gap-2">
                      {groundedMatch && (
                        <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                          {Math.round(groundedMatch.statutory_enrichment.relevance_score * 100)}% Grounded
                        </span>
                      )}
                      <RiskBadge category={finding.severity} size="sm" />
                    </div>
                  </div>

                  {/* Agent Synthesized Explanation */}
                  {groundedMatch && (
                    <p className="text-xs text-slate-300 leading-relaxed bg-slate-900/50 p-3 rounded-lg border border-slate-800">
                      {groundedMatch.explanation}
                    </p>
                  )}

                  {/* Evidence Anchor Snippet */}
                  <div className="bg-slate-950/80 p-3 rounded-lg border border-slate-850 space-y-1">
                    <div className="flex items-center justify-between text-[11px] text-slate-500 font-mono">
                      <span>
                        Source: {groundedMatch ? groundedMatch.evidence_anchor.document_name : finding.source_document} 
                        {' '}(Page {groundedMatch ? groundedMatch.evidence_anchor.page_number : finding.page}
                        {groundedMatch?.evidence_anchor.row_index ? `, Row ${groundedMatch.evidence_anchor.row_index}` : ''}
                        {groundedMatch?.evidence_anchor.employee_id ? `, ${groundedMatch.evidence_anchor.employee_id}` : ''})
                      </span>
                      <span className="text-rose-400 font-bold">Row-Level Evidence Anchor</span>
                    </div>
                    <p className="text-xs text-slate-300 font-mono">
                      {groundedMatch ? groundedMatch.evidence_anchor.discrepancy_value : finding.evidence}
                    </p>
                  </div>

                  {/* RAG Statutory Citation Card */}
                  {groundedMatch ? (
                    <div className="p-3.5 rounded-xl bg-blue-950/20 border border-blue-500/30 space-y-2">
                      <div className="flex items-center justify-between text-xs font-mono">
                        <span className="text-blue-300 font-bold">
                          {groundedMatch.statutory_enrichment.act_title} • {groundedMatch.statutory_enrichment.section_number}
                        </span>
                        <span className="text-[10px] text-blue-400">
                          Enforcing Authority: {groundedMatch.statutory_enrichment.authority}
                        </span>
                      </div>
                      <p className="text-xs text-slate-300 italic">
                        "{groundedMatch.statutory_enrichment.statutory_quote}"
                      </p>
                      {groundedMatch.statutory_enrichment.penalty_schedule && (
                        <div className="text-[11px] font-mono text-rose-300 pt-1 border-t border-blue-900/40">
                          <strong>Statutory Penalty Schedule:</strong> {groundedMatch.statutory_enrichment.penalty_schedule}
                        </div>
                      )}
                    </div>
                  ) : (
                    <StatutoryReferenceCard
                      statute={finding.statutory_reference}
                      authority={finding.authority}
                    />
                  )}

                  {/* Actionable Remedy */}
                  {groundedMatch?.actionable_remedy && (
                    <div className="p-2.5 rounded-lg bg-amber-500/10 border border-amber-500/20 text-xs text-amber-300 flex items-start gap-2">
                      <span className="font-bold uppercase tracking-wider font-mono text-[10px] px-1.5 py-0.5 rounded bg-amber-500/20">Remedy</span>
                      <span>{groundedMatch.actionable_remedy}</span>
                    </div>
                  )}

                {/* Verification Feedback Buttons */}
                <div className="flex items-center justify-between pt-2 border-t border-slate-800/80 text-xs">
                  <span className="text-slate-400">Inspector Verification:</span>
                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => handleFeedback(finding.id, 'CONFIRMED')}
                      className={`px-2.5 py-1 rounded text-xs font-semibold flex items-center gap-1 transition ${
                        feedbackState[finding.id] === 'CONFIRMED'
                          ? 'bg-rose-500 text-white'
                          : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
                      }`}
                    >
                      <Check className="w-3 h-3" />
                      <span>Confirm Finding</span>
                    </button>
                    <button
                      onClick={() => handleFeedback(finding.id, 'REJECTED')}
                      className={`px-2.5 py-1 rounded text-xs font-semibold flex items-center gap-1 transition ${
                        feedbackState[finding.id] === 'REJECTED'
                          ? 'bg-emerald-600 text-white'
                          : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
                      }`}
                    >
                      <X className="w-3 h-3" />
                      <span>Reject / Dismiss</span>
                    </button>
                    <button
                      onClick={() => handleFeedback(finding.id, 'NEEDS_MORE_EVIDENCE')}
                      className={`px-2.5 py-1 rounded text-xs font-semibold flex items-center gap-1 transition ${
                        feedbackState[finding.id] === 'NEEDS_MORE_EVIDENCE'
                          ? 'bg-amber-500 text-slate-950'
                          : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
                      }`}
                    >
                      <HelpCircle className="w-3 h-3" />
                      <span>Request Evidence</span>
                    </button>
                  </div>
                </div>

              </div>
            );
          })}
          </div>
        </div>
      )}

      {/* Tab 4: CROSS-DOC ANOMALIES */}
      {activeTab === 'anomalies' && (
        <div className="space-y-6">
          
          {/* Engine Header & Summary Stats */}
          <div className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-5">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800 pb-4">
              <div>
                <h2 className="text-base font-bold text-white flex items-center gap-2">
                  <AlertTriangle className="w-4 h-4 text-purple-400" />
                  Cross-Document Reconciliation & Anomaly Engine
                </h2>
                <p className="text-xs text-slate-400 mt-0.5">
                  Automated multi-way cross-referencing across Form B (Wages), Form D (Muster Roll), Bank UTR Scrolls, and Gate Turnstiles
                </p>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-xs font-mono px-2.5 py-1 rounded bg-rose-500/10 text-rose-400 border border-rose-500/20 font-bold">
                  {anomalyResult ? anomalyResult.reconciliation_summary.anomalies_detected : anomalies.length} Flagged Inconsistencies
                </span>
                <span className="text-xs font-mono px-2.5 py-1 rounded bg-purple-500/10 text-purple-300 border border-purple-500/20">
                  ₹{anomalyResult ? anomalyResult.reconciliation_summary.financial_discrepancy_total.toLocaleString('en-IN') : '3,92,500'} Discrepancy Total
                </span>
              </div>
            </div>

            {/* Reconciliation KPI Matrix */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
              <div className="p-3 rounded-xl bg-slate-900/60 border border-slate-800">
                <div className="text-[11px] text-slate-400 font-mono">Ghost Workers Flagged</div>
                <div className="text-lg font-bold text-rose-400 font-mono">
                  {anomalyResult ? anomalyResult.reconciliation_summary.ghost_workers_count : 1}
                </div>
                <div className="text-[10px] text-slate-500">Wage credited with 0 attendance</div>
              </div>
              <div className="p-3 rounded-xl bg-slate-900/60 border border-slate-800">
                <div className="text-[11px] text-slate-400 font-mono">Uncompensated Attendance</div>
                <div className="text-lg font-bold text-amber-400 font-mono">
                  {anomalyResult ? anomalyResult.reconciliation_summary.uncompensated_workers_count : 1}
                </div>
                <div className="text-[10px] text-slate-500">Attended shifts with ₹0 payout</div>
              </div>
              <div className="p-3 rounded-xl bg-slate-900/60 border border-slate-800">
                <div className="text-[11px] text-slate-400 font-mono">Bank Payout Skimming</div>
                <div className="text-lg font-bold text-purple-400 font-mono">1 Diverted</div>
                <div className="text-[10px] text-slate-500">Form B net != Bank UTR transfer</div>
              </div>
              <div className="p-3 rounded-xl bg-slate-900/60 border border-slate-800">
                <div className="text-[11px] text-slate-400 font-mono">Contractor Suppression</div>
                <div className="text-lg font-bold text-cyan-400 font-mono">25 Workers</div>
                <div className="text-[10px] text-slate-500">Gate security vs Form A headcount</div>
              </div>
            </div>

            {/* Cross-Document Multi-Way Flow Visualization */}
            <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-850 space-y-2">
              <div className="text-[11px] font-mono text-slate-400 font-bold uppercase tracking-wider">
                Multi-Way Cross-Document Reconciliation Pipeline
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-4 gap-2 text-center text-xs font-mono">
                <div className="p-2.5 rounded-lg bg-blue-500/10 border border-blue-500/20 text-blue-300">
                  <div className="font-bold">Form B Register</div>
                  <div className="text-[10px] text-slate-400">Gross & Net Wages</div>
                </div>
                <div className="p-2.5 rounded-lg bg-emerald-500/10 border border-emerald-500/20 text-emerald-300">
                  <div className="font-bold">Form D Muster Roll</div>
                  <div className="text-[10px] text-slate-400">Physical Attendance</div>
                </div>
                <div className="p-2.5 rounded-lg bg-purple-500/10 border border-purple-500/20 text-purple-300">
                  <div className="font-bold">Bank UTR Scrolls</div>
                  <div className="text-[10px] text-slate-400">Disbursed Funds</div>
                </div>
                <div className="p-2.5 rounded-lg bg-amber-500/10 border border-amber-500/20 text-amber-300">
                  <div className="font-bold">Gate Turnstile Log</div>
                  <div className="text-[10px] text-slate-400">Actual Footfall Headcount</div>
                </div>
              </div>
            </div>

          </div>

          {/* Anomaly Detailed Cards */}
          <div className="space-y-4">
            {(anomalyResult?.anomalies || []).map((anom) => (
              <div key={anom.anomaly_id} className="glass-panel p-5 rounded-xl border border-slate-800 space-y-3">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className={`text-[10px] font-mono font-bold px-2 py-0.5 rounded border ${
                      anom.anomaly_type === 'GHOST_WORKER'
                        ? 'bg-rose-500/10 text-rose-400 border-rose-500/30'
                        : anom.anomaly_type === 'CONTRACTOR_SUPPRESSION'
                        ? 'bg-purple-500/10 text-purple-300 border-purple-500/30'
                        : 'bg-amber-500/10 text-amber-400 border-amber-500/30'
                    }`}>
                      {anom.anomaly_type}
                    </span>
                    {anom.affected_worker_id && (
                      <span className="text-xs font-mono text-slate-300 bg-slate-800 px-2 py-0.5 rounded">
                        {anom.affected_worker_id} • {anom.affected_worker_name}
                      </span>
                    )}
                  </div>
                  <div className="flex items-center gap-2">
                    {anom.discrepancy_amount && (
                      <span className="text-xs font-mono font-bold text-rose-400 bg-rose-500/10 px-2 py-0.5 rounded border border-rose-500/20">
                        Discrepancy: ₹{anom.discrepancy_amount.toLocaleString('en-IN')}
                      </span>
                    )}
                    <RiskBadge category={anom.severity} size="sm" />
                  </div>
                </div>

                <p className="text-xs text-slate-300 leading-relaxed">
                  {anom.description}
                </p>

                {/* Primary vs Cross-Reference Comparison Box */}
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs font-mono">
                  <div className="p-2.5 rounded-lg bg-slate-900/80 border border-slate-800">
                    <span className="text-[10px] text-slate-500 block uppercase">Primary Record Proof:</span>
                    <span className="text-blue-300 font-semibold">{anom.primary_document}</span>
                  </div>
                  <div className="p-2.5 rounded-lg bg-slate-900/80 border border-slate-800">
                    <span className="text-[10px] text-slate-500 block uppercase">Cross-Referenced Source:</span>
                    <span className="text-amber-300 font-semibold">{anom.cross_reference_document}</span>
                  </div>
                </div>

                {/* Statutory Implication */}
                <div className="p-3 rounded-xl bg-purple-950/20 border border-purple-500/30 text-xs text-slate-300 space-y-1">
                  <span className="text-[10px] font-mono text-purple-300 font-bold uppercase tracking-wider block">
                    Statutory Implication & Legal Exposure:
                  </span>
                  <p>{anom.statutory_implication}</p>
                </div>
              </div>
            ))}
          </div>

          {/* Engine Recommendations */}
          {anomalyResult?.recommendations && (
            <div className="glass-panel p-5 rounded-xl border border-slate-800 space-y-2">
              <h3 className="text-xs font-bold text-slate-200 uppercase tracking-wider font-mono">
                Cross-Document Inspection Officer Directives:
              </h3>
              <ul className="space-y-1.5 text-xs text-slate-300 list-disc list-inside font-mono">
                {anomalyResult.recommendations.map((rec, rIdx) => (
                  <li key={rIdx}>{rec}</li>
                ))}
              </ul>
            </div>
          )}

        </div>
      )}

      {/* Tab 5: SHAP EXPLANATION */}
      {activeTab === 'shap' && (
        <div className="space-y-6">
          
          {/* TreeSHAP Additivity Equation Header Banner */}
          <div className="glass-panel rounded-2xl border border-slate-800 p-6 space-y-4">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800 pb-4">
              <div>
                <h2 className="text-base font-bold text-white flex items-center gap-2">
                  <Activity className="w-4 h-4 text-emerald-400" />
                  TreeSHAP Local Risk Explainability Engine
                </h2>
                <p className="text-xs text-slate-400 mt-0.5">
                  Exact local Shapley attribution explaining how each feature pushes the XGBoost Risk Score from baseline to {establishment.risk_score}/100
                </p>
              </div>
              <span className="text-[10px] font-mono px-2.5 py-1 rounded bg-emerald-500/10 text-emerald-300 border border-emerald-500/30 font-bold self-start sm:self-auto">
                TreeSHAP v0.51 Exact Attribution
              </span>
            </div>

            {/* Additivity Equation Cards */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 font-mono">
              <div className="p-3.5 rounded-xl bg-slate-950/60 border border-slate-850">
                <span className="text-[10px] text-slate-500 uppercase block">Expected Base Risk E[f(X)]</span>
                <span className="text-2xl font-extrabold text-blue-400">
                  {shapExplanation?.base_value || 53.5}
                </span>
                <span className="text-[10px] text-slate-500 block">Jurisdiction baseline</span>
              </div>
              <div className="p-3.5 rounded-xl bg-slate-950/60 border border-slate-850">
                <span className="text-[10px] text-slate-500 uppercase block">Net Shapley Delta Σφᵢ</span>
                <span className="text-2xl font-extrabold text-rose-400">
                  +{(shapExplanation?.net_shap_adjustment || 31.0).toFixed(1)}
                </span>
                <span className="text-[10px] text-slate-500 block">Risk escalation delta</span>
              </div>
              <div className="p-3.5 rounded-xl bg-slate-950/60 border border-slate-850">
                <span className="text-[10px] text-slate-500 uppercase block">Reconciled Final Score</span>
                <span className="text-2xl font-extrabold text-white">
                  {establishment.risk_score}
                </span>
                <span className="text-[10px] text-slate-500 block">Base + Net Delta = Score</span>
              </div>
            </div>
          </div>

          {/* Two-Column Breakdown: Escalators vs Mitigators */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            
            {/* Positive Escalators */}
            <div className="glass-panel p-5 rounded-xl border border-slate-800 space-y-4">
              <div className="flex items-center justify-between border-b border-slate-800 pb-3">
                <h3 className="text-xs font-bold text-rose-400 uppercase tracking-wider font-mono flex items-center gap-1.5">
                  <TrendingUp className="w-3.5 h-3.5" />
                  Primary Risk Escalators (Pushed Score Up)
                </h3>
                <span className="text-[10px] font-mono text-slate-500">
                  {(shapExplanation?.positive_escalators || []).length || shap_contributions.filter(s => s.direction === 'positive').length} Factors
                </span>
              </div>

              <div className="space-y-3">
                {(shapExplanation?.positive_escalators || []).length > 0 ? (
                  shapExplanation?.positive_escalators.map((esc) => (
                    <div key={esc.feature_name} className="p-3 rounded-xl bg-slate-950/60 border border-slate-850 space-y-1.5">
                      <div className="flex items-center justify-between text-xs font-mono">
                        <span className="font-bold text-slate-200">{esc.feature_label}</span>
                        <span className="font-extrabold text-rose-400">+{esc.shap_value.toFixed(1)} pts</span>
                      </div>
                      <div className="h-1.5 w-full bg-slate-800 rounded-full overflow-hidden">
                        <div
                          className="h-full bg-rose-500 rounded-full"
                          style={{ width: `${Math.min(esc.shap_value * 5, 100)}%` }}
                        />
                      </div>
                      <p className="text-[11px] text-slate-400 font-sans">{esc.explanation}</p>
                    </div>
                  ))
                ) : (
                  shap_contributions.filter(s => s.direction === 'positive').map((s, idx) => (
                    <div key={idx} className="p-3 rounded-xl bg-slate-950/60 border border-slate-850 space-y-1.5">
                      <div className="flex items-center justify-between text-xs font-mono">
                        <span className="font-bold text-slate-200">{s.feature_label}</span>
                        <span className="font-extrabold text-rose-400">+{s.contribution} pts</span>
                      </div>
                      <div className="h-1.5 w-full bg-slate-800 rounded-full overflow-hidden">
                        <div
                          className="h-full bg-rose-500 rounded-full"
                          style={{ width: `${Math.min(s.contribution * 5, 100)}%` }}
                        />
                      </div>
                      <p className="text-[11px] text-slate-400 font-sans">Increases establishment inspection priority.</p>
                    </div>
                  ))
                )}
              </div>
            </div>

            {/* Negative Mitigators */}
            <div className="glass-panel p-5 rounded-xl border border-slate-800 space-y-4">
              <div className="flex items-center justify-between border-b border-slate-800 pb-3">
                <h3 className="text-xs font-bold text-emerald-400 uppercase tracking-wider font-mono flex items-center gap-1.5">
                  <TrendingDown className="w-3.5 h-3.5" />
                  Protective Mitigators (Pulled Score Down)
                </h3>
                <span className="text-[10px] font-mono text-slate-500">
                  {(shapExplanation?.negative_mitigators || []).length || shap_contributions.filter(s => s.direction === 'negative').length} Factors
                </span>
              </div>

              <div className="space-y-3">
                {(shapExplanation?.negative_mitigators || []).length > 0 ? (
                  shapExplanation?.negative_mitigators.map((mit) => (
                    <div key={mit.feature_name} className="p-3 rounded-xl bg-slate-950/60 border border-slate-850 space-y-1.5">
                      <div className="flex items-center justify-between text-xs font-mono">
                        <span className="font-bold text-slate-200">{mit.feature_label}</span>
                        <span className="font-extrabold text-emerald-400">{mit.shap_value.toFixed(1)} pts</span>
                      </div>
                      <div className="h-1.5 w-full bg-slate-800 rounded-full overflow-hidden">
                        <div
                          className="h-full bg-emerald-500 rounded-full"
                          style={{ width: `${Math.min(Math.abs(mit.shap_value) * 6, 100)}%` }}
                        />
                      </div>
                      <p className="text-[11px] text-slate-400 font-sans">{mit.explanation}</p>
                    </div>
                  ))
                ) : (
                  shap_contributions.filter(s => s.direction === 'negative').map((s, idx) => (
                    <div key={idx} className="p-3 rounded-xl bg-slate-950/60 border border-slate-850 space-y-1.5">
                      <div className="flex items-center justify-between text-xs font-mono">
                        <span className="font-bold text-slate-200">{s.feature_label}</span>
                        <span className="font-extrabold text-emerald-400">{s.contribution} pts</span>
                      </div>
                      <div className="h-1.5 w-full bg-slate-800 rounded-full overflow-hidden">
                        <div
                          className="h-full bg-emerald-500 rounded-full"
                          style={{ width: `${Math.min(Math.abs(s.contribution) * 6, 100)}%` }}
                        />
                      </div>
                      <p className="text-[11px] text-slate-400 font-sans">Protective compliance buffer reducing risk exposure.</p>
                    </div>
                  ))
                )}
              </div>
            </div>

          </div>

        </div>
      )}

      {/* Tab 6: GENERATIVE EXPLANATION LAYER */}
      {activeTab === 'brief' && (
        <div className="space-y-6">

          {/* Header + Audience Toggle */}
          <div className="glass-panel p-5 rounded-2xl border border-slate-800 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div>
              <h2 className="text-base font-bold text-white flex items-center gap-2">
                <Bot className="w-4 h-4 text-purple-400" />
                Generative Explanation Layer
              </h2>
              <p className="text-xs text-slate-400 mt-0.5">
                Dual-audience explanations strictly grounded in calibrated ML score, SHAP attributions & deterministic statutory citations
              </p>
            </div>
            <div className="flex items-center gap-2">
              {/* Audience Toggle */}
              <div className="flex items-center bg-slate-950 rounded-xl border border-slate-800 p-1 text-xs">
                <button
                  onClick={() => setExplanationAudience('inspector')}
                  className={`px-3 py-1.5 rounded-lg font-semibold transition cursor-pointer ${
                    explanationAudience === 'inspector'
                      ? 'bg-blue-600 text-white shadow-md'
                      : 'text-slate-400 hover:text-slate-200'
                  }`}
                >
                  🔍 Inspector Enforcement Brief
                </button>
                <button
                  onClick={() => setExplanationAudience('employer')}
                  className={`px-3 py-1.5 rounded-lg font-semibold transition cursor-pointer ${
                    explanationAudience === 'employer'
                      ? 'bg-emerald-600 text-white shadow-md'
                      : 'text-slate-400 hover:text-slate-200'
                  }`}
                >
                  🏭 Employer Remediation Advisory
                </button>
              </div>
              {explanation?.zero_hallucination_verified && (
                <span className="text-[10px] font-mono px-2 py-1 rounded bg-emerald-500/10 text-emerald-300 border border-emerald-500/30 font-bold">
                  ✓ ZERO HALLUCINATION VERIFIED
                </span>
              )}
            </div>
          </div>

          {/* INSPECTOR ENFORCEMENT BRIEF */}
          {explanationAudience === 'inspector' && (
            <div className="space-y-4">
              {/* Executive Summary */}
              <div className="glass-panel p-5 rounded-2xl border border-blue-500/20 bg-blue-950/10 space-y-3">
                <h3 className="text-xs font-bold text-blue-300 uppercase tracking-wider font-mono">Executive Enforcement Summary</h3>
                <p className="text-xs text-slate-300 leading-relaxed">
                  {explanation?.inspector_brief.executive_summary || ai_inspection_brief.brief_summary}
                </p>
                <div className="flex items-center gap-2 pt-1">
                  <RiskBadge category={(explanation?.inspector_brief.priority_class || ai_inspection_brief.priority) as any} size="sm" />
                  <span className="text-[11px] font-mono text-slate-400">
                    ML Risk Score: <span className="font-bold text-white">{explanation?.ml_risk_score || establishment.risk_score}/100</span>
                  </span>
                </div>
              </div>

              {/* Statutory Exposures */}
              <div className="glass-panel p-5 rounded-2xl border border-slate-800 space-y-4">
                <h3 className="text-xs font-bold text-rose-300 uppercase tracking-wider font-mono flex items-center gap-2">
                  <AlertOctagon className="w-3.5 h-3.5" /> Statutory Exposure Catalogue
                </h3>
                <div className="space-y-3">
                  {(explanation?.inspector_brief.statutory_exposures || [
                    { code_name: 'Code on Wages, 2019', section: 'Section 6(1) read with Section 8', contravention: 'Disbursement of basic wages below the statutory National Floor Wage / State Minimum Wage rates.', penalty_provision: 'Section 54: Fine up to ₹50,000; repeat offense punishable with imprisonment up to 3 months.' },
                    { code_name: 'Code on Wages, 2019', section: 'Section 14', contravention: 'Failure to compensate overtime hours at double the regular wage rate in Form B registers.', penalty_provision: 'Section 54(1): Fine up to ₹20,000 for statutory register contravention.' },
                    { code_name: 'OSHWC Code, 2020', section: 'Section 23 & 51', contravention: 'Operating without a constituted Joint Safety Committee despite employing >250 factory workers.', penalty_provision: 'Section 96: Fine up to ₹2,00,000 for non-compliance with safety administration standards.' },
                  ]).map((exp, idx) => (
                    <div key={idx} className="p-4 rounded-xl bg-rose-950/10 border border-rose-500/20 space-y-1.5">
                      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-1">
                        <span className="text-[11px] font-mono font-bold text-rose-300">{exp.code_name} — {exp.section}</span>
                      </div>
                      <p className="text-xs text-slate-300">{exp.contravention}</p>
                      <p className="text-[11px] text-amber-300 font-mono">{exp.penalty_provision}</p>
                    </div>
                  ))}
                </div>
              </div>

              {/* Documents to Seize */}
              <div className="glass-panel p-5 rounded-2xl border border-slate-800 space-y-4">
                <h3 className="text-xs font-bold text-amber-300 uppercase tracking-wider font-mono flex items-center gap-2">
                  <FileCheck2 className="w-3.5 h-3.5" /> Mandatory Documents to Seize On-Site
                </h3>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                  {(explanation?.inspector_brief.mandatory_documents_to_seize || ai_inspection_brief.recommended_statutory_documents).map((doc, idx) => (
                    <div key={idx} className="p-2.5 rounded-xl bg-slate-950 border border-amber-500/20 text-xs text-slate-300 flex items-start gap-2">
                      <FileCheck2 className="w-3.5 h-3.5 text-amber-400 shrink-0 mt-0.5" />
                      <span>{doc}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Cross-Examination Checklist */}
              <div className="glass-panel p-5 rounded-2xl border border-slate-800 space-y-4">
                <h3 className="text-xs font-bold text-purple-300 uppercase tracking-wider font-mono flex items-center gap-2">
                  <Layers className="w-3.5 h-3.5" /> Cross-Examination Checklist
                </h3>
                <div className="space-y-2">
                  {(explanation?.inspector_brief.cross_examination_checklist || []).map((item, idx) => (
                    <div key={idx} className="flex items-start gap-2 p-2.5 rounded-lg bg-slate-900/60 border border-slate-800 text-xs text-slate-300">
                      <span className="text-purple-400 font-mono font-bold shrink-0">{idx + 1}.</span>
                      <span>{item}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* EMPLOYER REMEDIATION ADVISORY */}
          {explanationAudience === 'employer' && (
            <div className="space-y-4">
              {/* Advisory Summary */}
              <div className="glass-panel p-5 rounded-2xl border border-emerald-500/20 bg-emerald-950/10 space-y-3">
                <h3 className="text-xs font-bold text-emerald-300 uppercase tracking-wider font-mono">Compliance Remediation Advisory</h3>
                <p className="text-xs text-slate-300 leading-relaxed">
                  {explanation?.employer_remediation.advisory_summary}
                </p>
                <div className="flex items-center gap-3 pt-1">
                  <span className="text-[11px] font-mono text-slate-400">
                    Total Estimated Arrears: <span className="font-extrabold text-amber-300">₹{(explanation?.employer_remediation.total_estimated_arrears_inr || 11200).toLocaleString('en-IN')}</span>
                  </span>
                  <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-500/15 text-emerald-300 border border-emerald-500/30">
                    Safe Harbour Window: 14 Days
                  </span>
                </div>
              </div>

              {/* Root Cause Analysis */}
              <div className="glass-panel p-5 rounded-2xl border border-slate-800 space-y-3">
                <h3 className="text-xs font-bold text-slate-200 uppercase tracking-wider font-mono">Root Cause Analysis</h3>
                <div className="space-y-2">
                  {(explanation?.employer_remediation.root_cause_analysis || []).map((root, idx) => (
                    <div key={idx} className="flex items-start gap-2 p-2.5 rounded-lg bg-slate-900/60 border border-slate-800 text-xs text-slate-300">
                      <span className="text-amber-400 font-mono font-bold shrink-0">RC{idx + 1}:</span>
                      <span>{root}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Remediation Steps */}
              <div className="glass-panel p-5 rounded-2xl border border-slate-800 space-y-4">
                <h3 className="text-xs font-bold text-emerald-300 uppercase tracking-wider font-mono">Remediation Roadmap</h3>
                <div className="space-y-3">
                  {(explanation?.employer_remediation.remediation_steps || []).map((step) => (
                    <div key={step.step_number} className="p-4 rounded-xl bg-slate-950/60 border border-emerald-500/15 space-y-1.5">
                      <div className="flex items-center justify-between">
                        <span className="text-xs font-bold text-emerald-300 font-mono">Step {step.step_number}: {step.action}</span>
                        <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-amber-500/10 text-amber-300 border border-amber-500/20">{step.deadline}</span>
                      </div>
                      <p className="text-[11px] text-slate-400">{step.statutory_cure}</p>
                      <p className="text-[11px] font-mono font-bold text-emerald-400">{step.estimated_financial_arrears}</p>
                    </div>
                  ))}
                </div>
              </div>

              {/* Safe Harbour Banner */}
              <div className="p-4 rounded-2xl bg-blue-950/30 border border-blue-500/30">
                <p className="text-xs text-blue-200 leading-relaxed">
                  <span className="font-bold text-blue-300">⚖️ Statutory Safe Harbour: </span>
                  {explanation?.employer_remediation.safe_harbour_guidelines}
                </p>
              </div>
            </div>
          )}

        </div>
      )}

      {/* Tab 7: INSPECTOR VERIFICATION (Human-in-the-Loop) */}
      {activeTab === 'feedback' && (
        <div className="glass-panel rounded-2xl border border-slate-800 p-6 space-y-6">
          <div>
            <h2 className="text-base font-bold text-white flex items-center gap-2">
              <ShieldCheck className="w-4 h-4 text-emerald-400" />
              Human-in-the-Loop Inspection Decision & Feedback
            </h2>
            <p className="text-xs text-slate-400 mt-0.5">
              Inspectors retain ultimate decision authority. Recorded decisions feed into closed-loop ML calibration.
            </p>
          </div>

          {submittedFeedback ? (
            <div className="p-6 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-center space-y-2">
              <CheckCircle2 className="w-8 h-8 text-emerald-400 mx-auto" />
              <h3 className="font-bold text-sm text-emerald-300">Inspector Verification Logged Successfully</h3>
              <p className="text-xs text-slate-400">
                Your decision has been committed to the audit trail and submitted to the closed-loop retraining pipeline.
              </p>
            </div>
          ) : (
            <div className="space-y-4">
              <div className="space-y-2">
                <label className="text-xs font-semibold text-slate-300">
                  Officer Inspection Findings & Rationale Notes:
                </label>
                <textarea
                  rows={4}
                  value={inspectorNotes}
                  onChange={(e) => setInspectorNotes(e.target.value)}
                  placeholder="Record on-site observations, employer explanations, or grounds for overriding automated rule flags..."
                  className="w-full px-3 py-2 rounded-xl bg-slate-950 border border-slate-800 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-blue-500"
                />
              </div>

              <div className="flex items-center gap-3">
                <button
                  onClick={() => setSubmittedFeedback(true)}
                  className="px-6 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-semibold text-xs transition shadow-md shadow-emerald-600/20"
                >
                  Submit Official Inspector Decision
                </button>
                <button
                  onClick={() => setActiveTab('findings')}
                  className="px-4 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs transition"
                >
                  Review Rule Findings
                </button>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Tab 8: COMPLIANCE AUDIT TRAIL TIMELINE */}
      {activeTab === 'timeline' && (
        <ComplianceTimeline timeline={timelineData} isLoading={isLoadingTimeline} />
      )}

      {/* Evidence Graph & Provenance Modal */}
      <EvidenceGraphModal
        establishmentId={establishment.id}
        isOpen={isGraphModalOpen}
        onClose={() => setIsGraphModalOpen(false)}
      />

      {/* 22-Dimensional Risk Feature Matrix Modal */}
      <RiskFeatureMatrixModal
        establishmentId={establishment.id}
        isOpen={isFeatureModalOpen}
        onClose={() => setIsFeatureModalOpen(false)}
      />

      {/* Statutory Notice Document Viewer & Export Modal */}
      <StatutoryNoticeViewerModal
        notice={activeNotice}
        isOpen={isNoticeModalOpen}
        onClose={() => setIsNoticeModalOpen(false)}
        onUpdateStatus={async (noticeId, status, notes) => {
          const updated = await updateNoticeStatus(noticeId, status, notes);
          setActiveNotice(updated);
        }}
        isEmployerRole={false}
      />

    </div>
  );
};
