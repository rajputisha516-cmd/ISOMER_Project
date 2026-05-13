import React, { useEffect, useRef, useState } from 'react'
import { Activity, AlertCircle, Plug, Zap } from 'lucide-react'
import io from 'socket.io-client'

import AlertPanel from '../components/AlertPanel'
import StatsCard from '../components/StatsCard'
import VideoStream from '../components/VideoStream'
import api from '../services/api'

const SOCKET_URL = import.meta.env.VITE_SOCKET_URL || 'http://localhost:5000'

function Dashboard() {
  const [streaming, setStreaming] = useState(false)
  const [streamError, setStreamError] = useState('')
  const [connectionState, setConnectionState] = useState('connecting')
  const [stats, setStats] = useState({
    detections: 0,
    alerts: 0,
    activeAlerts: 0,
    fps: 0
  })
  const [socket, setSocket] = useState(null)
  const lastFpsUpdateRef = useRef(0)

  useEffect(() => {
    const newSocket = io(SOCKET_URL)

    const handleConnect = () => {
      setConnectionState('connected')
      setStreamError('')
      newSocket.emit('start_stream', { source: 0 })
    }

    const handleDisconnect = () => {
      setConnectionState('disconnected')
      setStreaming(false)
      setStats(prev => ({ ...prev, fps: 0 }))
    }

    const handleConnectError = () => {
      setConnectionState('error')
      setStreaming(false)
      setStreamError('Unable to connect to the backend stream service.')
    }

    const handleStreamStarted = () => {
      setStreaming(true)
      setStreamError('')
    }

    const handleStreamStopped = () => {
      setStreaming(false)
      setStats(prev => ({ ...prev, fps: 0 }))
    }

    const handleStreamError = (data) => {
      setStreaming(false)
      setStats(prev => ({ ...prev, fps: 0 }))
      setStreamError(data?.message || 'Unable to start the video stream.')
    }

    const handleVideoFrame = (data) => {
      const now = Date.now()
      if (now - lastFpsUpdateRef.current < 500) {
        return
      }

      lastFpsUpdateRef.current = now
      setStats(prev => ({
        ...prev,
        fps: data?.fps || 0
      }))
    }

    newSocket.on('connect', handleConnect)
    newSocket.on('disconnect', handleDisconnect)
    newSocket.on('connect_error', handleConnectError)
    newSocket.on('stream_started', handleStreamStarted)
    newSocket.on('stream_stopped', handleStreamStopped)
    newSocket.on('stream_error', handleStreamError)
    newSocket.on('video_frame', handleVideoFrame)

    setSocket(newSocket)

    return () => {
      newSocket.off('connect', handleConnect)
      newSocket.off('disconnect', handleDisconnect)
      newSocket.off('connect_error', handleConnectError)
      newSocket.off('stream_started', handleStreamStarted)
      newSocket.off('stream_stopped', handleStreamStopped)
      newSocket.off('stream_error', handleStreamError)
      newSocket.off('video_frame', handleVideoFrame)
      newSocket.disconnect()
      setSocket(null)
    }
  }, [])

  useEffect(() => {
    const loadStats = async () => {
      try {
        const response = await api.get('/history/dashboard-stats')
        if (response.data.success) {
          setStats(prev => ({
            ...prev,
            detections: response.data.total_detections,
            alerts: response.data.total_alerts,
            activeAlerts: response.data.active_alerts
          }))
        }
      } catch (error) {
        console.error('Failed to fetch stats:', error)
      }
    }

    loadStats()
    const interval = setInterval(loadStats, 5000)
    return () => clearInterval(interval)
  }, [])

  const startStream = () => {
    if (!socket) {
      return
    }

    setStreamError('')
    socket.emit('start_stream', { source: 0 })
  }

  const stopStream = () => {
    if (!socket) {
      return
    }

    socket.emit('stop_stream')
  }

  const connectionLabel = {
    connecting: 'Connecting',
    connected: 'Connected',
    disconnected: 'Disconnected',
    error: 'Connection Error'
  }[connectionState] || 'Unknown'

  return (
    <div className="p-8 space-y-6">
      <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
        <div>
          <h2 className="text-3xl font-bold">Dashboard</h2>
          <div className="mt-2 flex items-center gap-2 text-sm text-gray-400">
            <Plug size={14} />
            <span>{connectionLabel}</span>
          </div>
        </div>

        <div className="flex flex-col items-start gap-3 lg:items-end">
          <div className="flex gap-3">
            <button
              onClick={startStream}
              disabled={streaming || connectionState !== 'connected'}
              className="px-6 py-2 bg-green-600 hover:bg-green-700 disabled:bg-gray-700 rounded-lg font-semibold transition"
            >
              Start Stream
            </button>
            <button
              onClick={stopStream}
              disabled={!streaming}
              className="px-6 py-2 bg-red-600 hover:bg-red-700 disabled:bg-gray-700 rounded-lg font-semibold transition"
            >
              Stop Stream
            </button>
          </div>

          {streamError && (
            <p className="text-sm text-red-400">{streamError}</p>
          )}
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <StatsCard
          icon={AlertCircle}
          label="Total Detections"
          value={stats.detections}
          trend="Stored detections"
        />
        <StatsCard
          icon={AlertCircle}
          label="Total Alerts"
          value={stats.alerts}
          trend={`${stats.activeAlerts} active`}
          color="red"
        />
        <StatsCard
          icon={Zap}
          label="Active Alerts"
          value={stats.activeAlerts}
          trend="Monitoring"
          color="yellow"
        />
        <StatsCard
          icon={Activity}
          label="FPS"
          value={Math.round(stats.fps)}
          trend={streaming ? 'Live stream' : 'Idle'}
          color="blue"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <VideoStream
            socket={socket}
            streaming={streaming}
            streamError={streamError}
            connectionState={connectionState}
          />
        </div>

        <div>
          <AlertPanel socket={socket} />
        </div>
      </div>

      <div className="glass p-6 rounded-lg">
        <h3 className="text-xl font-semibold mb-4">Intrusion Detection Zone</h3>
        <div className="bg-gray-800 rounded-lg h-64 flex items-center justify-center text-gray-500">
          <p>Zone visualization would appear here</p>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
