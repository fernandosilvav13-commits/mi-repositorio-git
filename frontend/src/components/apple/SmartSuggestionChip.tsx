"use client";

import { Lightbulb, Check, X } from "lucide-react";

interface SmartSuggestionChipProps {
  extractionColumn: string;
  crossrefColumn: string;
  isMatch: boolean; // true if names matched directly
  onAccept: () => void;
  onDismiss?: () => void; // optional — hide suggestion
}

const SmartSuggestionChip = ({
  extractionColumn,
  crossrefColumn,
  isMatch,
  onAccept,
  onDismiss,
}: SmartSuggestionChipProps) => {
  return (
    <div className="flex items-center gap-3 px-4 py-2 rounded-lg bg-[#0066cc]/3 border border-[#0066cc]/10">
      <Lightbulb size={16} className="text-action-blue shrink-0" />
      <span className="text-[14px] text-ink flex-1">
        Sugerencia: {extractionColumn} ↔ {crossrefColumn}
      </span>
      <button
        onClick={onAccept}
        className="text-action-blue hover:bg-action-blue/10 rounded-full p-1 transition-colors"
        aria-label="Aceptar sugerencia"
      >
        <Check size={18} />
      </button>
      {onDismiss && (
        <button
          onClick={onDismiss}
          className="text-[#7a7a7a] hover:text-ink rounded-full p-1 transition-colors"
          aria-label="Descartar sugerencia"
        >
          <X size={18} />
        </button>
      )}
    </div>
  );
};

export default SmartSuggestionChip;
