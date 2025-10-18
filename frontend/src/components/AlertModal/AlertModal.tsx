import React, { useEffect, useState } from 'react';
import './AlertModal.css';

export type AlertType = 'success' | 'warning' | 'error' | 'info';

interface AlertModalProps {
  type: AlertType;
  title: string;
  message: string;
  onClose: () => void;
  timer?: number;
  showConfirm?: boolean;
  onConfirm?: () => void;
  confirmText?: string;
  cancelText?: string;
}

const AlertModal: React.FC<AlertModalProps> = ({
  type,
  title,
  message,
  onClose,
  timer,
  showConfirm = false,
  onConfirm,
  confirmText = 'Да',
  cancelText = 'Нет'
}) => {
  const [timeLeft, setTimeLeft] = useState(timer || 0);

  useEffect(() => {
    if (timer && timer > 0) {
      setTimeLeft(timer);
      const interval = setInterval(() => {
        setTimeLeft(prev => {
          if (prev <= 1) {
            clearInterval(interval);
            return 0;
          }
          return prev - 1;
        });
      }, 1000);

      return () => clearInterval(interval);
    }
  }, [timer]);

  const getIcon = () => {
    switch (type) {
      case 'success': return '✅';
      case 'warning': return '⚠️';
      case 'error': return '❌';
      case 'info': return 'ℹ️';
      default: return 'ℹ️';
    }
  };

  const handleConfirm = () => {
    if (onConfirm) {
      onConfirm();
    }
    onClose();
  };

  return (
    <div className="modal-overlay" onClick={!showConfirm ? onClose : undefined}>
      <div className={`alert-modal alert-${type}`} onClick={e => e.stopPropagation()}>
        <div className="alert-header">
          <div className="alert-title-section">
            <span className="alert-icon">{getIcon()}</span>
            <h3 className="alert-title">{title}</h3>
          </div>
          <button className="alert-close-button" onClick={onClose}>×</button>
        </div>

        <div className="alert-body">
          <p className="alert-message">{message}</p>
          {timer && timeLeft > 0 && (
            <div className="alert-timer">
              Автоматическое закрытие через: {timeLeft} сек
            </div>
          )}
        </div>

        <div className="alert-actions">
          {showConfirm ? (
            <>
              <button className="alert-cancel-button" onClick={onClose}>
                {cancelText}
              </button>
              <button 
                className="alert-confirm-button" 
                onClick={handleConfirm}
                disabled={timeLeft > 0}
              >
                {confirmText} {timeLeft > 0 ? `(${timeLeft})` : ''}
              </button>
            </>
          ) : (
            <button className="alert-close-btn" onClick={onClose}>
              Закрыть
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default AlertModal;