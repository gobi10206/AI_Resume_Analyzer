import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  UploadCloud,
  FileCheck2,
  Briefcase,
  GitFork,
  Sparkles,
  ShieldCheck,
  FileText
} from 'lucide-react';

const NAV_ITEMS = [
  { label: 'Dashboard', path: '/', icon: LayoutDashboard },
  { label: 'Upload & Parse', path: '/upload', icon: UploadCloud },
  { label: 'Analysis Audit', path: '/analysis', icon: FileCheck2 },
  { label: 'Job Description Matcher', path: '/matcher', icon: Briefcase },
  { label: 'Career Roadmap', path: '/roadmap', icon: GitFork },
  { label: 'AI Resume Improver', path: '/improver', icon: Sparkles },
];

export const Sidebar: React.FC = () => {
  return (
    <aside className="hidden lg:flex w-64 flex-col border-r border-slate-800 bg-slate-950/60 p-4 shrink-0">
      <div className="px-3 py-2 text-xs font-bold uppercase tracking-wider text-slate-500">
        Navigation
      </div>
      <nav className="space-y-1.5 mt-2">
        {NAV_ITEMS.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                `flex items-center gap-3 rounded-xl px-3.5 py-2.5 text-sm font-medium transition-all ${
                  isActive
                    ? 'bg-indigo-600/15 text-indigo-400 border border-indigo-500/30 shadow-sm'
                    : 'text-slate-400 hover:bg-slate-900/80 hover:text-slate-200'
                }`
              }
            >
              <Icon className="h-4 w-4 shrink-0" />
              <span>{item.label}</span>
            </NavLink>
          );
        })}
      </nav>

      <div className="mt-auto border-t border-slate-800/80 pt-4">
        <div className="rounded-xl bg-slate-900/60 border border-slate-800 p-3.5">
          <div className="flex items-center gap-2 text-xs font-semibold text-emerald-400 mb-1">
            <ShieldCheck className="h-4 w-4" />
            <span>ATS Engine Ready</span>
          </div>
          <p className="text-[11px] text-slate-400 leading-relaxed">
            9-factor ATS compatibility verification & explainable scoring algorithm.
          </p>
        </div>
      </div>
    </aside>
  );
};
