import React from 'react';
import { useNavigate } from 'react-router-dom';
import './Header.css';

interface HeaderProps {
  showNavigation?: boolean;
}

const Header: React.FC<HeaderProps> = ({ showNavigation = true }) => {
  const navigate = useNavigate();

  return (
    <header className="header">
      <div className="header-content">
        {showNavigation && (
          <div className="header-left">
            <button className="nav-link">Мои проекты</button>
            <button className="nav-link">Все проекты</button>
          </div>
        )}
        
        <div className="header-right">
          <button className="icon-button">
            <span className="notification-bell">🔔</span>
          </button>
          <button 
            className="icon-button"
            onClick={() => navigate('/profile')}
          >
            <div className="user-avatar">
              <span>👤</span>
            </div>
          </button>
          <button 
            className="logout-button"
            onClick={() => navigate('/')}
          >
            Выйти
          </button>
        </div>
      </div>
    </header>
  );
};

export default Header;