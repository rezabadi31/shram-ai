import React, { useState, useEffect } from 'react';
import { X, Award, RefreshCw, BarChart3, ShieldCheck, Zap } from 'lucide-react';
import { ModelBenchmarkComparison } from '../types';
import { getModelBenchmark, trainModels } from '../services/api';

interface ModelBenchmarkModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const ModelBenchmarkModal: React.FC<ModelBenchmarkModalProps> = ({
  isOpen,
  onClose,
}) => {
  const [benchmark, setBenchmark] = useState<ModelBenchmarkComparison | null>(null);
  const [isTraining, setIsTraining] = useState(false);

  const loadBenchmark = () => {
    getModelBenchmark()
      .then((res) => setBenchmark(res))
      .catch(() => {});
  };

  useEffect(() => {
    if (isOpen) {
      loadBenchmark();
    }
  }, [isOpen]);

  const handleRetrain = async () => {
    setIsTraining(true);
    try {
      const res = await trainModels();
      setBenchmark(res.benchmark || res);
    } catch (e) {
      console.error(e);
    } finally {
      setIsTraining(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-md">
      <div className="relative w-full max-w-5xl rounded-2xl bg-slate-900 border border-slate-800 shadow-2xl flex flex-col max-h-[90vh] overflow-hidden">
        
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-slate-800">
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-xl bg-amber-500/10 text-amber-400 border border-amber-500/20">
              <Award className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-base font-bold text-white flex items-center gap-2">
                ML Risk Model Benchmark: XGBoost vs RF vs Logistic Regression
              </h2>
              <p className="text-xs text-slate-400">
                Rigorous 80/20 train/test evaluation on 1,000+ establishments feature matrix
              </p>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <button
              onClick={handleRetrain}
              disabled={isTraining}
              className="px-3.5 py-1.5 rounded-xl bg-amber-600 hover:bg-amber-500 text-white text-xs font-semibold flex items-center gap-1.5 transition shadow-md shadow-amber-600/20 disabled:opacity-50 cursor-pointer"
            >
              <RefreshCw className={`w-3.5 h-3.5 ${isTraining ? 'animate-spin' : ''}`} />
              <span>{isTraining ? 'Training Models...' : 'Retrain & Benchmark'}</span>
            </button>
            <button
              onClick={onClose}
              className="p-2 rounded-xl text-slate-400 hover:text-white hover:bg-slate-800 transition"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Mandate Callout Banner */}
        <div className="px-6 py-2.5 bg-gradient-to-r from-blue-950/30 to-slate-900 border-b border-blue-500/20 flex items-center justify-between text-xs font-mono">
          <span className="text-blue-300 font-bold flex items-center gap-1.5">
            <ShieldCheck className="w-4 h-4 text-blue-400" />
            Direct Mandate: ML MODEL determines score. LLM explains score.
          </span>
          {benchmark && (
            <span className="text-slate-400 text-[11px]">
              Training: {benchmark.total_training_samples} rows • Testing: {benchmark.total_testing_samples} rows
            </span>
          )}
        </div>

        {/* Content Body */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          
          {/* Active Champion Callout Card */}
          {benchmark && (
            <div className="p-5 rounded-2xl bg-gradient-to-r from-amber-950/30 via-slate-900 to-amber-950/20 border border-amber-500/30 space-y-2">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <div className="p-1.5 rounded-lg bg-amber-500/20 text-amber-300">
                    <Award className="w-4 h-4" />
                  </div>
                  <h3 className="text-sm font-bold text-white">
                    Active Production Champion: {benchmark.champion_model}
                  </h3>
                </div>
                <span className="text-[10px] font-mono px-2.5 py-1 rounded bg-amber-500/20 text-amber-300 border border-amber-500/30 font-bold">
                  ACTIVE CHAMPION
                </span>
              </div>
              <p className="text-xs text-slate-300">
                XGBoost histogram-based gradient tree boosting outperforms Random Forest and regularized Logistic Regression across ROC-AUC, F1 score, and Root Mean Squared Error on holdout compliance test sets.
              </p>
            </div>
          )}

          {/* Benchmark Comparison Table */}
          {benchmark && (
            <div className="space-y-3">
              <h3 className="text-xs font-bold text-slate-200 uppercase tracking-wider font-mono flex items-center gap-1.5">
                <BarChart3 className="w-3.5 h-3.5 text-blue-400" />
                Comparative Model Performance Evaluation
              </h3>

              <div className="overflow-x-auto rounded-xl border border-slate-800">
                <table className="w-full text-left text-xs">
                  <thead className="bg-slate-950 text-slate-400 font-mono text-[11px] uppercase border-b border-slate-800">
                    <tr>
                      <th className="p-3.5">Model / Algorithm</th>
                      <th className="p-3.5">Status</th>
                      <th className="p-3.5">ROC-AUC</th>
                      <th className="p-3.5">Precision</th>
                      <th className="p-3.5">Recall</th>
                      <th className="p-3.5">F1 Score</th>
                      <th className="p-3.5">RMSE</th>
                      <th className="p-3.5">Latency</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-800/80 font-mono">
                    {benchmark.models.map((m) => {
                      const isChampion = m.is_champion;

                      return (
                        <tr
                          key={m.model_name}
                          className={`transition ${
                            isChampion
                              ? 'bg-amber-950/20 hover:bg-amber-950/30'
                              : 'hover:bg-slate-900/40'
                          }`}
                        >
                          <td className="p-3.5">
                            <div className="font-sans font-bold text-slate-100">{m.model_name}</div>
                            <div className="text-[10px] text-slate-500">{m.algorithm}</div>
                          </td>
                          <td className="p-3.5">
                            {isChampion ? (
                              <span className="text-[10px] px-2 py-0.5 rounded font-bold bg-amber-500/20 text-amber-300 border border-amber-500/40 flex items-center gap-1 w-fit">
                                <Award className="w-3 h-3 text-amber-400" /> Champion
                              </span>
                            ) : (
                              <span className="text-[10px] px-2 py-0.5 rounded text-slate-400 bg-slate-800">
                                Benchmark
                              </span>
                            )}
                          </td>
                          <td className="p-3.5 font-bold text-emerald-400">{m.roc_auc.toFixed(3)}</td>
                          <td className="p-3.5 text-slate-200">{(m.precision * 100).toFixed(1)}%</td>
                          <td className="p-3.5 text-slate-200">{(m.recall * 100).toFixed(1)}%</td>
                          <td className="p-3.5 font-bold text-blue-400">{m.f1_score.toFixed(3)}</td>
                          <td className="p-3.5 text-amber-300">{m.rmse.toFixed(2)}</td>
                          <td className="p-3.5 text-slate-400 flex items-center gap-1">
                            <Zap className="w-3 h-3 text-yellow-400" />
                            {m.training_time_ms} ms
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* Technical Insight Box */}
          <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-850 space-y-2 text-xs">
            <h4 className="font-bold text-slate-200 uppercase tracking-wider font-mono text-[11px]">
              Why Tree-Based Ensembles (XGBoost) Dominate Labour Inspection Tabular Data:
            </h4>
            <p className="text-slate-400 leading-relaxed">
              Compliance risk features exhibit non-linear interactions (e.g. hazardous processes only compound risk when paired with high contract labour ratios or absent safety committees). Gradient boosted trees capture these step-function thresholds directly without assuming monotonic linearity, resulting in higher precision when identifying top-decile inspection targets.
            </p>
          </div>

        </div>

      </div>
    </div>
  );
};
