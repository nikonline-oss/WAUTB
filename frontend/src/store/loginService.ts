import { apiClient } from './client';
import { LoginResponse, User } from '../types/index';

export const authService = {
  async login(email: string, password: string): Promise<LoginResponse> {
    const formData = new FormData();
    formData.append('email', email);
    formData.append('password', password);

    const response = await apiClient.post<LoginResponse>('/login', formData);

    if (response.data.access_token) {
      localStorage.setItem('token', response.data.access_token);
    }

    return response.data;
  },

  logout(): void {
    localStorage.removeItem('token');
  },

  getToken(): string | null {
    return localStorage.getItem('token');
  },

  isAuthenticated(): boolean {
    return !!this.getToken();
  },
};