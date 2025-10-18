import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import { AppProvider } from './context/AppContext';
import { AlertProvider } from './context/AlertContext';
import LoginPage from './components/LoginPage/LoginPage';
import MainPage from './components/MainPage/MainPage';
import TableEditPage from './components/TableEditPage/TableEditPage';
import ProfilePage from './components/ProfilePage/ProfilePage';

function App() {
  return (
    <AlertProvider>
      <AppProvider>
        <Router>
          <div className="App">
            <Routes>
              <Route path="/" element={<LoginPage />} />
              <Route path="/main" element={<MainPage />} />
              <Route path="/table/:id" element={<TableEditPage />} />
              <Route path="/table/new" element={<TableEditPage />} />
              <Route path="/profile" element={<ProfilePage />} />
            </Routes>
          </div>
        </Router>
      </AppProvider>
    </AlertProvider>
  );
}

export default App;