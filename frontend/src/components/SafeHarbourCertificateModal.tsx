import React from 'react';
import { 
  Award, 
  ShieldCheck, 
  CheckCircle2, 
  Download, 
  X, 
  QrCode,
  Building2,
  Scale
} from 'lucide-react';
import { SafeHarbourCertificate } from '../types';

interface SafeHarbourCertificateModalProps {
  certificate: SafeHarbourCertificate | null;
  isOpen: boolean;
  onClose: () => void;
}

export const SafeHarbourCertificateModal: React.FC<SafeHarbourCertificateModalProps> = ({
  certificate,
  isOpen,
  onClose,
}) => {
  if (!isOpen || !certificate) return null;

  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-6 bg-slate-950/80 backdrop-blur-md overflow-y-auto animate-fadeIn">
      <div className="relative w-full max-w-3xl bg-slate-900 border-2 border-amber-500/40 rounded-3xl shadow-2xl shadow-amber-500/10 overflow-hidden flex flex-col my-auto">
        
        {/* Modal Top Bar */}
        <div className="px-6 py-3.5 bg-slate-950 border-b border-slate-800 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Award className="w-5 h-5 text-amber-400" />
            <span className="text-xs font-bold text-slate-200 tracking-wide">
              Official Statutory Safe Harbour Certificate (Form SH-01)
            </span>
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={handlePrint}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold text-xs transition cursor-pointer"
            >
              <Download className="w-3.5 h-3.5" />
              <span>Print / Download</span>
            </button>
            <button
              onClick={onClose}
              className="p-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-white transition cursor-pointer"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Certificate Parchment Body */}
        <div className="p-8 sm:p-10 space-y-6 bg-gradient-to-b from-slate-900 via-slate-950 to-slate-900 relative">
          
          {/* Subtle watermark seal background */}
          <div className="absolute inset-0 flex items-center justify-center opacity-5 pointer-events-none">
            <Scale className="w-96 h-96 text-amber-300" />
          </div>

          {/* Certificate Header */}
          <div className="text-center space-y-2 relative z-10 border-b border-amber-500/20 pb-6">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-amber-500/10 border border-amber-500/30 text-amber-400 text-[11px] font-bold uppercase tracking-wider">
              <ShieldCheck className="w-4 h-4" />
              <span>Central Labour Sphere • Statutory Compliance Authority</span>
            </div>
            
            <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
              Certificate of Safe Harbour Compliance
            </h1>
            
            <p className="text-xs font-mono text-slate-400">
              Certificate Ref: <strong className="text-amber-400">{certificate.certificate_number}</strong>
            </p>
          </div>

          {/* Core Recipient Details */}
          <div className="relative z-10 grid grid-cols-1 sm:grid-cols-2 gap-4 p-5 rounded-2xl bg-slate-900/80 border border-slate-800">
            <div className="space-y-1">
              <span className="text-[10px] font-mono text-slate-400 uppercase font-bold">Certified Establishment:</span>
              <h2 className="text-base font-bold text-white flex items-center gap-2">
                <Building2 className="w-4 h-4 text-amber-400" />
                <span>{certificate.establishment_name}</span>
              </h2>
              <p className="text-xs text-slate-400">
                Labour Identification No (LIN): <strong className="text-slate-200 font-mono">{certificate.lin}</strong>
              </p>
              <p className="text-xs text-slate-400">
                Registration: <strong className="text-slate-200 font-mono">{certificate.registration_number}</strong>
              </p>
            </div>

            <div className="space-y-1 sm:text-right">
              <span className="text-[10px] font-mono text-slate-400 uppercase font-bold">Audit Score & Status:</span>
              <div className="flex sm:justify-end items-center gap-2">
                <span className="text-3xl font-extrabold text-emerald-400 font-mono">
                  {certificate.certified_compliance_score}
                </span>
                <span className="text-xs text-slate-400 font-mono">/ 100</span>
              </div>
              <span className="inline-block text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
                {certificate.safe_harbour_status}
              </span>
              <p className="text-[11px] text-slate-400">
                Jurisdiction: {certificate.jurisdiction}
              </p>
            </div>
          </div>

          {/* Statutory Immunity & Exemption Declaration */}
          <div className="relative z-10 p-4 rounded-xl bg-amber-500/5 border border-amber-500/20 space-y-2 text-xs text-slate-300 leading-relaxed">
            <p className="font-semibold text-amber-300">
              Statutory Exemption Declaration & Audit Shield:
            </p>
            <p>
              This certifies that the establishment has completed voluntary self-audit filings under the <strong>Four Labour Codes</strong> and has rectified all flagged non-compliance findings. Pursuant to statutory compounding and self-certification policies, this establishment is granted a <strong>180-Day Safe Harbour Protection Window</strong>, de-prioritizing automated statutory enforcement audits unless substantiated grievances are lodged.
            </p>
          </div>

          {/* Cured Remediations Summary */}
          <div className="relative z-10 space-y-2">
            <span className="text-[10px] font-mono text-slate-400 uppercase tracking-wider font-bold">
              Verified Remediation Highlights:
            </span>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
              {certificate.cured_violations_summary.map((item, idx) => (
                <div key={idx} className="flex items-start gap-2 p-2.5 rounded-lg bg-slate-950/80 border border-slate-800 text-xs text-slate-300">
                  <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 shrink-0 mt-0.5" />
                  <span>{item}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Statutory Citations */}
          <div className="relative z-10 space-y-1">
            <span className="text-[10px] font-mono text-slate-400 uppercase tracking-wider font-bold">
              Applicable Enactments:
            </span>
            <ul className="text-xs text-slate-400 space-y-0.5 list-disc list-inside">
              {certificate.statutory_citations.map((cite, idx) => (
                <li key={idx}><span className="text-slate-300">{cite}</span></li>
              ))}
            </ul>
          </div>

          {/* Cryptographic Stamp & Verification Footer */}
          <div className="relative z-10 pt-4 border-t border-slate-800 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-xl bg-slate-800 border border-slate-700 text-amber-400">
                <QrCode className="w-9 h-9" />
              </div>
              <div className="space-y-0.5 text-left">
                <p className="text-[10px] font-mono text-slate-400 uppercase font-bold">SHA-256 Digital Verification Hash:</p>
                <p className="font-mono text-[10px] text-cyan-400 break-all max-w-xs">
                  {certificate.verification_hash_sha256}
                </p>
                <p className="text-[10px] text-slate-500">
                  Seal Ref: {certificate.digital_seal_id}
                </p>
              </div>
            </div>

            <div className="space-y-1 text-right">
              <p className="text-slate-400 text-[11px]">
                Valid: <strong className="text-white font-mono">{certificate.issue_date}</strong> to <strong className="text-amber-400 font-mono">{certificate.expiry_date}</strong>
              </p>
              <p className="text-[11px] text-slate-400 italic">
                {certificate.issuing_authority}
              </p>
            </div>
          </div>

        </div>

      </div>
    </div>
  );
};
