// src/components/TableEditPage/TableEditPage.tsx
import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Header from '../Header/Header';
import AccessSettingsModal from './AccessSettingsModal';
import { useApp, Table, Column } from '../../context/AppContext';
import { useAlert } from '../../context/AlertContext';
import './TableEditPage.css';

import paramaters_image from '../../assets/images/parameters.svg';

type ViewMode = 'view' | 'edit';
type SortOrder = 'none' | 'asc' | 'desc';

interface SortState {
  columnId: number | null;
  order: SortOrder;
}

interface DragState {
  type: 'column' | 'row';
  id: number;
  index: number;
}

const TableEditPage: React.FC = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { tables, updateTable, addTable } = useApp();
  const { showAlert } = useAlert();
  
  const [viewMode, setViewMode] = useState<ViewMode>('view');
  const [showSettings, setShowSettings] = useState(false);
  const [tableName, setTableName] = useState('Текущие заказы');
  const [isEditingName, setIsEditingName] = useState(false);
  const [sortState, setSortState] = useState<SortState>({ columnId: null, order: 'none' });
  const [dragState, setDragState] = useState<DragState | null>(null);
  
  // Новое состояние для блокировки управления столбцами
  const [columnsLocked, setColumnsLocked] = useState(false);
  
  const isNewTable = id === 'new';
  const currentTable = tables.find(t => t.id === Number(id)) || 
    (isNewTable ? null : tables[0]);

  const [localTable, setLocalTable] = useState<Table | null>(null);
  const [disabledCells, setDisabledCells] = useState<Set<string>>(new Set());
  const [disabledRows, setDisabledRows] = useState<Set<number>>(new Set());
  const [disabledColumns, setDisabledColumns] = useState<Set<number>>(new Set());

  useEffect(() => {
    if (isNewTable) {
      const newTable: Table = {
        id: Date.now(),
        name: 'Новая таблица',
        image: 'ФОТО',
        createdBy: 'currentUser',
        isMyProject: true,
        columns: [
          { id: 1, name: 'ID', type: 'number' },
          { id: 2, name: 'Название', type: 'text' },
        ],
        data: [
          { id: 1, data: { '1': 1, '2': 'Пример данных' } },
        ],
        disabledCells: new Set<string>(),
        disabledRows: new Set<number>(),
        disabledColumns: new Set<number>()
      };
      setLocalTable(newTable);
      setTableName(newTable.name);
    } else if (currentTable) {
      setLocalTable(currentTable);
      setTableName(currentTable.name);
      setDisabledCells(currentTable.disabledCells || new Set<string>());
      setDisabledRows(currentTable.disabledRows || new Set<number>());
      setDisabledColumns(currentTable.disabledColumns || new Set<number>());
    }
  }, [id, currentTable, isNewTable]);

  const saveTable = () => {
    if (!localTable) return;

    const tableToSave = {
      ...localTable,
      name: tableName,
      disabledCells: new Set<string>(disabledCells),
      disabledRows: new Set<number>(disabledRows),
      disabledColumns: new Set<number>(disabledColumns)
    };

    if (isNewTable) {
      addTable(tableToSave);
      navigate('/main');
    } else {
      updateTable(localTable.id, tableToSave);
    }
    setViewMode('view');
    
    showAlert({
      type: 'success',
      title: 'Успех',
      message: 'Таблица успешно сохранена',
      timer: 3
    });
  };

  const addColumn = () => {
    if (columnsLocked) {
      showAlert({
        type: 'warning',
        title: 'Ограничение',
        message: 'У вас нет прав для добавления столбцов',
        timer: 3
      });
      return;
    }

    const newColumn: Column = {
      id: Date.now(),
      name: `Столбец ${localTable!.columns.length + 1}`,
      type: 'text'
    };
    setLocalTable(prev => prev ? {
      ...prev,
      columns: [...prev.columns, newColumn],
      data: prev.data.map(row => ({
        ...row,
        data: { ...row.data, [newColumn.id]: '' }
      }))
    } : null);
  };

  const removeColumn = (columnId: number) => {
    if (columnsLocked) {
      showAlert({
        type: 'warning',
        title: 'Ограничение',
        message: 'У вас нет прав для удаления столбцов',
        timer: 3
      });
      return;
    }

    if (localTable!.columns.length <= 1) return;
    setLocalTable(prev => prev ? {
      ...prev,
      columns: prev.columns.filter(col => col.id !== columnId),
      data: prev.data.map(row => {
        const newData = { ...row.data };
        delete newData[columnId];
        return { ...row, data: newData };
      })
    } : null);
  };

  const updateColumn = (columnId: number, field: keyof Column, value: string) => {
    if (columnsLocked) {
      showAlert({
        type: 'warning',
        title: 'Ограничение',
        message: 'У вас нет прав для изменения столбцов',
        timer: 3
      });
      return;
    }

    setLocalTable(prev => prev ? {
      ...prev,
      columns: prev.columns.map(col => 
        col.id === columnId ? { 
          ...col, 
          [field]: field === 'type' ? value as 'text' | 'number' | 'timestamp' | 'list' : value 
        } : col
      )
    } : null);
  };

  const addRow = () => {
    const newRow = {
      id: Date.now(),
      data: localTable!.columns.reduce((acc, col) => {
        acc[col.id] = '';
        return acc;
      }, {} as Record<string, any>)
    };
    setLocalTable(prev => prev ? {
      ...prev,
      data: [...prev.data, newRow]
    } : null);
  };

  const removeRow = (rowId: number) => {
    setLocalTable(prev => prev ? {
      ...prev,
      data: prev.data.filter(row => row.id !== rowId)
    } : null);
  };

  const updateCell = (rowId: number, columnId: number, value: any) => {
    if (isCellDisabled(rowId, columnId)) return;
    
    setLocalTable(prev => prev ? {
      ...prev,
      data: prev.data.map(row => 
        row.id === rowId 
          ? { ...row, data: { ...row.data, [columnId]: value } }
          : row
      )
    } : null);
  };

  const handleSort = (columnId: number) => {
    setSortState(prev => {
      let newOrder: SortOrder = 'asc';
      if (prev.columnId === columnId) {
        if (prev.order === 'asc') newOrder = 'desc';
        else if (prev.order === 'desc') newOrder = 'none';
      }
      
      if (newOrder === 'none') {
        return { columnId: null, order: 'none' };
      }
      
      return { columnId, order: newOrder };
    });
  };

  const getSortedData = () => {
    if (sortState.order === 'none' || !sortState.columnId || !localTable) return localTable?.data || [];
    
    return [...localTable.data].sort((a, b) => {
      const aVal = a.data[sortState.columnId!];
      const bVal = b.data[sortState.columnId!];
      
      if (sortState.order === 'asc') {
        return aVal < bVal ? -1 : aVal > bVal ? 1 : 0;
      } else {
        return aVal > bVal ? -1 : aVal < bVal ? 1 : 0;
      }
    });
  };

  const handleDragStart = (type: 'column' | 'row', id: number, index: number) => {
    if (viewMode !== 'edit') return;
    if (type === 'column' && columnsLocked) return;
    setDragState({ type, id, index });
  };

  const handleDragOver = (e: React.DragEvent, targetIndex: number) => {
    e.preventDefault();
    if (!dragState || viewMode !== 'edit') return;
  };

  const handleDrop = (targetIndex: number) => {
    if (!dragState || viewMode !== 'edit' || !localTable) return;

    if (dragState.type === 'column') {
      if (columnsLocked) {
        showAlert({
          type: 'warning',
          title: 'Ограничение',
          message: 'У вас нет прав для перемещения столбцов',
          timer: 3
        });
        return;
      }

      const newColumns = [...localTable.columns];
      const [movedColumn] = newColumns.splice(dragState.index, 1);
      newColumns.splice(targetIndex, 0, movedColumn);
      
      setLocalTable(prev => prev ? { ...prev, columns: newColumns } : null);
      
      showAlert({
        type: 'success',
        title: 'Успех',
        message: 'Столбец перемещен',
        timer: 2
      });
    } else {
      const newData = [...localTable.data];
      const [movedRow] = newData.splice(dragState.index, 1);
      newData.splice(targetIndex, 0, movedRow);
      
      setLocalTable(prev => prev ? { ...prev, data: newData } : null);
      
      showAlert({
        type: 'success',
        title: 'Успех',
        message: 'Строка перемещена',
        timer: 2
      });
    }

    setDragState(null);
  };

  const toggleCellDisabled = (rowId: number, columnId: number) => {
    const cellKey = `${rowId}-${columnId}`;
    setDisabledCells(prev => {
      const newSet = new Set(prev);
      if (newSet.has(cellKey)) {
        newSet.delete(cellKey);
      } else {
        newSet.add(cellKey);
      }
      return newSet;
    });
  };

  const toggleRowDisabled = (rowId: number) => {
    setDisabledRows(prev => {
      const newSet = new Set(prev);
      if (newSet.has(rowId)) {
        newSet.delete(rowId);
      } else {
        newSet.add(rowId);
      }
      return newSet;
    });
  };

  const toggleColumnDisabled = (columnId: number) => {
    setDisabledColumns(prev => {
      const newSet = new Set(prev);
      if (newSet.has(columnId)) {
        newSet.delete(columnId);
      } else {
        newSet.add(columnId);
      }
      return newSet;
    });
  };

  const toggleColumnsLocked = () => {
    setColumnsLocked(prev => !prev);
    showAlert({
      type: 'info',
      title: columnsLocked ? 'Столбцы разблокированы' : 'Столбцы заблокированы',
      message: columnsLocked 
        ? 'Теперь можно управлять столбцами' 
        : 'Управление столбцами заблокировано',
      timer: 2
    });
  };

  const isCellDisabled = (rowId: number, columnId: number) => {
    return disabledCells.has(`${rowId}-${columnId}`) || 
           disabledRows.has(rowId) || 
           disabledColumns.has(columnId);
  };

  const sortedData = getSortedData();

  const getSortIcon = (columnId: number) => {
    if (sortState.columnId !== columnId) return '↕️';
    if (sortState.order === 'asc') return '↑';
    if (sortState.order === 'desc') return '↓';
    return '↕️';
  };

  const handleTableNameClick = () => {
    if (viewMode === 'edit') {
      setIsEditingName(true);
    }
  };

  if (!localTable) {
    return <div>Загрузка...</div>;
  }

  const { columns } = localTable;

  return (
    <div className="table-edit-page">
      <Header />
      
      <div className="table-edit-content">
        <div className="breadcrumb">
          <div className="breadcrumb-left">
            <span className="breadcrumb-text">
              Мои таблицы  
            </span>
            {isEditingName ? (
              <input
                type="text"
                value={tableName}
                onChange={(e) => setTableName(e.target.value)}
                onBlur={() => setIsEditingName(false)}
                onKeyPress={(e) => e.key === 'Enter' && setIsEditingName(false)}
                className="table-name-input"
                autoFocus
              />
            ) : (
              <span 
                className={`table-name ${viewMode === 'edit' ? 'editable' : ''}`}
                onClick={handleTableNameClick}
              >
                {tableName}
              </span>
            )}
          </div>
          <div className="breadcrumb-right">
            <div className="view-mode-toggle">
              <button 
                className={`mode-btn ${viewMode === 'view' ? 'active' : ''}`}
                onClick={() => setViewMode('view')}
              >
                Просмотр
              </button>
              <button 
                className={`mode-btn ${viewMode === 'edit' ? 'active' : ''}`}
                onClick={() => setViewMode('edit')}
              >
                Редактирование
              </button>
            </div>
            <button 
              className="settings-button"
              onClick={() => setShowSettings(true)}
            >
              <img src={paramaters_image} alt="" />
            </button>
          </div>
        </div>

        <div className="table-container">
          {viewMode === 'edit' && (
            <div className="table-actions">
              <button 
                className={`add-column-btn ${columnsLocked ? 'disabled' : ''}`}
                onClick={addColumn}
                title={columnsLocked ? 'Добавление столбцов заблокировано' : 'Добавить столбец'}
              >
                + Добавить столбец
              </button>
              <button className="add-row-btn" onClick={addRow}>
                + Добавить строку
              </button>
              <button 
                className="import-excel-btn"
                onClick={() => console.log('Импорт из Excel')}
              >
                Импорт из Excel
              </button>
              <button 
                className={`lock-columns-btn ${columnsLocked ? 'locked' : ''}`}
                onClick={toggleColumnsLocked}
                title={columnsLocked ? 'Разблокировать столбцы' : 'Заблокировать столбцы'}
              >
                {columnsLocked ? '🔓' : '🔒'} Столбцы
              </button>
              <div className="drag-hint">
                Перетаскивайте заголовки столбцов и строк для изменения порядка
              </div>
            </div>
          )}

          <div className="table-wrapper">
            <table className="data-table">
              <thead>
                <tr>
                  {columns.map((column, index) => (
                    <th 
                      key={column.id} 
                      className={`table-header ${disabledColumns.has(column.id) ? 'disabled' : ''} ${columnsLocked ? 'locked' : ''}`}
                      draggable={viewMode === 'edit' && !columnsLocked}
                      onDragStart={() => handleDragStart('column', column.id, index)}
                      onDragOver={(e) => handleDragOver(e, index)}
                      onDrop={() => handleDrop(index)}
                    >
                      <div className="column-header">
                        <div className="column-title-section">
                          {viewMode === 'edit' && !columnsLocked ? (
                            <input
                              type="text"
                              value={column.name}
                              onChange={(e) => updateColumn(column.id, 'name', e.target.value)}
                              className="column-name-input"
                            />
                          ) : (
                            <span className="column-name">{column.name}</span>
                          )}
                          <button 
                            className="sort-button"
                            onClick={() => handleSort(column.id)}
                          >
                            {getSortIcon(column.id)}
                          </button>
                        </div>
                        
                        {viewMode === 'edit' && (
                          <div className="column-controls">
                            {!columnsLocked ? (
                              <>
                                <select
                                  value={column.type}
                                  onChange={(e) => updateColumn(column.id, 'type', e.target.value as any)}
                                  className="column-type-select"
                                >
                                  <option value="text">Текст</option>
                                  <option value="number">Число</option>
                                  <option value="timestamp">Дата/время</option>
                                  <option value="list">Список</option>
                                </select>
                                <button 
                                  className={`toggle-disabled-btn ${disabledColumns.has(column.id) ? 'disabled' : ''}`}
                                  onClick={() => toggleColumnDisabled(column.id)}
                                  title={disabledColumns.has(column.id) ? 'Включить столбец' : 'Отключить столбец'}
                                >
                                  {disabledColumns.has(column.id) ? '👁️' : '👁️‍🗨️'}
                                </button>
                                {columns.length > 1 && (
                                  <button 
                                    className="remove-column-btn"
                                    onClick={() => removeColumn(column.id)}
                                    title="Удалить столбец"
                                  >
                                    ×
                                  </button>
                                )}
                              </>
                            ) : (
                              <span className="columns-locked-label">Заблокировано</span>
                            )}
                          </div>
                        )}
                      </div>
                    </th>
                  ))}
                  {viewMode === 'edit' && <th className="row-actions-header">Действия</th>}
                </tr>
              </thead>
              <tbody>
                {sortedData.map((row, rowIndex) => (
                  <tr 
                    key={row.id} 
                    className={`table-row ${disabledRows.has(row.id) ? 'disabled' : ''}`}
                    draggable={viewMode === 'edit'}
                    onDragStart={() => handleDragStart('row', row.id, rowIndex)}
                    onDragOver={(e) => handleDragOver(e, rowIndex)}
                    onDrop={() => handleDrop(rowIndex)}
                  >
                    {columns.map(column => (
                      <td 
                        key={column.id} 
                        className={`table-cell ${isCellDisabled(row.id, column.id) ? 'disabled' : ''}`}
                      >
                        {viewMode === 'edit' ? (
                          column.type === 'list' ? (
                            <select
                              value={row.data[column.id] || ''}
                              onChange={(e) => updateCell(row.id, column.id, e.target.value)}
                              className="cell-input"
                              disabled={isCellDisabled(row.id, column.id)}
                            >
                              <option value="">Выберите...</option>
                              <option value="Активный">Активный</option>
                              <option value="Завершен">Завершен</option>
                              <option value="Отменен">Отменен</option>
                            </select>
                          ) : column.type === 'timestamp' ? (
                            <input
                              type="datetime-local"
                              value={row.data[column.id] || ''}
                              onChange={(e) => updateCell(row.id, column.id, e.target.value)}
                              className="cell-input"
                              disabled={isCellDisabled(row.id, column.id)}
                            />
                          ) : (
                            <input
                              type={column.type === 'number' ? 'number' : 'text'}
                              value={row.data[column.id] || ''}
                              onChange={(e) => updateCell(row.id, column.id, e.target.value)}
                              className="cell-input"
                              disabled={isCellDisabled(row.id, column.id)}
                            />
                          )
                        ) : (
                          <span className="cell-value">{row.data[column.id] || ''}</span>
                        )}
                        {viewMode === 'edit' && (
                          <button 
                            className={`cell-toggle-btn ${isCellDisabled(row.id, column.id) ? 'disabled' : ''}`}
                            onClick={() => toggleCellDisabled(row.id, column.id)}
                            title={isCellDisabled(row.id, column.id) ? 'Включить ячейку' : 'Отключить ячейку'}
                          >
                            {isCellDisabled(row.id, column.id) ? '🔒' : '🔓'}
                          </button>
                        )}
                      </td>
                    ))}
                    {viewMode === 'edit' && (
                      <td className="row-actions-cell">
                        <button 
                          className={`toggle-row-btn ${disabledRows.has(row.id) ? 'disabled' : ''}`}
                          onClick={() => toggleRowDisabled(row.id)}
                          title={disabledRows.has(row.id) ? 'Включить строку' : 'Отключить строку'}
                        >
                          {disabledRows.has(row.id) ? '👁️' : '👁️‍🗨️'}
                        </button>
                        <button 
                          className="remove-row-btn"
                          onClick={() => removeRow(row.id)}
                          title="Удалить строку"
                        >
                          🗑️
                        </button>
                      </td>
                    )}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <button className="save-button" onClick={saveTable}>
          Сохранить
        </button>
      </div>

      {showSettings && (
        <AccessSettingsModal onClose={() => setShowSettings(false)} />
      )}
    </div>
  );
};

export default TableEditPage;