import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Header from '../Header/Header';
import { useApp, Column } from '../../context/AppContext';
import { useAlert } from '../../context/AlertContext';
import CreateTableModal from '../CreateTableModal/CreateTableModal';
import MembersModal from '../MembersModal/MembersModal';
import './MainPage.css';

import search_image from '../../assets/images/search.svg';
import filter_image from '../../assets/images/filter.svg';


const MainPage: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [activeMenu, setActiveMenu] = useState<number | null>(null);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showMembersModal, setShowMembersModal] = useState(false);
  const navigate = useNavigate();
  const { tables, deleteTable, addTable } = useApp();
  const { showAlert } = useAlert();

  

  const handleMenuToggle = (tableId: number, event: React.MouseEvent) => {
    event.stopPropagation();
    setActiveMenu(activeMenu === tableId ? null : tableId);
  };

  const handleMenuAction = (action: string, tableId: number) => {
    if (action === 'delete') {
      showAlert({
        type: 'warning',
        title: 'Удаление таблицы',
        message: `Вы уверены, что хотите удалить таблицу "${tables.find(t => t.id === tableId)?.name}"? Это действие нельзя отменить.`,
        timer: 5,
        showConfirm: true,
        onConfirm: () => {
          deleteTable(tableId);
          showAlert({
            type: 'success',
            title: 'Успех',
            message: 'Таблица успешно удалена',
            timer: 3
          });
        },
        confirmText: 'Удалить',
        cancelText: 'Отмена'
      });
    } else {
      console.log(`${action} table ${tableId}`);
    }
    setActiveMenu(null);
  };

  const handleMembersClick = (tableId: number, event: React.MouseEvent) => {
    event.stopPropagation();
    setShowMembersModal(true);
  };

  const handleCreateTable = (tableName: string) => {
    const columns: Column[] = [
      { id: 1, name: 'ID', type: 'number' },
      { id: 2, name: 'Название', type: 'text' },
    ];

    const newTable = {
      name: tableName,
      image: 'фото',// потом заменить на фотки
      createdBy: 'currentUser',
      isMyProject: true,
      columns: columns,
      data: [
        { id: 1, data: { '1': 1, '2': 'Пример данных' } },
      ],
      disabledCells: new Set<string>(),
      disabledRows: new Set<number>(),
      disabledColumns: new Set<number>()
    };

    addTable(newTable);

    showAlert({
      type: 'success',
      title: 'Успех',
      message: `Таблица "${tableName}" успешно создана`,
      timer: 3
    });
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
                className="search-tables-input"
              />
              <button className="filter-button"><img src={search_image} alt="" /></button>
            </div>
            <button className="filter-options-button"><img src={filter_image} alt="" /></button>
          </div>
        </div>

        <div className="tables-grid">
          {/* Карточка создания таблицы */}
          <div className="table-card create-card" onClick={() => setShowCreateModal(true)}>
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
                        className="dropdown-item delete-item"
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
                <span className="table-name-list">{table.name}</span>
                <button
                  className="members-button"
                  onClick={(e) => handleMembersClick(table.id, e)}
                >
                  сотрудники {/* тут иконка человечков или типо того, пока впадлу было  */}
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>

      {showCreateModal && (
        <CreateTableModal
          onClose={() => setShowCreateModal(false)}
          onCreate={handleCreateTable}
        />
      )}

      {showMembersModal && (
        <MembersModal onClose={() => setShowMembersModal(false)} />
      )}
    </div>
  );
};

export default MainPage;