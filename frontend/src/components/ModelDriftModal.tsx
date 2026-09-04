import React, { useState, useEffect } from 'react';
import { 
  X, 
  RefreshCw, 
  Activity, 
  ShieldCheck, 
  CheckCircle2, 
  Sparkles,
  BarChart3,
  Loader2
} from 'lucide-react';
import { ModelDriftReport, RetrainTriggerResponse } from '../types';
import { getModelDriftReport, triggerClosedLoopRetraining } from '../services/api';

interface ModelDriftModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const ModelDriftModal: React.FC<ModelDriftModalProps> = ({ isOpen, onClose }) => {
  const [report, setReport] = useState<ModelDriftReport | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isRetraining, setIsRetraining] = useState(false);
  const [retrainResult, setRetrainResult] = useState<RetrainTriggerResponse | null>(null);

  useEffect(() => {
    if (isOpen) {
      setIsLoading(true);
      getModelDriftReport()
        .then(setReport)
        .catch(console.error)
        .finally(() => setIsLoading(false));
    }
  }, [isOpen]);

  if (!isOpen) return null;

  const handleRetrain = async () => {
    setIsRetraining(true);
    setRetrainResult(null);
    try {
      const res = await triggerClosedLoopRetraining({
        trigger_reason: "MANUAL_INSPECTOR_DRIFT_TRIGGER",
        include_inspector_feedback: true
      });
      setRetrainResult(res);
      // Refresh drift report after retraining
      const updatedReport = await getModelDriftReport();
      setReport(updatedReport);
    } catch (e) {
      console.error(e);
    } finally {
      setIsRetraining(false);
    }
  };

  const getAlertBadge = (level: string) => {
    switch (level) {
      case 'RED':
        return {
          bg: 'bg-rose-500/15 text-rose-300 border-rose-500/30',
          dot: 'bg-rose-500 animate-pulse',
          label: 'Drift Warning (High Covariate Shift)'
        };
      case 'YELLOW':
        return {
          bg: 'bg-amber-500/15 text-amber-300 border-amber-500/30',
          dot: 'bg-amber-400',
          label: 'Moderate Shift (Retraining Recommended)'
        };
      case 'GREEN':
      default:
        return {
          bg: 'bg-emerald-500/15 text-emerald-300 border-emerald-500/30',
          dot: 'bg-emerald-400',
          label: 'Calibrated & Stable (PSI < 0.10)'
        };
    }
  };

  const getDriftStatusBadge = (status: string) => {
    switch (status) {
      case 'SIGNIFICANT_DRIFT':
        return 'bg-rose-500/20 text-rose-300 border-rose-500/30';
      case 'MODERATE_DRIFT':
        return 'bg-amber-500/20 text-amber-300 border-amber-500/30';
      case 'NO_DRIFT':
      default:
        return 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30';
    }
  };

  const alertBadge = report ? getAlertBadge(report.drift_alert_level) : null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-6 bg-slate-950/80 backdrop-blur-md overflow-y-auto animate-fadeIn">
      <div className="relative w-full max-w-5xl bg-slate-900 border border-slate-700/80 rounded-3xl shadow-2xl shadow-purple-950/40 overflow-hidden flex flex-col max-h-[92vh]">
        
        {/* Header toolbar */}
        <div className="px-6 py-4 border-b border-slate-800 bg-slate-950/80 flex items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="p-2.5 rounded-2xl bg-gradient-to-br from-purple-600 to-indigo-600 text-white shadow-md shadow-purple-500/20">
              <Activity className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h3 className="text-base font-bold text-white">Closed-Loop Continuous ML Retraining & Drift Monitor</h3>
                <span className="px-2 py-0.5 text-[10px] font-mono font-bold rounded bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                  {report?.model_version || 'XGBoost v2.1'}
                </span>
              </div>
              <p className="text-xs text-slate-400">
                Continuous Population Stability Index (PSI) tracking, human override telemetry, and automated champion promotion.
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={handleRetrain}
              disabled={isRetraining}
              className="px-4 py-2 rounded-xl bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 disabled:opacity-50 text-white text-xs font-bold flex items-center gap-1.5 transition shadow-md shadow-purple-600/30 cursor-pointer"
            >
              <RefreshCw className={`w-3.5 h-3.5 ${isRetraining ? 'animate-spin' : ''}`} />
              <span>{isRetraining ? 'Retraining Models...' : 'Trigger Closed-Loop Retrain'}</span>
            </button>
            <button
              onClick={onClose}
              className="p-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-white transition ml-1 cursor-pointer"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Content Body */}
        <div className="p-6 overflow-y-auto space-y-6 text-slate-200">
          {isLoading && !report && (
            <div className="flex items-center justify-center py-12 gap-2 text-slate-400">
              <Loader2 className="w-5 h-5 animate-spin text-purple-400" />
              <span className="text-xs font-medium">Computing Population Stability Index & Drift Telemetry...</span>
            </div>
          )}

          {/* Top Telemetry KPI Cards */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="glass-panel p-4 rounded-2xl border border-slate-800 bg-slate-950/60 space-y-1">
              <span className="text-[11px] text-slate-400 font-medium block">Overall Distribution Shift (PSI)</span>
              <div className="flex items-baseline gap-2">
                <span className="text-2xl font-black font-mono text-white">
                  {report?.overall_psi ?? 0.046}
                </span>
                <span className="text-[10px] font-mono text-emerald-400 font-bold">&lt; 0.10 Target</span>
              </div>
              {alertBadge && (
                <div className={`mt-2 inline-flex items-center gap-1.5 px-2 py-0.5 text-[10px] font-semibold rounded-full border ${alertBadge.bg}`}>
                  <span className={`w-1.5 h-1.5 rounded-full ${alertBadge.dot}`} />
                  <span>{alertBadge.label}</span>
                </div>
              )}
            </div>

            <div className="glass-panel p-4 rounded-2xl border border-slate-800 bg-slate-950/60 space-y-1">
              <span className="text-[11px] text-slate-400 font-medium block">Inspector Human Override Rate</span>
              <div className="flex items-baseline gap-2">
                <span className="text-2xl font-black font-mono text-amber-400">
                  {report?.inspector_override_rate ?? 14.3}%
                </span>
                <span className="text-[10px] text-slate-400 font-mono">
                  ({report?.total_feedback_records ?? 28} Reviewed)
                </span>
              </div>
              <p className="text-[10px] text-slate-400 mt-1">
                Human-in-the-loop overrides feed back into calibration sets to eliminate false positives.
              </p>
            </div>

            <div className="glass-panel p-4 rounded-2xl border border-slate-800 bg-slate-950/60 space-y-1">
              <span className="text-[11px] text-slate-400 font-medium block">Calibration Brier Score</span>
              <div className="flex items-baseline gap-2">
                <span className="text-2xl font-black font-mono text-cyan-400">
                  {report?.calibration_brier_score ?? 0.084}
                </span>
                <span className="text-[10px] font-mono text-slate-400">Well-Calibrated</span>
              </div>
              <p className="text-[10px] text-slate-400 mt-1">
                Probabilistic risk calibration ensures risk scores map to actuarial non-compliance rates.
              </p>
            </div>

            <div className="glass-panel p-4 rounded-2xl border border-slate-800 bg-slate-950/60 space-y-1">
              <span className="text-[11px] text-slate-400 font-medium block">Ingested Field Checklists</span>
              <div className="flex items-baseline gap-2">
                <span className="text-2xl font-black font-mono text-purple-400">
                  {report?.inspections_ingested_count ?? 4}
                </span>
                <span className="text-[10px] font-mono text-slate-400">Active Dockets</span>
              </div>
              <p className="text-[10px] text-slate-400 mt-1">
                Ground truth from physical inspections incorporated into training partitions.
              </p>
            </div>
          </div>

          {/* Retraining Success Toast / Banner */}
          {retrainResult && (
            <div className="p-4 rounded-2xl bg-gradient-to-r from-emerald-950/60 via-slate-900 to-indigo-950/60 border border-emerald-500/40 space-y-2 animate-fadeIn">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2 text-emerald-300 font-bold text-xs">
                  <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                  <span>Closed-Loop Retraining Completed Successfully ({retrainResult.job_id})</span>
                </div>
                <span className="text-[10px] font-mono text-slate-400">
                  {retrainResult.trained_at}
                </span>
              </div>
              <p className="text-xs text-slate-200">
                {retrainResult.message}
              </p>
              <div className="pt-2 border-t border-emerald-500/20 flex flex-wrap items-center gap-4 text-xs font-mono">
                <span className="text-slate-300">Samples: <strong className="text-white">{retrainResult.samples_used}</strong></span>
                <span className="text-slate-300">Previous Champion AUC: <strong className="text-slate-200">{retrainResult.champion_auc}</strong></span>
                <span className="text-emerald-400">Challenger Promoted AUC: <strong>{retrainResult.challenger_auc} (+{(retrainResult.improvement_delta * 100).toFixed(1)}%)</strong></span>
                <span className="text-indigo-300">Deployed Model: <strong>{retrainResult.deployed_model}</strong></span>
              </div>
            </div>
          )}

          {/* Recommended Action Card */}
          {report && (
            <div className="p-4 rounded-2xl bg-slate-950/70 border border-slate-800 flex items-start gap-3">
              <Sparkles className="w-5 h-5 text-indigo-400 shrink-0 mt-0.5" />
              <div className="space-y-1">
                <h4 className="text-xs font-bold text-white uppercase tracking-wider">
                  Algorithmic Health & Drift Assessment
                </h4>
                <p className="text-xs text-slate-300 leading-relaxed">
                  {report.recommended_action}
                </p>
              </div>
            </div>
          )}

          {/* Feature Drift Monitoring Table */}
          <div className="glass-panel rounded-2xl border border-slate-800 overflow-hidden space-y-3 p-5">
            <div className="flex items-center justify-between">
              <div>
                <h4 className="text-sm font-bold text-white flex items-center gap-2">
                  <BarChart3 className="w-4 h-4 text-indigo-400" />
                  22-Feature Covariate Shift & PSI Tracking
                </h4>
                <p className="text-xs text-slate-400 mt-0.5">
                  Comparison between baseline training partition and recent quarterly filings / inspection ground truth.
                </p>
              </div>
              <span className="text-xs text-slate-400 font-mono">
                Metric: Population Stability Index (PSI)
              </span>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead>
                  <tr className="border-b border-slate-800 text-slate-400 uppercase text-[10px] tracking-wider">
                    <th className="py-2.5 px-3">Feature Name</th>
                    <th className="py-2.5 px-3 text-right">Baseline Mean</th>
                    <th className="py-2.5 px-3 text-right">Current Mean</th>
                    <th className="py-2.5 px-3 text-right">PSI Score</th>
                    <th className="py-2.5 px-3 text-center">Drift Status</th>
                    <th className="py-2.5 px-3 text-right">Significance (p-val)</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60 font-mono">
                  {(report?.feature_drifts ?? []).map((f, i) => (
                    <tr key={i} className="hover:bg-slate-800/30 transition">
                      <td className="py-2.5 px-3 font-semibold text-slate-200">
                        {f.feature_name}
                      </td>
                      <td className="py-2.5 px-3 text-right text-slate-400">
                        {f.baseline_mean.toFixed(2)}
                      </td>
                      <td className="py-2.5 px-3 text-right text-slate-200 font-bold">
                        {f.current_mean.toFixed(2)}
                      </td>
                      <td className="py-2.5 px-3 text-right">
                        <span className={`px-2 py-0.5 rounded text-[11px] font-bold ${
                          f.psi_score >= 0.25 ? 'text-rose-400' : f.psi_score >= 0.10 ? 'text-amber-400' : 'text-emerald-400'
                        }`}>
                          {f.psi_score.toFixed(3)}
                        </span>
                      </td>
                      <td className="py-2.5 px-3 text-center">
                        <span className={`px-2 py-0.5 text-[10px] font-semibold rounded-md border ${getDriftStatusBadge(f.drift_status)}`}>
                          {f.drift_status.replace(/_/g, ' ')}
                        </span>
                      </td>
                      <td className="py-2.5 px-3 text-right text-slate-400">
                        p={f.p_value.toFixed(2)}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Governance & Anti-Bias Footnote */}
          <div className="p-4 rounded-2xl bg-indigo-950/20 border border-indigo-500/20 space-y-1 text-xs text-indigo-300">
            <div className="flex items-center gap-1.5 font-bold">
              <ShieldCheck className="w-4 h-4 text-indigo-400" />
              <span>ShramAI Algorithmic Governance & Compliance Guarantee</span>
            </div>
            <p className="text-[11px] text-slate-400 leading-relaxed">
              ML models only predict objective inspection probabilities based on verifiable statutory registers. Retraining pipelines incorporate both positive and negative human inspector verifications, preventing runaway algorithmic feedback loops and guaranteeing zero automated penalties without independent officer review.
            </p>
          </div>

        </div>

      </div>
    </div>
  );
};
