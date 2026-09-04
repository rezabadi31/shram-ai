import React, { useState, useEffect } from 'react';
import { X, Database, RefreshCw, Layers, ShieldAlert } from 'lucide-react';
import { DatasetSummaryMetrics, EstablishmentRecordSynthetic } from '../types';
import { getDatasetSummary, getDatasetSample, generateSyntheticDataset } from '../services/api';

interface SyntheticDataLabModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const SyntheticDataLabModal: React.FC<SyntheticDataLabModalProps> = ({
  isOpen,
  onClose,
}) => {
  const [summary, setSummary] = useState<DatasetSummaryMetrics | null>(null);
  const [samples, setSamples] = useState<EstablishmentRecordSynthetic[]>([]);
  const [isRegenerating, setIsRegenerating] = useState(false);
  const [activeFilter, setActiveFilter] = useState<string | null>(null);

  const loadData = () => {
    getDatasetSummary().then((res) => setSummary(res)).catch(() => {});
    getDatasetSample(8).then((res) => setSamples(res)).catch(() => {});
  };

  useEffect(() => {
    if (isOpen) {
      loadData();
    }
  }, [isOpen]);

  const handleRegenerate = async () => {
    setIsRegenerating(true);
    try {
      await generateSyntheticDataset(1000);
      loadData();
    } catch (e) {
      console.error(e);
    } finally {
      setIsRegenerating(false);
    }
  };

  if (!isOpen) return null;

  const filteredSamples = activeFilter
    ? samples.filter((s) => s.ground_truth_inspection_priority === activeFilter)
    : samples;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-md">
      <div className="relative w-full max-w-5xl rounded-2xl bg-slate-900 border border-slate-800 shadow-2xl flex flex-col max-h-[90vh] overflow-hidden">
        
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-slate-800">
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-xl bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">
              <Database className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-base font-bold text-white flex items-center gap-2">
                Synthetic Dataset Generator & ML Benchmark Lab
              </h2>
              <p className="text-xs text-slate-400">
                1,000+ statistically calibrated Indian industrial establishments for ML risk modeling & inspection prioritization
              </p>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <button
              onClick={handleRegenerate}
              disabled={isRegenerating}
              className="px-3.5 py-1.5 rounded-xl bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-semibold flex items-center gap-1.5 transition shadow-md shadow-cyan-600/20 disabled:opacity-50 cursor-pointer"
            >
              <RefreshCw className={`w-3.5 h-3.5 ${isRegenerating ? 'animate-spin' : ''}`} />
              <span>{isRegenerating ? 'Synthesizing...' : 'Regenerate Dataset'}</span>
            </button>
            <button
              onClick={onClose}
              className="p-2 rounded-xl text-slate-400 hover:text-white hover:bg-slate-800 transition"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Content Body */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          
          {/* Summary KPI Cards */}
          {summary && (
            <div className="grid grid-cols-2 sm:grid-cols-5 gap-3">
              <div className="p-3.5 rounded-xl bg-slate-950/60 border border-slate-850">
                <span className="text-[10px] text-slate-400 uppercase font-mono block">Establishments</span>
                <span className="text-xl font-extrabold text-white font-mono">{summary.total_establishments.toLocaleString()}</span>
                <span className="text-[10px] text-slate-500 block">Saved in data/</span>
              </div>
              <div className="p-3.5 rounded-xl bg-slate-950/60 border border-slate-850">
                <span className="text-[10px] text-slate-400 uppercase font-mono block">Avg Workforce</span>
                <span className="text-xl font-extrabold text-blue-400 font-mono">{summary.average_worker_count}</span>
                <span className="text-[10px] text-slate-500 block">Log-normal dist.</span>
              </div>
              <div className="p-3.5 rounded-xl bg-slate-950/60 border border-slate-850">
                <span className="text-[10px] text-slate-400 uppercase font-mono block">Avg Risk Score</span>
                <span className="text-xl font-extrabold text-rose-400 font-mono">{summary.average_risk_score}</span>
                <span className="text-[10px] text-slate-500 block">0 - 100 Calibrated</span>
              </div>
              <div className="p-3.5 rounded-xl bg-slate-950/60 border border-slate-850">
                <span className="text-[10px] text-slate-400 uppercase font-mono block">Total Violations</span>
                <span className="text-xl font-extrabold text-amber-400 font-mono">{summary.total_violations_simulated.toLocaleString()}</span>
                <span className="text-[10px] text-slate-500 block">Simulated non-compliances</span>
              </div>
              <div className="p-3.5 rounded-xl bg-slate-950/60 border border-slate-850">
                <span className="text-[10px] text-slate-400 uppercase font-mono block">Ghost Workers</span>
                <span className="text-xl font-extrabold text-purple-400 font-mono">{summary.total_ghost_workers_simulated.toLocaleString()}</span>
                <span className="text-[10px] text-slate-500 block">Cross-doc anomalies</span>
              </div>
            </div>
          )}

          {/* Two-Column Distributions: Sectors & Risk Categories */}
          {summary && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              
              {/* Sector Distribution */}
              <div className="glass-panel p-5 rounded-xl border border-slate-800 space-y-3">
                <h3 className="text-xs font-bold text-slate-200 uppercase tracking-wider font-mono flex items-center gap-1.5">
                  <Layers className="w-3.5 h-3.5 text-blue-400" />
                  Industrial Sector Representation
                </h3>
                <div className="space-y-2.5">
                  {summary.sector_distribution.map((sec) => (
                    <div key={sec.sector} className="space-y-1">
                      <div className="flex justify-between text-xs font-medium text-slate-300">
                        <span className="truncate">{sec.sector}</span>
                        <span className="font-mono text-slate-400">{sec.count} ({sec.percentage}%)</span>
                      </div>
                      <div className="h-1.5 w-full bg-slate-800 rounded-full overflow-hidden">
                        <div
                          className="h-full bg-gradient-to-r from-blue-500 to-indigo-500 rounded-full"
                          style={{ width: `${sec.percentage}%` }}
                        />
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Risk Distribution */}
              <div className="glass-panel p-5 rounded-xl border border-slate-800 space-y-3">
                <h3 className="text-xs font-bold text-slate-200 uppercase tracking-wider font-mono flex items-center gap-1.5">
                  <ShieldAlert className="w-3.5 h-3.5 text-rose-400" />
                  Calibrated Inspection Priority Distribution
                </h3>
                <div className="space-y-3 pt-2">
                  {summary.risk_distribution.map((item) => {
                    const isHigh = item.priority === 'HIGH';
                    const isMed = item.priority === 'MEDIUM';
                    const colorClass = isHigh ? 'bg-rose-500' : isMed ? 'bg-amber-500' : 'bg-emerald-500';
                    const textClass = isHigh ? 'text-rose-400' : isMed ? 'text-amber-400' : 'text-emerald-400';

                    return (
                      <div
                        key={item.priority}
                        onClick={() => setActiveFilter(activeFilter === item.priority ? null : item.priority)}
                        className={`p-3 rounded-xl border cursor-pointer transition ${
                          activeFilter === item.priority
                            ? 'bg-slate-800 border-white/20'
                            : 'bg-slate-950/60 border-slate-850 hover:bg-slate-900/60'
                        }`}
                      >
                        <div className="flex items-center justify-between text-xs font-mono">
                          <span className={`font-bold ${textClass}`}>{item.priority} RISK</span>
                          <span className="text-slate-300">{item.count} establishments ({item.percentage}%)</span>
                        </div>
                        <div className="h-1.5 w-full bg-slate-800 rounded-full overflow-hidden mt-2">
                          <div className={`h-full ${colorClass} rounded-full`} style={{ width: `${item.percentage}%` }} />
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>

            </div>
          )}

          {/* Sample Data Table Preview */}
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <h3 className="text-xs font-bold text-slate-200 uppercase tracking-wider font-mono">
                Synthetic Establishments Dataset Preview {activeFilter && `(Filtered: ${activeFilter})`}:
              </h3>
              <span className="text-[11px] text-slate-500 font-mono">
                Showing {filteredSamples.length} sampled records
              </span>
            </div>

            <div className="overflow-x-auto rounded-xl border border-slate-800">
              <table className="w-full text-left text-xs">
                <thead className="bg-slate-950 text-slate-400 font-mono text-[11px] uppercase border-b border-slate-800">
                  <tr>
                    <th className="p-3">ID</th>
                    <th className="p-3">Establishment Name</th>
                    <th className="p-3">Sector</th>
                    <th className="p-3">State & District</th>
                    <th className="p-3">Workforce</th>
                    <th className="p-3">Contract %</th>
                    <th className="p-3">Violations</th>
                    <th className="p-3">Risk Score</th>
                    <th className="p-3">Priority</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/80">
                  {filteredSamples.map((r) => (
                    <tr key={r.establishment_id} className="hover:bg-slate-900/40 transition">
                      <td className="p-3 font-mono font-bold text-blue-400">{r.establishment_id}</td>
                      <td className="p-3 text-slate-200 font-medium">{r.name}</td>
                      <td className="p-3 text-slate-400 text-[11px]">{r.industry_sector}</td>
                      <td className="p-3 text-slate-400 font-mono text-[11px]">{r.district}, {r.state}</td>
                      <td className="p-3 font-mono text-slate-200">{r.worker_count}</td>
                      <td className="p-3 font-mono text-slate-300">{Math.round(r.contract_worker_ratio * 100)}%</td>
                      <td className="p-3 font-mono text-amber-400">
                        {r.wage_violation_count + r.ot_violation_count + r.missing_register_count}
                      </td>
                      <td className="p-3 font-mono font-bold text-rose-400">{r.ground_truth_risk_score}</td>
                      <td className="p-3">
                        <span className={`text-[10px] font-mono px-2 py-0.5 rounded font-bold border ${
                          r.ground_truth_inspection_priority === 'HIGH'
                            ? 'bg-rose-500/10 text-rose-400 border-rose-500/30'
                            : r.ground_truth_inspection_priority === 'MEDIUM'
                            ? 'bg-amber-500/10 text-amber-400 border-amber-500/30'
                            : 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30'
                        }`}>
                          {r.ground_truth_inspection_priority}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

        </div>

      </div>
    </div>
  );
};
