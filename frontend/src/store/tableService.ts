import { Table, TableCreate, TableUpdate } from '../types/table';
import { apiClient } from './client';


export const tableService = {
  async getAllTables(): Promise<Table[]> {
    try {
      const response = await apiClient.get<Table[]>('/tables/');
      return response.data;
    } catch (error: any) {
      throw new Error(`Failed to fetch tables: ${error.message}`);
    }
  },

  // Получить таблицы текущего пользователя
  async getMyTables(): Promise<Table[]> {
    try {
      const response = await apiClient.get<Table[]>('/tables/my/');
      return response.data;
    } catch (error: any) {
      throw new Error(`Failed to fetch my tables: ${error.message}`);
    }
  },

  // Создать таблицу
  async createTable(tableData: TableCreate): Promise<Table> {
    try {
      const response = await apiClient.post<Table>('/tables/', tableData);
      return response.data;
    } catch (error: any) {
      throw new Error(`Failed to create table: ${error.message}`);
    }
  },

  // Обновить таблицу
  async updateTable(tableId: number, updates: TableUpdate): Promise<Table> {
    try {
      const response = await apiClient.put<Table>(`/tables/${tableId}`, updates);
      return response.data;
    } catch (error: any) {
      throw new Error(`Failed to update table: ${error.message}`);
    }
  },

  // Удалить таблицу
  async deleteTable(tableId: number): Promise<void> {
    try {
      await apiClient.delete(`/tables/${tableId}`);
    } catch (error: any) {
      throw new Error(`Failed to delete table: ${error.message}`);
    }
  },

  // Получить таблицу по ID
  async getTableById(tableId: number): Promise<Table> {
    try {
      const response = await apiClient.get<Table>(`/tables/${tableId}`);
      return response.data;
    } catch (error: any) {
      throw new Error(`Failed to fetch table: ${error.message}`);
    }
  },
};