import { Icon, type IconName } from '../components/ui/Icon'

const navigation: { label: string; icon: IconName; active?: boolean }[] = [
  { label: 'Overview', icon: 'dashboard', active: true }, { label: 'Flights', icon: 'flights' }, { label: 'Documents', icon: 'documents' }, { label: 'Simulations', icon: 'simulation' },
]

export function Sidebar({ open, onClose }: { open: boolean; onClose: () => void }) {
  return <aside className={`fixed inset-y-0 left-0 z-40 flex w-64 flex-col border-r border-slate-200 bg-white transition-transform duration-300 lg:translate-x-0 ${open ? 'translate-x-0' : '-translate-x-full'}`}>
    <div className="flex h-20 items-center gap-3 px-6">
      <div className="grid size-10 place-items-center rounded-xl bg-brand text-white shadow-lg shadow-blue-200"><Icon name="plane" className="size-5" /></div>
      <div><p className="text-lg font-bold tracking-tight">AeroTwin</p><p className="text-[10px] font-semibold uppercase tracking-[.18em] text-slate-400">Flight Intelligence</p></div>
    </div>
    <nav aria-label="Primary navigation" className="flex-1 px-3 py-5">
      <p className="mb-2 px-3 text-[11px] font-bold uppercase tracking-widest text-slate-400">Workspace</p>
      <ul className="space-y-1">{navigation.map(item => <li key={item.label}><a href="#" onClick={onClose} aria-current={item.active ? 'page' : undefined} className={`flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-semibold transition-colors ${item.active ? 'bg-blue-50 text-brand' : 'text-slate-500 hover:bg-slate-50 hover:text-slate-900'}`}><Icon name={item.icon} className="size-[18px]" />{item.label}{item.label === 'Documents' && <span className="ml-auto rounded-full bg-slate-100 px-2 py-0.5 text-[10px] text-slate-500">12</span>}</a></li>)}</ul>
      <p className="mb-2 mt-8 px-3 text-[11px] font-bold uppercase tracking-widest text-slate-400">Manage</p>
      <a href="#" className="flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-semibold text-slate-500 hover:bg-slate-50"><Icon name="settings" className="size-[18px]" />Settings</a>
    </nav>
    <div className="m-3 rounded-2xl bg-slate-950 p-4 text-white">
      <div className="mb-3 grid size-8 place-items-center rounded-lg bg-white/10"><Icon name="help" className="size-4" /></div><p className="text-sm font-semibold">Need a hand?</p><p className="mt-1 text-xs leading-5 text-slate-400">Explore the AeroTwin quick start guide.</p><button className="mt-3 text-xs font-semibold text-blue-300">View documentation →</button>
    </div>
  </aside>
}
