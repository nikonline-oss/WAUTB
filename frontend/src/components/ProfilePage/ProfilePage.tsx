import React from 'react';
import Header from '../Header/Header';
import './ProfilePage.css';

import testPersonImage from '../../assets/images/test_person.png';

const ProfilePage: React.FC = () => {
  return (
    <div className="profile-page">
      <Header />
      
      <div className="profile-content">
        <div className="profile-header">
          <div className="avatar-section">
            <div className="profile-avatar">
              <img src={testPersonImage} alt="Profile" className="avatar-image" />
            </div>
            <div className="profile-info">
              <h1 className="profile-name">Белый Михаил Иванович</h1>
              <p className="profile-position">
                Руководитель сервис-сервис жидкого полирования и инноватора
              </p>
            </div>
          </div>
        </div>

        <div className="profile-cards">
          <div className="profile-card">
            <h3 className="card-title">В работе</h3>
            <ul className="card-list">
              <li>Пример чего-то</li>
              <li>Пример чего-то</li>
            </ul>
          </div>

          <div className="profile-card">
            <h3 className="card-title">Доступ</h3>
            <ul className="card-list">
              <li>Пример чего-то</li>
              <li>Пример чего-то</li>
              <li>Пример чего-то</li>
            </ul>
          </div>

          <div className="profile-card">
            <h3 className="card-title">Права</h3>
            <ul className="card-list">
              <li>Пример чего-то</li>
              <li>Пример чего-то</li>
              <li>Пример чего-то</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProfilePage;