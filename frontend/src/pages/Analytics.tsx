import { useEffect, useState } from 'react'
import Layout from '../components/Layout'
import { analyticsService, Analytics as AnalyticsData } from '../services/analyticsService'
import { BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

const Analytics = () => {
  const [analytics, setAnalytics] = useState<AnalyticsData | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadAnalytics()
  }, [])

  const loadAnalytics = async () => {
    try {
      const data = await analyticsService.getAnalytics()
      setAnalytics(data)
    } catch (error) {
      console.error('Failed to load analytics', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <Layout>
        <div className="px-4 py-6">
          <p className="text-gray-500">Loading analytics...</p>
        </div>
      </Layout>
    )
  }

  if (!analytics) {
    return (
      <Layout>
        <div className="px-4 py-6">
          <p className="text-gray-500">No analytics data available</p>
        </div>
      </Layout>
    )
  }

  const priorityData = [
    { name: 'Low', value: analytics.priority_distribution.Low, color: '#10b981' },
    { name: 'Medium', value: analytics.priority_distribution.Medium, color: '#f59e0b' },
    { name: 'High', value: analytics.priority_distribution.High, color: '#ef4444' },
  ]

  const tasksPerDayData = analytics.tasks_per_day.map((item) => ({
    date: new Date(item.date).toLocaleDateString(),
    count: item.count,
  }))

  return (
    <Layout>
      <div className="px-4 py-6 sm:px-0">
        <h1 className="text-3xl font-bold text-gray-900 mb-6">Analytics</h1>

        <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4 mb-8">
          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="p-5">
              <dt className="text-sm font-medium text-gray-500 truncate">Total Tasks</dt>
              <dd className="mt-1 text-3xl font-semibold text-gray-900">
                {analytics.total_tasks}
              </dd>
            </div>
          </div>

          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="p-5">
              <dt className="text-sm font-medium text-gray-500 truncate">Completed</dt>
              <dd className="mt-1 text-3xl font-semibold text-green-600">
                {analytics.completed_tasks}
              </dd>
            </div>
          </div>

          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="p-5">
              <dt className="text-sm font-medium text-gray-500 truncate">Completion Rate</dt>
              <dd className="mt-1 text-3xl font-semibold text-indigo-600">
                {analytics.completion_percentage}%
              </dd>
            </div>
          </div>

          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="p-5">
              <dt className="text-sm font-medium text-gray-500 truncate">Productivity Score</dt>
              <dd className="mt-1 text-3xl font-semibold text-purple-600">
                {analytics.productivity_score}
              </dd>
            </div>
          </div>
        </div>

        {analytics.average_completion_time_hours && (
          <div className="bg-white shadow rounded-lg p-6 mb-6">
            <h3 className="text-lg font-medium text-gray-900 mb-2">Average Completion Time</h3>
            <p className="text-2xl font-semibold text-gray-700">
              {analytics.average_completion_time_hours.toFixed(1)} hours
            </p>
          </div>
        )}

        {analytics.most_productive_day && (
          <div className="bg-white shadow rounded-lg p-6 mb-6">
            <h3 className="text-lg font-medium text-gray-900 mb-2">Most Productive Day</h3>
            <p className="text-xl text-gray-700">
              {new Date(analytics.most_productive_day.date).toLocaleDateString()} -{' '}
              <span className="font-semibold">{analytics.most_productive_day.count} tasks</span>
            </p>
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
          <div className="bg-white shadow rounded-lg p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Priority Distribution</h3>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={priorityData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, value }) => `${name}: ${value}`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {priorityData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>

          {tasksPerDayData.length > 0 && (
            <div className="bg-white shadow rounded-lg p-6">
              <h3 className="text-lg font-medium text-gray-900 mb-4">Tasks Completed Per Day</h3>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={tasksPerDayData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="count" fill="#6366f1" name="Tasks" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          )}
        </div>

        <div className="bg-blue-50 border-l-4 border-blue-400 p-4">
          <div className="flex">
            <div className="ml-3">
              <h3 className="text-sm font-medium text-blue-800">Productivity Score Calculation</h3>
              <div className="mt-2 text-sm text-blue-700">
                <p>
                  Your productivity score is calculated based on:
                </p>
                <ul className="list-disc list-inside mt-2 space-y-1">
                  <li>Completed tasks (10 points each)</li>
                  <li>High priority completions (5 bonus points)</li>
                  <li>Medium priority completions (3 bonus points)</li>
                  <li>On-time completions (7 bonus points)</li>
                  <li>Overdue tasks (3 penalty points)</li>
                  <li>Normalized by days active</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  )
}

export default Analytics
