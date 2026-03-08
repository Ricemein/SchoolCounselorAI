import { useState } from 'react';
import { apiClient, StudentProfile } from '../api/client';
import { Loader2, Calendar as CalendarIcon } from 'lucide-react';

export function Timeline() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string>('');

  const [formData, setFormData] = useState({
    name: '',
    graduation_year: new Date().getFullYear() + 1,
    gpa: '',
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
        },
        cs_interests: [],
      };

      const response = await apiClient.generateTimeline(profile);
      setResult(response);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to generate timeline. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-gray-50 min-h-screen py-12">
      <div className="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <CalendarIcon className="h-16 w-16 text-primary-600 mx-auto mb-4" />
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Application Timeline
          </h1>
          <p className="text-xl text-gray-600">
            Generate a personalized timeline for your college applications
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
              <label className="label">Current GPA *</label>
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

            <div className="flex justify-center">
              <button type="submit" disabled={loading} className="btn-primary inline-flex items-center">
                {loading ? (
                  <>
                    <Loader2 className="animate-spin mr-2 h-5 w-5" />
                    Generating Timeline...
                  </>
                ) : (
                  'Generate Timeline'
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
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Your Application Timeline</h2>
            <div className="prose max-w-none">
              <pre className="whitespace-pre-wrap bg-gray-50 p-4 rounded-lg text-sm">
                {JSON.stringify(result.timeline, null, 2)}
              </pre>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
