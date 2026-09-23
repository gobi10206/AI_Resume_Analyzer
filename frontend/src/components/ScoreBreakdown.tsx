import React from 'react';
import { ScoreBreakdown as ScoreBreakdownType } from '../types';
import { CheckCircle2, AlertCircle } from 'lucide-react';

interface ScoreBreakdownProps {
  breakdown: ScoreBreakdownType;
}

export const ScoreBreakdown: React.FC<ScoreBreakdownProps> = ({ breakdown }) => {
  const categories = Object.values(breakdown);

  return (
    <div className="space-y-4">
      {categories.map((cat) => {
        let barColor = 'bg-emerald-500';
        if (cat.percentage < 60) barColor = 'bg-rose-500';
        else if (cat.percentage < 80) barColor = 'bg-amber-500';

        return (
          <div key={cat.category} className="rounded-xl border border-slate-800 bg-slate-900/50 p-4 transition hover:border-slate-700">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-semibold text-slate-200">{cat.category}</span>
              <div className="flex items-center gap-2">
                <span className="text-xs text-slate-400">Weight {cat.max_score} pts</span>
                <span className="text-sm font-bold text-white">{cat.score} / {cat.max_score}</span>
              </div>
            </div>

            {/* Progress Bar */}
            <div className="h-2 w-full rounded-full bg-slate-800 overflow-hidden mb-2">
              <div
                className={`h-full rounded-full ${barColor} transition-all duration-700`}
                style={{ width: `${cat.percentage}%` }}
              />
            </div>

            {/* Feedback */}
            <p className="text-xs text-slate-400 leading-relaxed">
              {cat.feedback}
            </p>
          </div>
        );
      })}
    </div>
  );
};
