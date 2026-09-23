import React from 'react';
import { CareerRoadmapPhase } from '../types';
import { CheckCircle2, Clock, BookOpen, Layers } from 'lucide-react';

interface RoadmapTimelineProps {
  phases: CareerRoadmapPhase[];
}

export const RoadmapTimeline: React.FC<RoadmapTimelineProps> = ({ phases }) => {
  return (
    <div className="relative pl-6 sm:pl-8 space-y-8 before:absolute before:left-3 before:top-2 before:bottom-2 before:w-0.5 before:bg-slate-800">
      {phases.map((phase) => (
        <div key={phase.phase_number} className="relative">
          {/* Timeline bullet dot */}
          <div className="absolute -left-6 sm:-left-8 top-1.5 flex h-6 w-6 items-center justify-center rounded-full bg-slate-900 border-2 border-indigo-500 text-[10px] font-bold text-indigo-400">
            {phase.phase_number}
          </div>

          <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-5 transition hover:border-slate-700">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-3">
              <div>
                <span className="inline-flex items-center gap-1 text-xs font-semibold text-indigo-400">
                  <Clock className="h-3.5 w-3.5" />
                  {phase.duration}
                </span>
                <h4 className="text-base font-bold text-white mt-0.5">{phase.title}</h4>
              </div>

              <div className="flex flex-wrap gap-1">
                {phase.focus_skills.map((s) => (
                  <span key={s} className="rounded-md bg-indigo-500/10 border border-indigo-500/20 px-2 py-0.5 text-[11px] font-medium text-indigo-300">
                    {s}
                  </span>
                ))}
              </div>
            </div>

            {/* Milestones */}
            <div className="space-y-2 mb-4">
              <span className="text-[11px] font-bold uppercase tracking-wider text-slate-400 block">
                Key Deliverables & Milestones:
              </span>
              {phase.milestones.map((m, idx) => (
                <div key={idx} className="flex items-start gap-2 text-xs text-slate-300">
                  <CheckCircle2 className="h-4 w-4 text-emerald-400 shrink-0 mt-0.5" />
                  <span>{m}</span>
                </div>
              ))}
            </div>

            {/* Courses & Recommended Project */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3 pt-3 border-t border-slate-800/80">
              <div className="rounded-xl bg-slate-950/50 p-3 border border-slate-800/60">
                <div className="flex items-center gap-1.5 text-xs font-semibold text-slate-300 mb-1.5">
                  <BookOpen className="h-3.5 w-3.5 text-violet-400" />
                  <span>Recommended Study Path</span>
                </div>
                <ul className="space-y-1 text-xs text-slate-400">
                  {phase.recommended_courses.map((c, i) => (
                    <li key={i} className="truncate">• {c}</li>
                  ))}
                </ul>
              </div>

              {phase.recommended_projects[0] && (
                <div className="rounded-xl bg-slate-950/50 p-3 border border-slate-800/60">
                  <div className="flex items-center gap-1.5 text-xs font-semibold text-slate-300 mb-1.5">
                    <Layers className="h-3.5 w-3.5 text-cyan-400" />
                    <span>Capstone Project: {phase.recommended_projects[0].name}</span>
                  </div>
                  <p className="text-xs text-slate-400 line-clamp-2">
                    {phase.recommended_projects[0].description}
                  </p>
                </div>
              )}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};
