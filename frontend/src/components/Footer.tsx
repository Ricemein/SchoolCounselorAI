import { GraduationCap, Github, Mail } from 'lucide-react';

export function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-gray-900 text-gray-300">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* About */}
          <div>
            <div className="flex items-center space-x-2 mb-4">
              <GraduationCap className="h-6 w-6 text-primary-400" />
              <span className="text-lg font-bold text-white">College Counselor AI</span>
            </div>
            <p className="text-sm text-gray-400">
              AI-powered college admissions counseling for computer science and engineering programs at top research universities.
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="text-white font-semibold mb-4">Quick Links</h3>
            <ul className="space-y-2 text-sm">
              <li><a href="/profile-analysis" className="hover:text-primary-400 transition-colors">Profile Analysis</a></li>
              <li><a href="/university-matcher" className="hover:text-primary-400 transition-colors">University Matcher</a></li>
              <li><a href="/essay-coach" className="hover:text-primary-400 transition-colors">Essay Coach</a></li>
              <li><a href="/timeline" className="hover:text-primary-400 transition-colors">Timeline Generator</a></li>
            </ul>
          </div>

          {/* Contact */}
          <div>
            <h3 className="text-white font-semibold mb-4">Connect</h3>
            <div className="space-y-3">
              <a
                href="https://github.com/Ricemein/SchoolCounselorAI"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center space-x-2 hover:text-primary-400 transition-colors"
              >
                <Github className="h-5 w-5" />
                <span className="text-sm">GitHub</span>
              </a>
              <a
                href="mailto:support@collegecounselorai.com"
                className="flex items-center space-x-2 hover:text-primary-400 transition-colors"
              >
                <Mail className="h-5 w-5" />
                <span className="text-sm">Contact Us</span>
              </a>
            </div>
          </div>
        </div>

        <div className="mt-8 pt-8 border-t border-gray-800 text-center text-sm">
          <p>&copy; {currentYear} College Counselor AI. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
}
