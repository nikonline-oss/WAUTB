export interface User {
  id: number;
  name: string;
  email: string;
  role: string;
  position: string;
}

export interface Table {
  id: number;
  name: string;
  description?: string;
  createdBy: number;
  createdAt: string;
  columns: TableColumn[];
  data: TableRow[];
}

export interface TableColumn {
  id: number;
  name: string;
  type: 'text' | 'number' | 'timestamp' | 'list';
  options?: string[];
}

export interface TableRow {
  id: number;
  tableId: number;
  data: Record<string, any>;
  createdBy: number;
  updatedBy: number;
  version: number;
}