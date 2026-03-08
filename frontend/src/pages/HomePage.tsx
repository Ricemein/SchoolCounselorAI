import { Link } from 'react-router-dom';
import { 
  GraduationCap, 
  Target, 
  FileText, 
  Calendar, 
  Search, 
  Sparkles,
  ArrowRight,
  CheckCircle
} from 'lucide-react';

export function HomePage() {
  const features = [
    {
      icon: <Target className="h-6 w-6" />,
      title: 'Profile Analysis',
      description: 'Get comprehensive analysis of your academic profile and personalized recommendations',
      href: '/profile-analysis',
      color: 'bg-blue-500',
    },
    {
      icon: <GraduationCap className="h-6 w-6" />,
      title: 'University Matcher',
      description: 'Find the best CS/Engineering programs that match your profile and interests',
      href: '/university-matcher',
      color: 'bg-purple-500',
    },
    {
      icon: <FileText className="h-6 w-6" />,
      title: 'Essay Coach',
      description: 'Get AI-powered feedback on your college essays and topic suggestions',
      href: '/essay-coach',
      color: 'bg-green-500',
    },
    {
      icon: <Calendar className="h-6 w-6" />,
      title: 'Timeline Generator',
      description: 'Create a personalized application timeline with key milestones',
      href: '/timeline',
      color: 'bg-orange-500',
    },
    {
      icon: <Search className="h-6 w-6" />,
      title: 'Research Finder',
      description: 'Discover research opportunities that align with your interests',
      href: '/research-finder',
      color: 'bg-pink-500',
    },
  ];

  const benefits = [
    'AI-powered personalized recommendations',
    'Focus on top CS/Engineering programs',
    'Comprehensive profile analysis',
    'Essay writing assistance',
    'Research opportunity matching',
    'Application timeline planning',
  ];

  return (
    <div className="bg-white">
      {/* Hero Section */}
      <div className="relative bg-gradient-to-br from-primary-600 to-primary-800 text-white">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-24">
          <div className="text-center">
            <div className="flex justify-center mb-6">
              <Sparkles className="h-16 w-16 text-primary-200" />
            </div>
            <h1 className="text-5xl font-bold mb-6">
              AI-Powered College Counseling
            </h1>
            <p className="text-xl text-primary-100 mb-8 max-w-3xl mx-auto">
              Get personalized guidance for computer science and engineering admissions
              at top research universities. Powered by advanced AI technology.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                to="/profile-analysis"
                className="inline-flex items-center justify-center btn-primary bg-white text-primary-600 hover:bg-primary-50"
              >
                Start Profile Analysis
                <ArrowRight className="ml-2 h-5 w-5" />
              </Link>
              <Link
                to="/university-matcher"
                className="inline-flex items-center justify-center btn-secondary border-white text-white hover:bg-white/10"
              >
                Find Your Universities
              </Link>
            </div>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-20">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">
            Everything You Need for College Applications
          </h2>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Our AI counselor provides comprehensive support throughout your college admissions journey
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature) => (
            <Link
              key={feature.title}
              to={feature.href}
              className="card hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1"
            >
              <div className={`${feature.color} w-12 h-12 rounded-lg flex items-center justify-center text-white mb-4`}>
                {feature.icon}
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-2">
                {feature.title}
              </h3>
              <p className="text-gray-600">
                {feature.description}
              </p>
              <div className="mt-4 flex items-center text-primary-600 font-semibold">
                Learn more
                <ArrowRight className="ml-2 h-4 w-4" />
              </div>
            </Link>
          ))}
        </div>
      </div>

      {/* Benefits Section */}
      <div className="bg-gray-50 py-20">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-3xl font-bold text-gray-900 mb-6">
                Why Choose Our AI Counselor?
              </h2>
              <p className="text-lg text-gray-600 mb-8">
                Our platform combines cutting-edge AI technology with comprehensive knowledge
                of top computer science and engineering programs to provide you with
                personalized, data-driven guidance.
              </p>
              <ul className="space-y-4">
                {benefits.map((benefit) => (
                  <li key={benefit} className="flex items-start">
                    <CheckCircle className="h-6 w-6 text-green-500 mr-3 flex-shrink-0 mt-0.5" />
                    <span className="text-gray-700">{benefit}</span>
                  </li>
                ))}
              </ul>
            </div>
            <div className="card">
              <h3 className="text-2xl font-bold text-gray-900 mb-4">
                Get Started Today
              </h3>
              <p className="text-gray-600 mb-6">
                Begin your college admissions journey with our AI counselor. 
                Get personalized insights and recommendations tailored to your profile.
              </p>
              <Link
                to="/profile-analysis"
                className="block w-full btn-primary text-center"
              >
                Analyze Your Profile
              </Link>
            </div>
          </div>
        </div>
      </div>

      {/* Stats Section */}
      <div className="bg-white py-20">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-center">
            <div>
              <div className="text-5xl font-bold text-primary-600 mb-2">50+</div>
              <div className="text-gray-600">Top Universities</div>
            </div>
            <div>
              <div className="text-5xl font-bold text-primary-600 mb-2">100+</div>
              <div className="text-gray-600">CS/Engineering Programs</div>
            </div>
            <div>
              <div className="text-5xl font-bold text-primary-600 mb-2">24/7</div>
              <div className="text-gray-600">AI Counseling Available</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
