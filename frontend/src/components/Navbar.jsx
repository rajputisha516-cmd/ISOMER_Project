import React from 'react'
import { Menu, AlertCircle, Wifi, Power } from 'lucide-react'

function Navbar({ onMenuClick }) {
  const [isOnline, setIsOnline] = React.useState(true)

  return (
    <nav className="bg-gray-900 border-b border-gray-800 px-6 py-4 flex items-center justify-between">
      <div className="flex items-center gap-4">
        <button
          onClick={onMenuClick}
          className="p-2 hover:bg-gray-800 rounded-lg transition"
        >
          <Menu size={24} />
        </button>
        
        <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">
          Surveillance System
        </h1>
      </div>

      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2 px-4 py-2 bg-gray-800 rounded-lg">
          <Wifi size={18} className={isOnline ? 'text-green-400' : 'text-red-400'} />
          <span className="text-sm">{isOnline ? 'Online' : 'Offline'}</span>
        </div>

        <button className="p-2 hover:bg-gray-800 rounded-lg transition">
          <AlertCircle size={24} className="text-yellow-400" />
        </button>

        <button className="p-2 hover:bg-gray-800 rounded-lg transition">
          <Power size={24} className="text-red-400" />
        </button>
      </div>
    </nav>
  )
}

export default Navbar
