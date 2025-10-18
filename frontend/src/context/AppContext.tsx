import React, { createContext, useContext, useState, ReactNode } from 'react';
import { apiClient } from '../store/client';

export interface Table {
  id: number;
  name: string;
  image: string;
  createdBy: string;
  isMyProject: boolean;
  columns: Column[];
  data: TableRow[];
  disabledCells?: Set<string>;
  disabledRows?: Set<number>;
  disabledColumns?: Set<number>;
}

export interface Column {
  id: number;
  name: string;
  type: 'text' | 'number' | 'timestamp' | 'list';
}

export interface TableRow {
  id: number;
  data: Record<string, any>;
}

interface AppContextType {
  tables: Table[];
  currentView: 'my' | 'all';
  setCurrentView: (view: 'my' | 'all') => void;
  addTable: (table: Omit<Table, 'id'>) => void;
  deleteTable: (tableId: number) => void;
  updateTable: (tableId: number, updates: Partial<Table>) => void;
}

const AppContext = createContext<AppContextType | undefined>(undefined);

export const AppProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  
  

  const [allTables, setAllTables] = useState<Table[]>([
    { 
      id: 1, 
      name: 'Таблица1', 
      image: 'фото', // потом заменить на фотки
      createdBy: 'user1',
      isMyProject: true,
      columns: [
        { id: 1, name: 'ID', type: 'number' },
        { id: 2, name: 'Название', type: 'text' },
        { id: 3, name: 'Статус', type: 'list' },
      ],
      data: [
        { id: 1, data: { '1': 1, '2': 'Проект А', '3': 'Активный' } },
        { id: 2, data: { '1': 2, '2': 'Проект Б', '3': 'Завершен' } },
      ],
      disabledCells: new Set(),
      disabledRows: new Set(),
      disabledColumns: new Set()
    },
    { 
      id: 2, 
      name: 'Таблица2', 
      image: 'фото', 
      createdBy: 'user2',
      isMyProject: false,
      columns: [
        { id: 1, name: 'ID', type: 'number' },
        { id: 2, name: 'Задача', type: 'text' },
      ],
      data: [
        { id: 1, data: { '1': 1, '2': 'Задача 1' } },
      ],
      disabledCells: new Set(),
      disabledRows: new Set(),
      disabledColumns: new Set()
    },
    { 
      id: 3, 
      name: 'Таблица3', 
      image: 'фото', 
      createdBy: 'user1',
      isMyProject: true,
      columns: [
        { id: 1, name: 'ID', type: 'number' },
        { id: 2, name: 'Описание', type: 'text' },
      ],
      data: [
        { id: 1, data: { '1': 1, '2': 'Описание 1' } },
      ],
      disabledCells: new Set(),
      disabledRows: new Set(),
      disabledColumns: new Set()
    },
  ]);

  const [currentView, setCurrentView] = useState<'my' | 'all'>('my');

  const addTable = (tableData: Omit<Table, 'id'>) => {
    const newTable: Table = {
      ...tableData,
      id: Date.now(),
      disabledCells: tableData.disabledCells || new Set(),
      disabledRows: tableData.disabledRows || new Set(),
      disabledColumns: tableData.disabledColumns || new Set()
    };
    setAllTables(prev => [...prev, newTable]);
  };

  const deleteTable = (tableId: number) => {
    setAllTables(prev => prev.filter(table => table.id !== tableId));
  };

  const updateTable = (tableId: number, updates: Partial<Table>) => {
    setAllTables(prev => prev.map(table => 
      table.id === tableId ? { 
        ...table, 
        ...updates,
        disabledCells: updates.disabledCells || table.disabledCells || new Set(),
        disabledRows: updates.disabledRows || table.disabledRows || new Set(),
        disabledColumns: updates.disabledColumns || table.disabledColumns || new Set()
      } : table
    ));
  };

  const filteredTables = allTables.filter(table => 
    currentView === 'all' || table.isMyProject
  );

  return (
    <AppContext.Provider value={{
      tables: filteredTables,
      currentView,
      setCurrentView,
      addTable,
      deleteTable,
      updateTable,
    }}>
      {children}
    </AppContext.Provider>
  );
};

export const useApp = () => {
  const context = useContext(AppContext);
  if (context === undefined) {
    throw new Error('useApp must be used within an AppProvider');
  }
  return context;
};