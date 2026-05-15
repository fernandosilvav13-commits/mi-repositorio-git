'use client'

import Link from 'next/link'

export default function GlobalNav() {
  return (
    <header className="sticky top-0 z-50 h-11 w-full bg-black text-white">
      <nav className="mx-auto flex h-full max-w-7xl items-center justify-between px-6 text-[12px] font-normal tracking-tight">
        <div className="flex items-center gap-8">
          <Link href="/" className="hover:opacity-80 transition-opacity">
            <span className="font-semibold">Proyecto Prueba</span>
          </Link>
          <div className="hidden md:flex gap-8">
            <Link href="/templates" className="hover:opacity-80 transition-opacity">Templates</Link>
            <Link href="/rules" className="hover:opacity-80 transition-opacity">Rules</Link>
            <Link href="/extraction" className="hover:opacity-80 transition-opacity">Extraction</Link>
            <Link href="/export" className="hover:opacity-80 transition-opacity">Export</Link>
          </div>
        </div>
        <div className="flex items-center gap-6">
          <Link href="/wizard" className="hover:opacity-80 transition-opacity">Wizard</Link>
        </div>
      </nav>
    </header>
  )
}
