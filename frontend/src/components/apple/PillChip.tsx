import React from "react";
import { cn } from "@/lib/utils";

interface PillChipProps {
  selected?: boolean;
  onClick?: () => void;
  children: React.ReactNode;
  className?: string;
  variant?: "selectable" | "status";
  statusType?: "matched" | "unmatched" | "processing";
}

const PillChip = ({
  selected = false,
  onClick,
  children,
  className,
  variant = "selectable",
  statusType,
}: PillChipProps) => {
  if (variant === "status") {
    const statusColors: Record<string, string> = {
      matched:
        "bg-[#34c759]/10 text-[#34c759] border border-[#34c759]/20",
      unmatched:
        "bg-[#ff9500]/10 text-[#ff9500] border border-[#ff9500]/20",
      processing:
        "bg-[#007aff]/10 text-[#007aff] border border-[#007aff]/20",
    };

    return (
      <span
        aria-label={`Status: ${statusType}`}
        className={cn(
          "rounded-full px-3 py-1 text-[14px] font-medium",
          statusType ? statusColors[statusType] || statusColors.unmatched : statusColors.unmatched,
          className
        )}
      >
        {children}
      </span>
    );
  }

  return (
    <button
      onClick={onClick}
      className={cn(
        "rounded-full px-6 py-3 text-[14px] font-medium transition-all duration-300 active-scale",
        selected
          ? "border-2 border-action-blue text-action-blue bg-white"
          : "border border-[#e0e0e0] text-ink bg-white hover:border-[#7a7a7a]",
        className
      )}
    >
      {children}
    </button>
  );
};

export default PillChip;
