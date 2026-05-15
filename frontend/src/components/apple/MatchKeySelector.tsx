"use client";

import { useState } from "react";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Button } from "@/components/ui/button";
import { Plus, X, Lightbulb } from "lucide-react";

interface MatchKeyPair {
  extraction: string;
  crossref: string;
}

interface MatchKeySelectorProps {
  columns: string[]; // crossref columns
  extractionColumns: string[]; // extraction template columns
  suggestedKeys: MatchKeyPair[]; // auto-suggested from column name overlap
  value: MatchKeyPair[];
  onChange: (keys: MatchKeyPair[]) => void;
}

const MatchKeySelector = ({
  columns,
  extractionColumns,
  suggestedKeys,
  value,
  onChange,
}: MatchKeySelectorProps) => {
  const [acceptedSuggestions, setAcceptedSuggestions] = useState<Set<number>>(new Set());

  const updateKey = (index: number, field: "extraction" | "crossref", newValue: string) => {
    const next = value.map((pair, i) =>
      i === index ? { ...pair, [field]: newValue } : pair
    );
    onChange(next);
  };

  const removeKey = (index: number) => {
    onChange(value.filter((_, i) => i !== index));
  };

  const addKey = () => {
    onChange([...value, { extraction: "", crossref: "" }]);
  };

  const acceptSuggestion = (idx: number, suggestion: MatchKeyPair) => {
    onChange([...value, suggestion]);
    setAcceptedSuggestions((prev) => new Set(prev).add(idx));
  };

  const hasUnusedExtractionColumns =
    extractionColumns.filter((c) => !value.find((v) => v.extraction === c)).length > 0;
  const hasUnusedCrossrefColumns =
    columns.filter((c) => !value.find((v) => v.crossref === c)).length > 0;
  const canAddMore = hasUnusedExtractionColumns && hasUnusedCrossrefColumns;

  const visibleSuggestions = suggestedKeys.filter((_, idx) => !acceptedSuggestions.has(idx));

  return (
    <div className="space-y-4">
      <div>
        <p className="text-[14px] font-semibold uppercase text-ink">
          Clave(s) de coincidencia
        </p>
        <p className="text-[14px] text-[#7a7a7a] mt-1">
          Seleccione las columnas que la IA usará para encontrar coincidencias
        </p>
      </div>

      {/* Auto-suggested Keys */}
      {visibleSuggestions.length > 0 && (
        <div className="space-y-2">
          {visibleSuggestions.map((suggestion, idx) => (
            <div
              key={`suggest-${idx}`}
              className="flex items-center gap-3 px-4 py-2 rounded-lg bg-[#0066cc]/3 border border-[#0066cc]/10"
            >
              <Lightbulb size={16} className="text-action-blue shrink-0" />
              <span className="text-[14px] text-ink flex-1">
                Sugerencia: {suggestion.extraction} ↔ {suggestion.crossref}
              </span>
              <button
                onClick={() => acceptSuggestion(idx, suggestion)}
                className="text-[14px] font-medium text-action-blue hover:underline shrink-0"
              >
                Usar sugerencia
              </button>
            </div>
          ))}
        </div>
      )}

      {/* Match Key Rows */}
      {value.length > 0 && (
        <div className="space-y-3">
          {value.map((pair, idx) => (
            <div
              key={idx}
              className="flex gap-4 items-center animate-in fade-in slide-in-from-left-2"
            >
              <div className="flex-1">
                <Select
                  value={pair.extraction}
                  onValueChange={(v) => v && updateKey(idx, "extraction", v)}
                >
                  <SelectTrigger className="w-full bg-parchment rounded-lg px-4 py-3 text-ink border border-[#e0e0e0]">
                    <SelectValue placeholder="Campo extraído" />
                  </SelectTrigger>
                  <SelectContent>
                    {extractionColumns.map((col) => (
                      <SelectItem key={col} value={col}>
                        {col}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              <div className="text-[#7a7a7a] text-center w-8 shrink-0">↔</div>
              <div className="flex-1">
                <Select
                  value={pair.crossref}
                  onValueChange={(v) => v && updateKey(idx, "crossref", v)}
                >
                  <SelectTrigger className="w-full bg-parchment rounded-lg px-4 py-3 text-ink border border-[#e0e0e0]">
                    <SelectValue placeholder="Campo referencia" />
                  </SelectTrigger>
                  <SelectContent>
                    {columns.map((col) => (
                      <SelectItem key={col} value={col}>
                        {col}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              <button
                onClick={() => removeKey(idx)}
                className="text-[#7a7a7a] hover:text-red-500 transition-colors shrink-0"
              >
                <X size={20} />
              </button>
            </div>
          ))}
        </div>
      )}

      {/* Add Another Key Button */}
      {canAddMore && (
        <button
          onClick={addKey}
          className="text-[14px] font-medium text-action-blue hover:underline flex items-center gap-1"
        >
          <Plus size={16} />
          Agregar otra clave
        </button>
      )}
    </div>
  );
};

export default MatchKeySelector;
