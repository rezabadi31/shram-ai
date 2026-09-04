import React, { useState, useEffect } from 'react';
import { X, GitCommit, FileText, AlertTriangle, Scale, Building2, CheckCircle2, ArrowRight, Layers, Sparkles } from 'lucide-react';
import { EvidenceGraphResponse, EvidenceGraphNode, ProvenancePathResponse } from '../types';
import { getEstablishmentEvidenceGraph, getProvenancePath } from '../services/api';

interface EvidenceGraphModalProps {
  establishmentId: string;
  isOpen: boolean;
  onClose: () => void;
}

export const EvidenceGraphModal: React.FC<EvidenceGraphModalProps> = ({
  establishmentId,
  isOpen,
  onClose,
}) => {
  const [graphData, setGraphData] = useState<EvidenceGraphResponse | null>(null);
  const [selectedNode, setSelectedNode] = useState<EvidenceGraphNode | null>(null);
  const [provenance, setProvenance] = useState<ProvenancePathResponse | null>(null);

  useEffect(() => {
    if (isOpen) {
      getEstablishmentEvidenceGraph(establishmentId).then((res) => {
        setGraphData(res);
        if (res.nodes.length > 0) {
          const defaultTarget = res.nodes.find((n: EvidenceGraphNode) => n.tier === 4) || res.nodes[0];
          setSelectedNode(defaultTarget);
        }
      }).catch(() => {});
    }
  }, [isOpen, establishmentId]);

  useEffect(() => {
    if (selectedNode) {
      getProvenancePath(establishmentId, selectedNode.id).then((res) => {
        setProvenance(res);
      }).catch(() => {});
    }
  }, [selectedNode, establishmentId]);

  if (!isOpen) return null;

  const getTierColor = (tier: number) => {
    switch (tier) {
      case 1: return 'border-amber-500/50 bg-amber-500/10 text-amber-300';
      case 2: return 'border-blue-500/50 bg-blue-500/10 text-blue-300';
      case 3: return 'border-emerald-500/50 bg-emerald-500/10 text-emerald-300';
      case 4: return 'border-rose-500/50 bg-rose-500/10 text-rose-300';
      case 5: return 'border-purple-500/50 bg-purple-500/10 text-purple-300';
      default: return 'border-slate-700 bg-slate-800 text-slate-300';
    }
  };

  const getTierIcon = (tier: number) => {
    switch (tier) {
      case 1: return Building2;
      case 2: return FileText;
      case 3: return GitCommit;
      case 4: return AlertTriangle;
      case 5: return Scale;
      default: return Layers;
    }
  };

  const tiers = [
    { tier: 1, title: 'Tier 1: Establishment Root' },
    { tier: 2, title: 'Tier 2: Audited Documents' },
    { tier: 3, title: 'Tier 3: Canonical Worker Records' },
    { tier: 4, title: 'Tier 4: Violations & Anomalies' },
    { tier: 5, title: 'Tier 5: Statutory Citations' },
  ];

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-md">
      <div className="relative w-full max-w-5xl rounded-2xl bg-slate-900 border border-slate-800 shadow-2xl flex flex-col max-h-[90vh] overflow-hidden">
        
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-slate-800">
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-xl bg-purple-500/10 text-purple-400 border border-purple-500/20">
              <Layers className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-base font-bold text-white flex items-center gap-2">
                Evidence Graph & Lineage Provenance Explorer
              </h2>
              <p className="text-xs text-slate-400">
                End-to-end mathematical & legal lineage connecting raw documents to statutory violations
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-2 rounded-xl text-slate-400 hover:text-white hover:bg-slate-800 transition"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Provenance Path Breadcrumb */}
        {provenance && (
          <div className="px-6 py-3 bg-purple-950/20 border-b border-purple-500/20 flex items-center gap-2 overflow-x-auto text-xs font-mono">
            <span className="text-purple-300 font-bold uppercase tracking-wider text-[10px] flex items-center gap-1">
              <Sparkles className="w-3 h-3 text-purple-400" /> Active Provenance Lineage:
            </span>
            <div className="flex items-center gap-1.5 text-slate-300">
              {provenance.path_node_ids.map((nid, idx) => {
                const node = graphData?.nodes.find((n) => n.id === nid);
                const isSelected = selectedNode?.id === nid;
                return (
                  <React.Fragment key={nid}>
                    {idx > 0 && <ArrowRight className="w-3 h-3 text-purple-400 flex-shrink-0" />}
                    <span
                      onClick={() => node && setSelectedNode(node)}
                      className={`px-2 py-0.5 rounded cursor-pointer transition ${
                        isSelected
                          ? 'bg-purple-500 text-white font-bold'
                          : 'bg-slate-800/80 text-slate-300 hover:bg-slate-700'
                      }`}
                    >
                      {node?.label.split(':')[0] || nid}
                    </span>
                  </React.Fragment>
                );
              })}
            </div>
          </div>
        )}

        {/* Content Body: 5-Tier Columns + Inspector Drawer */}
        <div className="flex-1 overflow-y-auto p-6 grid grid-cols-1 lg:grid-cols-3 gap-6">
          
          {/* 5-Tier Graph Columns (Spans 2 cols) */}
          <div className="lg:col-span-2 space-y-4">
            {tiers.map((t) => {
              const tierNodes = (graphData?.nodes || []).filter((n) => n.tier === t.tier);
              const Icon = getTierIcon(t.tier);

              return (
                <div key={t.tier} className="p-3.5 rounded-xl bg-slate-950/60 border border-slate-850 space-y-2">
                  <div className="flex items-center justify-between text-xs font-mono">
                    <span className="text-slate-400 font-bold flex items-center gap-1.5">
                      <Icon className="w-3.5 h-3.5 text-slate-500" />
                      {t.title}
                    </span>
                    <span className="text-[10px] text-slate-500 font-mono">
                      {tierNodes.length} Nodes
                    </span>
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                    {tierNodes.map((node) => {
                      const isSelected = selectedNode?.id === node.id;
                      const isInProvenance = provenance?.path_node_ids.includes(node.id);

                      return (
                        <div
                          key={node.id}
                          onClick={() => setSelectedNode(node)}
                          className={`p-2.5 rounded-xl border text-xs cursor-pointer transition flex flex-col justify-between space-y-1.5 ${
                            isSelected
                              ? 'ring-2 ring-purple-400 border-transparent shadow-lg bg-slate-800 text-white'
                              : isInProvenance
                              ? `${getTierColor(node.tier)} border-opacity-100`
                              : `${getTierColor(node.tier)} opacity-75 hover:opacity-100`
                          }`}
                        >
                          <div className="flex items-center justify-between">
                            <span className="font-mono text-[10px] uppercase font-bold tracking-wider">
                              {node.id}
                            </span>
                            {isInProvenance && (
                              <CheckCircle2 className="w-3 h-3 text-purple-400" />
                            )}
                          </div>
                          <p className="text-xs font-medium truncate">{node.label}</p>
                        </div>
                      );
                    })}
                  </div>
                </div>
              );
            })}
          </div>

          {/* Node Inspector Drawer */}
          <div className="glass-panel p-5 rounded-xl border border-slate-800 space-y-4 flex flex-col justify-between">
            <div className="space-y-3">
              <h3 className="text-xs font-bold text-slate-200 uppercase tracking-wider font-mono flex items-center gap-1.5">
                <Layers className="w-3.5 h-3.5 text-blue-400" />
                Evidence Node Inspector
              </h3>

              {selectedNode ? (
                <div className="space-y-3 text-xs">
                  <div className="p-3 rounded-lg bg-slate-950 border border-slate-800 space-y-1">
                    <span className="text-[10px] text-slate-500 font-mono uppercase block">Node Label</span>
                    <span className="text-slate-100 font-semibold">{selectedNode.label}</span>
                  </div>

                  <div className="grid grid-cols-2 gap-2 font-mono text-[11px]">
                    <div className="p-2 rounded bg-slate-950 border border-slate-800">
                      <span className="text-slate-500 block">ID:</span>
                      <strong className="text-slate-200">{selectedNode.id}</strong>
                    </div>
                    <div className="p-2 rounded bg-slate-950 border border-slate-800">
                      <span className="text-slate-500 block">Tier:</span>
                      <strong className="text-purple-400">Tier {selectedNode.tier}</strong>
                    </div>
                  </div>

                  {/* Properties */}
                  <div className="p-3 rounded-lg bg-slate-950 border border-slate-800 space-y-2">
                    <span className="text-[10px] text-slate-500 font-mono uppercase block">
                      Node Properties & Provenance Payload
                    </span>
                    <div className="space-y-1 font-mono text-[11px]">
                      {Object.entries(selectedNode.properties).map(([k, v]) => (
                        <div key={k} className="flex justify-between text-slate-400">
                          <span className="capitalize">{k.replace('_', ' ')}:</span>
                          <strong className="text-slate-200">{String(v)}</strong>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Connected Edges */}
                  <div className="p-3 rounded-lg bg-slate-950 border border-slate-800 space-y-1.5">
                    <span className="text-[10px] text-slate-500 font-mono uppercase block">Connected Graph Edges</span>
                    <div className="space-y-1 text-[11px] font-mono text-slate-400">
                      {(graphData?.edges || [])
                        .filter((e) => e.source === selectedNode.id || e.target === selectedNode.id)
                        .map((e, idx) => (
                          <div key={idx} className="flex items-center gap-1.5">
                            <span className="text-purple-400">{e.source}</span>
                            <ArrowRight className="w-2.5 h-2.5 text-slate-500" />
                            <span className="text-blue-400">{e.target}</span>
                            <span className="text-[10px] text-slate-500">({e.label})</span>
                          </div>
                        ))}
                    </div>
                  </div>

                </div>
              ) : (
                <div className="text-xs text-slate-500 italic py-8 text-center">
                  Select a node from any tier to inspect its mathematical & legal provenance.
                </div>
              )}
            </div>

            <button
              onClick={onClose}
              className="w-full py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-white font-semibold text-xs transition"
            >
              Close Explorer
            </button>
          </div>

        </div>

      </div>
    </div>
  );
};
