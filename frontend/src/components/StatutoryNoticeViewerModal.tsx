import React, { useState } from 'react';
import { 
  X, 
  Printer, 
  Copy, 
  Check, 
  Scale, 
  FileText, 
  BadgeCheck, 
  Download,
  Send
} from 'lucide-react';
import { StatutoryNotice } from '../types';

interface StatutoryNoticeViewerModalProps {
  notice: StatutoryNotice | null;
  isOpen: boolean;
  onClose: () => void;
  onUpdateStatus?: (noticeId: string, status: string, notes?: string) => void;
  isEmployerRole?: boolean;
}

export const StatutoryNoticeViewerModal: React.FC<StatutoryNoticeViewerModalProps> = ({
  notice,
  isOpen,
  onClose,
  onUpdateStatus,
  isEmployerRole = false,
}) => {
  const [copied, setCopied] = useState(false);
  const [responseText, setResponseText] = useState('');
  const [isSubmittingResponse, setIsSubmittingResponse] = useState(false);
  const [responseSubmitted, setResponseSubmitted] = useState(false);

  if (!isOpen || !notice) return null;

  const handleCopy = () => {
    navigator.clipboard.writeText(notice.formal_legal_text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2500);
  };

  const handlePrint = () => {
    window.print();
  };

  const handleDownloadTxt = () => {
    const blob = new Blob([notice.formal_legal_text], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `${notice.notice_number.replace(/\//g, '_')}.txt`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  const handleSubmitResponse = async (status: string) => {
    if (!onUpdateStatus) return;
    setIsSubmittingResponse(true);
    try {
      await onUpdateStatus(notice.notice_id, status, responseText);
      setResponseSubmitted(true);
    } catch (e) {
      console.error(e);
    } finally {
      setIsSubmittingResponse(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-6 bg-slate-950/80 backdrop-blur-md overflow-y-auto animate-fadeIn">
      <div className="relative w-full max-w-4xl bg-slate-900 border border-slate-700/80 rounded-3xl shadow-2xl shadow-indigo-950/50 overflow-hidden flex flex-col max-h-[92vh]">
        
        {/* Header toolbar */}
        <div className="px-6 py-4 border-b border-slate-800 bg-slate-950/80 flex items-center justify-between gap-4">
          <div className="flex items-center gap-2.5">
            <div className="p-2 rounded-xl bg-amber-500/10 border border-amber-500/30 text-amber-400">
              <Scale className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h3 className="text-base font-bold text-white">Statutory Show Cause Notice</h3>
                <span className="px-2 py-0.5 text-[10px] font-mono font-bold rounded bg-rose-500/20 text-rose-300 border border-rose-500/30">
                  {notice.status}
                </span>
              </div>
              <p className="text-xs text-slate-400 font-mono">
                Ref: {notice.notice_number} • Issued: {notice.issue_date}
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={handleCopy}
              className="px-3 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 border border-slate-700 text-xs font-medium text-slate-200 flex items-center gap-1.5 transition"
              title="Copy official notice text"
            >
              {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5 text-slate-400" />}
              <span>{copied ? 'Copied' : 'Copy'}</span>
            </button>
            <button
              onClick={handleDownloadTxt}
              className="px-3 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 border border-slate-700 text-xs font-medium text-slate-200 flex items-center gap-1.5 transition"
              title="Download notice as text document"
            >
              <Download className="w-3.5 h-3.5 text-slate-400" />
              <span>Export</span>
            </button>
            <button
              onClick={handlePrint}
              className="px-3 py-1.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-xs font-medium text-white flex items-center gap-1.5 transition shadow-sm shadow-indigo-600/30"
              title="Print official notice"
            >
              <Printer className="w-3.5 h-3.5" />
              <span>Print</span>
            </button>
            <button
              onClick={onClose}
              className="p-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-white transition ml-1"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Scrollable Notice Document Body */}
        <div className="p-6 overflow-y-auto space-y-6 text-slate-200">
          
          {/* Government Formal Header Paper */}
          <div className="p-6 sm:p-8 rounded-2xl bg-white text-slate-900 border border-slate-300 shadow-xl space-y-6 font-serif">
            
            {/* National Emblem & Authority Header */}
            <div className="text-center border-b-2 border-slate-900 pb-4 space-y-1">
              <div className="w-10 h-10 mx-auto rounded-full border border-slate-800 flex items-center justify-center font-sans font-black text-xs tracking-widest text-slate-800 mb-1">
                GOI
              </div>
              <h2 className="text-lg font-extrabold uppercase tracking-wide">
                GOVERNMENT OF INDIA
              </h2>
              <h3 className="text-sm font-semibold uppercase tracking-wider text-slate-700">
                MINISTRY OF LABOUR AND EMPLOYMENT
              </h3>
              <p className="text-xs uppercase font-sans tracking-wide text-slate-600 font-semibold">
                {notice.issuing_authority}
              </p>
            </div>

            {/* Reference Bar */}
            <div className="flex flex-col sm:flex-row justify-between text-xs font-mono border-b border-slate-300 pb-3 gap-1 text-slate-700">
              <div>
                <strong>NOTICE REF:</strong> {notice.notice_number}
              </div>
              <div>
                <strong>DATE OF SERVICE:</strong> {notice.issue_date}
              </div>
            </div>

            {/* Addressee */}
            <div className="text-xs space-y-1 font-sans">
              <p className="font-bold text-slate-800">TO:</p>
              <p className="font-bold text-slate-900 text-sm">{notice.establishment_name}</p>
              <p className="text-slate-700">Labour Identification Number (LIN): <span className="font-mono font-bold">{notice.registration_number}</span></p>
              <p className="text-slate-600">Establishment Code: {notice.establishment_id}</p>
            </div>

            {/* Subject */}
            <div className="bg-slate-100 p-3 rounded-lg border-l-4 border-slate-900 font-sans text-xs font-semibold leading-relaxed">
              <span className="font-bold uppercase tracking-wider text-slate-900">SUBJECT: </span>
              STATUTORY SHOW CAUSE NOTICE UNDER CODE ON WAGES, 2019 (SECTION 50 & 54) AND OCCUPATIONAL SAFETY, HEALTH AND WORKING CONDITIONS CODE, 2020 (SECTION 96)
            </div>

            {/* Preamble */}
            <p className="text-xs leading-relaxed text-slate-800 font-sans">
              WHEREAS, an automated statutory inspection and cross-document reconciliation was conducted by the 
              <strong> ShramAI Digital Compliance Engine</strong> under the supervision of <strong>{notice.issuing_officer}</strong>; 
              and examination of statutory records and registers revealed the following prima facie non-compliances and contraventions of labour legislation:
            </p>

            {/* Violations Table */}
            <div className="overflow-x-auto border border-slate-300 rounded-lg font-sans">
              <table className="w-full text-left text-xs border-collapse">
                <thead>
                  <tr className="bg-slate-200 text-slate-900 border-b border-slate-300 font-bold">
                    <th className="p-2.5 w-10 text-center">#</th>
                    <th className="p-2.5">Statutory Section</th>
                    <th className="p-2.5">Contravention Finding</th>
                    <th className="p-2.5 text-right">Max Fine</th>
                    <th className="p-2.5 text-center">Cure Window</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-200">
                  {notice.violations.map((v, i) => (
                    <tr key={i} className="hover:bg-slate-50">
                      <td className="p-2.5 text-center font-bold">{i + 1}</td>
                      <td className="p-2.5 font-semibold text-slate-900">
                        <div>{v.statutory_code}</div>
                        <div className="text-[11px] text-slate-600 font-mono">{v.section}</div>
                      </td>
                      <td className="p-2.5 text-slate-700">{v.finding_description}</td>
                      <td className="p-2.5 text-right font-mono font-bold text-rose-800 whitespace-nowrap">
                        ₹{v.prescribed_fine_inr.toLocaleString('en-IN')}
                      </td>
                      <td className="p-2.5 text-center font-bold text-amber-700 whitespace-nowrap">
                        {v.rectification_window_days} Days
                      </td>
                    </tr>
                  ))}
                  <tr className="bg-slate-100 font-bold border-t-2 border-slate-300">
                    <td colSpan={3} className="p-2.5 text-right uppercase tracking-wider text-slate-700">
                      Total Statutory Fine Exposure:
                    </td>
                    <td className="p-2.5 text-right font-mono text-rose-900 text-sm">
                      ₹{notice.total_penalty_exposure_inr.toLocaleString('en-IN')}
                    </td>
                    <td className="p-2.5 text-center text-[10px] text-slate-500">
                      Compoundable
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            {/* Directive Body */}
            <div className="space-y-3 text-xs leading-relaxed text-slate-800 font-sans">
              <p>
                <strong>NOW, THEREFORE, NOTICE IS HEREBY GIVEN</strong> requiring you to <strong>SHOW CAUSE</strong> within 14 days of the receipt of this notice (on or before <span className="font-bold underline text-rose-900">{notice.response_deadline}</span>) as to why statutory penal proceedings should not be instituted against you under Section 54 of the Code on Wages, 2019 and/or Section 96 of the OSHWC Code, 2020.
              </p>
              <p>
                You are further directed to submit proof of wage differential arrears disbursement and rectified Form B / Form D registers via the Shram Suvidha portal, or submit an application for <strong>compounding of offences under Section 56 of the Code on Wages, 2019</strong>.
              </p>
              <p className="text-slate-600 italic">
                TAKE NOTICE that failure to submit an adequate explanation or cure the violations within the stipulated deadline shall result in the initiation of formal prosecution before the Chief Judicial Magistrate without further notice.
              </p>
            </div>

            {/* Signature & Digital Verification Seal */}
            <div className="pt-6 border-t-2 border-slate-900 flex flex-col sm:flex-row justify-between items-end gap-4 font-sans">
              <div className="p-3 bg-slate-100 rounded-xl border border-slate-300 space-y-1 text-left w-full sm:w-auto">
                <div className="flex items-center gap-1.5 text-slate-800 font-bold text-xs">
                  <BadgeCheck className="w-4 h-4 text-emerald-600" />
                  <span>Tamper-Evident Digital Verification Seal</span>
                </div>
                <div className="text-[10px] font-mono text-slate-600 break-all">
                  {notice.digital_signature_hash}
                </div>
                <div className="text-[9px] text-slate-500">
                  Authenticated via ShramAI Public Verification Authority
                </div>
              </div>

              <div className="text-right space-y-1">
                <div className="font-bold text-slate-900 text-xs">{notice.issuing_officer}</div>
                <div className="text-[11px] text-slate-600">Labour Enforcement Officer (Central)</div>
                <div className="text-[10px] text-slate-500">{notice.issuing_authority}</div>
              </div>
            </div>

          </div>

          {/* Employer Response Panel (if employer view) */}
          {isEmployerRole && (
            <div className="p-5 rounded-2xl bg-slate-950/80 border border-slate-800 space-y-4">
              <div className="flex items-center justify-between">
                <h4 className="text-xs font-bold text-white flex items-center gap-2">
                  <FileText className="w-4 h-4 text-indigo-400" />
                  Formal Employer Response & Compounding Application
                </h4>
                <span className="text-[11px] text-amber-400 font-mono">
                  Deadline: {notice.response_deadline}
                </span>
              </div>

              {responseSubmitted ? (
                <div className="p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-center space-y-1">
                  <Check className="w-6 h-6 text-emerald-400 mx-auto" />
                  <p className="text-xs font-bold text-emerald-300">Response Submitted to Labour Authority</p>
                  <p className="text-[11px] text-slate-400">Your explanation and payment scrolls have been logged in the audit trail.</p>
                </div>
              ) : (
                <div className="space-y-3">
                  <textarea
                    rows={3}
                    value={responseText}
                    onChange={(e) => setResponseText(e.target.value)}
                    placeholder="Enter response details (e.g. Arrears disbursed via RTGS UTR #..., rectified Form B uploaded, or application for Section 56 Compounding)..."
                    className="w-full px-3 py-2 text-xs bg-slate-900 border border-slate-700 rounded-xl text-slate-200 placeholder-slate-500 focus:outline-none focus:border-indigo-500"
                  />
                  <div className="flex flex-wrap items-center gap-2.5">
                    <button
                      onClick={() => handleSubmitResponse('RESPONDED')}
                      disabled={isSubmittingResponse || !responseText.trim()}
                      className="px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white font-semibold text-xs transition flex items-center gap-1.5"
                    >
                      <Send className="w-3.5 h-3.5" />
                      <span>{isSubmittingResponse ? 'Submitting...' : 'File Formal Explanation'}</span>
                    </button>
                    <button
                      onClick={() => handleSubmitResponse('COMPOUNDED')}
                      disabled={isSubmittingResponse}
                      className="px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 disabled:opacity-50 text-white font-semibold text-xs transition flex items-center gap-1.5"
                    >
                      <Scale className="w-3.5 h-3.5" />
                      <span>Apply for Sec 56 Compounding</span>
                    </button>
                  </div>
                </div>
              )}
            </div>
          )}

        </div>

      </div>
    </div>
  );
};
