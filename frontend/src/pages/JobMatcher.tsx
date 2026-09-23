import React, { useState } from 'react';
import { ApiClient } from '../services/api';
import { JobDescriptionMatchResponse } from '../types';
import { ScoreGauge } from '../components/ScoreGauge';
import { Briefcase, Check, AlertCircle, Sparkles, Loader2, Info } from 'lucide-react';

export const JobMatcher: React.FC = () => {
  const [jdText, setJdText] = useState('');
  const [matching, setMatching] = useState(false);
  const [result, setResult] = useState<JobDescriptionMatchResponse | null>(null);

  const sampleJD = `Senior Software Engineer - Full Stack
Company: TechCorp Global
Location: San Francisco, CA

We are looking for a Senior Full Stack Engineer to lead the architecture of our cloud-native applications.
Responsibilities:
• Architect, develop, and maintain high-throughput backend services using Python, FastAPI, and PostgreSQL.
• Design responsive, interactive user interfaces with React, TypeScript, and modern CSS frameworks.
• Deploy scalable containerized microservices to AWS utilizing Docker, Kubernetes, and automated CI/CD pipelines.
• Collaborate in Agile Scrum teams, conduct code reviews, and mentor junior engineers.

Requirements:
• 3+ years experience with Python, TypeScript, React, Docker, and AWS.
• Solid background in database design (SQL, PostgreSQL, Redis) and REST API principles.
• Familiarity with message brokers (Kafka) or GraphQL is a strong plus.`;

  const handleMatch = async () => {
    if (!jdText.trim()) return;
    setMatching(true);
    try {
      const resumes = await ApiClient.listResumes();
      const resumeId = resumes[0]?.id || 'demo-resume-1';
      const data = await ApiClient.matchJobDescription(resumeId, jdText);
      setResult(data);
    } catch (e) {
      console.error(e);
    } finally {
      setMatching(false);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-extrabold text-white">Job Description Matching Engine</h2>
        <p className="text-xs sm:text-sm text-slate-400 mt-1">
          Paste any real-world job posting to calculate semantic vector alignment, skill gap percentages, and keyword relevance.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Input Area */}
        <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-5 space-y-4">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold uppercase tracking-wider text-slate-400">
              Target Job Description
            </span>
            <button
              onClick={() => setJdText(sampleJD)}
              className="text-xs text-indigo-400 hover:text-indigo-300 font-medium"
            >
              Paste Sample Full Stack JD
            </button>
          </div>

          <textarea
            rows={14}
            value={jdText}
            onChange={(e) => setJdText(e.target.value)}
            placeholder="Paste complete job description text here (including responsibilities, qualifications, and tech stack requirements)..."
            className="w-full rounded-xl border border-slate-800 bg-slate-950 p-4 text-xs sm:text-sm text-slate-200 placeholder-slate-600 focus:border-indigo-500 focus:outline-none leading-relaxed font-mono"
          />

          <button
            onClick={handleMatch}
            disabled={!jdText.trim() || matching}
            className="w-full inline-flex items-center justify-center gap-2 rounded-xl bg-indigo-600 py-3 text-sm font-semibold text-white shadow-lg shadow-indigo-600/25 hover:bg-indigo-500 disabled:opacity-50 transition"
          >
            {matching ? (
              <>
                <Loader2 className="h-4 w-4 animate-spin" />
                <span>Computing Semantic Similarity & Vector Overlap...</span>
              </>
            ) : (
              <>
                <Sparkles className="h-4 w-4" />
                <span>Calculate Match & Keyword Gaps</span>
              </>
            )}
          </button>
        </div>

        {/* Results Area */}
        <div className="space-y-6">
          {result ? (
            <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-6 space-y-6">
              <div className="flex flex-col sm:flex-row items-center justify-around gap-4 border-b border-slate-800 pb-5">
                <ScoreGauge score={result.overall_match_percentage} label="Blended Match" size={140} />
                <div className="space-y-2 text-center sm:text-left">
                  <span className="inline-block px-3 py-1 rounded-full text-xs font-bold bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
                    {result.ats_compatibility_verdict}
                  </span>
                  <div className="text-xs text-slate-400 space-y-1">
                    <p>Semantic Text Overlap: <strong className="text-white">{result.semantic_similarity}%</strong></p>
                    <p>Skill Fit Ratio: <strong className="text-white">{result.skill_match_percentage}%</strong></p>
                  </div>
                </div>
              </div>

              {/* Matching Skills */}
              <div>
                <span className="text-xs font-bold uppercase tracking-wider text-emerald-400 block mb-2">
                  Matching Skills ({result.matching_skills.length})
                </span>
                <div className="flex flex-wrap gap-1.5">
                  {result.matching_skills.map((s) => (
                    <span key={s} className="inline-flex items-center gap-1 rounded bg-emerald-950/40 border border-emerald-800/50 px-2 py-0.5 text-xs text-emerald-300">
                      <Check className="h-3 w-3" />
                      {s}
                    </span>
                  ))}
                </div>
              </div>

              {/* Missing Skills */}
              {result.missing_skills.length > 0 && (
                <div>
                  <span className="text-xs font-bold uppercase tracking-wider text-rose-400 block mb-2">
                    Missing Target Skills ({result.missing_skills.length})
                  </span>
                  <div className="flex flex-wrap gap-1.5">
                    {result.missing_skills.map((s) => (
                      <span key={s} className="inline-flex items-center gap-1 rounded bg-rose-950/30 border border-rose-800/40 px-2 py-0.5 text-xs text-rose-300">
                        <AlertCircle className="h-3 w-3" />
                        {s}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {/* Recommendations */}
              <div className="space-y-2 pt-2 border-t border-slate-800">
                <span className="text-xs font-bold uppercase tracking-wider text-slate-400">
                  Target Optimization Advice
                </span>
                <ul className="space-y-1.5 text-xs text-slate-300">
                  {result.recommendations.map((rec, i) => (
                    <li key={i} className="flex items-start gap-2">
                      <Info className="h-3.5 w-3.5 text-indigo-400 shrink-0 mt-0.5" />
                      <span>{rec}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          ) : (
            <div className="h-full rounded-2xl border border-slate-800 bg-slate-900/30 p-12 flex flex-col items-center justify-center text-center">
              <Briefcase className="h-10 w-10 text-slate-700 mb-3" />
              <h4 className="text-sm font-bold text-slate-400">No Job Description Analyzed</h4>
              <p className="text-xs text-slate-500 mt-1 max-w-xs">
                Paste a job description on the left and click Calculate Match to view compatibility breakdown.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
