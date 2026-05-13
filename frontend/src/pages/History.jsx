import React, { useEffect, useState } from 'react'
import { Download, Filter } from 'lucide-react'
import api from '../services/api'

function History() {
  const [detections, setDetections] = useState([])
  const [alerts, setAlerts] = useState([])
  const [activeTab, setActiveTab] = useState('detections')
  const [loading, setLoading] = useState(false)
  const [startDate, setStartDate] = useState('')
  const [endDate, setEndDate] = useState('')

  useEffect(() => {
    fetchHistory()
  }, [activeTab, startDate, endDate])

  const fetchHistory = async () => {
    try {
      setLoading(true)
      
      if (activeTab === 'detections') {
        const params = {}
        if (startDate) params.start_date = startDate
        if (endDate) params.end_date = endDate
        
        const response = await api.get('/history/detections', { params })
        if (response.data.success) {
          setDetections(response.data.detections)
        }
      } else {
        const params = {}
        if (startDate) params.start_date = startDate
        if (endDate) params.end_date = endDate
        
        const response = await api.get('/history/alerts', { params })
        if (response.data.success) {
          setAlerts(response.data.alerts)
        }
      }
    } catch (error) {
      console.error('Failed to fetch history:', error)
    } finally {
      setLoading(false)
    }
  }

  const exportToCSV = async () => {
    try {
      const response = await api.get('/history/export/csv', {
        responseType: 'blob'
      })
      
      const url = window.URL.createObjectURL(response.data)
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', `history_${new Date().toISOString().split('T')[0]}.csv`)
      document.body.appendChild(link)
      link.click()
      link.remove()
      window.URL.revokeObjectURL(url)
    } catch (error) {
      console.error('Failed to export:', error)
    }
  }

  return (
    <div className="p-8 space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-3xl font-bold">Detection History</h2>
        <button
          onClick={exportToCSV}
          className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg transition"
        >
          <Download size={18} />
          Export CSV
        </button>
      </div>

      {/* Filters */}
      <div className="glass p-6 rounded-lg flex gap-4">
        <div className="flex-1">
          <label className="block text-sm text-gray-400 mb-2">Start Date</label>
          <input
            type="date"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
            className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg focus:outline-none focus:border-blue-500"
          />
        </div>
        <div className="flex-1">
          <label className="block text-sm text-gray-400 mb-2">End Date</label>
          <input
            type="date"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
            className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg focus:outline-none focus:border-blue-500"
          />
        </div>
        <div className="flex items-end">
          <button
            onClick={fetchHistory}
            className="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg transition flex items-center gap-2"
          >
            <Filter size={18} />
            Apply
          </button>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex gap-4 border-b border-gray-800">
        <button
          onClick={() => setActiveTab('detections')}
          className={`px-6 py-3 font-semibold border-b-2 transition ${
            activeTab === 'detections'
              ? 'border-blue-500 text-blue-400'
              : 'border-transparent text-gray-400 hover:text-gray-300'
          }`}
        >
          Detections ({detections.length})
        </button>
        <button
          onClick={() => setActiveTab('alerts')}
          className={`px-6 py-3 font-semibold border-b-2 transition ${
            activeTab === 'alerts'
              ? 'border-blue-500 text-blue-400'
              : 'border-transparent text-gray-400 hover:text-gray-300'
          }`}
        >
          Alerts ({alerts.length})
        </button>
      </div>

      {/* Content */}
      {loading ? (
        <div className="text-center text-gray-400">Loading...</div>
      ) : (
        <>
          {activeTab === 'detections' && (
            <div className="space-y-4">
              {detections.length === 0 ? (
                <div className="glass p-6 rounded-lg text-center text-gray-400">
                  No detections found
                </div>
              ) : (
                detections.map((detection) => (
                  <div key={detection.id} className="glass p-4 rounded-lg flex items-center justify-between hover:bg-white/15 transition">
                    <div className="flex-1">
                      <p className="font-semibold text-blue-400">{detection.frame_id}</p>
                      <p className="text-sm text-gray-400">{new Date(detection.timestamp).toLocaleString()}</p>
                      <p className="text-sm mt-2">
                        Objects: {detection.objects_detected?.length || 0} | Confidence: {(detection.confidence_score * 100).toFixed(1)}%
                      </p>
                    </div>
                    <div className="text-right">
                      {detection.image_path && (
                        <a href={detection.image_path} className="text-blue-400 hover:text-blue-300 text-sm">
                          View Image
                        </a>
                      )}
                    </div>
                  </div>
                ))
              )}
            </div>
          )}

          {activeTab === 'alerts' && (
            <div className="space-y-4">
              {alerts.length === 0 ? (
                <div className="glass p-6 rounded-lg text-center text-gray-400">
                  No alerts found
                </div>
              ) : (
                alerts.map((alert) => (
                  <div
                    key={alert.id}
                    className={`glass p-4 rounded-lg flex items-center justify-between hover:bg-white/15 transition border-l-4 ${
                      alert.severity === 'high'
                        ? 'border-red-500'
                        : alert.severity === 'medium'
                        ? 'border-yellow-500'
                        : 'border-blue-500'
                    }`}
                  >
                    <div className="flex-1">
                      <p className="font-semibold capitalize">{alert.alert_type || alert.type}</p>
                      <p className="text-sm text-gray-400">{alert.message}</p>
                      <p className="text-xs text-gray-500 mt-1">{new Date(alert.timestamp).toLocaleString()}</p>
                    </div>
                    <div className="text-right">
                      <span className={`px-3 py-1 rounded text-sm font-semibold ${
                        alert.severity === 'high'
                          ? 'bg-red-900 text-red-200'
                          : alert.severity === 'medium'
                          ? 'bg-yellow-900 text-yellow-200'
                          : 'bg-blue-900 text-blue-200'
                      }`}>
                        {alert.severity}
                      </span>
                    </div>
                  </div>
                ))
              )}
            </div>
          )}
        </>
      )}
    </div>
  )
}

export default History
