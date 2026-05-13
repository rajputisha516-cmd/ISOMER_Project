import React, { useEffect, useRef, useState } from 'react'
import { AlertTriangle, Play } from 'lucide-react'

function VideoStream({ socket, streaming, streamError, connectionState, currentDetections }) {
  const imageRef = useRef(null)
  const [fps, setFps] = useState(0)
  const [hasFrame, setHasFrame] = useState(false)

  useEffect(() => {
    if (!socket) {
      return undefined
    }

    const handleVideoFrame = (data) => {
      if (imageRef.current) {
        imageRef.current.src = `data:image/jpeg;base64,${data.frame}`
      }

      setHasFrame(true)
      setFps(Math.round(data?.fps || 0))
    }

    const handleStreamStopped = () => {
      setHasFrame(false)
      setFps(0)
      if (imageRef.current) {
        imageRef.current.removeAttribute('src')
      }
    }

    socket.on('video_frame', handleVideoFrame)
    socket.on('stream_stopped', handleStreamStopped)

    return () => {
      socket.off('video_frame', handleVideoFrame)
      socket.off('stream_stopped', handleStreamStopped)
    }
  }, [socket])

  useEffect(() => {
    if (streaming) {
      return
    }

    setHasFrame(false)
    setFps(0)
    if (imageRef.current) {
      imageRef.current.removeAttribute('src')
    }
  }, [streaming])

  const waitingForFrames = streaming && !hasFrame && !streamError
  const uniqueDetections = Array.isArray(currentDetections)
    ? currentDetections.reduce((accumulator, detection) => {
        const label = detection?.class_name
        if (!label || accumulator.includes(label)) {
          return accumulator
        }
        return [...accumulator, label]
      }, [])
    : []

  return (
    <div className="glass p-6 rounded-lg h-full flex flex-col">
      <h3 className="text-xl font-semibold mb-4">Live Stream</h3>

      <div className="flex-1 flex items-center justify-center bg-gray-800 rounded-lg overflow-hidden relative min-h-[420px]">
        <img
          ref={imageRef}
          alt="Live surveillance stream"
          className="w-full h-full object-cover"
        />

        {!streaming && !streamError && (
          <div className="absolute inset-0 flex items-center justify-center bg-black/50">
            <div className="text-center">
              <Play size={48} className="mx-auto mb-4 text-gray-500" />
              <p className="text-gray-400">Stream not active</p>
            </div>
          </div>
        )}

        {waitingForFrames && (
          <div className="absolute inset-0 flex items-center justify-center bg-black/50">
            <div className="text-center">
              <p className="text-lg font-semibold text-white">Waiting for camera frames...</p>
              <p className="mt-2 text-sm text-gray-300">The backend is connected and starting the capture.</p>
            </div>
          </div>
        )}

        {streamError && (
          <div className="absolute inset-0 flex items-center justify-center bg-black/65">
            <div className="max-w-md text-center px-6">
              <AlertTriangle size={40} className="mx-auto mb-4 text-red-400" />
              <p className="text-lg font-semibold text-red-300">Camera stream unavailable</p>
              <p className="mt-2 text-sm text-gray-200">{streamError}</p>
            </div>
          </div>
        )}

        {streaming && hasFrame && (
          <div className="absolute top-4 right-4 flex items-center gap-2 px-3 py-2 bg-black/70 rounded-lg">
            <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse" />
            <span className="text-sm text-green-400">LIVE</span>
          </div>
        )}

        {fps > 0 && (
          <div className="absolute bottom-4 right-4 px-3 py-2 bg-black/70 rounded-lg text-sm text-blue-400">
            FPS: {fps}
          </div>
        )}
      </div>

      <div className="mt-4 text-sm text-gray-400 space-y-1">
        <p>Resolution: 640x480</p>
        <p>Status: {streaming ? 'Active' : 'Inactive'}</p>
        <p>Connection: {connectionState}</p>
        <p>Detections in frame: {currentDetections?.length || 0}</p>
      </div>

      <div className="mt-4">
        <p className="text-sm text-gray-400 mb-2">Detected classes</p>
        {uniqueDetections.length > 0 ? (
          <div className="flex flex-wrap gap-2">
            {uniqueDetections.map((label) => (
              <span
                key={label}
                className="px-3 py-1 rounded-full bg-blue-500/15 border border-blue-500/30 text-blue-200 text-xs uppercase tracking-wide"
              >
                {label}
              </span>
            ))}
          </div>
        ) : (
          <p className="text-sm text-gray-500">No objects detected in the latest frame.</p>
        )}
      </div>
    </div>
  )
}

export default VideoStream
