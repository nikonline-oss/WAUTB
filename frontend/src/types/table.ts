export interface Table {
  id: number;
  name: string;
  image: string;
  createdBy: string;
  isMyProject: boolean;
  columns: TableColumn[];
  data: TableRow[];
  disabledCells: Set<string>;
  disabledRows: Set<number>;
  disabledColumns: Set<number>;
}

export interface TableColumn {
  id: number;
  name: string;
  type: 'number' | 'text' | 'list' | 'date' | 'boolean';
  options?: string[]; // для типа list
}

export interface TableRow {
  id: number;
  data: Record<number, any>; // columnId -> value
}

// API схемы
export interface TableCreate {
  name: string;
  image?: string;
  columns: Omit<TableColumn, 'id'>[];
}

export interface TableUpdate {
  name?: string;
  image?: string;
  columns?: TableColumn[];
}