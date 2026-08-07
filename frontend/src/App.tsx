import { useState } from 'react'
import { AppShell } from './layouts/AppShell'
import { DashboardPage } from './pages/DashboardPage'

function App() {
  const [sidebarOpen, setSidebarOpen] = useState(false)

  return (
    <AppShell sidebarOpen={sidebarOpen} onSidebarOpenChange={setSidebarOpen}>
      <DashboardPage />
    </AppShell>
  )
}

export default App
