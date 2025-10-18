import React, { createContext, useContext, useState, ReactNode } from 'react';
import AlertModal, { AlertType } from '../components/AlertModal/AlertModal';

interface AlertOptions {
  type: AlertType;
  title: string;
  message: string;
  timer?: number;
  showConfirm?: boolean;
  onConfirm?: () => void;
  confirmText?: string;
  cancelText?: string;
}

interface AlertContextType {
  showAlert: (options: AlertOptions) => void;
}

const AlertContext = createContext<AlertContextType | undefined>(undefined);

export const AlertProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [alert, setAlert] = useState<AlertOptions & { isOpen: boolean } | null>(null);

  const showAlert = (options: AlertOptions) => {
    setAlert({ ...options, isOpen: true });
  };

  const closeAlert = () => {
    setAlert(null);
  };

  return (
    <AlertContext.Provider value={{ showAlert }}>
      {children}
      {alert?.isOpen && (
        <AlertModal
          type={alert.type}
          title={alert.title}
          message={alert.message}
          onClose={closeAlert}
          timer={alert.timer}
          showConfirm={alert.showConfirm}
          onConfirm={alert.onConfirm}
          confirmText={alert.confirmText}
          cancelText={alert.cancelText}
        />
      )}
    </AlertContext.Provider>
  );
};

export const useAlert = () => {
  const context = useContext(AlertContext);
  if (context === undefined) {
    throw new Error('useAlert must be used within an AlertProvider');
  }
  return context;
};