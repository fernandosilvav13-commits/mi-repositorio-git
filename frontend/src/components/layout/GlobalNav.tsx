'use client'

import Link from 'next/link'
import { useAuth } from '@/lib/auth-context'

const AUTH_ENABLED = !!(process.env.NEXT_PUBLIC_SUPABASE_URL && process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY)

export default function GlobalNav() {
  const { user, loading, logout } = useAuth()

  return (
    <header className="sticky top-0 z-50 h-11 w-full bg-black text-white">
      <nav className="mx-auto flex h-full max-w-7xl items-center justify-between px-6 text-[12px] font-normal tracking-tight">
        <div className="flex items-center gap-8">
          <Link href="/" className="hover:opacity-80 transition-opacity">
            <span className="font-semibold">Proyecto Prueba</span>
          </Link>
        </div>
        <div className="flex items-center gap-6">
          <Link href="/wizard" className="hover:opacity-80 transition-opacity">Wizard</Link>
          {AUTH_ENABLED && !loading && user ? (
            <button onClick={logout} className="hover:opacity-80 transition-opacity cursor-pointer">
              Cerrar sesión
            </button>
          ) : AUTH_ENABLED ? (
            <Link href="/login" className="hover:opacity-80 transition-opacity">
              Iniciar sesión
            </Link>
          ) : null}
        </div>
      </nav>
    </header>
  )
}
