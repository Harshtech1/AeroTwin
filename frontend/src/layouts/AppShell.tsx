import type { ReactNode } from 'react'
import { Sidebar } from './Sidebar'
import { Navbar } from './Navbar'

export function AppShell({ children, sidebarOpen, onSidebarOpenChange }: { children: ReactNode; sidebarOpen: boolean; onSidebarOpenChange: (open: boolean) => void }) {
  return <div className="min-h-screen bg-canvas text-ink">
    <Sidebar open={sidebarOpen} onClose={() => onSidebarOpenChange(false)} />
    {sidebarOpen && <button aria-label="Close navigation" className="fixed inset-0 z-30 bg-slate-950/30 backdrop-blur-sm lg:hidden" onClick={() => onSidebarOpenChange(false)} />}
    <div className="lg:pl-64">
      <Navbar onMenu={() => onSidebarOpenChange(true)} />
      <main className="mx-auto max-w-[1500px] px-4 py-6 sm:px-6 sm:py-8 xl:px-10">{children}</main>
    </div>
  </div>
}
