import api from './api'

export interface User {
  id: number
  email: string
  name: string
}

export interface AuthResponse {
  user: User
  access: string
  refresh: string
}

export const authService = {
  async register(email: string, name: string, password: string): Promise<AuthResponse> {
    const response = await api.post('/auth/register/', { email, name, password })
    return response.data
  },

  async login(email: string, password: string): Promise<AuthResponse> {
    const response = await api.post('/auth/login/', { email, password })
    return response.data
  },

  logout() {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user')
  },

  getCurrentUser(): User | null {
    const userStr = localStorage.getItem('user')
    return userStr ? JSON.parse(userStr) : null
  },

  isAuthenticated(): boolean {
    return !!localStorage.getItem('access_token')
  },
}
