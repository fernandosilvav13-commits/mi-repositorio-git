"use client";

import { Button } from "@/components/ui/button";
import { Lightbulb, Check, X } from "lucide-react";

interface SmartSuggestionChipProps {
  extractionColumn: string;
  crossrefColumn: string;
  isMatch?: boolean; // true if names matched directly
  onAccept: () => void;
  onDismiss?: () => void; // optional — hide suggestion
}

const SmartSuggestionChip = ({
  extractionColumn,
  crossrefColumn,
  onAccept,
  onDismiss,
}: SmartSuggestionChipProps) => {
  return (
    <div className="flex items-center gap-3 px-4 py-2 rounded-lg bg-[#0066cc]/3 border border-[#0066cc]/10 animate-in fade-in slide-in-from-left-2">
      <Lightbulb size={16} className="text-action-blue" />
      <span className="text-[14px] text-ink">
        Sugerencia: <span className="font-medium">{extractionColumn}</span> ↔ <span className="font-medium">{crossrefColumn}</span>
      </span>
      <div className="flex items-center gap-1 ml-auto">
        <Button
          variant="ghost"
          size="icon"
          className="h-8 w-8 text-action-blue hover:bg-[#0066cc]/10 rounded-full"
          onClick={onAccept}
          title="Usar sugerencia"
        >
          <Check size={16} />
        </Button>
        {onDismiss && (
          <Button
            variant="ghost"
            size="icon"
            className="h-8 w-8 text-[#7a7a7a] hover:text-ink rounded-full"
            onClick={onDismiss}
            title="Descartar"
          >
            <X size={16} />
          </Button>
        )}
      </div>
    </div>
  );
};

export default SmartSuggestionChip;
