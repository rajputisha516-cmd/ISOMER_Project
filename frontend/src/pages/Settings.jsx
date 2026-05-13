import React, { useEffect, useState } from 'react'
import {
  Activity,
  AlertTriangle,
  CheckCircle2,
  FileVideo,
  Loader2,
  RefreshCw,
  Trash2,
  Upload
} from 'lucide-react'

import api from '../services/api'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000'
const SOCKET_URL = import.meta.env.VITE_SOCKET_URL || 'http://localhost:5000'

function formatBytes(bytes) {
  if (!bytes) {
    return '0 B'
  }

  const units = ['B', 'KB', 'MB', 'GB']
  let value = bytes
  let index = 0

  while (value >= 1024 && index < units.length - 1) {
    value /= 1024
    index += 1
  }

  return `${value.toFixed(value >= 10 || index === 0 ? 0 : 1)} ${units[index]}`
}

function Settings() {
  const [selectedFile, setSelectedFile] = useState(null)
  const [selectedVideo, setSelectedVideo] = useState('')
  const [uploadedVideos, setUploadedVideos] = useState([])
  const [analysisResults, setAnalysisResults] = useState(null)
  const [isLoadingVideos, setIsLoadingVideos] = useState(false)
  const [isUploading, setIsUploading] = useState(false)
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [uploadProgress, setUploadProgress] = useState(0)
  const [uploadError, setUploadError] = useState('')
  const [statusMessage, setStatusMessage] = useState('')

  const loadVideos = async () => {
    try {
      setIsLoadingVideos(true)
      const response = await api.get('/video/list')
      const videos = Array.isArray(response.data?.videos) ? response.data.videos : []

      setUploadedVideos(videos)
      setSelectedVideo((current) => {
        if (current && videos.some(video => video.filename === current)) {
          return current
        }
        return videos[0]?.filename || ''
      })
    } catch (error) {
      console.error('Failed to load videos:', error)
      setUploadError('Failed to load uploaded videos.')
    } finally {
      setIsLoadingVideos(false)
    }
  }

  useEffect(() => {
    loadVideos()
  }, [])

  const handleFileChange = (event) => {
    const file = event.target.files?.[0] || null
    setSelectedFile(file)
    setUploadError('')
    setStatusMessage('')
  }

  const handleUpload = async () => {
    if (!selectedFile) {
      setUploadError('Choose a video file before uploading.')
      return
    }

    const formData = new FormData()
    formData.append('file', selectedFile)

    try {
      setIsUploading(true)
      setUploadError('')
      setStatusMessage('')
      setUploadProgress(0)

      const response = await api.post('/video/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        onUploadProgress: (progressEvent) => {
          if (!progressEvent.total) {
            return
          }

          setUploadProgress(
            Math.round((progressEvent.loaded / progressEvent.total) * 100)
          )
        }
      })

      if (!response.data?.success) {
        throw new Error(response.data?.error || response.data?.message || 'Upload failed')
      }

      const uploadedFilename = response.data.filename
      setSelectedVideo(uploadedFilename)
      setStatusMessage(response.data.message || 'Video uploaded successfully.')
      setAnalysisResults(null)
      await loadVideos()
    } catch (error) {
      console.error('Failed to upload video:', error)
      setUploadError(error.response?.data?.error || error.message || 'Upload failed.')
    } finally {
      setIsUploading(false)
    }
  }

  const handleVideoAnalysis = async (filename = selectedVideo) => {
    if (!filename) {
      setUploadError('Select an uploaded video to analyze.')
      return
    }

    try {
      setIsAnalyzing(true)
      setUploadError('')
      setStatusMessage('')

      const response = await api.post('/video/analyze', {
        filename
      })

      if (!response.data?.success) {
        throw new Error(response.data?.error || response.data?.message || 'Analysis failed')
      }

      setAnalysisResults(response.data.analysis)
      setStatusMessage(response.data.message || 'Video analysis completed successfully.')
    } catch (error) {
      console.error('Failed to analyze video:', error)
      setUploadError(
        error.response?.data?.error || error.message || 'Failed to analyze the video.'
      )
    } finally {
      setIsAnalyzing(false)
    }
  }

  const handleDeleteVideo = async (filename) => {
    if (!window.confirm(`Delete ${filename}?`)) {
      return
    }

    try {
      setUploadError('')
      setStatusMessage('')
      await api.delete(`/video/delete/${encodeURIComponent(filename)}`)

      setAnalysisResults((current) => {
        if (selectedVideo === filename) {
          return null
        }
        return current
      })
      setStatusMessage('Video deleted successfully.')

      if (selectedVideo === filename) {
        setSelectedVideo('')
      }

      await loadVideos()
    } catch (error) {
      console.error('Failed to delete video:', error)
      setUploadError(error.response?.data?.error || error.message || 'Delete failed.')
    }
  }

  const detectionEntries = Object.entries(analysisResults?.detection_counts || {})
  const alerts = analysisResults?.alerts || []
  const sampleFrames = analysisResults?.sample_frames || []
  const videoProperties = analysisResults?.video_properties

  return (
    <div className="p-8 space-y-6">
      <div className="flex flex-col gap-3 lg:flex-row lg:items-end lg:justify-between">
        <div>
          <h2 className="text-3xl font-bold">Settings and Video Analysis</h2>
          <p className="mt-2 text-sm text-gray-400">
            Upload a recording, run the backend analyzer, and review the sampled results.
          </p>
        </div>

        <button
          onClick={loadVideos}
          disabled={isLoadingVideos}
          className="inline-flex items-center gap-2 px-4 py-2 bg-gray-800 hover:bg-gray-700 disabled:bg-gray-800/60 rounded-lg transition"
        >
          <RefreshCw size={16} className={isLoadingVideos ? 'animate-spin' : ''} />
          Refresh uploads
        </button>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
        <div className="xl:col-span-2 space-y-6">
          <div className="glass p-6 rounded-lg space-y-4">
            <div className="flex items-center gap-3">
              <Upload className="text-blue-400" />
              <h3 className="text-xl font-semibold">Upload Video</h3>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-[1fr_auto] gap-4">
              <input
                type="file"
                accept=".mp4,.avi,.mov,.flv,.wmv"
                onChange={handleFileChange}
                className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg focus:outline-none focus:border-blue-500"
              />

              <button
                onClick={handleUpload}
                disabled={!selectedFile || isUploading}
                className="inline-flex items-center justify-center gap-2 px-5 py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-700 rounded-lg font-semibold transition"
              >
                {isUploading ? <Loader2 size={18} className="animate-spin" /> : <Upload size={18} />}
                {isUploading ? 'Uploading...' : 'Upload'}
              </button>
            </div>

            {selectedFile && (
              <p className="text-sm text-gray-400">
                Selected file: <span className="text-gray-200">{selectedFile.name}</span>
              </p>
            )}

            {isUploading && (
              <div className="space-y-2">
                <div className="h-2 bg-gray-800 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-blue-500 transition-all"
                    style={{ width: `${uploadProgress}%` }}
                  />
                </div>
                <p className="text-sm text-gray-400">Upload progress: {uploadProgress}%</p>
              </div>
            )}

            {statusMessage && (
              <div className="flex items-start gap-3 rounded-lg border border-green-600/40 bg-green-900/20 px-4 py-3 text-sm text-green-200">
                <CheckCircle2 size={18} className="mt-0.5 shrink-0" />
                <span>{statusMessage}</span>
              </div>
            )}

            {uploadError && (
              <div className="flex items-start gap-3 rounded-lg border border-red-600/40 bg-red-900/20 px-4 py-3 text-sm text-red-200">
                <AlertTriangle size={18} className="mt-0.5 shrink-0" />
                <span>{uploadError}</span>
              </div>
            )}
          </div>

          <div className="glass p-6 rounded-lg space-y-4">
            <div className="flex items-center gap-3">
              <FileVideo className="text-cyan-400" />
              <h3 className="text-xl font-semibold">Uploaded Videos</h3>
            </div>

            {uploadedVideos.length === 0 ? (
              <p className="text-gray-400">
                No uploaded videos yet. Upload one above to start analysis.
              </p>
            ) : (
              <div className="space-y-3">
                {uploadedVideos.map((video) => {
                  const isSelected = selectedVideo === video.filename

                  return (
                    <div
                      key={video.filename}
                      className={`rounded-lg border p-4 transition ${
                        isSelected
                          ? 'border-blue-500 bg-blue-500/10'
                          : 'border-gray-800 bg-gray-900/60'
                      }`}
                    >
                      <div className="flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between">
                        <div className="space-y-1">
                          <button
                            onClick={() => setSelectedVideo(video.filename)}
                            className="text-left text-base font-semibold text-gray-100 hover:text-blue-300 transition"
                          >
                            {video.filename}
                          </button>
                          <p className="text-sm text-gray-400">
                            {formatBytes(video.size)} | Updated {new Date(video.modified_time).toLocaleString()}
                          </p>
                        </div>

                        <div className="flex flex-wrap gap-3">
                          <button
                            onClick={() => {
                              setSelectedVideo(video.filename)
                              handleVideoAnalysis(video.filename)
                            }}
                            disabled={isAnalyzing}
                            className="inline-flex items-center gap-2 px-4 py-2 bg-emerald-600 hover:bg-emerald-700 disabled:bg-gray-700 rounded-lg transition"
                          >
                            {isAnalyzing && selectedVideo === video.filename ? (
                              <Loader2 size={16} className="animate-spin" />
                            ) : (
                              <Activity size={16} />
                            )}
                            Analyze
                          </button>

                          <button
                            onClick={() => handleDeleteVideo(video.filename)}
                            className="inline-flex items-center gap-2 px-4 py-2 bg-red-600 hover:bg-red-700 rounded-lg transition"
                          >
                            <Trash2 size={16} />
                            Delete
                          </button>
                        </div>
                      </div>
                    </div>
                  )
                })}
              </div>
            )}
          </div>
        </div>

        <div className="space-y-6">
          <div className="glass p-6 rounded-lg space-y-3">
            <h3 className="text-xl font-semibold">Runtime Connections</h3>
            <div className="space-y-2 text-sm">
              <p className="text-gray-400">API URL</p>
              <p className="rounded-lg bg-gray-900/70 px-3 py-2 text-gray-200 break-all">{API_URL}</p>
              <p className="text-gray-400">Socket URL</p>
              <p className="rounded-lg bg-gray-900/70 px-3 py-2 text-gray-200 break-all">{SOCKET_URL}</p>
              <p className="text-gray-400">Supported video types: MP4, AVI, MOV, FLV, WMV</p>
            </div>
          </div>

          <div className="glass p-6 rounded-lg space-y-3">
            <h3 className="text-xl font-semibold">Current Selection</h3>
            <p className="text-sm text-gray-400">
              {selectedVideo || 'No uploaded video selected.'}
            </p>
            <button
              onClick={() => handleVideoAnalysis()}
              disabled={!selectedVideo || isAnalyzing}
              className="w-full inline-flex items-center justify-center gap-2 px-4 py-3 bg-cyan-600 hover:bg-cyan-700 disabled:bg-gray-700 rounded-lg font-semibold transition"
            >
              {isAnalyzing ? <Loader2 size={18} className="animate-spin" /> : <Activity size={18} />}
              {isAnalyzing ? 'Analyzing...' : 'Analyze Selected Video'}
            </button>
          </div>

          {analysisResults && (
            <div className="glass p-6 rounded-lg space-y-4">
              <h3 className="text-xl font-semibold">Analysis Summary</h3>

              <div className="grid grid-cols-1 gap-3">
                <div className="rounded-lg bg-gray-900/70 px-4 py-3">
                  <p className="text-sm text-gray-400">Frames processed</p>
                  <p className="text-2xl font-bold">{analysisResults.total_frames_processed}</p>
                </div>
                <div className="rounded-lg bg-gray-900/70 px-4 py-3">
                  <p className="text-sm text-gray-400">Detections</p>
                  <p className="text-2xl font-bold">{analysisResults.total_detections}</p>
                </div>
                <div className="rounded-lg bg-gray-900/70 px-4 py-3">
                  <p className="text-sm text-gray-400">Alerts</p>
                  <p className="text-2xl font-bold">{analysisResults.total_alerts}</p>
                </div>
              </div>

              {videoProperties && (
                <div className="rounded-lg bg-gray-900/70 px-4 py-3 text-sm text-gray-300 space-y-1">
                  <p>Resolution: {videoProperties.width} x {videoProperties.height}</p>
                  <p>FPS: {Number(videoProperties.fps || 0).toFixed(2)}</p>
                  <p>Duration: {Number(videoProperties.duration_seconds || 0).toFixed(2)} seconds</p>
                </div>
              )}
            </div>
          )}
        </div>
      </div>

      {analysisResults && (
        <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
          <div className="glass p-6 rounded-lg space-y-4">
            <h3 className="text-xl font-semibold">Detection Breakdown</h3>
            {detectionEntries.length === 0 ? (
              <p className="text-gray-400">No objects were detected in the processed frames.</p>
            ) : (
              <div className="space-y-3">
                {detectionEntries.map(([label, count]) => (
                  <div key={label} className="rounded-lg bg-gray-900/70 px-4 py-3 flex items-center justify-between">
                    <span className="capitalize text-gray-200">{label}</span>
                    <span className="font-semibold text-blue-300">{count}</span>
                  </div>
                ))}
              </div>
            )}
          </div>

          <div className="glass p-6 rounded-lg space-y-4">
            <h3 className="text-xl font-semibold">Alert Details</h3>
            {alerts.length === 0 ? (
              <p className="text-gray-400">No intrusion alerts were triggered during analysis.</p>
            ) : (
              <div className="space-y-3">
                {alerts.map((alert, index) => (
                  <div key={`${alert.timestamp}-${index}`} className="rounded-lg border border-red-700/40 bg-red-900/20 px-4 py-3">
                    <p className="font-semibold text-red-300 capitalize">{alert.type}</p>
                    <p className="text-sm text-gray-200 mt-1">{alert.message}</p>
                    <p className="text-xs text-gray-400 mt-2">
                      Frame {alert.frame_number} | {new Date(alert.timestamp).toLocaleString()}
                    </p>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}

      {sampleFrames.length > 0 && (
        <div className="glass p-6 rounded-lg space-y-4">
          <h3 className="text-xl font-semibold">Sample Frames</h3>
          <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-4">
            {sampleFrames.map((sample) => (
              <div key={sample.frame_number} className="rounded-lg overflow-hidden border border-gray-800 bg-gray-900/70">
                <img
                  src={`data:image/jpeg;base64,${sample.frame}`}
                  alt={`Sample frame ${sample.frame_number}`}
                  className="w-full h-56 object-cover"
                />
                <div className="p-4 space-y-1 text-sm text-gray-300">
                  <p className="font-semibold">Frame {sample.frame_number}</p>
                  <p>Detections: {sample.detections?.length || 0}</p>
                  <p>Motion detected: {sample.motion_data?.detected ? 'Yes' : 'No'}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default Settings
