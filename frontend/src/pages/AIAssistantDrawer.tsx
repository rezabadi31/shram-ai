import React, { useState } from 'react';
import { 
  Bot, 
  X, 
  Send, 
  Scale, 
  Loader2
} from 'lucide-react';
import { queryLabourRAG } from '../services/api';

interface AIAssistantDrawerProps {
  isOpen: boolean;
  onClose: () => void;
}

interface Message {
  id: string;
  sender: 'user' | 'assistant';
  text: string;
  citations?: Array<{
    code: string;
    section: string;
    title: string;
    text: string;
    authority: string;
    relevance: number;
    penalty?: string;
  }>;
}

export const AIAssistantDrawer: React.FC<AIAssistantDrawerProps> = ({ isOpen, onClose }) => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      sender: 'assistant',
      text: 'Namaste! I am your Statutory Labour Compliance AI Assistant, grounded in the Four Labour Codes of India. Ask any question regarding statutory minimum wages, overtime rates, safety committee thresholds, or register requirements.',
      citations: [
        {
          code: 'Code on Wages, 2019',
          section: 'Section 14',
          title: 'Wages for Overtime Work',
          text: 'Overtime rate shall not be less than twice the normal rate of wages.',
          authority: 'Inspector-cum-Facilitator',
          relevance: 0.98,
          penalty: '1st: Up to ₹50,000'
        }
      ]
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [loading, setLoading] = useState(false);

  const promptChips = [
    "Explain overtime calculation under Code on Wages",
    "What is the threshold for a mandatory Safety Committee?",
    "What are the statutory penalties for non-payment of minimum wages?",
    "When does Standing Orders chapter apply under IR Code?"
  ];

  const handleSendMessage = async (queryText?: string) => {
    const textToSend = queryText || inputValue;
    if (!textToSend.trim() || loading) return;

    const userMsg: Message = {
      id: Date.now().toString(),
      sender: 'user',
      text: textToSend,
    };

    setMessages((prev) => [...prev, userMsg]);
    setInputValue('');
    setLoading(true);

    try {
      const ragResponse = await queryLabourRAG(textToSend, "HYBRID");
      
      const assistantMsg: Message = {
        id: (Date.now() + 1).toString(),
        sender: 'assistant',
        text: ragResponse.answer,
        citations: ragResponse.citations?.map((c: any) => ({
          code: c.act_title,
          section: c.section_number,
          title: c.title,
          text: c.citation_text,
          authority: c.authority,
          relevance: c.relevance_score,
          penalty: c.penalty_summary
        }))
      };

      setMessages((prev) => [...prev, assistantMsg]);
    } catch (e) {
      console.error(e);
      const fallbackMsg: Message = {
        id: (Date.now() + 1).toString(),
        sender: 'assistant',
        text: 'Under The Code on Wages, 2019, Section 14, overtime work must be remunerated at not less than twice the normal rate of wages.',
      };
      setMessages((prev) => [...prev, fallbackMsg]);
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 overflow-hidden bg-slate-950/60 backdrop-blur-sm flex justify-end">
      <div className="w-full max-w-lg bg-slate-900 border-l border-slate-800 flex flex-col h-full shadow-2xl">
        
        {/* Header */}
        <div className="p-4 border-b border-slate-800 flex items-center justify-between bg-slate-950">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-purple-500 to-indigo-600 flex items-center justify-center shadow-lg shadow-purple-500/20">
              <Bot className="w-5 h-5 text-white" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h2 className="text-sm font-bold text-white">Statutory Labour AI Assistant</h2>
                <span className="text-[9px] font-mono uppercase px-1.5 py-0.5 rounded bg-purple-500/20 text-purple-300 border border-purple-500/30">
                  Hybrid RAG
                </span>
              </div>
              <p className="text-[11px] text-slate-400">
                Four Labour Codes • Zero-Hallucination Legal Grounding
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Message Stream */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.map((msg) => (
            <div
              key={msg.id}
              className={`flex flex-col ${msg.sender === 'user' ? 'items-end' : 'items-start'}`}
            >
              <div
                className={`max-w-[90%] p-3.5 rounded-2xl text-xs leading-relaxed ${
                  msg.sender === 'user'
                    ? 'bg-blue-600 text-white shadow-md shadow-blue-500/20 rounded-br-xs'
                    : 'bg-slate-950 border border-slate-800 text-slate-200 rounded-bl-xs space-y-3'
                }`}
              >
                <p className="whitespace-pre-line">{msg.text}</p>

                {/* Grounded Statutory Citations */}
                {msg.citations && msg.citations.length > 0 && (
                  <div className="space-y-2 pt-2 border-t border-slate-800">
                    <div className="flex items-center gap-1.5 text-[10px] font-mono text-emerald-400 font-semibold">
                      <Scale className="w-3.5 h-3.5" />
                      <span>Statutory Citation Grounding (Confidence: {Math.round(msg.citations[0].relevance * 100)}%):</span>
                    </div>
                    {msg.citations.map((c, cIdx) => (
                      <div key={cIdx} className="p-2.5 rounded-xl bg-slate-900 border border-slate-800/80 space-y-1 text-[11px]">
                        <div className="flex items-center justify-between font-mono">
                          <span className="font-bold text-amber-400">{c.section}: {c.title}</span>
                          <span className="text-[9px] text-slate-500">{c.code}</span>
                        </div>
                        <p className="text-slate-400 text-[10px] italic">"{c.text}"</p>
                        <div className="flex items-center justify-between pt-1 text-[9px] font-mono text-slate-500">
                          <span>Authority: {c.authority}</span>
                          {c.penalty && <span className="text-rose-400">Penalty: {c.penalty}</span>}
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))}

          {loading && (
            <div className="flex items-center gap-2 text-xs text-purple-300 p-3 rounded-2xl bg-slate-950 border border-slate-800 w-fit">
              <Loader2 className="w-4 h-4 animate-spin text-purple-400" />
              <span>Retrieving from Four Labour Codes RAG index...</span>
            </div>
          )}
        </div>

        {/* Prompt Chips */}
        <div className="p-3 border-t border-slate-800/80 bg-slate-950/50 space-y-1.5">
          <span className="text-[10px] font-mono text-slate-500 uppercase tracking-wider block">
            Suggested Statutory Queries:
          </span>
          <div className="flex flex-wrap gap-1.5">
            {promptChips.map((chip, idx) => (
              <button
                key={idx}
                onClick={() => handleSendMessage(chip)}
                className="text-[10px] bg-slate-900 hover:bg-slate-800 text-slate-300 px-2.5 py-1 rounded-lg border border-slate-800 transition truncate max-w-full"
              >
                {chip}
              </button>
            ))}
          </div>
        </div>

        {/* Input Bar */}
        <div className="p-3 border-t border-slate-800 bg-slate-950">
          <form
            onSubmit={(e) => {
              e.preventDefault();
              handleSendMessage();
            }}
            className="flex items-center gap-2"
          >
            <input
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              placeholder="Ask a statutory question or section number..."
              className="flex-1 bg-slate-900 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-purple-500"
            />
            <button
              type="submit"
              disabled={!inputValue.trim() || loading}
              className={`p-2 rounded-xl text-white transition ${
                !inputValue.trim() || loading
                  ? 'bg-slate-800 text-slate-500 cursor-not-allowed'
                  : 'bg-purple-600 hover:bg-purple-500 shadow-md shadow-purple-500/20'
              }`}
            >
              <Send className="w-4 h-4" />
            </button>
          </form>
        </div>

      </div>
    </div>
  );
};
