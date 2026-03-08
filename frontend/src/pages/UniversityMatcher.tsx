import { useState } from 'react';
import { apiClient, StudentProfile } from '../api/client';
import { Loader2, Building2 } from 'lucide-react';

export function UniversityMatcher() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string>('');

  const [formData, setFormData] = useState({
    name: '',
    graduation_year: new Date().getFullYear() + 1,
    gpa: '',
    sat_total: '',
    cs_interests: '',
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setResult(null);

    try {
      const profile: StudentProfile = {
        name: formData.name,
        graduation_year: formData.graduation_year,
        academic_record: {
          gpa: parseFloat(formData.gpa),
          sat_total: formData.sat_total ? parseInt(formData.sat_total) : undefined,
        },
        cs_interests: formData.cs_interests ? formData.cs_interests.split(',').map(s => s.trim()) : [],
      };

      const response = await apiClient.matchUniversities(profile);
      setResult(response);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to match universities. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-gray-50 min-h-screen py-12">
      <div className="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <Building2 className="h-16 w-16 text-primary-600 mx-auto mb-4" />
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            University Matcher
          </h1>
          <p className="text-xl text-gray-600">
            Find the best CS/Engineering programs that match your profile
          </p>
        </div>

        <div className="card mb-8">
          <form onSubmit={handleSubmit} className="space-y-6">
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
              <label className="label">Graduation Year *</label>
              <input
                type="number"
                required
                className="input"
                value={formData.graduation_year}
                onChange={(e) => setFormData({ ...formData, graduation_year: parseInt(e.target.value) })}
              />
            </div>
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
              <label className="label">CS Interests (comma-separated)</label>
              <input
                type="text"
                className="input"
                placeholder="AI/ML, Robotics, Cybersecurity"
                value={formData.cs_interests}
                onChange={(e) => setFormData({ ...formData, cs_interests: e.target.value })}
              />
            </div>

            <div className="flex justify-center">
              <button type="submit" disabled={loading} className="btn-primary inline-flex items-center">
                {loading ? (
                  <>
                    <Loader2 className="animate-spin mr-2 h-5 w-5" />
                    Finding Matches...
                  </>
                ) : (
                  'Find Universities'
                )}
              </button>
            </div>
          </form>
        </div>

        {error && (
          <div className="card bg-red-50 border-red-200 text-red-700 mb-8">
            <p>{error}</p>
          </div>
        )}

        {result && (
          <div className="card">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">University Matches</h2>
            <div className="prose max-w-none">
              <pre className="whitespace-pre-wrap bg-gray-50 p-4 rounded-lg text-sm">
                {JSON.stringify(result.matches, null, 2)}
              </pre>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
