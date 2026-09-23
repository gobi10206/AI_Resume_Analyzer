import React, { useState, useRef } from 'react';
import { UploadCloud, FileText, CheckCircle2, AlertCircle, Loader2 } from 'lucide-react';
import { ApiClient } from '../services/api';

interface FileUploadProps {
  onSuccess: (resumeId: string) => void;
}

export const FileUpload: React.FC<FileUploadProps> = ({ onSuccess }) => {
  const [dragActive, setDragActive] = useState(false);
  const [file, setFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [error, setError] = useState<string | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const validateFile = (selectedFile: File): boolean => {
    setError(null);
    const validExts = ['.pdf', '.docx', '.txt'];
    const name = selectedFile.name.toLowerCase();
    const isVal = validExts.some((ext) => name.endsWith(ext));
    if (!isVal) {
      setError('Please upload a valid PDF, DOCX, or TXT resume.');
      return false;
    }
    if (selectedFile.size > 15 * 1024 * 1024) {
      setError('File exceeds 15MB limit.');
      return false;
    }
    return true;
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const dropped = e.dataTransfer.files[0];
      if (validateFile(dropped)) {
        setFile(dropped);
      }
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const selected = e.target.files[0];
      if (validateFile(selected)) {
        setFile(selected);
      }
    }
  };

  const handleUpload = async () => {
    if (!file) return;
    setIsUploading(true);
    setUploadProgress(20);

    const interval = setInterval(() => {
      setUploadProgress((prev) => (prev >= 90 ? 90 : prev + 15));
    }, 200);

    try {
      const res = await ApiClient.uploadResume(file);
      clearInterval(interval);
      setUploadProgress(100);
      setTimeout(() => {
        setIsUploading(false);
        onSuccess(res.id);
      }, 500);
    } catch (err: any) {
      clearInterval(interval);
      setIsUploading(false);
      setError(err.message || 'Upload failed');
    }
  };

  const loadSampleResume = () => {
    const sampleText = `Alex Rivera
alex.rivera@example.com | (555) 349-2018 | San Francisco, CA
linkedin.com/in/alexrivera-tech | github.com/alexrivera-dev

SUMMARY
Innovative Full Stack Engineer with 4+ years designing scalable microservices.

EXPERIENCE
Senior Software Engineer at CloudScale Systems (Jan 2022 - Present)
• Architected cloud-native distributed backend services using Python, FastAPI, and PostgreSQL, improving throughput by 42%.
• Deployed Kubernetes clusters across AWS using Terraform and GitHub Actions.

EDUCATION
B.S. in Computer Science - UC Berkeley (2016-2020) | GPA: 3.85 / 4.0

TECHNICAL SKILLS
Python, TypeScript, React, FastAPI, Docker, Kubernetes, AWS, PostgreSQL, Redis`;

    const sampleFile = new File([sampleText], 'Sample_FullStack_Resume.txt', { type: 'text/plain' });
    setFile(sampleFile);
    setError(null);
  };

  return (
    <div className="space-y-4">
      <div
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        onClick={() => inputRef.current?.click()}
        className={`relative flex flex-col items-center justify-center rounded-2xl border-2 border-dashed p-8 text-center cursor-pointer transition-all ${
          dragActive
            ? 'border-indigo-500 bg-indigo-950/20'
            : 'border-slate-800 bg-slate-900/40 hover:border-slate-700 hover:bg-slate-900/60'
        }`}
      >
        <input
          ref={inputRef}
          type="file"
          accept=".pdf,.docx,.txt"
          onChange={handleChange}
          className="hidden"
        />

        <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-indigo-600/10 border border-indigo-500/20 text-indigo-400 mb-3 shadow-inner">
          <UploadCloud className="h-7 w-7" />
        </div>

        <h4 className="text-base font-bold text-white mb-1">
          {file ? file.name : 'Drag & drop your resume file here'}
        </h4>
        <p className="text-xs text-slate-400 mb-3">
          Supported formats: PDF, DOCX, TXT (Maximum file size: 15MB)
        </p>

        {file && (
          <div className="inline-flex items-center gap-2 rounded-lg bg-slate-800/80 px-3 py-1.5 text-xs text-slate-300">
            <FileText className="h-4 w-4 text-indigo-400" />
            <span>{(file.size / 1024).toFixed(1)} KB</span>
          </div>
        )}
      </div>

      {error && (
        <div className="flex items-center gap-2 rounded-xl bg-rose-950/30 border border-rose-800/40 p-3 text-xs text-rose-300">
          <AlertCircle className="h-4 w-4 shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {isUploading && (
        <div className="space-y-2">
          <div className="flex justify-between text-xs text-slate-400">
            <span>Parsing document structure & running NLP entity extraction...</span>
            <span className="font-bold text-indigo-400">{uploadProgress}%</span>
          </div>
          <div className="h-2 w-full rounded-full bg-slate-800 overflow-hidden">
            <div
              className="h-full rounded-full bg-gradient-to-r from-indigo-500 to-violet-500 transition-all duration-300"
              style={{ width: `${uploadProgress}%` }}
            />
          </div>
        </div>
      )}

      <div className="flex flex-col sm:flex-row items-center justify-between gap-3 pt-2">
        <button
          type="button"
          onClick={loadSampleResume}
          className="text-xs text-indigo-400 hover:text-indigo-300 underline underline-offset-4 font-medium"
        >
          Load pre-filled sample candidate resume
        </button>

        <button
          type="button"
          disabled={!file || isUploading}
          onClick={handleUpload}
          className="w-full sm:w-auto inline-flex items-center justify-center gap-2 rounded-xl bg-indigo-600 px-6 py-2.5 text-sm font-semibold text-white shadow-md shadow-indigo-600/30 hover:bg-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed transition"
        >
          {isUploading ? (
            <>
              <Loader2 className="h-4 w-4 animate-spin" />
              <span>Analyzing Resume...</span>
            </>
          ) : (
            <>
              <UploadCloud className="h-4 w-4" />
              <span>Run AI Analysis</span>
            </>
          )}
        </button>
      </div>
    </div>
  );
};
