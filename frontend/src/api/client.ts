import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface AcademicRecord {
  gpa: number;
  sat_total?: number;
  sat_math?: number;
  sat_verbal?: number;
  act_composite?: number;
  ap_courses?: string[];
  honors_courses?: string[];
}

export interface Extracurricular {
  name: string;
  category: string;
  years_involved: number;
  leadership_role?: string;
  description?: string;
  hours_per_week?: number;
}

export interface StudentProfile {
  name: string;
  email?: string;
  graduation_year: number;
  academic_record: AcademicRecord;
  cs_interests: string[];
  extracurriculars?: Extracurricular[];
  target_programs?: string[];
}

export interface EssayRequest {
  essay_text: string;
  essay_prompt?: string;
}

export const apiClient = {
  // Health check
  checkHealth: async () => {
    const response = await api.get('/api/health');
    return response.data;
  },

  // Profile analysis
  analyzeProfile: async (profile: StudentProfile) => {
    const response = await api.post('/api/analyze-profile', profile);
    return response.data;
  },

  // University matching
  matchUniversities: async (profile: StudentProfile, preferences?: any) => {
    const response = await api.post('/api/match-universities', {
      student_profile: profile,
      preferences: preferences || {},
    });
    return response.data;
  },

  // Essay analysis
  analyzeEssay: async (essay: EssayRequest) => {
    const response = await api.post('/api/analyze-essay', essay);
    return response.data;
  },

  // Essay topic suggestions
  suggestEssayTopics: async (profile: StudentProfile) => {
    const response = await api.post('/api/suggest-essay-topics', profile);
    return response.data;
  },

  // Generate timeline
  generateTimeline: async (profile: StudentProfile) => {
    const response = await api.post('/api/generate-timeline', profile);
    return response.data;
  },

  // Find research opportunities
  findResearchOpportunities: async (profile: StudentProfile) => {
    const response = await api.post('/api/find-research-opportunities', profile);
    return response.data;
  },

  // Get universities
  getUniversities: async () => {
    const response = await api.get('/api/universities');
    return response.data;
  },
};

export default api;
