import React, { useState } from 'react';
import { ApiClient } from '../services/api';
import { ResumeImprovementResponse } from '../types';
import { ImprovementModal } from '../components/ImprovementModal';
import { Sparkles, Loader2, Wand2, Check } from 'lucide-react';

export const ResumeEditor: React.FC = () => {
  const [section, setSection] = useState<'summary' | 'experience' | 'projects' | 'skills'>('experience');
  const [targetRole, setTargetRole] = useState('Full Stack Engineer');
  const [content, setContent] = useState('');
  const [loading, setLoading] = useState(false);
  const [improvedData, setImprovedData] = useState<ResumeImprovementResponse | null>(null);

  const sampleInputs = {
    summary: 'Hardworking software engineer looking to work in a reputed company to grow my skills.',
    experience: `• Responsible for backend code and APIs.
• Fixed database performance issues.
• Worked with team on automated deployment.`,
    projects: 'Web Store Project: Made an online shop with Python and React with user login and cart.',
    skills: 'Python, SQL, React, Docker, Git'
  };

  const handleImprove = async () => {
    setLoading(true);
    try {
      const resumes = await ApiClient.listResumes();
      const resumeId = resumes[0]?.id || 'demo-resume-1';
      const res = await ApiClient.improveSection(resumeId, section, content || sampleInputs[section], targetRole);
      setImprovedData(res);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div>
        <h2 className="text-2xl font-extrabold text-white">AI-Powered Resume Section Improver</h2>
        <p className="text-xs sm:text-sm text-slate-400 mt-1">
          Transform weak, passive phrasing into Google XYZ formula bullet points with active verbs and quantifiable metrics.
        </p>
      </div>

      <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-6 space-y-6">
        {/* Section Selector */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          {(['summary', 'experience', 'projects', 'skills'] as const).map((s) => (
            <button
              key={s}
              onClick={() => {
                setSection(s);
                setContent(sampleInputs[s]);
              }}
              className={`rounded-xl py-2.5 px-3 text-xs font-semibold capitalize transition ${
                section === s
                  ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/30'
                  : 'bg-slate-950 border border-slate-800 text-slate-400 hover:text-slate-200'
              }`}
            >
              {s}
            </button>
          ))}
        </div>

        {/* Target Role */}
        <div>
          <label className="text-xs font-bold uppercase tracking-wider text-slate-400 block mb-1.5">
            Target Career Title
          </label>
          <input
            type="text"
            value={targetRole}
            onChange={(e) => setTargetRole(e.target.value)}
            className="w-full sm:w-80 rounded-xl border border-slate-800 bg-slate-950 px-3.5 py-2 text-xs sm:text-sm text-white focus:border-indigo-500 focus:outline-none"
          />
        </div>

        {/* Input Text */}
        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <label className="text-xs font-bold uppercase tracking-wider text-slate-400">
              Draft or Existing Text to Enhance
            </label>
            <button
              onClick={() => setContent(sampleInputs[section])}
              className="text-xs text-indigo-400 hover:text-indigo-300 font-medium"
            >
              Load Sample Text
            </button>
          </div>

          <textarea
            rows={7}
            value={content}
            onChange={(e) => setContent(e.target.value)}
            placeholder="Type or paste your bullet points or section text here..."
            className="w-full rounded-xl border border-slate-800 bg-slate-950 p-4 text-xs sm:text-sm text-slate-200 focus:border-indigo-500 focus:outline-none font-mono leading-relaxed"
          />
        </div>

        <button
          onClick={handleImprove}
          disabled={loading}
          className="w-full inline-flex items-center justify-center gap-2 rounded-xl bg-indigo-600 py-3 text-sm font-semibold text-white shadow-lg shadow-indigo-600/30 hover:bg-indigo-500 disabled:opacity-50 transition"
        >
          {loading ? (
            <>
              <Loader2 className="h-4 w-4 animate-spin" />
              <span>Applying Metric Formulation & Power Verbs...</span>
            </>
          ) : (
            <>
              <Wand2 className="h-4 w-4" />
              <span>Enhance Section with AI</span>
            </>
          )}
        </button>
      </div>

      {improvedData && (
        <ImprovementModal data={improvedData} onClose={() => setImprovedData(null)} />
      )}
    </div>
  );
};
