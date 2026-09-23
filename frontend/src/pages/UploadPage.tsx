import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { FileUpload } from '../components/FileUpload';
import { ApiClient } from '../services/api';
import { ResumeListItem } from '../types';
import { FileText, Trash2, CheckCircle2, ArrowRight } from 'lucide-react';

export const UploadPage: React.FC = () => {
  const navigate = useNavigate();
  const [resumes, setResumes] = useState<ResumeListItem[]>([]);
  const [loading, setLoading] = useState(true);

  const loadList = async () => {
    try {
      const data = await ApiClient.listResumes();
      setResumes(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadList();
  }, []);

  const handleUploadSuccess = (resumeId: string) => {
    navigate('/analysis');
  };

  const handleDelete = async (id: string) => {
    if (confirm('Permanently delete this resume version and associated analytics?')) {
      await ApiClient.deleteResume(id);
      loadList();
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      <div>
        <h2 className="text-2xl font-extrabold text-white">Resume Document Ingestion</h2>
        <p className="text-xs sm:text-sm text-slate-400 mt-1">
          Upload PDF, DOCX, or TXT resumes for natural language parsing, entity recognition, and ATS scoring.
        </p>
      </div>

      <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-6">
        <FileUpload onSuccess={handleUploadSuccess} />
      </div>

      {/* Uploaded Versions List */}
      <div className="space-y-4">
        <h3 className="text-sm font-bold uppercase tracking-wider text-slate-400">
          Saved Resume Versions
        </h3>

        {resumes.length === 0 ? (
          <div className="rounded-xl border border-slate-800 bg-slate-900/30 p-8 text-center text-xs text-slate-500">
            No resume versions saved yet. Upload your first document above.
          </div>
        ) : (
          <div className="space-y-3">
            {resumes.map((r) => (
              <div
                key={r.id}
                className="flex items-center justify-between rounded-xl border border-slate-800 bg-slate-900/60 p-4 hover:border-slate-700 transition"
              >
                <div className="flex items-center gap-3">
                  <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-indigo-500/10 text-indigo-400">
                    <FileText className="h-5 w-5" />
                  </div>
                  <div>
                    <h5 className="text-sm font-semibold text-white">{r.file_name}</h5>
                    <span className="text-[11px] text-slate-400">
                      Version {r.version} • {(r.file_size / 1024).toFixed(1)} KB • {r.created_at}
                    </span>
                  </div>
                </div>

                <div className="flex items-center gap-3">
                  <button
                    onClick={() => navigate('/analysis')}
                    className="inline-flex items-center gap-1.5 rounded-lg bg-indigo-600/10 border border-indigo-500/20 px-3 py-1.5 text-xs font-semibold text-indigo-300 hover:bg-indigo-600/20 transition"
                  >
                    <span>View Audit</span>
                    <ArrowRight className="h-3.5 w-3.5" />
                  </button>

                  <button
                    onClick={() => handleDelete(r.id)}
                    className="flex h-8 w-8 items-center justify-center rounded-lg border border-slate-800 text-slate-400 hover:border-rose-800 hover:text-rose-400 transition"
                  >
                    <Trash2 className="h-4 w-4" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
