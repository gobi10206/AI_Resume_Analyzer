import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { ApiClient } from '../services/api';
import { AnalysisResponse, RoleMatchItem } from '../types';
import { ScoreGauge } from '../components/ScoreGauge';
import { ScoreBreakdown } from '../components/ScoreBreakdown';
import { AtsReport } from '../components/AtsReport';
import { SkillGapChart } from '../components/SkillGapChart';
import { RoleMatchCard } from '../components/RoleMatchCard';
import {
  UploadCloud,
  CheckCircle2,
  AlertTriangle,
  FileText,
  Award,
  ArrowRight,
  Sparkles,
  Briefcase
} from 'lucide-react';

export const Dashboard: React.FC = () => {
  const [analysis, setAnalysis] = useState<AnalysisResponse | null>(null);
  const [roles, setRoles] = useState<RoleMatchItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      try {
        const resumes = await ApiClient.listResumes();
        const resumeId = resumes[0]?.id || 'demo-resume-1';
        const [anData, roData] = await Promise.all([
          ApiClient.getAnalysis(resumeId),
          ApiClient.getRecommendations(resumeId)
        ]);
        setAnalysis(anData);
        setRoles(roData);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  if (loading || !analysis) {
    return (
      <div className="flex h-96 items-center justify-center">
        <div className="text-center space-y-3">
          <div className="h-8 w-8 animate-spin rounded-full border-2 border-indigo-500 border-t-transparent mx-auto" />
          <p className="text-xs text-slate-400">Loading AI Intelligence Engine...</p>
        </div>
      </div>
    );
  }

  const pInfo = analysis.parsed_data.personal_info;

  return (
    <div className="space-y-8">
      {/* Welcome Banner */}
      <div className="rounded-3xl border border-slate-800 bg-gradient-to-r from-slate-900 via-indigo-950/20 to-slate-900 p-6 sm:p-8">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div>
            <span className="inline-flex items-center gap-1.5 rounded-full bg-indigo-500/10 border border-indigo-500/20 px-3 py-1 text-xs font-semibold text-indigo-400 mb-3">
              <Sparkles className="h-3.5 w-3.5" />
              Comprehensive Resume Intelligence
            </span>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
              {pInfo.full_name || 'Candidate'}
            </h1>
            <p className="text-xs sm:text-sm text-slate-400 mt-1 max-w-2xl leading-relaxed">
              {analysis.parsed_data.summary || 'AI-analyzed candidate profile with verified technical competencies, ATS compatibility ratings, and tailored career trajectories.'}
            </p>
          </div>

          <div className="flex items-center gap-3">
            <Link
              to="/matcher"
              className="inline-flex items-center gap-2 rounded-xl border border-slate-700 bg-slate-800/80 px-4 py-2.5 text-xs font-semibold text-slate-200 hover:bg-slate-700 transition"
            >
              <Briefcase className="h-4 w-4 text-indigo-400" />
              <span>Match Job Description</span>
            </Link>
            <Link
              to="/improver"
              className="inline-flex items-center gap-2 rounded-xl bg-indigo-600 px-4 py-2.5 text-xs font-semibold text-white hover:bg-indigo-500 shadow-md shadow-indigo-600/30 transition"
            >
              <Sparkles className="h-4 w-4" />
              <span>AI Section Improver</span>
            </Link>
          </div>
        </div>
      </div>

      {/* Top Stat Gauges & Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
        <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-5 flex flex-col items-center justify-between">
          <ScoreGauge score={analysis.overall_score} label="Overall Resume Score" />
          <p className="text-xs text-slate-400 text-center px-4">
            Weighted across Experience (25%), Skills (25%), Formatting (20%), Education (15%), and Completeness (15%).
          </p>
        </div>

        <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-5 flex flex-col items-center justify-between">
          <ScoreGauge score={analysis.ats_score} label="ATS Compatibility Score" />
          <div className="w-full text-center mt-2">
            <span className="inline-flex items-center gap-1 text-xs font-bold text-emerald-400 bg-emerald-500/10 px-2.5 py-1 rounded-full border border-emerald-500/20">
              {analysis.ats_report.verdict}
            </span>
          </div>
        </div>

        <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-6 flex flex-col justify-between">
          <div>
            <span className="text-xs font-bold uppercase tracking-wider text-slate-400">Inventory Summary</span>
            <div className="grid grid-cols-2 gap-4 mt-4">
              <div className="rounded-xl bg-slate-950/60 p-3 border border-slate-800">
                <span className="text-2xl font-black text-white">{analysis.extracted_skills_count}</span>
                <span className="text-[11px] block text-slate-400 mt-0.5">Verified Skills</span>
              </div>
              <div className="rounded-xl bg-slate-950/60 p-3 border border-slate-800">
                <span className="text-2xl font-black text-indigo-400">{analysis.parsed_data.experience.length}</span>
                <span className="text-[11px] block text-slate-400 mt-0.5">Work Roles</span>
              </div>
              <div className="rounded-xl bg-slate-950/60 p-3 border border-slate-800">
                <span className="text-2xl font-black text-cyan-400">{analysis.parsed_data.projects.length}</span>
                <span className="text-[11px] block text-slate-400 mt-0.5">Projects</span>
              </div>
              <div className="rounded-xl bg-slate-950/60 p-3 border border-slate-800">
                <span className="text-2xl font-black text-violet-400">{analysis.parsed_data.certifications.length}</span>
                <span className="text-[11px] block text-slate-400 mt-0.5">Certifications</span>
              </div>
            </div>
          </div>

          <Link
            to="/analysis"
            className="mt-4 inline-flex items-center justify-center gap-1.5 text-xs font-semibold text-indigo-400 hover:text-indigo-300"
          >
            <span>View Full Audit Details</span>
            <ArrowRight className="h-3.5 w-3.5" />
          </Link>
        </div>
      </div>

      {/* Main Breakdown & Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-6">
            <h3 className="text-base font-bold text-white mb-4">Category-Wise Evaluation Breakdown</h3>
            <ScoreBreakdown breakdown={analysis.score_breakdown} />
          </div>

          <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-6">
            <h3 className="text-base font-bold text-white mb-4">Technical Skill Category Distribution</h3>
            <SkillGapChart categorizedSkills={analysis.parsed_data.categorized_skills} />
          </div>
        </div>

        {/* Strengths & Weaknesses Sidebar */}
        <div className="space-y-6">
          <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-5 space-y-4">
            <div className="flex items-center gap-2 text-emerald-400 font-bold text-sm">
              <CheckCircle2 className="h-4 w-4" />
              <span>Identified Key Strengths</span>
            </div>
            <div className="space-y-3">
              {analysis.strengths.slice(0, 3).map((s, idx) => (
                <div key={idx} className="rounded-xl bg-slate-950/50 p-3 border border-slate-800">
                  <h5 className="text-xs font-bold text-slate-200">{s.title}</h5>
                  <p className="text-[11px] text-slate-400 mt-1 leading-relaxed">{s.description}</p>
                </div>
              ))}
            </div>
          </div>

          <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-5 space-y-4">
            <div className="flex items-center gap-2 text-amber-400 font-bold text-sm">
              <AlertTriangle className="h-4 w-4" />
              <span>Actionable Improvements</span>
            </div>
            <div className="space-y-3">
              {analysis.weaknesses.slice(0, 3).map((w, idx) => (
                <div key={idx} className="rounded-xl bg-slate-950/50 p-3 border border-slate-800">
                  <h5 className="text-xs font-bold text-slate-200">{w.title}</h5>
                  <p className="text-[11px] text-slate-400 mt-1 leading-relaxed">{w.actionable_tip}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Recommended Job Roles */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-lg font-bold text-white">Recommended Job Roles</h3>
            <p className="text-xs text-slate-400">
              Matched against industry benchmark requirements with quantified skill fit.
            </p>
          </div>
          <Link
            to="/roadmap"
            className="inline-flex items-center gap-1 text-xs font-semibold text-indigo-400 hover:text-indigo-300"
          >
            <span>Explore All 12 Roles</span>
            <ArrowRight className="h-3.5 w-3.5" />
          </Link>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
          {roles.slice(0, 3).map((role) => (
            <RoleMatchCard key={role.role_id} role={role} />
          ))}
        </div>
      </div>
    </div>
  );
};
