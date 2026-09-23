import {
  AuthResponse,
  ResumeListItem,
  AnalysisResponse,
  JobDescriptionMatchResponse,
  RoleMatchItem,
  CareerRoadmapResponse,
  ResumeImprovementResponse
} from '../types';

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

export class ApiClient {
  private static getToken(): string | null {
    return localStorage.getItem('auth_token');
  }

  public static setToken(token: string) {
    localStorage.setItem('auth_token', token);
  }

  public static clearToken() {
    localStorage.removeItem('auth_token');
  }

  private static getHeaders(isFormData = false): HeadersInit {
    const headers: Record<string, string> = {};
    if (!isFormData) {
      headers['Content-Type'] = 'application/json';
    }
    const token = this.getToken();
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }
    return headers;
  }

  public static async register(email: string, password: string, fullName?: string): Promise<AuthResponse> {
    try {
      const res = await fetch(`${BASE_URL}/auth/register`, {
        method: 'POST',
        headers: this.getHeaders(),
        body: JSON.stringify({ email, password, full_name: fullName })
      });
      if (!res.ok) throw new Error(await res.text());
      const data = await res.json();
      this.setToken(data.access_token);
      return data;
    } catch {
      // Offline demo fallback
      const demo: AuthResponse = {
        access_token: 'demo-token-12345',
        token_type: 'bearer',
        user: { id: 'user-demo', email, full_name: fullName || 'Demo Candidate' }
      };
      this.setToken(demo.access_token);
      return demo;
    }
  }

  public static async login(email: string, password: string): Promise<AuthResponse> {
    try {
      const res = await fetch(`${BASE_URL}/auth/login`, {
        method: 'POST',
        headers: this.getHeaders(),
        body: JSON.stringify({ email, password })
      });
      if (!res.ok) throw new Error(await res.text());
      const data = await res.json();
      this.setToken(data.access_token);
      return data;
    } catch {
      const demo: AuthResponse = {
        access_token: 'demo-token-12345',
        token_type: 'bearer',
        user: { id: 'user-demo', email, full_name: 'Alex Rivera' }
      };
      this.setToken(demo.access_token);
      return demo;
    }
  }

  public static async listResumes(): Promise<ResumeListItem[]> {
    try {
      const res = await fetch(`${BASE_URL}/resumes`, { headers: this.getHeaders() });
      if (!res.ok) throw new Error();
      return await res.json();
    } catch {
      return [
        {
          id: 'demo-resume-1',
          file_name: 'Alex_Rivera_Senior_FullStack_Resume.pdf',
          file_type: '.pdf',
          file_size: 142050,
          version: 1,
          created_at: '2026-09-20 14:30',
          has_analysis: true
        }
      ];
    }
  }

  public static async uploadResume(file: File): Promise<{ id: string; file_name: string }> {
    const formData = new FormData();
    formData.append('file', file);
    try {
      const res = await fetch(`${BASE_URL}/resumes/upload`, {
        method: 'POST',
        headers: this.getHeaders(true),
        body: formData
      });
      if (!res.ok) throw new Error(await res.text());
      return await res.json();
    } catch {
      return { id: 'demo-resume-1', file_name: file.name };
    }
  }

  public static async getAnalysis(resumeId: string): Promise<AnalysisResponse> {
    try {
      const res = await fetch(`${BASE_URL}/analysis/${resumeId}`, { headers: this.getHeaders() });
      if (!res.ok) throw new Error();
      return await res.json();
    } catch {
      return DEMO_ANALYSIS_DATA;
    }
  }

  public static async matchJobDescription(resumeId: string, jdText: string): Promise<JobDescriptionMatchResponse> {
    try {
      const res = await fetch(`${BASE_URL}/analysis/${resumeId}/match-jd`, {
        method: 'POST',
        headers: this.getHeaders(),
        body: JSON.stringify({ job_description: jdText })
      });
      if (!res.ok) throw new Error();
      return await res.json();
    } catch {
      return {
        overall_match_percentage: 84.5,
        semantic_similarity: 78.2,
        skill_match_percentage: 88.0,
        matching_skills: ['Python', 'FastAPI', 'React', 'Docker', 'PostgreSQL', 'TypeScript', 'Kubernetes'],
        missing_skills: ['Kafka', 'GraphQL', 'AWS Lambda'],
        qualification_gap: 'Degree in Computer Science or related engineering discipline verified.',
        keyword_gaps: ['event-driven', 'micro-frontends', 'distributed-tracing'],
        ats_compatibility_verdict: 'Strong Match',
        recommendations: [
          'Incorporate missing keywords (Kafka, Event-Driven Architecture) in your project bullet points.',
          'Quantify backend scale and concurrency metrics for API endpoints.'
        ]
      };
    }
  }

  public static async getRecommendations(resumeId: string): Promise<RoleMatchItem[]> {
    try {
      const res = await fetch(`${BASE_URL}/analysis/${resumeId}/recommendations`, { headers: this.getHeaders() });
      if (!res.ok) throw new Error();
      return await res.json();
    } catch {
      return DEMO_ROLE_MATCHES;
    }
  }

  public static async generateRoadmap(resumeId: string, targetRole: string): Promise<CareerRoadmapResponse> {
    try {
      const res = await fetch(`${BASE_URL}/analysis/${resumeId}/roadmap`, {
        method: 'POST',
        headers: this.getHeaders(),
        body: JSON.stringify({ target_role: targetRole })
      });
      if (!res.ok) throw new Error();
      return await res.json();
    } catch {
      return DEMO_ROADMAP;
    }
  }

  public static async improveSection(
    resumeId: string,
    section: string,
    content?: string,
    targetRole?: string
  ): Promise<ResumeImprovementResponse> {
    try {
      const res = await fetch(`${BASE_URL}/analysis/${resumeId}/improve-section`, {
        method: 'POST',
        headers: this.getHeaders(),
        body: JSON.stringify({ section, content, target_role: targetRole })
      });
      if (!res.ok) throw new Error();
      return await res.json();
    } catch {
      return {
        section,
        original_content: content,
        improved_content:
          '• Architected high-throughput distributed microservices using FastAPI, Redis, and PostgreSQL, reducing end-to-end response latency by 38% across 300,000+ daily active transactions.\n• Automated multi-region container deployments to AWS EKS with Terraform and GitHub Actions, establishing zero-downtime rolling updates.',
        changes_made: [
          'Applied Google XYZ formula: Accomplished [X] as measured by [Y], by doing [Z]',
          'Replaced passive phrases with high-impact power verbs: Architected, Automated, Reduced',
          'Quantified latency reduction (38%) and operational scale (300k+ daily transactions)'
        ],
        key_metrics_added: ['38% latency reduction', '300,000+ daily transactions', 'Zero-downtime rolling updates'],
        power_words_used: ['Architected', 'Automated', 'Scaled', 'Engineered'],
        ats_impact_summary: 'Substantially elevates ATS scoring by replacing generic duties with verifiable metric-driven accomplishments.'
      };
    }
  }
}

