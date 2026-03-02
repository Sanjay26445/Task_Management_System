import api from './api'

export interface Analytics {
  total_tasks: number
  completed_tasks: number
  completion_percentage: number
  tasks_per_day: Array<{ date: string; count: number }>
  most_productive_day: { date: string; count: number } | null
  average_completion_time_hours: number | null
  priority_distribution: {
    Low: number
    Medium: number
    High: number
  }
  productivity_score: number
}

export const analyticsService = {
  async getAnalytics(): Promise<Analytics> {
    const response = await api.get('/analytics/')
    return response.data
  },
}
