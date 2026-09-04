import React, { useState, useEffect } from 'react';
import { X, Binary } from 'lucide-react';
import { FeatureExtractionResponse, FeatureCategory } from '../types';
import { extractEstablishmentFeatures } from '../services/api';

interface RiskFeatureMatrixModalProps {
  establishmentId: string;
  isOpen: boolean;
  onClose: () => void;
}

export const RiskFeatureMatrixModal: React.FC<RiskFeatureMatrixModalProps> = ({
  establishmentId,
  isOpen,
  onClose,
}) => {
  const [data, setData] = useState<FeatureExtractionResponse | null>(null);
  const [selectedCategory, setSelectedCategory] = useState<FeatureCategory | 'ALL'>('ALL');

  useEffect(() => {
    if (isOpen) {
      extractEstablishmentFeatures(establishmentId)
        .then((res) => setData(res))
        .catch(() => {});
    }
  }, [isOpen, establishmentId]);

  if (!isOpen) return null;

  const categories: { id: FeatureCategory | 'ALL'; label: string; color: string }[] = [
    { id: 'ALL', label: 'All 22 Features', color: 'text-slate-200' },
    { id: 'DEMOGRAPHIC', label: 'Demographic & Structural', color: 'text-blue-400' },
    { id: 'DETERMINISTIC', label: 'Deterministic Violations', color: 'text-amber-400' },
    { id: 'ANOMALY', label: 'Cross-Register Anomalies', color: 'text-rose-400' },
    { id: 'HISTORICAL', label: 'Historical Enforcement', color: 'text-indigo-400' },
    { id: 'INTERACTION', label: 'Risk Interactions', color: 'text-purple-400' },
  ];

  const features = data?.features || [];
  const filteredFeatures = selectedCategory === 'ALL'
    ? features
    : features.filter((f) => f.category === selectedCategory);

  const getCategoryBadgeClass = (cat: FeatureCategory) => {
    switch (cat) {
      case 'DEMOGRAPHIC': return 'bg-blue-500/10 text-blue-300 border-blue-500/30';
      case 'DETERMINISTIC': return 'bg-amber-500/10 text-amber-300 border-amber-500/30';
      case 'ANOMALY': return 'bg-rose-500/10 text-rose-300 border-rose-500/30';
      case 'HISTORICAL': return 'bg-indigo-500/10 text-indigo-300 border-indigo-500/30';
      case 'INTERACTION': return 'bg-purple-500/10 text-purple-300 border-purple-500/30';
      default: return 'bg-slate-800 text-slate-300 border-slate-700';
    }
  };

  const getBarColorClass = (cat: FeatureCategory) => {
    switch (cat) {
      case 'DEMOGRAPHIC': return 'bg-blue-500';
      case 'DETERMINISTIC': return 'bg-amber-500';
      case 'ANOMALY': return 'bg-rose-500';
      case 'HISTORICAL': return 'bg-indigo-500';
      case 'INTERACTION': return 'bg-purple-500';
      default: return 'bg-slate-400';
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-md">
      <div className="relative w-full max-w-5xl rounded-2xl bg-slate-900 border border-slate-800 shadow-2xl flex flex-col max-h-[90vh] overflow-hidden">
        
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-slate-800">
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-xl bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
              <Binary className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-base font-bold text-white flex items-center gap-2">
                22-Dimensional Risk Feature Vector Matrix
              </h2>
              <p className="text-xs text-slate-400">
                Engineered feature inputs feeding XGBoost / Random Forest risk models and SHAP explainability
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

        {/* Category Tabs Filter */}
        <div className="px-6 py-3 bg-slate-950/60 border-b border-slate-800 flex items-center gap-2 overflow-x-auto text-xs font-mono">
          {categories.map((c) => (
            <button
              key={c.id}
              onClick={() => setSelectedCategory(c.id)}
              className={`px-3 py-1.5 rounded-lg border whitespace-nowrap transition cursor-pointer ${
                selectedCategory === c.id
                  ? 'bg-slate-800 border-white/20 text-white font-bold shadow'
                  : 'bg-slate-950 border-slate-800 text-slate-400 hover:text-slate-200'
              }`}
            >
              {c.label}
            </button>
          ))}
        </div>

        {/* Content Body */}
        <div className="flex-1 overflow-y-auto p-6 space-y-3">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {filteredFeatures.map((feat) => {
              const pct = Math.round(feat.normalized_value * 100);

              return (
                <div
                  key={feat.name}
                  className="p-4 rounded-xl bg-slate-950/60 border border-slate-850 hover:border-slate-750 transition space-y-2.5"
                >
                  <div className="flex items-start justify-between gap-2">
                    <div className="space-y-0.5">
                      <span className={`text-[9px] font-mono font-bold px-2 py-0.5 rounded border ${getCategoryBadgeClass(feat.category)}`}>
                        {feat.category}
                      </span>
                      <h4 className="text-xs font-bold text-slate-100 pt-1">{feat.label}</h4>
                      <p className="text-[10px] text-slate-400 font-mono">{feat.name}</p>
                    </div>
                    <div className="text-right font-mono">
                      <span className="text-sm font-extrabold text-white">{feat.raw_value}</span>
                      <span className="text-[10px] text-slate-500 block">Raw Value</span>
                    </div>
                  </div>

                  {/* Formula and Progress Bar */}
                  <div className="space-y-1.5 pt-1">
                    <div className="flex items-center justify-between text-[10px] font-mono text-slate-400">
                      <span className="text-slate-500 truncate max-w-[200px]">f: {feat.formula}</span>
                      <span className="text-slate-300 font-semibold">{pct}% Normalized</span>
                    </div>
                    <div className="h-1.5 w-full bg-slate-800 rounded-full overflow-hidden">
                      <div
                        className={`h-full ${getBarColorClass(feat.category)} rounded-full`}
                        style={{ width: `${Math.max(4, pct)}%` }}
                      />
                    </div>
                  </div>

                </div>
              );
            })}
          </div>
        </div>

        {/* Footer */}
        <div className="px-6 py-3 bg-slate-950 border-t border-slate-800 flex items-center justify-between text-xs font-mono text-slate-400">
          <span>Vector Length: {features.length} Features Loaded</span>
          <button
            onClick={onClose}
            className="px-4 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-white font-semibold transition"
          >
            Close Matrix
          </button>
        </div>

      </div>
    </div>
  );
};
