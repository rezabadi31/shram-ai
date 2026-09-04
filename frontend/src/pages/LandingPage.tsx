import React, { useState } from 'react';
import { 
  Building2,
  FileSearch,
  ArrowRight,
  Scale,
  BookOpen,
  X,
  FileText,
  Cpu,
  ShieldCheck,
  TrendingUp,
  AlertTriangle
} from 'lucide-react';
import { SystemHealth } from '../types';
import { fetchCodeDetails } from '../services/api';

interface LandingPageProps {
  onOpenLogin: (role: 'employer' | 'inspector') => void;
  health?: SystemHealth | null;
}

export const LandingPage: React.FC<LandingPageProps> = ({ onOpenLogin }) => {
  const [selectedCodeDetails, setSelectedCodeDetails] = useState<any | null>(null);

  const handleOpenCode = async (codeId: string) => {
    try {
      const details = await fetchCodeDetails(codeId);
      setSelectedCodeDetails(details);
    } catch (e) {
      console.error(e);
    }
  };

  const intelligenceSteps = [
    { title: "Documents", desc: "Statutory Registers & Payroll", icon: FileText, color: "text-blue-400" },
    { title: "AI Analysis", desc: "OCR Extraction & Schema Normalization", icon: Cpu, color: "text-cyan-400" },
    { title: "Compliance", desc: "Deterministic Rule Validation & RAG", icon: Scale, color: "text-indigo-400" },
    { title: "Risk", desc: "Calibrated XGBoost & SHAP Attribution", icon: TrendingUp, color: "text-amber-400" },
    { title: "Inspection Intelligence", desc: "Prioritized Queue & On-Site Docket", icon: ShieldCheck, color: "text-emerald-400" },
  ];

  const labourCodes = [
    { code_id: "wages_2019", name: "Code on Wages, 2019", act: "Act No. 29 of 2019", key_areas: "Floor Wage, Universal Minimum Wage, Double Overtime, 50% Deduction Ceiling, Form A/B Registers", authority: "Chief Labour Commissioner (Central)" },
    { code_id: "ir_2020", name: "Industrial Relations Code, 2020", act: "Act No. 35 of 2020", key_areas: "Trade Union Recognition, Standing Orders (300+ Threshold), Works Committee, Retrenchment", authority: "Industrial Tribunals / Conciliation Officers" },
    { code_id: "ss_2020", name: "Code on Social Security, 2020", act: "Act No. 36 of 2020", key_areas: "EPFO (20+), ESIC (10+), Gratuity (Fixed-Term Pro-Rata), 26-Wk Maternity, Gig Worker Welfare", authority: "EPFO / ESIC Regional Commissioners" },
    { code_id: "oshwc_2020", name: "OSH & Working Conditions Code, 2020", act: "Act No. 37 of 2020", key_areas: "Factory Threshold (20/40), Safety Committee (250+), 8 Hr Daily Limit, Health Checkups", authority: "Directorate General Factory Advice (DGFASLI)" }
  ];

  return (
    <div className="space-y-12">
      
      {/* Hero Section */}
      <section className="relative overflow-hidden rounded-3xl border border-slate-800/80 bg-gradient-to-b from-slate-900 via-slate-950 to-slate-950 p-8 sm:p-14 shadow-2xl">
        <div className="absolute -top-24 -right-24 w-96 h-96 rounded-full bg-blue-600/10 blur-3xl pointer-events-none" />
        <div className="absolute -bottom-24 -left-24 w-96 h-96 rounded-full bg-cyan-600/10 blur-3xl pointer-events-none" />

        <div className="max-w-3xl space-y-6 relative z-10">
          <div className="space-y-2">
            <h1 className="text-4xl sm:text-6xl font-extrabold tracking-tight text-white leading-tight">
              ShramAI
            </h1>
            <p className="text-lg sm:text-2xl font-semibold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 via-cyan-300 to-indigo-300">
              AI-Powered Labour Compliance & Inspection Intelligence
            </p>
          </div>

          <p className="text-sm sm:text-base text-slate-300 leading-relaxed max-w-2xl">
            Transform labour documents into evidence-backed compliance insights, risk intelligence, and inspection priorities.
          </p>

          {/* Primary Role Authentication Buttons */}
          <div className="pt-3 flex flex-wrap items-center gap-4">
            <button
              onClick={() => onOpenLogin('employer')}
              className="flex items-center gap-2.5 px-6 py-3.5 rounded-xl bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-400 hover:to-amber-500 text-slate-950 font-bold text-sm shadow-lg shadow-amber-500/20 transition cursor-pointer"
            >
              <Building2 className="w-4 h-4" />
              <span>Employer Login</span>
              <ArrowRight className="w-4 h-4" />
            </button>

            <button
              onClick={() => onOpenLogin('inspector')}
              className="flex items-center gap-2.5 px-6 py-3.5 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white font-bold text-sm shadow-lg shadow-blue-500/25 transition cursor-pointer"
            >
              <FileSearch className="w-4 h-4" />
              <span>Inspector Login</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      </section>

      {/* Intelligence Flow Visual Representation */}
      <section className="glass-panel p-6 sm:p-8 rounded-2xl border border-slate-800/80">
        <div className="mb-6">
          <h2 className="text-xs uppercase font-mono font-bold tracking-wider text-slate-400">
            Intelligence Flow
          </h2>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3 relative">
          {intelligenceSteps.map((step, idx) => {
            const Icon = step.icon;
            return (
              <div 
                key={idx} 
                className="bg-slate-900/90 p-4 rounded-xl border border-slate-800/80 flex flex-col justify-between relative group hover:border-slate-700 transition"
              >
                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-[10px] font-mono font-bold text-slate-500">0{idx + 1}</span>
                    <Icon className={`w-4 h-4 ${step.color}`} />
                  </div>
                  <h3 className="font-semibold text-sm text-slate-100 group-hover:text-white transition">
                    {step.title}
                  </h3>
                </div>
                <p className="text-[11px] text-slate-400 mt-2 leading-relaxed">
                  {step.desc}
                </p>
              </div>
            );
          })}
        </div>
      </section>

      {/* Ground Truth: The Four Labour Codes Foundation */}
      <section className="space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-base font-bold text-slate-100 flex items-center gap-2">
              <Scale className="w-4 h-4 text-cyan-400" />
              The Four Labour Codes of India
            </h2>
            <p className="text-xs text-slate-400">
              Deterministic statutory rule validation and semantic grounding based on enacted Indian labour legislation
            </p>
          </div>
          <span className="text-xs font-mono text-slate-400 bg-slate-900 px-2.5 py-1 rounded border border-slate-800">
            Statutory Framework
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {labourCodes.map((code, idx) => (
            <div 
              key={idx} 
              onClick={() => handleOpenCode(code.code_id)}
              className="glass-panel p-5 rounded-2xl border border-slate-800 hover:border-cyan-500/50 hover:bg-slate-900/80 transition flex flex-col justify-between cursor-pointer group shadow-lg"
            >
              <div className="space-y-2.5">
                <div className="flex items-center justify-between">
                  <span className="text-[10px] font-mono font-bold text-cyan-400 bg-cyan-500/10 px-2 py-0.5 rounded border border-cyan-500/20">
                    {code.act}
                  </span>
                  <BookOpen className="w-3.5 h-3.5 text-slate-500 group-hover:text-cyan-400 transition" />
                </div>
                <h3 className="font-bold text-sm text-slate-100 group-hover:text-cyan-300 transition">{code.name}</h3>
                <p className="text-xs text-slate-400 leading-relaxed">{code.key_areas}</p>
              </div>
              <div className="mt-4 pt-3 border-t border-slate-800/80 flex items-center justify-between text-[11px] text-slate-400 font-medium group-hover:text-cyan-300">
                <span>Statutory Details</span>
                <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-1 transition" />
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Statutory Code Explorer Modal */}
      {selectedCodeDetails && (
        <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-md flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-3xl w-full max-w-4xl max-h-[85vh] flex flex-col shadow-2xl overflow-hidden">
            
            <div className="p-5 border-b border-slate-800 flex items-center justify-between bg-slate-950/60">
              <div className="flex items-center gap-3">
                <div className="p-2 rounded-xl bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">
                  <Scale className="w-5 h-5" />
                </div>
                <div>
                  <div className="flex items-center gap-2">
                    <h2 className="text-base font-bold text-white">{selectedCodeDetails.summary?.title}</h2>
                    <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-cyan-500/20 text-cyan-300 border border-cyan-500/30">
                      {selectedCodeDetails.summary?.act_number}
                    </span>
                  </div>
                  <p className="text-xs text-slate-400">
                    {selectedCodeDetails.summary?.total_sections} Sections across {selectedCodeDetails.summary?.total_chapters} Chapters
                  </p>
                </div>
              </div>

              <button
                onClick={() => setSelectedCodeDetails(null)}
                className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition cursor-pointer"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            <div className="flex-1 overflow-y-auto p-6 space-y-6">
              <div className="p-4 rounded-2xl bg-slate-950 border border-slate-800 space-y-3">
                <p className="text-xs text-slate-300 leading-relaxed font-medium">
                  {selectedCodeDetails.summary?.primary_objective}
                </p>
                <div className="flex flex-wrap gap-1.5 pt-2 border-t border-slate-900">
                  <span className="text-[10px] font-mono text-slate-500 uppercase py-0.5">Amalgamated Acts:</span>
                  {selectedCodeDetails.summary?.repealed_acts?.map((act: string, aIdx: number) => (
                    <span key={aIdx} className="text-[10px] font-mono bg-slate-900 px-2 py-0.5 rounded border border-slate-800 text-slate-400">
                      {act}
                    </span>
                  ))}
                </div>
              </div>

              <div className="space-y-4">
                <h3 className="text-xs font-bold text-white uppercase tracking-wider font-mono">
                  Ground-Truth Statutory Provisions & Penalty Schedules:
                </h3>
                
                <div className="space-y-3">
                  {selectedCodeDetails.sections?.map((sec: any, sIdx: number) => (
                    <div key={sIdx} className="p-4 rounded-2xl bg-slate-950/80 border border-slate-800 space-y-2.5 hover:border-slate-700 transition">
                      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                        <div className="flex items-center gap-2">
                          <span className="text-xs font-bold text-cyan-400 font-mono bg-cyan-500/10 px-2.5 py-0.5 rounded border border-cyan-500/20">
                            {sec.section_number}
                          </span>
                          <h4 className="text-xs font-bold text-white">{sec.title}</h4>
                        </div>
                        <span className="text-[10px] font-mono text-slate-400">
                          {sec.chapter_title}
                        </span>
                      </div>

                      <p className="text-xs text-slate-300 leading-relaxed">
                        {sec.statutory_text}
                      </p>

                      {sec.penalties && (
                        <div className="p-3 rounded-xl bg-rose-500/10 border border-rose-500/20 space-y-1">
                          <span className="text-[10px] font-bold text-rose-300 font-mono uppercase flex items-center gap-1">
                            <AlertTriangle className="w-3 h-3" />
                            Statutory Penalty Exposure:
                          </span>
                          <p className="text-xs text-rose-200">
                            First Offense: <strong>{sec.penalties.first_offense_fine_inr}</strong> • Imprisonment: {sec.penalties.imprisonment_applicable ? sec.penalties.imprisonment_max_duration : 'None'}
                          </p>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

    </div>
  );
};
