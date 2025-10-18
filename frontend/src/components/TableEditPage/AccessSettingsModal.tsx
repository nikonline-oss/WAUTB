import React, { useState } from 'react';
import './AccessSettingsModal.css';

import search_image from '../../assets/images/search.svg';
import paramaters_image from '../../assets/images/parameters.svg';

interface AccessSettingsModalProps {
  onClose: () => void;
}

interface AccessRule {
  id: number;
  name: string;
  enabled: boolean;
}

interface Employee {
  id: number;
  name: string;
  selected: boolean;
}

const AccessSettingsModal: React.FC<AccessSettingsModalProps> = ({ onClose }) => {
  const [accessRules, setAccessRules] = useState<AccessRule[]>([
    { id: 1, name: 'Строгий доступ', enabled: true },
    { id: 2, name: 'Свободный доступ просмотра', enabled: false },
    { id: 3, name: 'Ограниченное редактирование', enabled: true },
  ]);

  const [employees, setEmployees] = useState<Employee[]>([
    { id: 1, name: 'Иванов Иван', selected: false },
    { id: 2, name: 'Петров Петр', selected: false },
    { id: 3, name: 'Сидорова Анна', selected: false },
    { id: 4, name: 'Кузнецов Алексей', selected: false },
  ]);

  const [searchTerm, setSearchTerm] = useState('');

  const toggleAccessRule = (ruleId: number) => {
    setAccessRules(accessRules.map(rule =>
      rule.id === ruleId ? { ...rule, enabled: !rule.enabled } : rule
    ));
  };

  const toggleEmployee = (employeeId: number) => {
    setEmployees(employees.map(employee =>
      employee.id === employeeId ? { ...employee, selected: !employee.selected } : employee
    ));
  };

  const filteredEmployees = employees.filter(employee =>
    employee.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={e => e.stopPropagation()}>
        <div className="modal-header">
          <h2 className="modal-title">Настройки доступа</h2>
          <button className="modal-close-button" onClick={onClose}>
            <img src={paramaters_image} alt="" />
          </button>
        </div>

        <div className="modal-body">
          <div className="access-rules-section">
            <h3 className="section-title">Правила доступа</h3>
            <div className="access-rules-list">
              {accessRules.map(rule => (
                <div key={rule.id} className="access-rule-item">
                  <span className="rule-name">{rule.name}</span>
                  <label className="checkbox-container">
                    <input
                      type="checkbox"
                      checked={rule.enabled}
                      onChange={() => toggleAccessRule(rule.id)}
                    />
                    <span className="checkmark"></span>
                  </label>
                </div>
              ))}
            </div>
          </div>

          <div className="editing-rights-section">
            <h3 className="section-title">Право на редактирование</h3>
            <div className="search-container">
              <input
                type="text"
                placeholder="Поиск сотрудников..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="search-input"
              />
              <button className="search-button"><img src={search_image} alt="" /></button>
            </div>
            
            <div className="employees-list">
              {filteredEmployees.map(employee => (
                <div key={employee.id} className="employee-item">
                  <span className="employee-name">{employee.name}</span>
                  <label className="checkbox-container">
                    <input
                      type="checkbox"
                      checked={employee.selected}
                      onChange={() => toggleEmployee(employee.id)}
                    />
                    <span className="checkmark"></span>
                  </label>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="modal-actions">
          <button className="cancel-button" onClick={onClose}>
            Отмена
          </button>
          <button className="save-settings-button">
            Сохранить настройки
          </button>
        </div>
      </div>
    </div>
  );
};

export default AccessSettingsModal;