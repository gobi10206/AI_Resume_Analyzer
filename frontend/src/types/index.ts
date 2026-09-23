export interface User {
  id: string;
  email: string;
  full_name?: string;
  created_at?: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export interface ResumeListItem {
  id: string;
  file_name: string;
  file_type: string;
  file_size: number;
  version: number;
  created_at: string;
  has_analysis: boolean;
}

export interface ParsedPersonalInfo {
  full_name?: string;
  email?: string;
  phone?: string;
  location?: string;
  linkedin?: string;
  github?: string;
  portfolio?: string;
}

export interface ParsedEducation {
  degree?: string;
  institution?: string;
  field_of_study?: string;
  graduation_year?: string;
  gpa?: string;
}

export interface ParsedExperience {
  job_title?: string;
  company?: string;
  location?: string;
  start_date?: string;
  end_date?: string;
  duration_months?: number;
  bullet_points: string[];
}

export interface ParsedProject {
  title?: string;
  description?: string;
  technologies: string[];
  link?: string;
}

export interface ParsedResumeData {
  personal_info: ParsedPersonalInfo;
  summary?: string;
  skills: string[];
  categorized_skills: Record<string, string[]>;
  education: ParsedEducation[];
  experience: ParsedExperience[];
  projects: ParsedProject[];
  certifications: string[];
  languages: string[];
  estimated_experience_years: number;
}

export interface CategoryScore {
  category: string;
  score: number;
  max_score: number;
  percentage: number;
  feedback: string;
}

export interface ScoreBreakdown {
  contact_and_completeness: CategoryScore;
  experience_and_impact: CategoryScore;
  skills_and_relevance: CategoryScore;
  education_and_certifications: CategoryScore;
  formatting_and_structure: CategoryScore;
}

export interface StrengthWeaknessItem {
  title: string;
  description: string;
  impact: 'High' | 'Medium' | 'Low';
  actionable_tip: string;
}

export interface AtsCheckItem {
  check_name: string;
  status: 'passed' | 'warning' | 'failed';
  details: string;
  recommendation?: string;
}

export interface AtsReport {
  ats_score: number;
  verdict: string;
  passed_checks_count: number;
  total_checks_count: number;
  checks: AtsCheckItem[];
  formatting_notes: string[];
}

export interface AnalysisResponse {
  id: string;
  resume_id: string;
  overall_score: number;
  ats_score: number;
  score_breakdown: ScoreBreakdown;
  strengths: StrengthWeaknessItem[];
  weaknesses: StrengthWeaknessItem[];
  ats_report: AtsReport;
  parsed_data: ParsedResumeData;
  extracted_skills_count: number;
  created_at: string;
}

export interface RoleMatchItem {
  role_id: string;
  role_title: string;
  department: string;
  match_percentage: number;
  matching_skills: string[];
  missing_skills: string[];
  skill_gap_percentage: number;
  suggested_learning_path: Array<{
    step: number;
    title: string;
    description: string;
  }>;
  recommended_projects: Array<{
    title: string;
    description: string;
    tech_stack: string[];
  }>;
  recommended_certifications: string[];
}

export interface JobDescriptionMatchResponse {
  overall_match_percentage: number;
  semantic_similarity: number;
  skill_match_percentage: number;
  matching_skills: string[];
  missing_skills: string[];
  qualification_gap?: string;
  experience_gap?: string;
  keyword_gaps: string[];
  ats_compatibility_verdict: string;
  recommendations: string[];
}

export interface CareerRoadmapPhase {
  phase_number: number;
  duration: string;
  title: string;
  focus_skills: string[];
  milestones: string[];
  recommended_courses: string[];
  recommended_projects: Array<{
    name: string;
    description: string;
    tech_stack: string[];
  }>;
}

export interface CareerRoadmapResponse {
  target_role: string;
  readiness_level: string;
  current_match_score: number;
  estimated_timeframe: string;
  phases: CareerRoadmapPhase[];
  recommended_certifications: string[];
  portfolio_improvements: string[];
}

export interface ResumeImprovementResponse {
  section: string;
  original_content?: string;
  improved_content: string;
  changes_made: string[];
  key_metrics_added: string[];
  power_words_used: string[];
  ats_impact_summary: string;
}
