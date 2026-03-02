import api from './api'

export interface Task {
  id: number
  title: string
  description: string
  priority: 'Low' | 'Medium' | 'High'
  status: 'Pending' | 'Completed' | 'Archived'
  due_date: string | null
  created_at: string
  updated_at: string
}

export const taskService = {
  async getTasks(filters?: { status?: string; priority?: string }): Promise<Task[]> {
    const params = new URLSearchParams()
    if (filters?.status) params.append('status', filters.status)
    if (filters?.priority) params.append('priority', filters.priority)
    
    const response = await api.get(`/tasks/?${params.toString()}`)
    return response.data.results || response.data
  },

  async getTask(id: number): Promise<Task> {
    const response = await api.get(`/tasks/${id}/`)
    return response.data
  },

  async createTask(data: Partial<Task>): Promise<Task> {
    const response = await api.post('/tasks/', data)
    return response.data
  },

  async updateTask(id: number, data: Partial<Task>): Promise<Task> {
    const response = await api.put(`/tasks/${id}/`, data)
    return response.data
  },

  async deleteTask(id: number): Promise<void> {
    await api.delete(`/tasks/${id}/`)
  },

  async completeTask(id: number): Promise<Task> {
    const response = await api.post(`/tasks/${id}/complete/`)
    return response.data
  },

  async archiveTask(id: number): Promise<Task> {
    const response = await api.post(`/tasks/${id}/archive/`)
    return response.data
  },
}
