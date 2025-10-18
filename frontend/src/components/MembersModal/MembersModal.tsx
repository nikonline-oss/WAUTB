import React from 'react';
import './MembersModal.css';

import member1 from '../../assets/images/test_person.png';
import member2 from '../../assets/images/test_person.png';
import member3 from '../../assets/images/test_person.png';
import member4 from '../../assets/images/test_person.png';

interface MembersModalProps {
  onClose: () => void;
}

interface Member {
  id: number;
  name: string;
  role: string;
  avatar: string;
}

const MembersModal: React.FC<MembersModalProps> = ({ onClose }) => {
  const members: Member[] = [
    { id: 1, name: 'Иванов Иван', role: 'Администратор', avatar: member1 },
    { id: 2, name: 'Петров Петр', role: 'Редактор', avatar: member2 },
    { id: 3, name: 'Сидорова Анна', role: 'Наблюдатель', avatar: member3 },
    { id: 4, name: 'Кузнецов Алексей', role: 'Редактор', avatar: member4 },
  ];

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content members-modal" onClick={e => e.stopPropagation()}>
        <div className="modal-header">
          <h2 className="modal-title">Участники таблицы</h2>
          <button className="modal-close-button" onClick={onClose}>×</button>
        </div>

        <div className="modal-body">
          <div className="members-list">
            {members.map(member => (
              <div key={member.id} className="member-item">
                <div className="member-avatar">
                  <img src={member.avatar} alt={member.name} />
                </div>
                <div className="member-info">
                  <h4 className="member-name">{member.name}</h4>
                  <p className="member-role">{member.role}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="modal-actions">
          <button className="close-button" onClick={onClose}>
            Закрыть
          </button>
        </div>
      </div>
    </div>
  );
};

export default MembersModal;