import type { ReactNode } from 'react'

export function Badge({ tone = 'neutral', children }: { tone?: 'success' | 'warning' | 'neutral'; children: ReactNode }) {
  const tones = { success: 'bg-emerald-50 text-emerald-700', warning: 'bg-amber-50 text-amber-700', neutral: 'bg-slate-100 text-slate-600' }
  return <span className={`inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-xs font-semibold ${tones[tone]}`}>{children}</span>
}
