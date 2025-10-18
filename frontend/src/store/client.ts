import axios, { AxiosInstance, AxiosResponse, AxiosError } from 'axios';

const API_BASE_URL = 'http://localhost:8000';

class ApiClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    this.setupInterceptors();
  }

  private setupInterceptors(): void {
    // Request interceptor - добавляем токен
    this.client.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('auth_token');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error: AxiosError) => {
        return Promise.reject(error);
      }
    );

    // Response interceptor - обработка ошибок
    this.client.interceptors.response.use(
      (response: AxiosResponse) => response,
      (error: AxiosError) => {
        if (error.response?.status === 401) {
          this.handleUnauthorized();
        }
        return Promise.reject(error);
      }
    );
  }

  private handleUnauthorized(): void {
    localStorage.removeItem('auth_token');
    window.location.href = '/login';
  }

  public get<T>(url: string, params?: any): Promise<AxiosResponse<T>> {
    return this.client.get<T>(url, { params });
  }

  public post<T>(url: string, data?: any): Promise<AxiosResponse<T>> {
    return this.client.post<T>(url, data);
  }

  public put<T>(url: string, data?: any): Promise<AxiosResponse<T>> {
    return this.client.put<T>(url, data);
  }

  public delete<T>(url: string): Promise<AxiosResponse<T>> {
    return this.client.delete<T>(url);
  }
}

export const apiClient = new ApiClient();