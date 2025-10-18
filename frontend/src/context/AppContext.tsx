import React, { createContext, useContext, useState, ReactNode } from 'react';

export interface Table {
  id: number;
  name: string;
  image: string;
  createdBy: string;
  isMyProject: boolean;
  columns: Column[];
  data: TableRow[];
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
      name: 'Мощь: 3х30м', 
      image: '📊', 
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
      ]
    },
    { 
      id: 2, 
      name: 'Мощь: 2х20м', 
      image: '📊', 
      createdBy: 'user2',
      isMyProject: false,
      columns: [
        { id: 1, name: 'ID', type: 'number' },
        { id: 2, name: 'Задача', type: 'text' },
      ],
      data: [
        { id: 1, data: { '1': 1, '2': 'Задача 1' } },
      ]
    },
    { 
      id: 3, 
      name: 'Мощь: 1х10м', 
      image: '📊', 
      createdBy: 'user1',
      isMyProject: true,
      columns: [
        { id: 1, name: 'ID', type: 'number' },
        { id: 2, name: 'Описание', type: 'text' },
      ],
      data: [
        { id: 1, data: { '1': 1, '2': 'Описание 1' } },
      ]
    },
  ]);

  const [currentView, setCurrentView] = useState<'my' | 'all'>('my');

  const addTable = (tableData: Omit<Table, 'id'>) => {
    const newTable: Table = {
      ...tableData,
      id: Date.now(),
    };
    setAllTables(prev => [...prev, newTable]);
  };

  const deleteTable = (tableId: number) => {
    setAllTables(prev => prev.filter(table => table.id !== tableId));
  };

  const updateTable = (tableId: number, updates: Partial<Table>) => {
    setAllTables(prev => prev.map(table => 
      table.id === tableId ? { ...table, ...updates } : table
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