import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Header } from './components/Header';
import { Footer } from './components/Footer';
import { HomePage } from './pages/HomePage';
import { ProfileAnalysis } from './pages/ProfileAnalysis';
import { UniversityMatcher } from './pages/UniversityMatcher';
import { EssayCoach } from './pages/EssayCoach';
import { Timeline } from './pages/Timeline';
import { ResearchFinder } from './pages/ResearchFinder';

function App() {
  return (
    <Router>
      <div className="min-h-screen flex flex-col">
        <Header />
        <main className="flex-grow">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/profile-analysis" element={<ProfileAnalysis />} />
            <Route path="/university-matcher" element={<UniversityMatcher />} />
            <Route path="/essay-coach" element={<EssayCoach />} />
            <Route path="/timeline" element={<Timeline />} />
            <Route path="/research-finder" element={<ResearchFinder />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  );
}

export default App;
