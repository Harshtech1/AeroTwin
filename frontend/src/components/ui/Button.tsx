import type { ButtonHTMLAttributes, ReactNode } from 'react'

type Props = ButtonHTMLAttributes<HTMLButtonElement> & { variant?: 'primary' | 'secondary' | 'ghost'; children: ReactNode }

export function Button({ variant = 'primary', className = '', ...props }: Props) {
  const variants = { primary: 'bg-brand text-white shadow-sm hover:bg-brand-dark', secondary: 'border border-slate-200 bg-white text-slate-700 hover:bg-slate-50', ghost: 'text-slate-500 hover:bg-slate-100 hover:text-slate-900' }
  return <button className={`inline-flex h-10 items-center justify-center gap-2 rounded-xl px-4 text-sm font-semibold transition-colors disabled:pointer-events-none disabled:opacity-50 ${variants[variant]} ${className}`} {...props} />
}