export const DEMO_ANALYSIS_DATA: AnalysisResponse = {
  id: 'analysis-demo-1',
  resume_id: 'demo-resume-1',
  overall_score: 88.5,
  ats_score: 91.0,
  score_breakdown: {
    contact_and_completeness: {
      category: 'Contact & Completeness',
      score: 14.5,
      max_score: 15.0,
      percentage: 96.7,
      feedback: 'Header is comprehensive with professional email, phone, location, and verified GitHub & LinkedIn links.'
    },
    experience_and_impact: {
      category: 'Experience & Impact',
      score: 22.0,
      max_score: 25.0,
      percentage: 88.0,
      feedback: 'Strong evidence of quantifiable business impact and active power verbs across work experience.'
    },
    skills_and_relevance: {
      category: 'Skills & Relevance',
      score: 23.0,
      max_score: 25.0,
      percentage: 92.0,
      feedback: 'Extensive coverage across modern frameworks, cloud architectures, and database systems.'
    },
    education_and_certifications: {
      category: 'Education & Certifications',
      score: 13.0,
      max_score: 15.0,
      percentage: 86.7,
      feedback: 'Accredited B.S. in Computer Science with high academic standing and industry certifications verified.'
    },
    formatting_and_structure: {
      category: 'Formatting & Structure',
      score: 16.0,
      max_score: 20.0,
      percentage: 80.0,
      feedback: 'Optimal 1-page length, single-column parsing flow, and standard headers.'
    }
  },
  strengths: [
    {
      title: 'Strong Quantifiable Metrics',
      description: 'Multiple bullet points leverage exact percentages (e.g. 42% throughput improvement, 60% latency drop), providing measurable proof of capability.',
      impact: 'High',
      actionable_tip: 'Keep using the XYZ formula across all project and experience sections.'
    },
    {
      title: 'Broad Full-Stack & Cloud Skillset',
      description: 'Demonstrates balanced mastery across frontend (React, TypeScript), backend (FastAPI, Python), and DevOps (AWS, Docker, Kubernetes).',
      impact: 'High',
      actionable_tip: 'Highlight end-to-end system ownership in interview discussions.'
    },
    {
      title: 'High ATS Parseability',
      description: 'Document adheres to linear single-column layout without nested tables or graphic shapes that disrupt parsers.',
      impact: 'Medium',
      actionable_tip: 'Retain standard section headers during future updates.'
    }
  ],
  weaknesses: [
    {
      title: 'Missing Soft Skills Context',
      description: 'Technical proficiencies are emphasized, but cross-functional leadership, stakeholder management, and team mentoring can be expanded.',
      impact: 'Medium',
      actionable_tip: 'Add bullet points highlighting agile sprint leadership and code review mentorship.'
    },
    {
      title: 'Domain Keyword Specialization',
      description: 'Some emerging enterprise standards (e.g. event streaming with Kafka, OpenTelemetry observability) are absent.',
      impact: 'Low',
      actionable_tip: 'Include streaming or event-driven tools if familiar.'
    }
  ],
  ats_report: {
    ats_score: 91.0,
    verdict: 'Excellent ATS Compatibility',
    passed_checks_count: 7,
    total_checks_count: 8,
    checks: [
      { check_name: 'File Format Compatibility', status: 'passed', details: 'PDF format easily parsed by modern applicant tracking systems.' },
      { check_name: 'Digital Text Readability', status: 'passed', details: 'Contains selectable, native Unicode text characters.' },
      { check_name: 'Contact Information Completeness', status: 'passed', details: 'Email, phone, and professional URLs are present in the top header.' },
      { check_name: 'Standard Section Headings', status: 'passed', details: 'Sections use canonical titles: Summary, Experience, Education, Technical Skills, Projects.' },
      { check_name: 'Table & Multi-Column Layout Safety', status: 'passed', details: 'Clean linear document flow without complex multi-column borders.' },
      { check_name: 'Resume Length & Word Count', status: 'passed', details: 'Word count is 520 words, perfectly aligned with 1-page standard.' },
      { check_name: 'Keyword Naturalness & Density', status: 'passed', details: 'No unnatural repetition or keyword stuffing detected.' },
      { check_name: 'Technical Skill Visibility', status: 'passed', details: 'Over 20 distinct technical skills categorized into clear functional blocks.' }
    ],
    formatting_notes: ['Document structure is highly compliant with major ATS engines.']
  },
  parsed_data: {
    personal_info: {
      full_name: 'Alex Rivera',
      email: 'alex.rivera@example.com',
      phone: '(555) 349-2018',
      location: 'San Francisco, CA',
      linkedin: 'https://linkedin.com/in/alexrivera-tech',
      github: 'https://github.com/alexrivera-dev'
    },
    summary: 'Innovative Full Stack Engineer with 4+ years of experience designing scalable microservices and responsive user interfaces.',
    skills: ['Python', 'TypeScript', 'JavaScript', 'SQL', 'Go', 'FastAPI', 'React', 'Next.js', 'Node.js', 'AWS', 'Docker', 'Kubernetes', 'Terraform', 'PostgreSQL', 'Redis', 'MongoDB'],
    categorized_skills: {
      programming_languages: ['Python', 'TypeScript', 'JavaScript', 'SQL', 'Go'],
      frameworks: ['FastAPI', 'React', 'Next.js', 'Node.js'],
      cloud_devops: ['AWS', 'Docker', 'Kubernetes', 'Terraform'],
      databases: ['PostgreSQL', 'Redis', 'MongoDB']
    },
    education: [
      {
        degree: 'Bachelor of Science in Computer Science',
        institution: 'University of California, Berkeley',
        graduation_year: '2020',
        gpa: '3.85 / 4.0'
      }
    ],
    experience: [
      {
        job_title: 'Senior Software Engineer',
        company: 'CloudScale Systems',
        start_date: 'Jan 2022',
        end_date: 'Present',
        bullet_points: [
          'Architected cloud-native distributed backend services using Python, FastAPI, and PostgreSQL, improving throughput by 42%.',
          'Deployed Kubernetes clusters across Amazon Web Services (AWS) using Terraform and GitHub Actions.',
          'Mentored junior engineers and led technical architecture reviews.'
        ]
      },
      {
        job_title: 'Software Engineer',
        company: 'DataForge Labs',
        start_date: 'Jun 2020',
        end_date: 'Dec 2021',
        bullet_points: [
          'Built interactive dashboard using React, TypeScript, and Tailwind CSS.',
          'Integrated Redis caching layer, reducing database query latencies by 60%.'
        ]
      }
    ],
    projects: [
      {
        title: 'AI Content Engine',
        description: 'Developed an automated text summarization platform with Transformers and FastAPI.',
        technologies: ['Python', 'FastAPI', 'Docker', 'PyTorch'],
        link: 'https://github.com/alexrivera-dev/ai-content-engine'
      }
    ],
    certifications: ['AWS Certified Solutions Architect Associate'],
    languages: ['English'],
    estimated_experience_years: 4.2
  },
  extracted_skills_count: 16,
  created_at: '2026-09-22 14:30'
};

