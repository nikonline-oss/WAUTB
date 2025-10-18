import React, { useState } from 'react';
import './TemplateModal.css';

import search_image from '../../assets/images/search.svg';

interface TemplateModalProps {
  onClose: () => void;
  onSelect: () => void;
}

interface Template {
  id: number;
  name: string;
  description: string;
  category: string;
}

const TemplateModal: React.FC<TemplateModalProps> = ({ onClose, onSelect }) => {
  const [searchTerm, setSearchTerm] = useState('');
  
  const templates: Template[] = [
    { id: 1, name: 'Проектная документация', description: 'Шаблон для управления проектами', category: 'Проекты' },
    { id: 2, name: 'Учет сотрудников', description: 'База данных сотрудников компании', category: 'HR' },
    { id: 3, name: 'Финансовый отчет', description: 'Шаблон для финансовой отчетности', category: 'Финансы' },
    { id: 4, name: 'Складской учет', description: 'Учет товаров на складе', category: 'Логистика' },
  ];

  const filteredTemplates = templates.filter(template =>
    template.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    template.description.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content create-modal" onClick={e => e.stopPropagation()}>
        <div className="modal-header">
          <h2 className="modal-title">Выбор шаблона</h2>
          <button className="modal-close-button" onClick={onClose}>×</button>
        </div>

        <div className="modal-body">
          <div className="search-container">
            <input
              type="text"
              placeholder="Поиск шаблонов..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="search-input"
            />
            <button className="search-button"><img src={search_image} alt="" /></button>
          </div>

          <div className="templates-list">
            {filteredTemplates.map(template => (
              <div key={template.id} className="template-item" onClick={onSelect}>
                <div className="template-info">
                  <h4 className="template-name">{template.name}</h4>
                  <p className="template-description">{template.description}</p>
                  <span className="template-category">{template.category}</span>
                </div>
                <button className="select-template-btn">Выбрать</button>
              </div>
            ))}
          </div>
        </div>

        <div className="modal-actions">
          <button className="cancel-button" onClick={onClose}>
            Назад
          </button>
        </div>
      </div>
    </div>
  );
};

export default TemplateModal;