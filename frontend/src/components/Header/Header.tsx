import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useApp } from '../../context/AppContext';
import './Header.css';

import notifications_image from '../../assets/images/notifications.svg';
import exit_image from '../../assets/images/exit.svg';
import testPersonImage from '../../assets/images/test_person.png';

interface HeaderProps {
  showNavigation?: boolean;
}

const Header: React.FC<HeaderProps> = ({ showNavigation = true }) => {
  const navigate = useNavigate();
  const { currentView, setCurrentView } = useApp();

  const handleNavigation = (view: 'my' | 'all') => {
    setCurrentView(view);
    navigate('/main');
  };

  return (
    <header className="header">
      <div className="header-content">
        {showNavigation && (
          <div className="header-left">
            <button 
              className={`nav-link ${currentView === 'my' ? 'active' : ''}`}
              onClick={() => handleNavigation('my')}
            >
              Мои проекты
            </button>
            <button 
              className={`nav-link ${currentView === 'all' ? 'active' : ''}`}
              onClick={() => handleNavigation('all')}
            >
              Все проекты
            </button>
          </div>
        )}
        
        <div className="header-right">
          <button className="icon-button">
            <span className="notification-bell">
              <img src={notifications_image} alt="Уведомления" />
            </span>
          </button>
          <button 
            className="icon-button"
            onClick={() => navigate('/profile')}
          >
            <div className="user-avatar">
              <img src={testPersonImage} alt="Профиль" />
            </div>
          </button>
          <button 
            className="logout-button"
            onClick={() => navigate('/')}
          >
            <img src={exit_image} alt="Выйти" />
          </button>
        </div>
      </div>
    </header>
  );
};

export default Header;