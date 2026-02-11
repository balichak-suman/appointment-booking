import React, { useState } from 'react';
import Sidebar from './Sidebar';
import Header from './Header';
import DashboardContent from './DashboardContent';
import Doctors from './Doctors';
import Patients from './Patients';
import Appointments from './Appointments';
import './index.css';
import './Sidebar.css';

function App() {
  const [activeMenu, setActiveMenu] = useState('dashboard');
  const [sidebarOpen, setSidebarOpen] = useState(true);

  const getPageTitle = () => {
    switch (activeMenu) {
      case 'dashboard':
        return 'Admin Dashboard';
      case 'doctors':
        return 'Doctors Management';
      case 'patients':
        return 'Patients Management';
      case 'appointments':
        return 'Appointments';
      case 'settings':
        return 'Settings';
      default:
        return 'Dashboard';
    }
  };

  const getBreadcrumb = () => {
    switch (activeMenu) {
      case 'dashboard':
        return ['Home', 'Dashboard'];
      case 'doctors':
        return ['Home', 'Management', 'Doctors'];
      case 'patients':
        return ['Home', 'Management', 'Patients'];
      case 'appointments':
        return ['Home', 'Appointments'];
      case 'settings':
        return ['Home', 'Settings'];
      default:
        return ['Home', getPageTitle()];
    }
  };

  const renderContent = () => {
    switch (activeMenu) {
      case 'dashboard':
        return <DashboardContent />;
      case 'doctors':
        return <Doctors />;
      case 'patients':
        return <Patients />;
      case 'appointments':
        return <Appointments />;
      case 'settings':
        return (
          <div className="content-area">
            <h2>Settings</h2>
            <p>Application settings will be displayed here.</p>
          </div>
        );
      default:
        return <DashboardContent />;
    }
  };

  return (
    <div className="app-container">
      <Sidebar activeMenu={activeMenu} setActiveMenu={setActiveMenu} />
      <div className="main-content">
        <Header
          pageTitle={getPageTitle()}
          breadcrumb={getBreadcrumb()}
          onToggleSidebar={() => setSidebarOpen(!sidebarOpen)}
        />
        {renderContent()}
      </div>
    </div>
  );
}

export default App;
