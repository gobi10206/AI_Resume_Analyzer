import React from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell
} from 'recharts';

interface SkillGapChartProps {
  categorizedSkills: Record<string, string[]>;
}

export const SkillGapChart: React.FC<SkillGapChartProps> = ({ categorizedSkills }) => {
  const data = Object.entries(categorizedSkills).map(([cat, skills]) => {
    const label = cat
      .replace(/_/g, ' ')
      .replace(/\b\w/g, (l) => l.toUpperCase());
    return {
      category: label,
      count: skills.length
    };
  });

  const COLORS = ['#6366f1', '#8b5cf6', '#ec4899', '#06b6d4', '#10b981', '#f59e0b', '#3b82f6'];

  if (data.length === 0) {
    return (
      <div className="flex h-48 items-center justify-center text-xs text-slate-500">
        No categorized skills data available.
      </div>
    );
  }

  return (
    <div className="w-full h-64">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data} margin={{ top: 10, right: 10, left: -20, bottom: 20 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
          <XAxis
            dataKey="category"
            stroke="#64748b"
            fontSize={11}
            tickLine={false}
            angle={-15}
            textAnchor="end"
          />
          <YAxis stroke="#64748b" fontSize={11} tickLine={false} />
          <Tooltip
            contentStyle={{
              backgroundColor: '#0f172a',
              borderColor: '#334155',
              borderRadius: '8px',
              fontSize: '12px',
              color: '#f8fafc'
            }}
          />
          <Bar dataKey="count" radius={[4, 4, 0, 0]}>
            {data.map((_, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};
