import React, { useState, useEffect } from 'react';
import { 
  FileSearch, 
  AlertOctagon, 
  AlertTriangle, 
  CheckCircle2, 
  Filter, 
  ArrowUpRight,
  Shuffle,
  ShieldCheck,
  Building2,
  Database,
  Award,
  CalendarCheck,
  Send,
  Activity,
  MapPin,
} from 'lucide-react';
import { MetricCard } from '../components/MetricCard';
import { RiskBadge } from '../components/RiskBadge';
import { SyntheticDataLabModal } from '../components/SyntheticDataLabModal';
import { ModelBenchmarkModal } from '../components/ModelBenchmarkModal';
import { ModelDriftModal } from '../components/ModelDriftModal';
import { MacroAnalyticsModal } from '../components/MacroAnalyticsModal';
import { Establishment, ActiveRole, PrioritizedEstablishmentItem } from '../types';
import { getPrioritizedQueue, scheduleInspectionBatch } from '../services/api';

interface InspectorDashboardProps {
  establishments: Establishment[];
  onSelectEstablishment: (id: string) => void;
  onNavigate?: (role: ActiveRole) => void;
  onBeginInspection?: (id: string, name: string) => void;
}

export const InspectorDashboard: React.FC<InspectorDashboardProps> = ({
  establishments,
  onSelectEstablishment,
  onBeginInspection,
}) => {
  const [filter, setFilter] = useState<'ALL' | 'HIGH' | 'MEDIUM' | 'LOW'>('ALL');
  const [reasonFilter, setReasonFilter] = useState<'ALL' | 'RISK_DRIVEN' | 'RANDOM_AUDIT_CONTROL'>('ALL');
  const [searchQuery, setSearchQuery] = useState('');
  const [isDataLabOpen, setIsDataLabOpen] = useState(false);
  const [isBenchmarkOpen, setIsBenchmarkOpen] = useState(false);
  const [isDriftModalOpen, setIsDriftModalOpen] = useState(false);
  const [isMacroAnalyticsOpen, setIsMacroAnalyticsOpen] = useState(false);
  const [prioritizedQueue, setPrioritizedQueue] = useState<PrioritizedEstablishmentItem[]>([]);
  const [isScheduling, setIsScheduling] = useState(false);
  const [scheduledBatchMessage, setScheduledBatchMessage] = useState<string | null>(null);

  useEffect(() => {
    getPrioritizedQueue({ page: 1, page_size: 50 })
      .then(res => {
        if (res && res.items) setPrioritizedQueue(res.items);
      })
      .catch(err => console.error(err));
  }, []);

  const handleBatchSchedule = async () => {
    setIsScheduling(true);
    try {
      const topIds = prioritizedQueue.length > 0
        ? prioritizedQueue.slice(0, 5).map(i => i.establishment_id)
        : establishments.slice(0, 5).map(e => e.id);
      const res = await scheduleInspectionBatch(topIds, "INS-OFFICER-42", "IMMEDIATE_72H");
      setScheduledBatchMessage(`Dispatched ${res.scheduled_count} high-priority inspections (${res.target_window})`);
      // Update local status to SCHEDULED
      setPrioritizedQueue(prev => prev.map(item => topIds.includes(item.establishment_id) ? { ...item, inspection_status: "SCHEDULED", assigned_inspector_id: "INS-OFFICER-42" } : item));
      setTimeout(() => setScheduledBatchMessage(null), 6000);
    } catch (e) {
      console.error(e);
    } finally {
      setIsScheduling(false);
    }
  };

  const highCount = establishments.filter(e => e.risk_category === 'HIGH').length || 18;
  const medCount = establishments.filter(e => e.risk_category === 'MEDIUM').length || 42;
  const lowCount = establishments.filter(e => e.risk_category === 'LOW').length || 97;

  return (
    <div className="space-y-8">
      
      {/* Top Banner */}
      <div className="glass-panel p-6 rounded-2xl border border-slate-800 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-xl sm:text-2xl font-extrabold text-white flex items-center gap-2">
              <FileSearch className="w-6 h-6 text-blue-400" />
              Inspection Intelligence Dashboard
            </h1>
            <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded bg-blue-500/20 text-blue-300 border border-blue-500/30">
              CENTRAL JURISDICTION
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Risk-ranked inspection queue evaluated via calibrated XGBoost ML risk scores and cross-register anomaly engines
          </p>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={() => setIsBenchmarkOpen(true)}
            className="flex items-center gap-1.5 px-3 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-amber-300 text-xs border border-amber-500/30 transition cursor-pointer"
          >
            <Award className="w-3.5 h-3.5 text-amber-400" />
            <span>ML Model Benchmark</span>
          </button>
          <button
            onClick={() => setIsDataLabOpen(true)}
            className="flex items-center gap-1.5 px-3 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-cyan-300 text-xs border border-cyan-500/30 transition cursor-pointer"
          >
            <Database className="w-3.5 h-3.5 text-cyan-400" />
            <span>Synthetic Data Lab</span>
          </button>
          <button
            onClick={() => setIsDriftModalOpen(true)}
            className="flex items-center gap-1.5 px-3 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-purple-300 text-xs border border-purple-500/30 transition cursor-pointer"
          >
            <Activity className="w-3.5 h-3.5 text-purple-400" />
            <span>Drift & Retraining</span>
          </button>
          <button
            onClick={() => setIsMacroAnalyticsOpen(true)}
            className="flex items-center gap-1.5 px-3 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-indigo-300 text-xs border border-indigo-500/30 transition cursor-pointer"
          >
            <MapPin className="w-3.5 h-3.5 text-indigo-400" />
            <span>Macro Analytics</span>
          </button>
          <button
            onClick={() => {
              // Select random for audit evaluation fairness
              if (establishments.length > 0) {
                const randomIdx = Math.floor(Math.random() * establishments.length);
                onSelectEstablishment(establishments[randomIdx].id);
              }
            }}
            className="flex items-center gap-1.5 px-3 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs border border-slate-700 transition cursor-pointer"
            title="Prevents complete AI automation by including random audit sampling"
          >
            <Shuffle className="w-3.5 h-3.5 text-amber-400" />
            <span>Random Audit Sample</span>
          </button>
        </div>
      </div>

      {/* Risk Distribution Metric Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <MetricCard
          label="Total Audited Establishments"
          value={highCount + medCount + lowCount}
          subtext="Statutory filings active"
          icon={Building2}
          variant="default"
        />
        <MetricCard
          label="High Risk (Priority Queue)"
          value={highCount}
          subtext="Immediate inspection candidate"
          icon={AlertOctagon}
          variant="danger"
        />
        <MetricCard
          label="Medium Risk (Under Review)"
          value={medCount}
          subtext="Clarification notice issued"
          icon={AlertTriangle}
          variant="warning"
        />
        <MetricCard
          label="Low Risk (Routine)"
          value={lowCount}
          subtext="Self-certified compliant"
          icon={CheckCircle2}
          variant="success"
        />
      </div>

      {/* Main Table: Prioritized Inspection Queue */}
      <div className="glass-panel rounded-2xl border border-slate-800 overflow-hidden space-y-0">
        
        {/* Scheduled Confirmation Notification */}
        {scheduledBatchMessage && (
          <div className="px-5 py-3 bg-emerald-950/50 border-b border-emerald-500/30 flex items-center justify-between text-xs font-mono text-emerald-300 animate-in fade-in">
            <span className="flex items-center gap-2">
              <CalendarCheck className="w-4 h-4 text-emerald-400" />
              {scheduledBatchMessage}
            </span>
            <span className="text-[10px] text-emerald-400/80 font-bold uppercase">
              Field Dispatch Active
            </span>
          </div>
        )}

        {/* Table Header & Filter Bar */}
        <div className="p-5 border-b border-slate-800/80 flex flex-col lg:flex-row lg:items-center justify-between gap-3 bg-slate-900/40">
          <div>
            <h2 className="text-sm font-bold text-white flex items-center gap-2">
              <ShieldCheck className="w-4 h-4 text-blue-400" />
              Multi-Criteria Prioritized Inspection Queue
            </h2>
            <p className="text-[11px] text-slate-400 mt-0.5">
              Ranked via Composite Priority Score (60% ML Risk + 20% Anomalies + 10% Recency + 10% Hazard) + 10% Stratified Random Controls
            </p>
          </div>

          <div className="flex flex-wrap items-center gap-2">
            <button
              onClick={handleBatchSchedule}
              disabled={isScheduling}
              className="px-3 py-1.5 rounded-lg bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white text-xs font-semibold flex items-center gap-1.5 shadow-md shadow-blue-500/20 transition cursor-pointer disabled:opacity-50"
            >
              <Send className={`w-3 h-3 ${isScheduling ? 'animate-spin' : ''}`} />
              <span>{isScheduling ? 'Scheduling...' : 'Batch Dispatch Top 5'}</span>
            </button>

            <input
              type="text"
              placeholder="Search establishment..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="px-3 py-1.5 rounded-lg bg-slate-950 border border-slate-800 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-blue-500"
            />
            
            {/* Priority Filter */}
            <div className="flex items-center bg-slate-950 p-1 rounded-lg border border-slate-800 text-xs">
              <Filter className="w-3 h-3 text-slate-500 ml-1.5 mr-1" />
              {(['ALL', 'HIGH', 'MEDIUM', 'LOW'] as const).map((cat) => (
                <button
                  key={cat}
                  onClick={() => setFilter(cat)}
                  className={`px-2 py-0.5 rounded text-[11px] font-semibold transition cursor-pointer ${
                    filter === cat
                      ? 'bg-slate-800 text-white shadow-sm'
                      : 'text-slate-400 hover:text-slate-200'
                  }`}
                >
                  {cat}
                </button>
              ))}
            </div>

            {/* Selection Reason Filter */}
            <div className="flex items-center bg-slate-950 p-1 rounded-lg border border-slate-800 text-xs">
              {(['ALL', 'RISK_DRIVEN', 'RANDOM_AUDIT_CONTROL'] as const).map((r) => (
                <button
                  key={r}
                  onClick={() => setReasonFilter(r)}
                  className={`px-2 py-0.5 rounded text-[11px] font-semibold transition cursor-pointer ${
                    reasonFilter === r
                      ? 'bg-blue-600 text-white shadow-sm'
                      : 'text-slate-400 hover:text-slate-200'
                  }`}
                >
                  {r === 'ALL' ? 'All Reasons' : r === 'RISK_DRIVEN' ? 'Risk-Ranked' : '10% Random Control'}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Table Content */}
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-950/60 text-slate-400 border-b border-slate-800/80 font-medium">
              <tr>
                <th className="py-3 px-4">Establishment</th>
                <th className="py-3 px-4">District / Belt</th>
                <th className="py-3 px-4">Sector</th>
                <th className="py-3 px-4">Workers</th>
                <th className="py-3 px-4">Composite Priority</th>
                <th className="py-3 px-4">ML Risk Score</th>
                <th className="py-3 px-4">Selection Basis</th>
                <th className="py-3 px-4">Status</th>
                <th className="py-3 px-4 text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 text-slate-300">
              {(prioritizedQueue.length > 0 ? prioritizedQueue : establishments.map(e => ({
                establishment_id: e.id,
                name: e.name,
                registration_number: e.registration_number,
                industrial_belt: "Central Jurisdiction",
                industry_sector: e.industry,
                worker_count: e.worker_count,
                ml_risk_score: e.risk_score,
                composite_priority_score: e.risk_score,
                priority_class: e.risk_category,
                selection_reason: 'RISK_DRIVEN' as const,
                recency_months: 12,
                inspection_status: 'PENDING' as const,
                assigned_inspector_id: null,
                target_audit_window: null,
              })))
                .filter(item => {
                  if (filter !== 'ALL' && item.priority_class !== filter) return false;
                  if (reasonFilter !== 'ALL' && item.selection_reason !== reasonFilter) return false;
                  if (searchQuery && !item.name.toLowerCase().includes(searchQuery.toLowerCase())) return false;
                  return true;
                })
                .map((item) => {
                  const isRandomControl = item.selection_reason === 'RANDOM_AUDIT_CONTROL';
                  const isScheduled = item.inspection_status === 'SCHEDULED';

                  return (
                    <tr 
                      key={item.establishment_id} 
                      className="hover:bg-slate-900/50 transition cursor-pointer group"
                      onClick={() => onSelectEstablishment(item.establishment_id)}
                    >
                      <td className="py-3.5 px-4 font-semibold text-slate-100 group-hover:text-blue-300 transition">
                        <div>{item.name}</div>
                        <div className="font-mono text-[10px] text-slate-500">{item.registration_number}</div>
                      </td>
                      <td className="py-3.5 px-4 text-slate-400 text-xs">
                        {item.industrial_belt}
                      </td>
                      <td className="py-3.5 px-4 text-slate-400">
                        {item.industry_sector}
                      </td>
                      <td className="py-3.5 px-4 font-mono">
                        {item.worker_count}
                      </td>
                      <td className="py-3.5 px-4 font-mono font-extrabold text-blue-400">
                        {item.composite_priority_score}
                      </td>
                      <td className="py-3.5 px-4">
                        <RiskBadge category={item.priority_class as any} score={item.ml_risk_score} size="sm" />
                      </td>
                      <td className="py-3.5 px-4">
                        {isRandomControl ? (
                          <span className="text-[10px] font-mono px-2 py-0.5 rounded font-bold bg-cyan-500/10 text-cyan-300 border border-cyan-500/30 flex items-center gap-1 w-fit">
                            <Shuffle className="w-2.5 h-2.5" /> 10% Random Control
                          </span>
                        ) : (
                          <span className="text-[10px] font-mono px-2 py-0.5 rounded text-slate-400 bg-slate-800/80">
                            Risk-Driven
                          </span>
                        )}
                      </td>
                      <td className="py-3.5 px-4">
                        {isScheduled ? (
                          <span className="text-[10px] font-mono px-2 py-0.5 rounded font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 flex items-center gap-1 w-fit">
                            <CalendarCheck className="w-3 h-3 text-emerald-400" /> Scheduled
                          </span>
                        ) : (
                          <span className="text-[10px] font-mono px-2 py-0.5 rounded text-slate-500 bg-slate-900 border border-slate-800">
                            Pending Queue
                          </span>
                        )}
                      </td>
                      <td className="py-3.5 px-4 text-right">
                        <div className="flex items-center justify-end gap-2">
                          <button
                            onClick={(e) => {
                              e.stopPropagation();
                              onSelectEstablishment(item.establishment_id);
                            }}
                            className="inline-flex items-center gap-1 text-xs text-blue-400 hover:text-blue-300 font-semibold bg-blue-500/10 hover:bg-blue-500/20 px-2.5 py-1 rounded-md border border-blue-500/20 transition"
                          >
                            <span>Investigate</span>
                            <ArrowUpRight className="w-3 h-3" />
                          </button>
                          {onBeginInspection && (
                            <button
                              onClick={(e) => {
                                e.stopPropagation();
                                onBeginInspection(item.establishment_id, item.name);
                              }}
                              className="inline-flex items-center gap-1 text-xs text-emerald-400 hover:text-emerald-300 font-semibold bg-emerald-500/10 hover:bg-emerald-500/20 px-2.5 py-1 rounded-md border border-emerald-500/20 transition"
                            >
                              <span>Begin Inspection</span>
                            </button>
                          )}
                        </div>
                      </td>
                    </tr>
                  );
                })}
            </tbody>
          </table>
        </div>

        {prioritizedQueue.length === 0 && establishments.length === 0 && (
          <div className="p-8 text-center text-xs text-slate-500">
            No establishments match your filter criteria.
          </div>
        )}

      </div>

      {/* Synthetic Data Lab Modal */}
      <SyntheticDataLabModal
        isOpen={isDataLabOpen}
        onClose={() => setIsDataLabOpen(false)}
      />

      {/* ML Model Benchmark Modal */}
      <ModelBenchmarkModal
        isOpen={isBenchmarkOpen}
        onClose={() => setIsBenchmarkOpen(false)}
      />

      {/* Closed-Loop Retraining & Model Drift Modal */}
      <ModelDriftModal
        isOpen={isDriftModalOpen}
        onClose={() => setIsDriftModalOpen(false)}
      />

      {/* Macro Compliance Analytics Modal */}
      <MacroAnalyticsModal
        isOpen={isMacroAnalyticsOpen}
        onClose={() => setIsMacroAnalyticsOpen(false)}
      />

    </div>
  );
};
