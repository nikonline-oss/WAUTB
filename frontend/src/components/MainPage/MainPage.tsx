import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Header from '../Header/Header';
import { useApp } from '../../context/AppContext';
import './MainPage.css';

const MainPage: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [activeMenu, setActiveMenu] = useState<number | null>(null);
  const navigate = useNavigate();
  const { tables, deleteTable } = useApp();

  const handleMenuToggle = (tableId: number, event: React.MouseEvent) => {
    event.stopPropagation();
    setActiveMenu(activeMenu === tableId ? null : tableId);
  };

  const handleMenuAction = (action: string, tableId: number) => {
    console.log(`${action} table ${tableId}`);
    if (action === 'delete') {
      deleteTable(tableId);
    }
    setActiveMenu(null);
  };

  const filteredTables = tables.filter(table =>
    table.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="main-page">
      <Header />
      
      <div className="main-content">
        <div className="page-header">
          <h1 className="page-title">Мои таблицы</h1>
          <div className="search-section">
            <div className="search-container">
              <input
                type="text"
                placeholder="введите название таблицы..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="search-input"
              />
              <button className="filter-button">🔍</button>
            </div>
            <button className="filter-options-button">🎛️</button>
          </div>
        </div>

        <div className="tables-grid">
          {/* Карточка создания таблицы */}
          <div className="table-card create-card" onClick={() => navigate('/table/new')}>
            <div className="create-card-content">
              <span className="create-icon">+</span>
              <span className="create-text">Создать таблицу</span>
            </div>
          </div>

          {/* Карточки таблиц */}
          {filteredTables.map((table) => (
            <div key={table.id} className="table-card" onClick={() => navigate(`/table/${table.id}`)}>
              <div className="card-header">
                <div className="menu-container">
                  <button 
                    className="menu-button"
                    onClick={(e) => handleMenuToggle(table.id, e)}
                  >
                    ⋯
                  </button>
                  {activeMenu === table.id && (
                    <div className="dropdown-menu">
                      <button 
                        className="dropdown-item"
                        onClick={() => handleMenuAction('export', table.id)}
                      >
                        Экспортировать
                      </button>
                      <button 
                        className="dropdown-item"
                        onClick={() => handleMenuAction('send', table.id)}
                      >
                        Отправить
                      </button>
                      <button 
                        className="dropdown-item"
                        onClick={() => handleMenuAction('delete', table.id)}
                      >
                        Удалить
                      </button>
                    </div>
                  )}
                </div>
              </div>
              <div className="card-image">
                {table.image}
              </div>
              <div className="card-footer">
                <span className="table-name">{table.name}</span>
                <button className="members-button">👥</button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default MainPage;