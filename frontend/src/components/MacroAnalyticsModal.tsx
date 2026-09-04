import React, { useState, useEffect } from 'react';
import { 
  X, 
  Building2, 
  TrendingUp, 
  ShieldAlert, 
  MapPin, 
  Sparkles,
  Loader2
} from 'lucide-react';
import { MacroOverviewResponse } from '../types';
import { getMacroAnalyticsOverview } from '../services/api';

interface MacroAnalyticsModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const MacroAnalyticsModal: React.FC<MacroAnalyticsModalProps> = ({ isOpen, onClose }) => {
  const [data, setData] = useState<MacroOverviewResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [selectedJurisdiction, setSelectedJurisdiction] = useState<string | null>(null);

  useEffect(() => {
    if (isOpen) {
      setIsLoading(true);
      getMacroAnalyticsOverview()
        .then(res => {
          setData(res);
          if (res.jurisdictions && res.jurisdictions.length > 0) {
            setSelectedJurisdiction(res.jurisdictions[0].jurisdiction_id);
          }
        })
        .catch(console.error)
        .finally(() => setIsLoading(false));
    }
  }, [isOpen]);

  if (!isOpen) return null;

  const getHazardBadge = (tier: string) => {
    switch (tier) {
      case 'HIGH_HAZARD':
        return 'bg-rose-500/15 text-rose-300 border-rose-500/30';
      case 'MEDIUM_HAZARD':
        return 'bg-amber-500/15 text-amber-300 border-amber-500/30';
      case 'LOW_HAZARD':
      default:
        return 'bg-emerald-500/15 text-emerald-300 border-emerald-500/30';
    }
  };

  const activeJur = data?.jurisdictions.find(j => j.jurisdiction_id === selectedJurisdiction) || data?.jurisdictions[0];

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-6 bg-slate-950/80 backdrop-blur-md overflow-y-auto animate-fadeIn">
      <div className="relative w-full max-w-6xl bg-slate-900 border border-slate-700/80 rounded-3xl shadow-2xl shadow-indigo-950/50 overflow-hidden flex flex-col max-h-[92vh]">
        
        {/* Header toolbar */}
        <div className="px-6 py-4 border-b border-slate-800 bg-slate-950/80 flex items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="p-2.5 rounded-2xl bg-gradient-to-br from-indigo-600 to-blue-600 text-white shadow-md shadow-indigo-500/20">
              <MapPin className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h3 className="text-base font-bold text-white">Macro Compliance Analytics & Multi-District Intelligence</h3>
                <span className="px-2 py-0.5 text-[10px] font-mono font-bold rounded bg-blue-500/20 text-blue-300 border border-blue-500/30">
                  Central Sphere
                </span>
              </div>
              <p className="text-xs text-slate-400">
                Executive dashboard tracking cross-jurisdictional compliance, high-hazard sector risk, and statutory arrears recovery.
              </p>
            </div>
          </div>

