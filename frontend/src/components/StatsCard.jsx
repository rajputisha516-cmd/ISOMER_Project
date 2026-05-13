import React from 'react'

function StatsCard({ icon: Icon, label, value, trend, color = 'blue' }) {
  const colorClasses = {
    blue: 'border-blue-500/30 text-blue-400',
    red: 'border-red-500/30 text-red-400',
    yellow: 'border-yellow-500/30 text-yellow-400',
    green: 'border-green-500/30 text-green-400'
  }

  return (
    <div className={`glass p-6 rounded-lg border ${colorClasses[color]}`}>
      <div className="flex items-start justify-between">
        <div>
          <p className="text-gray-400 text-sm">{label}</p>
          <p className="text-3xl font-bold mt-2">{value}</p>
          <p className="text-xs text-gray-500 mt-2">{trend}</p>
        </div>
        <Icon size={32} className={`opacity-50 text-${color}-400`} />
      </div>
    </div>
  )
}

export default StatsCard
