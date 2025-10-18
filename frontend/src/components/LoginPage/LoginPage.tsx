import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './LoginPage.css';

const LoginPage: React.FC = () => {
  const [login, setLogin] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Здесь будет логика авторизации
    navigate('/main');
  };

  return (
    <div className="login-page">
      <div className="login-container">
        <h1 className="login-title">ВХОД</h1>
        <form onSubmit={handleSubmit} className="login-form">
          <div className="input-group">
            <input
              type="text"
              placeholder="Внутренний логин"
              value={login}
              onChange={(e) => setLogin(e.target.value)}
              className="input-field"
              required
            />
          </div>
          <div className="input-group">
            <input
              type="password"
              placeholder="Пароль"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="input-field"
              required
            />
          </div>
          <button type="submit" className="login-button">
            ВОЙТИ
          </button>
        </form>
      </div>
    </div>
  );
};

export default LoginPage;