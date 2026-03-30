import { HashRouter, Routes, Route } from 'react-router-dom';
import { AppProvider } from './store/AppContext';
import Layout from './components/Layout';
import VideoProduction from './pages/VideoProduction';
import ChannelIntelligence from './pages/ChannelIntelligence';
import IdeaLab from './pages/IdeaLab';
import MarketingPlanner from './pages/MarketingPlanner';

export default function App() {
  return (
    <AppProvider>
      <HashRouter>
        <Layout>
          <Routes>
            <Route path="/" element={<VideoProduction />} />
            <Route path="/intelligence" element={<ChannelIntelligence />} />
            <Route path="/ideas" element={<IdeaLab />} />
            <Route path="/marketing" element={<MarketingPlanner />} />
          </Routes>
        </Layout>
      </HashRouter>
    </AppProvider>
  );
}
