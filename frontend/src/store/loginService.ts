import { apiClient } from './client';
import { LoginResponse, User } from '../types/index';

export const authService = {
  async login(email: string, password: string): Promise<LoginResponse> {
    const formData = new FormData();
    formData.append('email', email);
    formData.append('password', password);
    try {
      const response = await apiClient.post<LoginResponse>('/login', formData);
      if (response.data.access_token) {
        localStorage.setItem('token', response.data.access_token);
      }
      return response.data;
    } catch (error: any) {
      if (error.response) {
        const status = error.response.status;
        const message = error.response.data?.detail || 'Login failed';
        
        switch (status) {
          case 400:
            throw new Error(`Bad request: ${message}`);
          case 401:
            throw new Error(`Invalid credentials: ${message}`);
          case 404:
            throw new Error('Login endpoint not found');
          case 500:
            throw new Error('Server error. Please try again later.');
          default:
            throw new Error(`Login failed: ${message}`);
        }
      } else if (error.request) {
        throw new Error('Network error. Please check your connection.');
      } else {
        throw new Error(`Login error: ${error.message}`);
      }
    }
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