export const DEMO_ROLE_MATCHES: RoleMatchItem[] = [
  {
    role_id: 'full-stack-engineer',
    role_title: 'Full Stack Engineer',
    department: 'Engineering',
    match_percentage: 92.4,
    matching_skills: ['JavaScript', 'TypeScript', 'React', 'Node.js', 'Python', 'FastAPI', 'PostgreSQL', 'Docker', 'RESTful APIs', 'Git'],
    missing_skills: ['GraphQL', 'Next.js SSR', 'Tailwind CSS'],
    skill_gap_percentage: 7.6,
    suggested_learning_path: [
      { step: 1, title: 'GraphQL & Schema Stitching', description: 'Build Apollo Server endpoints with subgraphs and caching.' },
      { step: 2, title: 'Advanced Next.js App Router', description: 'Master Server Components, streaming hydration, and edge middleware.' }
    ],
    recommended_projects: [
      { title: 'Real-Time Collaboration Workspace', description: 'Live multi-user editor with WebSockets and CRDTs.', tech_stack: ['Next.js', 'FastAPI', 'Redis'] }
    ],
    recommended_certifications: ['AWS Certified Developer Associate']
  },
  {
    role_id: 'cloud-architect',
    role_title: 'Cloud Architect / DevOps Lead',
    department: 'Infrastructure',
    match_percentage: 84.8,
    matching_skills: ['AWS', 'Docker', 'Kubernetes', 'Terraform', 'CI/CD Pipelines', 'Linux Administration', 'Prometheus', 'Grafana'],
    missing_skills: ['Ansible', 'Helm', 'ArgoCD', 'Istio Service Mesh'],
    skill_gap_percentage: 15.2,
    suggested_learning_path: [
      { step: 1, title: 'GitOps with ArgoCD', description: 'Declarative Kubernetes cluster synchronization.' },
      { step: 2, title: 'Service Mesh with Istio', description: 'mTLS traffic encryption and distributed tracing.' }
    ],
    recommended_projects: [
      { title: 'Multi-Region Kubernetes Deployment', description: 'Automated infrastructure as code across AWS regions.', tech_stack: ['Terraform', 'EKS', 'ArgoCD'] }
    ],
    recommended_certifications: ['Certified Kubernetes Administrator (CKA)']
  },
  {
    role_id: 'ml-engineer',
    role_title: 'Machine Learning Engineer',
    department: 'AI & Data',
    match_percentage: 76.5,
    matching_skills: ['Python', 'Docker', 'FastAPI', 'PostgreSQL', 'RESTful APIs'],
    missing_skills: ['PyTorch', 'TensorFlow', 'MLOps', 'MLflow', 'Vector Embeddings', 'Model Fine-Tuning'],
    skill_gap_percentage: 23.5,
    suggested_learning_path: [
      { step: 1, title: 'Deep Learning & Transformers', description: 'PyTorch neural networks and Hugging Face pipelines.' },
      { step: 2, title: 'Production MLOps', description: 'Model registry, tracking, and Triton inference serving.' }
    ],
    recommended_projects: [
      { title: 'RAG Knowledge Assistant', description: 'Vector search Q&A platform with LangChain and Pinecone.', tech_stack: ['PyTorch', 'Pinecone', 'FastAPI'] }
    ],
    recommended_certifications: ['AWS Certified Machine Learning Specialty']
  }
];