          <button
            onClick={onClose}
            className="p-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-white transition cursor-pointer"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content Body */}
        <div className="p-6 overflow-y-auto space-y-6 text-slate-200">
          
          {isLoading && !data && (
            <div className="flex items-center justify-center py-16 gap-2 text-slate-400">
              <Loader2 className="w-5 h-5 animate-spin text-indigo-400" />
              <span className="text-xs font-medium">Aggregating multi-district statutory compliance feeds...</span>
            </div>
          )}

          {data && (
            <>
              {/* National Compliance Index Header Banner */}
              <div className="p-6 rounded-2xl bg-gradient-to-r from-indigo-950/70 via-slate-900 to-blue-950/60 border border-indigo-500/30 flex flex-col lg:flex-row lg:items-center justify-between gap-6 shadow-xl">
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-bold text-indigo-300 uppercase tracking-wider flex items-center gap-1.5">
                      <Sparkles className="w-3.5 h-3.5 text-indigo-400" />
                      Composite National Labour Compliance Index
                    </span>
                    <span className="px-2 py-0.5 text-[10px] font-mono rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 font-bold">
                      +10.7% YTD
                    </span>
                  </div>
                  <div className="flex items-baseline gap-3">
                    <span className="text-4xl font-black font-mono text-white">
                      {data.national_compliance_index}%
                    </span>
                    <span className="text-xs text-slate-400">
                      Grounded across 4 Labour Codes & {data.total_active_establishments.toLocaleString()} Active Units
                    </span>
                  </div>
                  <p className="text-xs text-slate-300 max-w-2xl leading-relaxed">
                    Automated register reconciliation and proactive safe harbour self-cures have driven an 11% increase in statutory compliance without increasing intrusive physical inspection quotas.
                  </p>
                </div>

                <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                  <div className="p-3 rounded-xl bg-slate-950/80 border border-slate-800 text-center">
                    <span className="block text-[10px] text-slate-400 uppercase font-medium">Protected Workforce</span>
                    <span className="text-base font-bold text-white font-mono">{(data.total_registered_workforce / 1000000).toFixed(2)}M</span>
                  </div>
                  <div className="p-3 rounded-xl bg-slate-950/80 border border-slate-800 text-center">
                    <span className="block text-[10px] text-slate-400 uppercase font-medium">Arrears Recovered</span>
                    <span className="text-base font-bold text-emerald-400 font-mono">₹{(data.total_arrears_recovered_inr / 10000000).toFixed(1)} Cr</span>
                  </div>
                  <div className="p-3 rounded-xl bg-slate-950/80 border border-slate-800 text-center">
                    <span className="block text-[10px] text-slate-400 uppercase font-medium">Penalties Assessed</span>
                    <span className="text-base font-bold text-rose-400 font-mono">₹{(data.total_penalties_assessed_inr / 10000000).toFixed(1)} Cr</span>
                  </div>
                  <div className="p-3 rounded-xl bg-slate-950/80 border border-slate-800 text-center">
                    <span className="block text-[10px] text-slate-400 uppercase font-medium">Safe Harbour Units</span>
                    <span className="text-base font-bold text-cyan-400 font-mono">{data.safe_harbour_achieved_count}</span>
                  </div>
                </div>
              </div>

              {/* Multi-District Comparison Section */}
              <div className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-4">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                  <div>
                    <h4 className="text-sm font-bold text-white flex items-center gap-2">
                      <Building2 className="w-4 h-4 text-indigo-400" />
                      Multi-District Central Sphere Breakdown
                    </h4>
                    <p className="text-xs text-slate-400 mt-0.5">
                      Comparative compliance density and high-risk facility quotas across regional industrial clusters.
                    </p>
                  </div>
                  <span className="text-xs font-mono text-slate-400">
                    5 Major Economic Clusters Monitored
                  </span>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                  {/* Left Table: District Listing */}
                  <div className="lg:col-span-2 overflow-x-auto">
                    <table className="w-full text-left text-xs">
                      <thead>
                        <tr className="border-b border-slate-800 text-slate-400 uppercase text-[10px] tracking-wider">
                          <th className="py-2.5 px-3">Jurisdiction Cluster</th>
                          <th className="py-2.5 px-3 text-right">Units</th>
                          <th className="py-2.5 px-3 text-right">Compliance</th>
                          <th className="py-2.5 px-3 text-right">High Risk</th>
                          <th className="py-2.5 px-3 text-right">Arrears Recovered</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-slate-800/60 font-mono">
                        {data.jurisdictions.map((j) => {
                          const isSelected = selectedJurisdiction === j.jurisdiction_id;
                          return (
                            <tr
                              key={j.jurisdiction_id}
                              onClick={() => setSelectedJurisdiction(j.jurisdiction_id)}
                              className={`cursor-pointer transition ${
                                isSelected ? 'bg-indigo-600/20 border-l-2 border-indigo-500' : 'hover:bg-slate-800/40'
                              }`}
                            >
                              <td className="py-3 px-3 font-semibold text-slate-200">
                                <div>{j.jurisdiction_name}</div>
                                <div className="text-[10px] text-slate-500">{j.jurisdiction_id} • {j.sphere}</div>
                              </td>
                              <td className="py-3 px-3 text-right text-slate-300">
                                {j.total_establishments}
                              </td>
                              <td className="py-3 px-3 text-right font-bold text-emerald-400">
                                {j.compliance_rate_pct}%
                              </td>
                              <td className="py-3 px-3 text-right font-bold text-rose-400">
                                {j.high_risk_count}
                              </td>
                              <td className="py-3 px-3 text-right text-slate-200">
                                ₹{(j.arrears_recovered_inr / 100000).toFixed(1)}L
                              </td>
                            </tr>
                          );
                        })}
                      </tbody>
                    </table>
                  </div>

                  {/* Right Card: Focused Cluster Detail */}
                  {activeJur && (
                    <div className="p-5 rounded-2xl bg-slate-950/80 border border-slate-800 space-y-4">
                      <div className="border-b border-slate-800 pb-3">
                        <span className="text-[10px] font-mono text-indigo-400 uppercase font-bold">Selected Jurisdiction</span>
                        <h5 className="text-sm font-bold text-white mt-0.5">{activeJur.jurisdiction_name}</h5>
                      </div>

                      <div className="space-y-2.5 text-xs">
                        <div className="flex justify-between py-1 border-b border-slate-800/80 text-slate-400">
                          <span>Audited Units:</span>
                          <strong className="text-slate-200 font-mono">{activeJur.audited_count} / {activeJur.total_establishments}</strong>
                        </div>
                        <div className="flex justify-between py-1 border-b border-slate-800/80 text-slate-400">
                          <span>Average Risk Score:</span>
                          <strong className="text-amber-400 font-mono">{activeJur.average_risk_score} / 100</strong>
                        </div>
                        <div className="flex justify-between py-1 border-b border-slate-800/80 text-slate-400">
                          <span>Statutory Notices Served:</span>
                          <strong className="text-rose-400 font-mono">{activeJur.notices_issued_count} Notices</strong>
                        </div>
                        <div className="flex justify-between py-1 text-slate-400">
                          <span>Total Arrears Recovered:</span>
                          <strong className="text-emerald-400 font-mono">₹{activeJur.arrears_recovered_inr.toLocaleString('en-IN')}</strong>
                        </div>
                      </div>

                      {/* Visual progress bar */}
                      <div className="space-y-1 pt-2">
                        <div className="flex justify-between text-[11px] text-slate-400">
                          <span>Audit Coverage</span>
                          <span className="font-mono text-slate-200">{((activeJur.audited_count / activeJur.total_establishments) * 100).toFixed(0)}%</span>
                        </div>
                        <div className="w-full h-2 rounded-full bg-slate-800 overflow-hidden">
                          <div 
                            className="h-full bg-indigo-500 rounded-full" 
                            style={{ width: `${(activeJur.audited_count / activeJur.total_establishments) * 100}%` }}
                          />
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              </div>

              {/* High-Hazard Sector Risk Heatmap */}
              <div className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-4">
                <div className="flex items-center justify-between">
                  <div>
                    <h4 className="text-sm font-bold text-white flex items-center gap-2">
                      <ShieldAlert className="w-4 h-4 text-rose-400" />
                      Industrial Sector Hazard & Non-Compliance Matrix
                    </h4>
                    <p className="text-xs text-slate-400 mt-0.5">
                      Actuarial non-compliance rates and primary statutory contravention sections by industry vertical.
                    </p>
                  </div>
                  <span className="text-xs font-mono text-slate-400">
                    Grounded in OSHWC Code 2020 Thresholds
                  </span>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {data.sectors.map((s) => (
                    <div key={s.sector_id} className="p-4 rounded-2xl bg-slate-950/70 border border-slate-800 space-y-2.5 hover:border-slate-700 transition">
                      <div className="flex items-center justify-between">
                        <span className={`px-2 py-0.5 text-[10px] font-bold rounded border ${getHazardBadge(s.hazard_tier)}`}>
                          {s.hazard_tier.replace(/_/g, ' ')}
                        </span>
                        <span className="text-[11px] font-mono text-slate-400">{s.total_units} Units</span>
                      </div>
                      <h5 className="text-xs font-bold text-white">
                        {s.sector_name}
                      </h5>
                      <div className="space-y-1 text-[11px]">
                        <div className="flex justify-between text-slate-400">
                          <span>Non-Compliance Rate:</span>
                          <strong className="text-rose-400 font-mono">{s.non_compliance_rate_pct}%</strong>
                        </div>
                        <div className="flex justify-between text-slate-400">
                          <span>Est. Wage Underpayment:</span>
                          <strong className="text-amber-400 font-mono">₹{(s.estimated_underpayment_inr / 100000).toFixed(1)}L</strong>
                        </div>
                      </div>
                      <div className="pt-2 border-t border-slate-800/80 text-[10px] text-slate-400">
                        <span className="text-slate-500 font-semibold block mb-0.5">Primary Contravention:</span>
                        <span className="text-slate-300 font-mono leading-tight block">{s.top_violation_code}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Monthly Trajectory Chart */}
              <div className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-4">
                <div className="flex items-center justify-between">
                  <div>
                    <h4 className="text-sm font-bold text-white flex items-center gap-2">
                      <TrendingUp className="w-4 h-4 text-emerald-400" />
                      8-Month Longitudinal Compliance & Safe Harbour Trend
                    </h4>
                    <p className="text-xs text-slate-400 mt-0.5">
                      Demonstrates systemic compliance index rise alongside increased automated audits and voluntary remediation.
                    </p>
                  </div>
                  <span className="text-xs font-mono text-emerald-400 font-bold">
                    Index: 72.1% → 82.8%
                  </span>
                </div>

                <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-8 gap-2.5">
                  {data.monthly_trend.map((pt, idx) => (
                    <div key={idx} className="p-3 rounded-xl bg-slate-950/70 border border-slate-800 text-center space-y-1">
                      <span className="text-[11px] font-bold text-slate-400 block">{pt.month}</span>
                      <span className="text-sm font-black font-mono text-emerald-400 block">{pt.compliance_index}%</span>
                      <div className="text-[10px] font-mono text-slate-500 space-y-0.5 pt-1 border-t border-slate-800/60">
                        <div>{pt.audits_completed} Audits</div>
                        <div className="text-cyan-400">+{pt.safe_harbour_achieved} Safe</div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </>
          )}

        </div>

      </div>
    </div>
  );
};
