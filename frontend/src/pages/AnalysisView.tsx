import React, { useState, useEffect } from 'react';
import { ApiClient } from '../services/api';
import { AnalysisResponse } from '../types';
import { ScoreGauge } from '../components/ScoreGauge';
import { ScoreBreakdown } from '../components/ScoreBreakdown';
import { AtsReport } from '../components/AtsReport';
import {
  FileText,
  CheckCircle2,
  AlertTriangle,
  Code2,
  GraduationCap,
  Briefcase,
  Layers,
  Sparkles
} from 'lucide-react';

export const AnalysisView: React.FC = () => {
  const [analysis, setAnalysis] = useState<AnalysisResponse | null>(null);
  const [activeTab, setActiveTab] = useState<'overview' | 'breakdown' | 'ats' | 'entities'>('overview');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const resumes = await ApiClient.listResumes();
        const resumeId = resumes[0]?.id || 'demo-resume-1';
        const data = await ApiClient.getAnalysis(resumeId);
        setAnalysis(data);
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  if (loading || !analysis) {
    return (
      <div className="flex h-96 items-center justify-center">
        <div className="h-8 w-8 animate-spin rounded-full border-2 border-indigo-500 border-t-transparent" />
      </div>
    );
  }

  const pData = analysis.parsed_data;

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-extrabold text-white">In-Depth Resume Audit</h2>
          <p className="text-xs sm:text-sm text-slate-400 mt-0.5">
            Detailed breakdown of scoring criteria, NLP entity extraction, and ATS compatibility metrics.
          </p>
        </div>

        {/* Tab switcher */}
        <div className="flex items-center gap-1 rounded-xl bg-slate-900/90 border border-slate-800 p-1">
          {(['overview', 'breakdown', 'ats', 'entities'] as const).map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`rounded-lg px-3 py-1.5 text-xs font-semibold capitalize transition ${
                activeTab === tab
                  ? 'bg-indigo-600 text-white shadow-sm'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              {tab === 'ats' ? 'ATS Report' : tab}
            </button>
          ))}
        </div>
      </div>

      {activeTab === 'overview' && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-6 flex flex-col items-center justify-center">
            <ScoreGauge score={analysis.overall_score} label="Overall Score" size={180} />
            <div className="mt-4 w-full grid grid-cols-2 gap-2 text-center text-xs">
              <div className="rounded-lg bg-slate-950 p-2 border border-slate-800">
                <span className="text-slate-400 block text-[11px]">ATS Rating</span>
                <span className="font-bold text-emerald-400">{analysis.ats_score}/100</span>
              </div>
              <div className="rounded-lg bg-slate-950 p-2 border border-slate-800">
                <span className="text-slate-400 block text-[11px]">Total Skills</span>
                <span className="font-bold text-indigo-400">{analysis.extracted_skills_count}</span>
              </div>
            </div>
          </div>

          <div className="lg:col-span-2 space-y-4">
            <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-6">
              <h3 className="text-base font-bold text-white mb-3">Core Strengths Identified</h3>
              <div className="space-y-3">
                {analysis.strengths.map((s, i) => (
                  <div key={i} className="rounded-xl bg-slate-950/50 p-3.5 border border-slate-800 flex items-start gap-3">
                    <CheckCircle2 className="h-5 w-5 text-emerald-400 shrink-0 mt-0.5" />
                    <div>
                      <h5 className="text-xs font-bold text-white">{s.title}</h5>
                      <p className="text-xs text-slate-400 mt-1 leading-relaxed">{s.description}</p>
                      <span className="inline-block mt-2 rounded bg-indigo-950/40 border border-indigo-500/20 px-2 py-0.5 text-[10px] font-medium text-indigo-300">
                        Tip: {s.actionable_tip}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-6">
              <h3 className="text-base font-bold text-white mb-3">Improvement Opportunities</h3>
              <div className="space-y-3">
                {analysis.weaknesses.map((w, i) => (
                  <div key={i} className="rounded-xl bg-slate-950/50 p-3.5 border border-slate-800 flex items-start gap-3">
                    <AlertTriangle className="h-5 w-5 text-amber-400 shrink-0 mt-0.5" />
                    <div>
                      <h5 className="text-xs font-bold text-white">{w.title}</h5>
                      <p className="text-xs text-slate-400 mt-1 leading-relaxed">{w.description}</p>
                      <p className="text-xs text-amber-400/90 mt-1.5 font-medium">
                        Action: {w.actionable_tip}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'breakdown' && (
        <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-6 max-w-3xl">
          <h3 className="text-base font-bold text-white mb-4">Five-Factor Scoring Breakdown</h3>
          <ScoreBreakdown breakdown={analysis.score_breakdown} />
        </div>
      )}

      {activeTab === 'ats' && (
        <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-6">
          <AtsReport report={analysis.ats_report} />
        </div>
      )}

      {activeTab === 'entities' && (
        <div className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Personal Info */}
            <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-5 space-y-3">
              <div className="flex items-center gap-2 text-indigo-400 font-bold text-sm">
                <FileText className="h-4 w-4" />
                <span>Extracted Contact Info</span>
              </div>
              <div className="text-xs space-y-1.5 text-slate-300">
                <p><strong className="text-slate-400">Name:</strong> {pData.personal_info.full_name || 'N/A'}</p>
                <p><strong className="text-slate-400">Email:</strong> {pData.personal_info.email || 'N/A'}</p>
                <p><strong className="text-slate-400">Phone:</strong> {pData.personal_info.phone || 'N/A'}</p>
                <p><strong className="text-slate-400">Location:</strong> {pData.personal_info.location || 'N/A'}</p>
                <p><strong className="text-slate-400">LinkedIn:</strong> {pData.personal_info.linkedin || 'N/A'}</p>
                <p><strong className="text-slate-400">GitHub:</strong> {pData.personal_info.github || 'N/A'}</p>
              </div>
            </div>

            {/* Education */}
            <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-5 space-y-3">
              <div className="flex items-center gap-2 text-violet-400 font-bold text-sm">
                <GraduationCap className="h-4 w-4" />
                <span>Education Credentials</span>
              </div>
              <div className="space-y-2">
                {pData.education.map((edu, idx) => (
                  <div key={idx} className="text-xs text-slate-300 border-l-2 border-violet-500 pl-3 py-0.5">
                    <span className="font-bold text-white">{edu.degree}</span>
                    <p className="text-slate-400">{edu.institution} ({edu.graduation_year || 'Year unstated'})</p>
                    {edu.gpa && <p className="text-indigo-400 font-medium">GPA: {edu.gpa}</p>}
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Extracted Skills */}
          <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-6 space-y-4">
            <div className="flex items-center gap-2 text-cyan-400 font-bold text-sm">
              <Code2 className="h-4 w-4" />
              <span>Categorized Technical Taxonomy ({pData.skills.length} skills)</span>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {Object.entries(pData.categorized_skills).map(([cat, skills]) => (
                <div key={cat} className="rounded-xl bg-slate-950/50 p-3.5 border border-slate-800/80">
                  <span className="text-[11px] font-bold uppercase tracking-wider text-slate-400 block mb-2">
                    {cat.replace(/_/g, ' ')}
                  </span>
                  <div className="flex flex-wrap gap-1">
                    {skills.map((s) => (
                      <span key={s} className="rounded bg-slate-800 px-2 py-0.5 text-[11px] text-slate-300 font-medium">
                        {s}
                      </span>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