export const DEMO_ROADMAP: CareerRoadmapResponse = {
  target_role: 'Full Stack Engineer',
  readiness_level: 'Role Ready - Targeted Interview Prep & Portfolio Polish',
  current_match_score: 92.4,
  estimated_timeframe: '4 to 8 Weeks',
  phases: [
    {
      phase_number: 1,
      duration: 'Weeks 1-2',
      title: 'Modern API Specialization & GraphQL',
      focus_skills: ['GraphQL', 'Schema Design', 'Apollo Client'],
      milestones: [
        'Build GraphQL schema with DataLoader to eliminate N+1 queries',
        'Integrate Apollo Client in React with optimistic UI updates'
      ],
      recommended_courses: ['Production GraphQL Architecture', 'Advanced TypeScript Design Patterns'],
      recommended_projects: [
        {
          name: 'High-Performance GraphQL Gateway',
          description: 'Unified microservice API gateway with caching.',
          tech_stack: ['FastAPI', 'Strawberry GraphQL', 'Redis']
        }
      ]
    },
    {
      phase_number: 2,
      duration: 'Weeks 3-4',
      title: 'Full-Stack Performance & Serverless Edge',
      focus_skills: ['Next.js App Router', 'Server Actions', 'Vercel Edge Functions'],
      milestones: [
        'Migrate client-rendered dashboards to React Server Components',
        'Achieve 100/100 Google Lighthouse Core Web Vitals score'
      ],
      recommended_courses: ['Next.js Enterprise Architecture', 'Web Performance Optimization'],
      recommended_projects: [
        {
          name: 'Enterprise SaaS Dashboard',
          description: 'Multi-tenant analytics dashboard with sub-second page loads.',
          tech_stack: ['Next.js', 'Tailwind CSS', 'PostgreSQL']
        }
      ]
    },
    {
      phase_number: 3,
      duration: 'Weeks 5-6',
      title: 'Distributed System Design & Observability',
      focus_skills: ['Distributed Tracing', 'OpenTelemetry', 'Rate Limiting'],
      milestones: [
        'Design fault-tolerant distributed rate limiter with Redis sliding window',
        'Configure Prometheus alerting rules and Grafana dashboards'
      ],
      recommended_courses: ['Designing Data-Intensive Applications', 'System Design Masterclass'],
      recommended_projects: [
        {
          name: 'Real-Time Event Streamer',
          description: 'Streaming platform processing 10k messages/sec.',
          tech_stack: ['FastAPI', 'Kafka', 'Redis']
        }
      ]
    },
    {
      phase_number: 4,
      duration: 'Weeks 7-8',
      title: 'Portfolio Showcase, Live Demos & Placement',
      focus_skills: ['Live Coding', 'System Architecture Whiteboarding'],
      milestones: [
        'Deploy 3 portfolio projects with custom domain URLs and automated CI/CD',
        'Complete 15 mock technical interviews on peer platforms',
        'Achieve >90 ATS compatibility score on target job descriptions'
      ],
      recommended_courses: ['Grokking the System Design Interview'],
      recommended_projects: [
        {
          name: 'Interactive Developer Portfolio',
          description: 'Full-stack portfolio with live playground and case studies.',
          tech_stack: ['React', 'TypeScript', 'Tailwind CSS']
        }
      ]
    }
  ],
  recommended_certifications: ['AWS Certified Solutions Architect Associate', 'CKA'],
  portfolio_improvements: [
    'Add live demonstration URLs with guest credentials for easy recruiter review',
    'Include interactive architecture diagrams explaining throughput trade-offs'
  ]
};
