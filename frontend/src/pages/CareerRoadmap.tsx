import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { ApiClient } from '../services/api';
import { CareerRoadmapResponse, RoleMatchItem } from '../types';
import { RoadmapTimeline } from '../components/RoadmapTimeline';
import { GitFork, Award, CheckCircle2, ArrowUpRight, Sparkles, Loader2 } from 'lucide-react';

export const CareerRoadmap: React.FC = () => {
  const [searchParams] = useSearchParams();
  const roleFromQuery = searchParams.get('role');

  const [roles, setRoles] = useState<RoleMatchItem[]>([]);
  const [selectedRole, setSelectedRole] = useState<string>(roleFromQuery || 'Full Stack Engineer');
  const [roadmap, setRoadmap] = useState<CareerRoadmapResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);

  useEffect(() => {
    async function loadRoles() {
      try {
        const resumes = await ApiClient.listResumes();
        const resumeId = resumes[0]?.id || 'demo-resume-1';
        const recs = await ApiClient.getRecommendations(resumeId);
        setRoles(recs);

        const target = roleFromQuery || (recs[0]?.role_title || 'Full Stack Engineer');
        setSelectedRole(target);

        const rm = await ApiClient.generateRoadmap(resumeId, target);
        setRoadmap(rm);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
    loadRoles();
  }, [roleFromQuery]);

  const handleRoleChange = async (newRole: string) => {
    setSelectedRole(newRole);
    setGenerating(true);
    try {
      const resumes = await ApiClient.listResumes();
      const resumeId = resumes[0]?.id || 'demo-resume-1';
      const rm = await ApiClient.generateRoadmap(resumeId, newRole);
      setRoadmap(rm);
    } catch (err) {
      console.error(err);
    } finally {
      setGenerating(false);
    }
  };

  if (loading || !roadmap) {
    return (
      <div className="flex h-96 items-center justify-center">
        <div className="h-8 w-8 animate-spin rounded-full border-2 border-indigo-500 border-t-transparent" />
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Header Banner */}
      <div className="rounded-3xl border border-slate-800 bg-gradient-to-r from-slate-900 via-indigo-950/20 to-slate-900 p-6 sm:p-8">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div>
            <span className="inline-flex items-center gap-1.5 rounded-full bg-indigo-500/10 border border-indigo-500/20 px-3 py-1 text-xs font-semibold text-indigo-400 mb-2">
              <GitFork className="h-3.5 w-3.5" />
              Target Career Trajectory
            </span>
            <h2 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
              {roadmap.target_role}
            </h2>
            <p className="text-xs sm:text-sm text-slate-400 mt-1 max-w-xl">
              Personalized {roadmap.estimated_timeframe} skill acquisition timeline and capstone milestone sequence.
            </p>
          </div>

          <div className="flex items-center gap-3">
            <div className="rounded-2xl bg-slate-950/80 border border-slate-800 p-4 text-center sm:text-right">
              <span className="text-[11px] font-bold uppercase tracking-wider text-slate-400 block">Current Readiness</span>
              <span className="text-xl font-extrabold text-indigo-400">{Math.round(roadmap.current_match_score)}% Match</span>
            </div>
          </div>
        </div>
      </div>

      {/* Role Selection Tabs */}
      <div>
        <span className="text-xs font-bold uppercase tracking-wider text-slate-400 block mb-3">
          Select Target Industry Role
        </span>
        <div className="flex flex-wrap gap-2">
          {roles.map((r) => (
            <button
              key={r.role_id}
              onClick={() => handleRoleChange(r.role_title)}
              className={`rounded-xl px-3.5 py-2 text-xs font-semibold transition flex items-center gap-2 ${
                selectedRole === r.role_title
                  ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/30'
                  : 'bg-slate-900/80 text-slate-400 border border-slate-800 hover:border-slate-700 hover:text-slate-200'
              }`}
            >
              <span>{r.role_title}</span>
              <span className={`text-[10px] px-1.5 py-0.2 rounded-full ${
                selectedRole === r.role_title ? 'bg-indigo-700 text-indigo-100' : 'bg-slate-800 text-slate-400'
              }`}>
                {Math.round(r.match_percentage)}%
              </span>
            </button>
          ))}
        </div>
      </div>

      {generating ? (
        <div className="flex h-64 items-center justify-center gap-2 text-xs text-slate-400">
          <Loader2 className="h-5 w-5 animate-spin text-indigo-500" />
          <span>Generating customized skill timeline for {selectedRole}...</span>
        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Timeline */}
          <div className="lg:col-span-2 space-y-6">
            <h3 className="text-base font-bold text-white">4-Phase Development Milestones</h3>
            <RoadmapTimeline phases={roadmap.phases} />
          </div>

          {/* Right Sidebar: Certs & Portfolio */}
          <div className="space-y-6">
            {/* Certifications */}
            <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-5 space-y-3">
              <div className="flex items-center gap-2 text-violet-400 font-bold text-sm">
                <Award className="h-4 w-4" />
                <span>Recommended Certifications</span>
              </div>
              <div className="space-y-2">
                {roadmap.recommended_certifications.map((c, i) => (
                  <div key={i} className="rounded-xl bg-slate-950/50 p-3 border border-slate-800 text-xs text-slate-300 font-medium">
                    {c}
                  </div>
                ))}
              </div>
            </div>

            {/* Portfolio Improvements */}
            <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-5 space-y-3">
              <div className="flex items-center gap-2 text-cyan-400 font-bold text-sm">
                <Sparkles className="h-4 w-4" />
                <span>Portfolio Polish Checklist</span>
              </div>
              <div className="space-y-2 text-xs text-slate-400">
                {roadmap.portfolio_improvements.map((item, idx) => (
                  <div key={idx} className="flex items-start gap-2">
                    <CheckCircle2 className="h-4 w-4 text-emerald-400 shrink-0 mt-0.5" />
                    <span>{item}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
