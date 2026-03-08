import { useState } from 'react';
import { apiClient, StudentProfile } from '../api/client';
import { Loader2, UserCircle } from 'lucide-react';

export function ProfileAnalysis() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string>('');

  const [formData, setFormData] = useState({
    name: '',
    email: '',
    graduation_year: new Date().getFullYear() + 1,
    gpa: '',
    sat_total: '',
    sat_math: '',
    sat_verbal: '',
    act_composite: '',
    ap_courses: '',
    honors_courses: '',
    cs_interests: '',
    extracurriculars: '',
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setResult(null);

    try {
      const profile: StudentProfile = {
        name: formData.name,
        email: formData.email || undefined,
        graduation_year: formData.graduation_year,
        academic_record: {
          gpa: parseFloat(formData.gpa),
          sat_total: formData.sat_total ? parseInt(formData.sat_total) : undefined,
          sat_math: formData.sat_math ? parseInt(formData.sat_math) : undefined,
          sat_verbal: formData.sat_verbal ? parseInt(formData.sat_verbal) : undefined,
          act_composite: formData.act_composite ? parseInt(formData.act_composite) : undefined,
          ap_courses: formData.ap_courses ? formData.ap_courses.split(',').map(s => s.trim()) : [],
          honors_courses: formData.honors_courses ? formData.honors_courses.split(',').map(s => s.trim()) : [],
        },
        cs_interests: formData.cs_interests ? formData.cs_interests.split(',').map(s => s.trim()) : [],
      };

      const response = await apiClient.analyzeProfile(profile);
      setResult(response);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to analyze profile. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-gray-50 min-h-screen py-12">
      <div className="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-12">
          <UserCircle className="h-16 w-16 text-primary-600 mx-auto mb-4" />
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Profile Analysis
          </h1>
          <p className="text-xl text-gray-600">
            Get a comprehensive analysis of your academic profile and personalized recommendations
          </p>
        </div>

        {/* Form */}
        <div className="card mb-8">
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Personal Information */}
            <div>
              <h2 className="text-xl font-bold text-gray-900 mb-4">Personal Information</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="label">Name *</label>
                  <input
                    type="text"
                    required
                    className="input"
                    value={formData.name}
                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  />
                </div>
                <div>
                  <label className="label">Email</label>
                  <input
                    type="email"
                    className="input"
                    value={formData.email}
                    onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  />
                </div>
                <div>
                  <label className="label">Graduation Year *</label>
                  <input
                    type="number"
                    required
                    className="input"
                    value={formData.graduation_year}
                    onChange={(e) => setFormData({ ...formData, graduation_year: parseInt(e.target.value) })}
                  />
                </div>
              </div>
            </div>

            {/* Academic Information */}
            <div>
              <h2 className="text-xl font-bold text-gray-900 mb-4">Academic Record</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="label">GPA (4.0 scale) *</label>
                  <input
                    type="number"
                    step="0.01"
                    min="0"
                    max="4"
                    required
                    className="input"
                    value={formData.gpa}
                    onChange={(e) => setFormData({ ...formData, gpa: e.target.value })}
                  />
                </div>
                <div>
                  <label className="label">SAT Total</label>
                  <input
                    type="number"
                    min="400"
                    max="1600"
                    className="input"
                    value={formData.sat_total}
                    onChange={(e) => setFormData({ ...formData, sat_total: e.target.value })}
                  />
                </div>
                <div>
                  <label className="label">SAT Math</label>
                  <input
                    type="number"
                    min="200"
                    max="800"
                    className="input"
                    value={formData.sat_math}
                    onChange={(e) => setFormData({ ...formData, sat_math: e.target.value })}
                  />
                </div>
                <div>
                  <label className="label">SAT Verbal</label>
                  <input
                    type="number"
                    min="200"
                    max="800"
                    className="input"
                    value={formData.sat_verbal}
                    onChange={(e) => setFormData({ ...formData, sat_verbal: e.target.value })}
                  />
                </div>
                <div>
                  <label className="label">ACT Composite</label>
                  <input
                    type="number"
                    min="1"
                    max="36"
                    className="input"
                    value={formData.act_composite}
                    onChange={(e) => setFormData({ ...formData, act_composite: e.target.value })}
                  />
                </div>
              </div>
              <div className="mt-4">
                <label className="label">AP Courses (comma-separated)</label>
                <input
                  type="text"
                  className="input"
                  placeholder="AP Computer Science A, AP Calculus BC, AP Physics C"
                  value={formData.ap_courses}
                  onChange={(e) => setFormData({ ...formData, ap_courses: e.target.value })}
                />
              </div>
              <div className="mt-4">
                <label className="label">Honors Courses (comma-separated)</label>
                <input
                  type="text"
                  className="input"
                  placeholder="Honors Chemistry, Honors English"
                  value={formData.honors_courses}
                  onChange={(e) => setFormData({ ...formData, honors_courses: e.target.value })}
                />
              </div>
            </div>

            {/* Interests */}
            <div>
              <h2 className="text-xl font-bold text-gray-900 mb-4">CS Interests</h2>
              <label className="label">Areas of Interest (comma-separated)</label>
              <input
                type="text"
                className="input"
                placeholder="AI/ML, Robotics, Cybersecurity, Web Development"
                value={formData.cs_interests}
                onChange={(e) => setFormData({ ...formData, cs_interests: e.target.value })}
              />
            </div>

            {/* Submit Button */}
            <div className="flex justify-center">
              <button
                type="submit"
                disabled={loading}
                className="btn-primary inline-flex items-center"
              >
                {loading ? (
                  <>
                    <Loader2 className="animate-spin mr-2 h-5 w-5" />
                    Analyzing...
                  </>
                ) : (
                  'Analyze Profile'
                )}
              </button>
            </div>
          </form>
        </div>

        {/* Error */}
        {error && (
          <div className="card bg-red-50 border-red-200 text-red-700 mb-8">
            <p>{error}</p>
          </div>
        )}

        {/* Results */}
        {result && (
          <div className="card">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Analysis Results</h2>
            <div className="prose max-w-none">
              <pre className="whitespace-pre-wrap bg-gray-50 p-4 rounded-lg text-sm">
                {JSON.stringify(result.analysis, null, 2)}
              </pre>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
