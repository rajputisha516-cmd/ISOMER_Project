import React, { useEffect, useState } from 'react'
import { AlertCircle, Trash2 } from 'lucide-react'
import api from '../services/api'

function AlertPanel({ socket }) {
  const [alerts, setAlerts] = useState([])

  useEffect(() => {
    fetchAlerts()
    const interval = setInterval(fetchAlerts, 5000)
    return () => clearInterval(interval)
  }, [])

  useEffect(() => {
    if (!socket) {
      return undefined
    }

    const handleAlertTriggered = (data) => {
      setAlerts(prev => [data, ...prev].slice(0, 10))
    }

    socket.on('alert_triggered', handleAlertTriggered)

    return () => {
      socket.off('alert_triggered', handleAlertTriggered)
    }
  }, [socket])

  const fetchAlerts = async () => {
    try {
      const response = await api.get('/alert/active')
      if (response.data.success) {
        setAlerts(response.data.alerts)
      }
    } catch (error) {
      console.error('Failed to fetch alerts:', error)
    }
  }

  const acknowledgeAlert = async (alertId) => {
    try {
      await api.put(`/alert/acknowledge/${alertId}`)
      setAlerts(prev => prev.filter(a => a.id !== alertId))
    } catch (error) {
      console.error('Failed to acknowledge alert:', error)
    }
  }

  return (
    <div className="glass p-6 rounded-lg h-full flex flex-col">
      <h3 className="text-xl font-semibold mb-4 flex items-center gap-2">
        <AlertCircle className="text-red-400" />
        Active Alerts
      </h3>

      <div className="flex-1 overflow-y-auto space-y-2">
        {alerts.length === 0 ? (
          <p className="text-center text-gray-500 py-8">No active alerts</p>
        ) : (
          alerts.map((alert) => (
            <div
              key={alert.id}
              className="bg-red-900/20 border border-red-700/50 rounded-lg p-3 text-sm hover:bg-red-900/30 transition"
            >
              <div className="flex items-start justify-between gap-2 mb-1">
                <span className="font-semibold text-red-400 capitalize">
                  {alert.alert_type || alert.type || 'alert'}
                </span>
                {alert.id && (
                  <button
                    onClick={() => acknowledgeAlert(alert.id)}
                    className="text-gray-500 hover:text-gray-300 transition"
                  >
                    <Trash2 size={14} />
                  </button>
                )}
              </div>
              <p className="text-gray-400 mb-1">{alert.message}</p>
              <p className="text-xs text-gray-500">
                {new Date(alert.timestamp).toLocaleTimeString()}
              </p>
            </div>
          ))
        )}
      </div>
    </div>
  )
}

export default AlertPanel
