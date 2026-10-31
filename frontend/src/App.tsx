import React, { useState } from 'react';
import Layout from './components/Layout';
import OverviewPage from './pages/OverviewPage';
import RosterPage from './pages/RosterPage';
import ProjectsPage from './pages/ProjectsPage';
import AwardsPage from './pages/AwardsPage';
import InboxPage from './pages/InboxPage';
import SettingsPage from './pages/SettingsPage';

export const App: React.FC = () => {
  const [currentTab, setCurrentTab] = useState('overview');

  const renderContent = () => {
    switch (currentTab) {
      case 'overview':
        return <OverviewPage />;
      case 'team':
        return <RosterPage />;
      case 'projects':
        return <ProjectsPage />;
      case 'awards':
        return <AwardsPage />;
      case 'inbox':
        return <InboxPage />;
      case 'settings':
        return <SettingsPage />;
      default:
        return <OverviewPage />;
    }
  };

  return (
    <Layout currentTab={currentTab} setCurrentTab={setCurrentTab}>
      {renderContent()}
    </Layout>
  );
};

export default App;
