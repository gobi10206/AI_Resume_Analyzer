import React, { useState } from 'react';
import { ResumeImprovementResponse } from '../types';
import { Sparkles, Check, Copy, ArrowRight, Zap, Award } from 'lucide-react';

interface ImprovementModalProps {
  data: ResumeImprovementResponse;
  onClose: () => void;
}

export const ImprovementModal: React.FC<ImprovementModalProps> = ({ data, onClose }) => {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(data.improved_content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/80 backdrop-blur-sm p-4">
      <div className="w-full max-w-2xl rounded-2xl border border-slate-800 bg-slate-900 p-6 shadow-2xl space-y-5">
        <div className="flex items-center justify-between border-b border-slate-800 pb-4">
          <div className="flex items-center gap-2">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-indigo-500/10 text-indigo-400">
              <Sparkles className="h-4 w-4" />
            </div>
            <h3 className="text-lg font-bold text-white">AI Content Enhancement - {data.section}</h3>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-white text-sm font-semibold">✕</button>
        </div>

        {/* Comparison: Original vs Improved */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {data.original_content && (
            <div className="rounded-xl border border-slate-800 bg-slate-950/60 p-3.5">
              <span className="text-[11px] font-bold uppercase tracking-wider text-slate-500 block mb-2">Original Phrasing</span>
              <p className="text-xs text-slate-400 whitespace-pre-line leading-relaxed">{data.original_content}</p>
            </div>
          )}

          <div className="rounded-xl border border-indigo-500/30 bg-indigo-950/20 p-3.5">
            <span className="text-[11px] font-bold uppercase tracking-wider text-indigo-400 block mb-2">AI-Optimized (XYZ Formula)</span>
            <p className="text-xs text-indigo-100 whitespace-pre-line leading-relaxed font-medium">{data.improved_content}</p>
          </div>
        </div>

        {/* Changes Made */}
        <div className="space-y-2">
          <span className="text-xs font-bold uppercase tracking-wider text-slate-400">Optimization Actions</span>
          <div className="space-y-1.5">
            {data.changes_made.map((change, i) => (
              <div key={i} className="flex items-center gap-2 text-xs text-slate-300">
                <Check className="h-3.5 w-3.5 text-emerald-400 shrink-0" />
                <span>{change}</span>
              </div>
            ))}
          </div>
        </div>

        {/* ATS Impact Summary */}
        <div className="rounded-xl bg-emerald-950/20 border border-emerald-500/20 p-3 text-xs text-emerald-300 flex items-start gap-2">
          <Zap className="h-4 w-4 shrink-0 mt-0.5 text-emerald-400" />
          <span>{data.ats_impact_summary}</span>
        </div>

        <div className="flex items-center justify-end gap-3 pt-2">
          <button
            onClick={onClose}
            className="rounded-lg px-4 py-2 text-xs font-semibold text-slate-400 hover:text-white transition"
          >
            Close
          </button>
          <button
            onClick={handleCopy}
            className="inline-flex items-center gap-1.5 rounded-lg bg-indigo-600 px-4 py-2 text-xs font-semibold text-white hover:bg-indigo-500 transition"
          >
            {copied ? <Check className="h-3.5 w-3.5" /> : <Copy className="h-3.5 w-3.5" />}
            <span>{copied ? 'Copied!' : 'Copy Improved Text'}</span>
          </button>
        </div>
      </div>
    </div>
  );
};
