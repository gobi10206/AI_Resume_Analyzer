import React from 'react';
import { AtsReport as AtsReportType } from '../types';
import { CheckCircle2, AlertTriangle, XCircle, Info } from 'lucide-react';

interface AtsReportProps {
  report: AtsReportType;
}

export const AtsReport: React.FC<AtsReportProps> = ({ report }) => {
  return (
    <div className="space-y-6">
      {/* Overview Banner */}
      <div className="rounded-2xl border border-indigo-500/20 bg-indigo-950/20 p-5 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="text-xs font-bold uppercase tracking-wider text-indigo-400">ATS Verdict</span>
          </div>
          <h3 className="text-xl font-bold text-white mt-0.5">{report.verdict}</h3>
          <p className="text-xs text-slate-400 mt-1">
            Passed {report.passed_checks_count} of {report.total_checks_count} automated applicant tracking checks.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <div className="text-right">
            <span className="text-xs font-semibold text-slate-400">ATS Score</span>
            <div className="text-2xl font-black text-emerald-400">{Math.round(report.ats_score)}%</div>
          </div>
        </div>
      </div>

      {/* Checklist */}
      <div className="space-y-3">
        <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400 px-1">
          Automated Compatibility Audits
        </h4>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3.5">
          {report.checks.map((check) => {
            let Icon = CheckCircle2;
            let iconColor = 'text-emerald-400';
            let borderColor = 'border-slate-800/80';
            let bgBadge = 'bg-emerald-500/10 text-emerald-400';

            if (check.status === 'warning') {
              Icon = AlertTriangle;
              iconColor = 'text-amber-400';
              borderColor = 'border-amber-500/30';
              bgBadge = 'bg-amber-500/10 text-amber-400';
            } else if (check.status === 'failed') {
              Icon = XCircle;
              iconColor = 'text-rose-400';
              borderColor = 'border-rose-500/30';
              bgBadge = 'bg-rose-500/10 text-rose-400';
            }

            return (
              <div key={check.check_name} className={`rounded-xl border ${borderColor} bg-slate-900/60 p-4 transition flex flex-col justify-between`}>
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm font-semibold text-slate-200">{check.check_name}</span>
                    <span className={`text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full ${bgBadge}`}>
                      {check.status}
                    </span>
                  </div>
                  <p className="text-xs text-slate-400 leading-relaxed mb-3">
                    {check.details}
                  </p>
                </div>

                {check.recommendation && (
                  <div className="mt-2 rounded-lg bg-slate-950/60 p-2.5 text-[11px] text-amber-300/90 flex items-start gap-1.5 border border-amber-500/10">
                    <Info className="h-3.5 w-3.5 shrink-0 mt-0.5" />
                    <span>{check.recommendation}</span>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};
