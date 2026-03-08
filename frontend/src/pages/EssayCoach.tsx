import { useState } from 'react';
import { apiClient } from '../api/client';
import { Loader2, FileText } from 'lucide-react';

export function EssayCoach() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string>('');

  const [formData, setFormData] = useState({
    essay_text: '',
    essay_prompt: '',
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setResult(null);

    try {
      const response = await apiClient.analyzeEssay({
        essay_text: formData.essay_text,
        essay_prompt: formData.essay_prompt || undefined,
      });
      setResult(response);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to analyze essay. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-gray-50 min-h-screen py-12">
      <div className="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <FileText className="h-16 w-16 text-primary-600 mx-auto mb-4" />
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Essay Coach
          </h1>
          <p className="text-xl text-gray-600">
            Get AI-powered feedback on your college essays
          </p>
        </div>

        <div className="card mb-8">
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="label">Essay Prompt (optional)</label>
              <textarea
                className="input min-h-[100px]"
                placeholder="Enter the essay prompt or question..."
                value={formData.essay_prompt}
                onChange={(e) => setFormData({ ...formData, essay_prompt: e.target.value })}
              />
            </div>

            <div>
              <label className="label">Your Essay *</label>
              <textarea
                required
                className="input min-h-[300px]"
                placeholder="Paste your essay here (minimum 50 characters)..."
                value={formData.essay_text}
                onChange={(e) => setFormData({ ...formData, essay_text: e.target.value })}
              />
              <p className="text-sm text-gray-500 mt-2">
                Character count: {formData.essay_text.length}
              </p>
            </div>

            <div className="flex justify-center">
              <button 
                type="submit" 
                disabled={loading || formData.essay_text.length < 50} 
                className="btn-primary inline-flex items-center"
              >
                {loading ? (
                  <>
                    <Loader2 className="animate-spin mr-2 h-5 w-5" />
                    Analyzing Essay...
                  </>
                ) : (
                  'Get Feedback'
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
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Essay Feedback</h2>
            <div className="prose max-w-none">
              <pre className="whitespace-pre-wrap bg-gray-50 p-4 rounded-lg text-sm">
                {JSON.stringify(result.feedback, null, 2)}
              </pre>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
