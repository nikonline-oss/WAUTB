import React, { useState } from 'react';
import './CreateTableModal.css';
import TemplateModal from './TemplateModal';

interface CreateTableModalProps {
  onClose: () => void;
  onCreate: (tableName: string) => void;
}

interface Parameter {
  id: number;
  name: string;
  type: 'text' | 'number' | 'select';
  value: string;
  options?: string[];
}

const CreateTableModal: React.FC<CreateTableModalProps> = ({ onClose, onCreate }) => {
  const [tableName, setTableName] = useState('Новая таблица');
  const [parameters, setParameters] = useState<Parameter[]>([
    { id: 1, name: 'Тип данных', type: 'select', value: 'Текстовый', options: ['Текстовый', 'Числовой', 'Дата'] },
    { id: 2, name: 'Количество столбцов', type: 'number', value: '3' },
    { id: 3, name: 'Формат данных', type: 'select', value: 'Стандартный', options: ['Стандартный', 'Расширенный'] },
  ]);
  const [showTemplates, setShowTemplates] = useState(false);

  const updateParameter = (id: number, value: string) => {
    setParameters(prev => prev.map(param =>
      param.id === id ? { ...param, value } : param
    ));
  };

  const handleCreate = () => {
    onCreate(tableName);
    onClose();
  };

  if (showTemplates) {
    return <TemplateModal onClose={() => setShowTemplates(false)} onSelect={() => setShowTemplates(false)} />;
  }

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content create-modal" onClick={e => e.stopPropagation()}>
        <div className="modal-header">
          <h2 className="modal-title">Настройка базы данных</h2>
          <button className="modal-close-button" onClick={onClose}>×</button>
        </div>

        <div className="modal-body">
          <div className="table-name-section">
            <label className="section-title">Название таблицы</label>
            <input
              type="text"
              value={tableName}
              onChange={(e) => setTableName(e.target.value)}
              className="table-name-input"
              placeholder="Введите название таблицы"
            />
          </div>

          <div className="manual-config-section">
            <h3 className="section-title">Ручная настройка</h3>
            <div className="parameters-list">
              {parameters.map(param => (
                <div key={param.id} className="parameter-item">
                  <span className="parameter-name">{param.name}</span>
                  {param.type === 'select' ? (
                    <select
                      value={param.value}
                      onChange={(e) => updateParameter(param.id, e.target.value)}
                      className="parameter-value"
                    >
                      {param.options?.map(option => (
                        <option key={option} value={option}>{option}</option>
                      ))}
                    </select>
                  ) : (
                    <input
                      type={param.type}
                      value={param.value}
                      onChange={(e) => updateParameter(param.id, e.target.value)}
                      className="parameter-value"
                    />
                  )}
                </div>
              ))}
            </div>
          </div>

          <button
            className="use-template-btn"
            onClick={() => setShowTemplates(true)}
          >
            Использовать шаблон
          </button>

          <button
            className="import-excel-btn-1"
            onClick={() => console.log('Импорт из Excel')}
          >
            Импорт из Excel
          </button>
        </div>


        <div className="modal-actions">
          <button className="cancel-button" onClick={onClose}>
            Отмена
          </button>
          <button className="create-db-button" onClick={handleCreate}>
            Создать базу данных
          </button>
        </div>
      </div>
    </div>
  );
};

export default CreateTableModal;