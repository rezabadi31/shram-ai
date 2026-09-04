import React, { useState } from 'react';
import { 
  History, 
  FileText, 
  CheckCircle2, 
  AlertTriangle, 
  Activity, 
  AlertOctagon, 
  Calendar, 
  ShieldAlert, 
  Scale, 
  FileCheck2, 
  ShieldCheck, 
  Filter, 
  ChevronDown, 
  ChevronUp, 
  User, 
  Bot, 
  Cpu, 
  BadgeCheck,
  Building2,
  Clock,
  Sparkles
} from 'lucide-react';
import { EstablishmentTimeline } from '../types';

interface ComplianceTimelineProps {
  timeline: EstablishmentTimeline | null;
  isLoading?: boolean;
}

export const ComplianceTimeline: React.FC<ComplianceTimelineProps> = ({ timeline, isLoading = false }) => {
  const [selectedActor, setSelectedActor] = useState<string>('ALL');
  const [selectedSeverity, setSelectedSeverity] = useState<string>('ALL');
  const [expandedEvents, setExpandedEvents] = useState<Record<string, boolean>>({});

  if (isLoading) {
    return (
      <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-12 text-center backdrop-blur-md">
        <div className="inline-block animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-indigo-500 mb-4"></div>
        <p className="text-slate-400 font-medium">Loading statutory compliance audit trail...</p>
      </div>
    );
  }

  if (!timeline || !timeline.events || timeline.events.length === 0) {
    return (
      <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-12 text-center backdrop-blur-md">
        <History className="w-12 h-12 text-slate-600 mx-auto mb-3" />
        <h4 className="text-lg font-semibold text-slate-300 mb-1">No Audit Trail Events Found</h4>
        <p className="text-sm text-slate-500 max-w-md mx-auto">
          No compliance audit trail has been logged yet for this establishment. Events are generated automatically as filings are processed and inspections conducted.
        </p>
      </div>
    );
  }

  const toggleExpand = (eventId: string) => {
    setExpandedEvents(prev => ({
      ...prev,
      [eventId]: !prev[eventId]
    }));
  };

  const getActorBadge = (actorType: string) => {
    switch (actorType) {
      case 'EMPLOYER':
        return {
          icon: <Building2 className="w-3.5 h-3.5 text-blue-400" />,
          label: 'Employer',
          bg: 'bg-blue-500/10 text-blue-300 border-blue-500/30'
        };
      case 'INSPECTOR':
        return {
          icon: <User className="w-3.5 h-3.5 text-amber-400" />,
          label: 'Labour Inspector',
          bg: 'bg-amber-500/10 text-amber-300 border-amber-500/30'
        };
      case 'ML_ENGINE':
        return {
          icon: <Cpu className="w-3.5 h-3.5 text-cyan-400" />,
          label: 'ML Risk Engine',
          bg: 'bg-cyan-500/10 text-cyan-300 border-cyan-500/30'
        };
      case 'SYSTEM':
      default:
        return {
          icon: <Bot className="w-3.5 h-3.5 text-purple-400" />,
          label: 'System Engine',
          bg: 'bg-purple-500/10 text-purple-300 border-purple-500/30'
        };
    }
  };

  const getSeverityStyle = (severity: string) => {
    switch (severity.toUpperCase()) {
      case 'CRITICAL':
        return {
          border: 'border-rose-500/40 hover:border-rose-500/70',
          badge: 'bg-rose-500/15 text-rose-300 border-rose-500/30',
          dot: 'bg-rose-500 ring-4 ring-rose-500/20',
          iconColor: 'text-rose-400'
        };
      case 'HIGH':
        return {
          border: 'border-orange-500/40 hover:border-orange-500/70',
          badge: 'bg-orange-500/15 text-orange-300 border-orange-500/30',
          dot: 'bg-orange-500 ring-4 ring-orange-500/20',
          iconColor: 'text-orange-400'
        };
      case 'MEDIUM':
        return {
          border: 'border-amber-500/40 hover:border-amber-500/70',
          badge: 'bg-amber-500/15 text-amber-300 border-amber-500/30',
          dot: 'bg-amber-500 ring-4 ring-amber-500/20',
          iconColor: 'text-amber-400'
        };
      case 'LOW':
        return {
          border: 'border-emerald-500/40 hover:border-emerald-500/70',
          badge: 'bg-emerald-500/15 text-emerald-300 border-emerald-500/30',
          dot: 'bg-emerald-500 ring-4 ring-emerald-500/20',
          iconColor: 'text-emerald-400'
        };
      case 'INFO':
      default:
        return {
          border: 'border-sky-500/40 hover:border-sky-500/70',
          badge: 'bg-sky-500/15 text-sky-300 border-sky-500/30',
          dot: 'bg-sky-500 ring-4 ring-sky-500/20',
          iconColor: 'text-sky-400'
        };
    }
  };

  const getEventIcon = (eventType: string) => {
    switch (eventType) {
      case 'DOCUMENT_SUBMITTED':
        return <FileText className="w-5 h-5 text-blue-400" />;
      case 'COMPLIANCE_EVALUATED':
        return <CheckCircle2 className="w-5 h-5 text-indigo-400" />;
      case 'ANOMALY_DETECTED':
        return <AlertTriangle className="w-5 h-5 text-orange-400" />;
      case 'RISK_ASSESSED':
        return <Activity className="w-5 h-5 text-cyan-400" />;
      case 'NOTICE_ISSUED':
        return <AlertOctagon className="w-5 h-5 text-amber-400" />;
      case 'INSPECTION_SCHEDULED':
        return <Calendar className="w-5 h-5 text-yellow-400" />;
      case 'VIOLATION_DETECTED':
        return <ShieldAlert className="w-5 h-5 text-rose-400" />;
      case 'PENALTY_PROPOSED':
        return <Scale className="w-5 h-5 text-rose-500" />;
      case 'REMEDIATION_SUBMITTED':
        return <FileCheck2 className="w-5 h-5 text-emerald-400" />;
      case 'SAFE_HARBOUR_ACHIEVED':
        return <ShieldCheck className="w-5 h-5 text-emerald-300" />;
      default:
        return <History className="w-5 h-5 text-slate-400" />;
    }
  };

  const filteredEvents = timeline.events.filter(evt => {
    const actorMatch = selectedActor === 'ALL' || evt.actor_type === selectedActor;
    const severityMatch = selectedSeverity === 'ALL' || evt.severity.toUpperCase() === selectedSeverity;
    return actorMatch && severityMatch;
  });

  const criticalCount = timeline.events.filter(e => e.severity === 'CRITICAL' || e.severity === 'HIGH').length;
  const safeHarbourAchieved = timeline.events.some(e => e.event_type === 'SAFE_HARBOUR_ACHIEVED');

  return (
    <div className="space-y-6">
      {/* Header Stat Bar */}
      <div className="bg-slate-900/70 border border-slate-800 rounded-2xl p-6 backdrop-blur-md shadow-xl">
        <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <History className="w-5 h-5 text-indigo-400" />
              <h3 className="text-lg font-bold text-white">Statutory Compliance Audit Trail</h3>
              <span className="px-2.5 py-0.5 text-xs font-semibold rounded-full bg-indigo-500/10 text-indigo-300 border border-indigo-500/20">
                Tamper-Evident Chronology
              </span>
            </div>
            <p className="text-xs text-slate-400">
              End-to-end statutory audit log tracking filings, ML assessments, notices, physical inspection findings, and remediation status.
            </p>
          </div>

          <div className="flex flex-wrap items-center gap-3">
            <div className="px-3 py-2 rounded-xl bg-slate-800/80 border border-slate-700/60 text-center">
              <span className="block text-[11px] text-slate-400 font-medium">Total Events</span>
              <span className="text-base font-bold text-white font-mono">{timeline.total_events}</span>
            </div>
            <div className="px-3 py-2 rounded-xl bg-slate-800/80 border border-slate-700/60 text-center">
              <span className="block text-[11px] text-slate-400 font-medium">Audit Window</span>
              <span className="text-xs font-semibold text-slate-300 font-mono">
                {timeline.first_audit_date} → {timeline.last_activity_date}
              </span>
            </div>
            <div className={`px-3 py-2 rounded-xl border text-center ${criticalCount > 0 ? 'bg-rose-500/10 border-rose-500/30' : 'bg-emerald-500/10 border-emerald-500/30'}`}>
              <span className="block text-[11px] text-slate-400 font-medium">High/Critical Flags</span>
              <span className={`text-base font-bold font-mono ${criticalCount > 0 ? 'text-rose-400' : 'text-emerald-400'}`}>
                {criticalCount}
              </span>
            </div>
            {safeHarbourAchieved && (
              <div className="px-3 py-2 rounded-xl bg-emerald-500/15 border border-emerald-500/30 text-center flex items-center gap-1.5">
                <BadgeCheck className="w-4 h-4 text-emerald-400" />
                <span className="text-xs font-bold text-emerald-300">Safe Harbour Active</span>
              </div>
            )}
          </div>
        </div>

        {/* Filter Controls */}
        <div className="mt-6 pt-5 border-t border-slate-800/80 flex flex-wrap items-center justify-between gap-4">
          <div className="flex flex-wrap items-center gap-2">
            <span className="text-xs font-semibold text-slate-400 flex items-center gap-1 mr-1">
              <Filter className="w-3.5 h-3.5" /> Filter Actor:
            </span>
            {['ALL', 'EMPLOYER', 'INSPECTOR', 'SYSTEM', 'ML_ENGINE'].map(actor => (
              <button
                key={actor}
                onClick={() => setSelectedActor(actor)}
                className={`px-2.5 py-1 text-xs font-medium rounded-lg transition-all ${
                  selectedActor === actor
                    ? 'bg-indigo-600 text-white shadow-sm shadow-indigo-600/30'
                    : 'bg-slate-800/80 text-slate-400 hover:text-white hover:bg-slate-700/80'
                }`}
              >
                {actor === 'ALL' ? 'All Actors' : actor.replace('_', ' ')}
              </button>
            ))}
          </div>

          <div className="flex flex-wrap items-center gap-2">
            <span className="text-xs font-semibold text-slate-400 mr-1">Severity:</span>
            {['ALL', 'CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'INFO'].map(sev => (
              <button
                key={sev}
                onClick={() => setSelectedSeverity(sev)}
                className={`px-2 py-0.5 text-xs font-medium rounded-lg transition-all ${
                  selectedSeverity === sev
                    ? 'bg-slate-200 text-slate-900 font-bold'
                    : 'bg-slate-800/80 text-slate-400 hover:text-white'
                }`}
              >
                {sev}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Timeline Stream */}
      <div className="relative pl-6 sm:pl-8 before:absolute before:left-3 sm:before:left-4 before:top-3 before:bottom-3 before:w-0.5 before:bg-gradient-to-b before:from-indigo-500 before:via-purple-500/50 before:to-emerald-500/40 space-y-6">
        {filteredEvents.map((evt, idx) => {
          const actorBadge = getActorBadge(evt.actor_type);
          const sevStyle = getSeverityStyle(evt.severity);
          const isExpanded = !!expandedEvents[evt.event_id];
          const hasMetadata = evt.metadata && Object.keys(evt.metadata).length > 0;

          return (
            <div key={evt.event_id || idx} className="relative group">
              {/* Timeline node icon */}
              <div className={`absolute -left-[27px] sm:-left-[31px] top-4 w-7 h-7 sm:w-8 sm:h-8 rounded-full bg-slate-950 border-2 ${sevStyle.border} flex items-center justify-center shadow-lg transition-transform group-hover:scale-110 z-10`}>
                <span className={`w-2.5 h-2.5 rounded-full ${sevStyle.dot}`}></span>
              </div>

              {/* Event Card */}
              <div className={`bg-slate-900/70 border ${sevStyle.border} rounded-2xl p-5 backdrop-blur-md shadow-lg transition-all hover:shadow-indigo-500/5 hover:bg-slate-900/90`}>
                <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-3 mb-2">
                  <div className="flex items-center gap-2.5">
                    <div className="p-2 rounded-xl bg-slate-800/90 border border-slate-700/60">
                      {getEventIcon(evt.event_type)}
                    </div>
                    <div>
                      <div className="flex flex-wrap items-center gap-2 mb-0.5">
                        <span className={`inline-flex items-center gap-1 px-2.5 py-0.5 text-[11px] font-semibold rounded-full border ${actorBadge.bg}`}>
                          {actorBadge.icon}
                          <span>{actorBadge.label}</span>
                        </span>
                        <span className={`inline-flex items-center px-2 py-0.5 text-[10px] font-bold rounded-md border ${sevStyle.badge}`}>
                          {evt.severity.toUpperCase()}
                        </span>
                        <span className="text-xs font-mono text-slate-500">
                          {evt.event_type.replace(/_/g, ' ')}
                        </span>
                      </div>
                      <h4 className="text-base font-bold text-white group-hover:text-indigo-300 transition-colors">
                        {evt.title}
                      </h4>
                    </div>
                  </div>

                  <div className="flex items-center gap-2 text-right self-start sm:self-auto shrink-0">
                    <div className="text-xs font-mono text-slate-400 flex items-center gap-1.5 bg-slate-800/60 px-2.5 py-1 rounded-lg border border-slate-700/50">
                      <Clock className="w-3.5 h-3.5 text-slate-400" />
                      <span>{evt.date_label}</span>
                    </div>
                  </div>
                </div>

                {/* Event Description */}
                <p className="text-sm text-slate-300 leading-relaxed pl-1 sm:pl-12">
                  {evt.description}
                </p>

                {/* Actor & Metadata Footer */}
                <div className="mt-3.5 pt-3 border-t border-slate-800/80 flex flex-wrap items-center justify-between gap-2 sm:pl-12">
                  <div className="flex items-center gap-2 text-xs text-slate-400">
                    <span className="font-semibold text-slate-500">Actor Entity:</span>
                    <span className="font-medium text-slate-300">{evt.actor}</span>
                  </div>

                  {hasMetadata && (
                    <button
                      onClick={() => toggleExpand(evt.event_id)}
                      className="inline-flex items-center gap-1 text-xs font-medium text-indigo-400 hover:text-indigo-300 transition-colors"
                    >
                      <span>{isExpanded ? 'Hide Statutory Metadata' : 'View Statutory Metadata'}</span>
                      {isExpanded ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
                    </button>
                  )}
                </div>

                {/* Collapsible Metadata Drawer */}
                {hasMetadata && isExpanded && (
                  <div className="mt-3 p-3.5 rounded-xl bg-slate-950/80 border border-slate-800/80 sm:ml-12 animate-fadeIn">
                    <div className="flex items-center gap-1.5 mb-2 text-xs font-bold text-slate-300">
                      <Sparkles className="w-3.5 h-3.5 text-indigo-400" />
                      <span>Event Telemetry & Statutory Payloads:</span>
                    </div>
                    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-2.5">
                      {Object.entries(evt.metadata || {}).map(([key, val]) => (
                        <div key={key} className="p-2 rounded-lg bg-slate-900/90 border border-slate-800">
                          <span className="block text-[10px] font-mono uppercase tracking-wider text-slate-500 mb-0.5">
                            {key.replace(/_/g, ' ')}
                          </span>
                          <span className="text-xs font-semibold text-slate-200 font-mono break-all">
                            {Array.isArray(val) ? val.join(', ') : typeof val === 'object' ? JSON.stringify(val) : String(val)}
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          );
        })}

        {filteredEvents.length === 0 && (
          <div className="p-8 text-center bg-slate-900/40 rounded-xl border border-slate-800">
            <p className="text-sm text-slate-400">No events match the selected actor or severity filters.</p>
          </div>
        )}
      </div>
    </div>
  );
};
