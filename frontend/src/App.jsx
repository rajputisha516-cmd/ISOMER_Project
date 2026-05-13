import React, { useState } from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import Sidebar from './components/Sidebar'
import Dashboard from './pages/Dashboard'
import Analytics from './pages/Analytics'
import History from './pages/History'
import Settings from './pages/Settings'

function App() {
  const [sidebarOpen, setSidebarOpen] = useState(true)

  return (
    <Router>
      <div className="flex h-screen bg-gray-950">
        <Sidebar isOpen={sidebarOpen} />
        
        <div className="flex-1 flex flex-col overflow-hidden">
          <Navbar onMenuClick={() => setSidebarOpen(!sidebarOpen)} />
          
          <main className="flex-1 overflow-auto bg-gradient-to-br from-gray-950 to-gray-900">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/analytics" element={<Analytics />} />
              <Route path="/history" element={<History />} />
              <Route path="/settings" element={<Settings />} />
            </Routes>
          </main>
        </div>
      </div>
    </Router>
  )
}

export default App
