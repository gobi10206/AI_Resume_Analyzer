import React from 'react';
import { RoleMatchItem } from '../types';
import { Check, AlertCircle, ArrowRight, Award } from 'lucide-react';
import { Link } from 'react-router-dom';

interface RoleMatchCardProps {
  role: RoleMatchItem;
}

export const RoleMatchCard: React.FC<RoleMatchCardProps> = ({ role }) => {
  let badgeColor = 'bg-emerald-500/15 text-emerald-400 border-emerald-500/30';
  if (role.match_percentage < 70) badgeColor = 'bg-amber-500/15 text-amber-400 border-amber-500/30';

  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-5 transition hover:border-indigo-500/40 hover:shadow-lg hover:shadow-indigo-950/20 flex flex-col justify-between">
      <div>
        <div className="flex items-start justify-between gap-2 mb-3">
          <div>
            <span className="text-[11px] font-bold uppercase tracking-wider text-indigo-400">
              {role.department}
            </span>
            <h4 className="text-base font-bold text-white">{role.role_title}</h4>
          </div>
          <span className={`inline-flex items-center px-2.5 py-1 rounded-full text-xs font-extrabold border ${badgeColor}`}>
            {Math.round(role.match_percentage)}% Match
          </span>
        </div>

        {/* Matching Skills */}
        <div className="mb-3">
          <span className="text-[11px] font-semibold text-slate-400 block mb-1.5">
            Matching Competencies ({role.matching_skills.length}):
          </span>
          <div className="flex flex-wrap gap-1.5">
            {role.matching_skills.slice(0, 6).map((s) => (
              <span key={s} className="inline-flex items-center gap-1 rounded-md bg-emerald-950/40 border border-emerald-800/50 px-2 py-0.5 text-[11px] text-emerald-300">
                <Check className="h-3 w-3" />
                {s}
              </span>
            ))}
            {role.matching_skills.length > 6 && (
              <span className="text-[10px] text-slate-500 self-center">
                +{role.matching_skills.length - 6} more
              </span>
            )}
          </div>
        </div>

        {/* Missing Skills */}
        {role.missing_skills.length > 0 && (
          <div className="mb-4">
            <span className="text-[11px] font-semibold text-slate-400 block mb-1.5">
              Identified Skill Gaps ({role.missing_skills.length}):
            </span>
            <div className="flex flex-wrap gap-1.5">
              {role.missing_skills.slice(0, 4).map((s) => (
                <span key={s} className="inline-flex items-center gap-1 rounded-md bg-rose-950/30 border border-rose-800/40 px-2 py-0.5 text-[11px] text-rose-300">
                  <AlertCircle className="h-3 w-3" />
                  {s}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>

      <div className="pt-3 border-t border-slate-800/80 flex items-center justify-between">
        <div className="flex items-center gap-1.5 text-xs text-slate-400">
          <Award className="h-4 w-4 text-indigo-400" />
          <span>{role.recommended_certifications[0] || 'Certification Path'}</span>
        </div>
        <Link
          to={`/roadmap?role=${encodeURIComponent(role.role_title)}`}
          className="inline-flex items-center gap-1 text-xs font-semibold text-indigo-400 hover:text-indigo-300 transition"
        >
          <span>View Roadmap</span>
          <ArrowRight className="h-3.5 w-3.5" />
        </Link>
      </div>
    </div>
  );
};
