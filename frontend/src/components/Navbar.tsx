import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Cpu, UploadCloud, Bell, User as UserIcon, LogOut } from 'lucide-react';
import { ApiClient } from '../services/api';

export const Navbar: React.FC = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    ApiClient.clearToken();
    navigate('/login');
  };

  return (
    <header className="sticky top-0 z-40 w-full border-b border-slate-800 bg-slate-950/80 backdrop-blur-md">
      <div className="flex h-16 items-center justify-between px-6">
        <div className="flex items-center gap-3">
          <Link to="/" className="flex items-center gap-2.5 font-bold text-xl tracking-tight text-white hover:opacity-95 transition">
            <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-tr from-indigo-600 to-violet-500 shadow-md shadow-indigo-500/20">
              <Cpu className="h-5 w-5 text-white" />
            </div>
            <span>AI Resume<span className="text-indigo-400">Analyzer</span></span>
          </Link>
          <span className="hidden md:inline-flex items-center rounded-md bg-indigo-500/10 px-2 py-0.5 text-xs font-semibold text-indigo-400 border border-indigo-500/20">
            v1.0 Production
          </span>
        </div>

        <div className="flex items-center gap-3">
          <Link
            to="/upload"
            className="flex items-center gap-2 rounded-lg bg-indigo-600 px-3.5 py-2 text-sm font-semibold text-white shadow-sm shadow-indigo-600/30 hover:bg-indigo-500 transition active:scale-[0.98]"
          >
            <UploadCloud className="h-4 w-4" />
            <span className="hidden sm:inline">Upload Resume</span>
          </Link>

          <button
            onClick={handleLogout}
            title="Sign Out"
            className="flex h-9 w-9 items-center justify-center rounded-lg border border-slate-800 bg-slate-900/80 text-slate-400 hover:border-slate-700 hover:text-rose-400 transition"
          >
            <LogOut className="h-4 w-4" />
          </button>
        </div>
      </div>
    </header>
  );
};
