"use client";

import React from "react";
import { cn } from "@/lib/utils";
import { ChevronDown, ChevronUp } from "lucide-react";
import PillChip from "./PillChip";

interface MatchSummaryBarProps {
  matchedCount: number;
  unmatchedCount: number;
  expandedSection: "matched" | "unmatched" | null;
  onToggleMatch: () => void;
  onToggleUnmatched: () => void;
  loading?: boolean;
}

const MatchSummaryBar = ({
  matchedCount,
  unmatchedCount,
  expandedSection,
  onToggleMatch,
  onToggleUnmatched,
  loading = false,
}: MatchSummaryBarProps) => {
  if (loading) {
    return (
      <div className="flex items-center justify-center px-5 py-4 rounded-lg bg-white border border-[#e0e0e0] animate-pulse">
        <span className="text-[14px] text-[#7a7a7a] font-medium">
          Cargando vista previa...
        </span>
      </div>
    );
  }

  return (
    <div className="flex flex-col md:flex-row items-center justify-between px-5 py-3 rounded-lg bg-white border border-[#e0e0e0] gap-4">
      {/* Left side — Counts */}
      <div className="flex flex-wrap items-center gap-4">
        <PillChip variant="status" statusType="matched">
          {matchedCount} coinciden
        </PillChip>
        <PillChip variant="status" statusType="unmatched">
          {unmatchedCount} sin coincidencia
        </PillChip>
        <span className="hidden md:inline text-[14px] text-[#7a7a7a]">
          {matchedCount} registros coinciden • {unmatchedCount} registros sin coincidencia
        </span>
      </div>

      {/* Right side — Expand toggles */}
      <div className="flex items-center gap-6">
        <button
          onClick={onToggleMatch}
          className={cn(
            "text-[14px] font-medium flex items-center gap-1 cursor-pointer hover:opacity-70 transition-opacity",
            expandedSection === "matched" ? "text-[#34c759]" : "text-[#7a7a7a]"
          )}
        >
          <span>Concordancia</span>
          {expandedSection === "matched" ? (
            <ChevronUp className="w-4 h-4" />
          ) : (
            <ChevronDown className="w-4 h-4" />
          )}
        </button>

        <button
          onClick={onToggleUnmatched}
          className={cn(
            "text-[14px] font-medium flex items-center gap-1 cursor-pointer hover:opacity-70 transition-opacity",
            expandedSection === "unmatched" ? "text-[#ff9500]" : "text-[#7a7a7a]"
          )}
        >
          <span>Sin concordancia</span>
          {expandedSection === "unmatched" ? (
            <ChevronUp className="w-4 h-4" />
          ) : (
            <ChevronDown className="w-4 h-4" />
          )}
        </button>
      </div>
    </div>
  );
};

export default MatchSummaryBar;
