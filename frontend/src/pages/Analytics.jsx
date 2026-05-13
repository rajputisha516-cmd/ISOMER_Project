import React, { useEffect, useState } from 'react'
import { BarChart, Bar, LineChart, Line, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import api from '../services/api'

function Analytics() {
  const [detectionStats, setDetectionStats] = useState(null)
  const [alertStats, setAlertStats] = useState(null)
  const [dailySummary, setDailySummary] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchAnalytics()
  }, [])

  const fetchAnalytics = async () => {
    try {
      setLoading(true)
      
      const [detRes, alertRes, dailyRes] = await Promise.all([
        api.get('/detection/statistics'),
        api.get('/alert/statistics'),
        api.get('/history/daily-summary')
      ])

      if (detRes.data.success) {
        setDetectionStats(detRes.data)
      }
      if (alertRes.data.success) {
        setAlertStats(alertRes.data)
      }
      if (dailyRes.data.success) {
        setDailySummary(dailyRes.data.summary)
      }
    } catch (error) {
      console.error('Failed to fetch analytics:', error)
    } finally {
      setLoading(false)
    }
  }

  const COLORS = ['#3b82f6', '#ef4444', '#10b981', '#f59e0b', '#8b5cf6', '#ec4899']

  if (loading) {
    return <div className="p-8">Loading analytics...</div>
  }

  return (
    <div className="p-8 space-y-6">
      <h2 className="text-3xl font-bold">Analytics & Insights</h2>

      {/* Detection Distribution */}
      {detectionStats && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="glass p-6 rounded-lg">
            <h3 className="text-xl font-semibold mb-4">Detection Distribution</h3>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={Object.entries(detectionStats.class_distribution || {}).map(([name, value]) => ({
                    name,
                    value
                  }))}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, value }) => `${name}: ${value}`}
                  outerRadius={100}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {Object.keys(detectionStats.class_distribution || {}).map((_, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>

          {/* Alert Severity Distribution */}
          {alertStats && (
            <div className="glass p-6 rounded-lg">
              <h3 className="text-xl font-semibold mb-4">Alert Severity Distribution</h3>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={[
                  { name: 'Low', value: alertStats.severity_distribution?.low || 0 },
                  { name: 'Medium', value: alertStats.severity_distribution?.medium || 0 },
                  { name: 'High', value: alertStats.severity_distribution?.high || 0 }
                ]}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#444" />
                  <XAxis stroke="#999" />
                  <YAxis stroke="#999" />
                  <Tooltip contentStyle={{ backgroundColor: '#1f2937', border: 'none' }} />
                  <Bar dataKey="value" fill="#3b82f6" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          )}
        </div>
      )}

      {/* Alert Type Distribution */}
      {alertStats && (
        <div className="glass p-6 rounded-lg">
          <h3 className="text-xl font-semibold mb-4">Alert Types</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={[
              { name: 'Intrusion', value: alertStats.type_distribution?.intrusion || 0 },
              { name: 'Motion', value: alertStats.type_distribution?.motion || 0 },
              { name: 'Unknown', value: alertStats.type_distribution?.unknown_object || 0 }
            ]}>
              <CartesianGrid strokeDasharray="3 3" stroke="#444" />
              <XAxis stroke="#999" />
              <YAxis stroke="#999" />
              <Tooltip contentStyle={{ backgroundColor: '#1f2937', border: 'none' }} />
              <Legend />
              <Bar dataKey="value" fill="#10b981" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* Daily Summary */}
      {dailySummary.length > 0 && (
        <div className="glass p-6 rounded-lg">
          <h3 className="text-xl font-semibold mb-4">7-Day Summary</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={dailySummary}>
              <CartesianGrid strokeDasharray="3 3" stroke="#444" />
              <XAxis stroke="#999" dataKey="date" />
              <YAxis stroke="#999" />
              <Tooltip contentStyle={{ backgroundColor: '#1f2937', border: 'none' }} />
              <Legend />
              <Line type="monotone" dataKey="detections" stroke="#3b82f6" strokeWidth={2} />
              <Line type="monotone" dataKey="alerts" stroke="#ef4444" strokeWidth={2} />
              <Line type="monotone" dataKey="intrusions" stroke="#f59e0b" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* Statistics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {detectionStats && (
          <div className="glass p-6 rounded-lg">
            <p className="text-gray-400 text-sm">Most Detected Object</p>
            <p className="text-2xl font-bold text-blue-400 mt-2">{detectionStats.most_detected}</p>
          </div>
        )}
        {alertStats && (
          <div className="glass p-6 rounded-lg">
            <p className="text-gray-400 text-sm">Total Alerts</p>
            <p className="text-2xl font-bold text-red-400 mt-2">{alertStats.total_alerts}</p>
          </div>
        )}
        {alertStats && (
          <div className="glass p-6 rounded-lg">
            <p className="text-gray-400 text-sm">Active Alerts</p>
            <p className="text-2xl font-bold text-yellow-400 mt-2">{alertStats.total_alerts - (alertStats.total_alerts / 4)}</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default Analytics
