'use client'

import { usePathname } from 'next/navigation'

export default function SubNav() {
  const pathname = usePathname()
  
  // Map pathname to a friendly name for the tagline
  const getPageTitle = () => {
    if (pathname.includes('wizard')) return 'Wizard'
    if (pathname.includes('templates')) return 'Templates'
    if (pathname.includes('rules')) return 'Rules'
    if (pathname.includes('extraction')) return 'Extraction'
    if (pathname.includes('export')) return 'Export'
    if (pathname.includes('crossref')) return 'Cross-Reference'
    return 'Dashboard'
  }

  return (
    <nav className="sticky top-11 z-40 h-13 w-full border-b border-[#e0e0e0] bg-[#f5f5f7]/80 backdrop-blur-md">
      <div className="mx-auto flex h-full max-w-7xl items-center justify-between px-6">
        <div className="flex items-center">
          <span className="text-[21px] font-semibold tracking-[0.231px] text-[#1d1d1f]">
            {getPageTitle()}
          </span>
        </div>
        <div className="flex items-center gap-4">
          <button className="bg-action-blue text-white rounded-pill px-4 py-1.5 text-[14px] font-normal transition-transform active:scale-95">
            Primary Action
          </button>
        </div>
      </div>
    </nav>
  )
}
