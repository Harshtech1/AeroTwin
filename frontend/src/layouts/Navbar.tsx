import { Button } from '../components/ui/Button'
import { Icon } from '../components/ui/Icon'

export function Navbar({ onMenu }: { onMenu: () => void }) {
  return <header className="sticky top-0 z-20 flex h-20 items-center border-b border-slate-200/80 bg-white/90 px-4 backdrop-blur-xl sm:px-6 xl:px-10">
    <button onClick={onMenu} aria-label="Open navigation" className="mr-3 grid size-10 place-items-center rounded-xl text-slate-600 hover:bg-slate-100 lg:hidden"><Icon name="menu" className="size-5" /></button>
    <div className="hidden max-w-sm flex-1 items-center gap-2 rounded-xl bg-slate-100/80 px-3 text-slate-400 sm:flex"><Icon name="search" className="size-4" /><input aria-label="Search" placeholder="Search flights, documents..." className="h-10 min-w-0 flex-1 bg-transparent text-sm text-slate-700 outline-none placeholder:text-slate-400" /><kbd className="text-[10px] font-semibold">⌘ K</kbd></div>
    <div className="ml-auto flex items-center gap-2 sm:gap-4"><Button className="hidden sm:inline-flex"><Icon name="plus" className="size-4" />New flight</Button><button aria-label="Notifications" className="relative grid size-10 place-items-center rounded-xl border border-slate-200 text-slate-500 hover:bg-slate-50"><Icon name="bell" className="size-[18px]" /><span className="absolute right-2 top-2 size-2 rounded-full border-2 border-white bg-brand" /></button><div className="h-8 w-px bg-slate-200"/><button className="flex items-center gap-2 rounded-xl p-1.5 hover:bg-slate-50"><span className="grid size-9 place-items-center rounded-xl bg-gradient-to-br from-blue-500 to-indigo-600 text-xs font-bold text-white">AM</span><span className="hidden text-left md:block"><span className="block text-sm font-semibold">Alex Morgan</span><span className="block text-[11px] text-slate-400">Flight Analyst</span></span><Icon name="chevron" className="hidden size-3 rotate-90 text-slate-400 md:block" /></button></div>
  </header>
}
