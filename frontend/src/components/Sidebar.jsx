import React from 'react'
import { Link, useLocation } from 'react-router-dom'
import { LayoutDashboard, BarChart3, History, Settings, ChevronRight, Camera } from 'lucide-react'

function Sidebar({ isOpen }) {
  const location = useLocation()

  const menuItems = [
    { path: '/', label: 'Dashboard', icon: LayoutDashboard },
    { path: '/analytics', label: 'Analytics', icon: BarChart3 },
    { path: '/history', label: 'Detection History', icon: History },
    { path: '/settings', label: 'Settings', icon: Settings }
  ]

  return (
    <aside className={`${
      isOpen ? 'w-64' : 'w-20'
    } bg-gray-900 border-r border-gray-800 transition-all duration-300 flex flex-col`}>
      <div className="p-6 flex items-center justify-center">
        <Camera className="text-blue-400" size={32} />
        {isOpen && <span className="ml-3 font-bold text-xl">Isomer</span>}
      </div>

      <nav className="flex-1 px-4 py-6 space-y-2">
        {menuItems.map((item) => (
          <Link
            key={item.path}
            to={item.path}
            className={`flex items-center gap-3 px-4 py-3 rounded-lg transition ${
              location.pathname === item.path
                ? 'bg-blue-600 text-white'
                : 'text-gray-400 hover:bg-gray-800'
            }`}
          >
            <item.icon size={20} />
            {isOpen && <span>{item.label}</span>}
            {isOpen && location.pathname === item.path && (
              <ChevronRight size={16} className="ml-auto" />
            )}
          </Link>
        ))}
      </nav>

      <div className="p-4 border-t border-gray-800">
        <div className={`text-xs text-gray-500 text-center ${isOpen ? 'block' : 'hidden'}`}>
          Copyright 2026 Isomer
        </div>
      </div>
    </aside>
  )
}

export default Sidebar
