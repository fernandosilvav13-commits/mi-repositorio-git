"use client";

import { useState } from "react";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Button } from "@/components/ui/button";
import { Plus, X } from "lucide-react";
import SmartSuggestionChip from "./SmartSuggestionChip";

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
  const addKeyRow = () => {
    onChange([...value, { extraction: "", crossref: "" }]);
  };

  const removeKeyRow = (index: number) => {
    const newValue = [...value];
    newValue.splice(index, 1);
    onChange(newValue);
  };

  const updateKeyRow = (index: number, field: keyof MatchKeyPair, val: string) => {
    const newValue = [...value];
    newValue[index] = { ...newValue[index], [field]: val };
    onChange(newValue);
  };

  const handleAcceptSuggestion = (suggestion: MatchKeyPair) => {
    // Check if it's already added to avoid duplicates
    if (!value.some(v => v.extraction === suggestion.extraction && v.crossref === suggestion.crossref)) {
      onChange([...value, suggestion]);
    }
  };

  return (
    <div className="space-y-4">
      <div>
        <h4 className="text-[14px] font-semibold uppercase tracking-wide text-ink">
          Clave(s) de coincidencia
        </h4>
        <p className="text-[14px] text-[#7a7a7a] mt-1">
          Seleccione las columnas que la IA usará para encontrar coincidencias
        </p>
      </div>

      {suggestedKeys.length > 0 && (
        <div className="flex flex-wrap gap-2 py-2">
          {suggestedKeys
            .filter(suggested => !value.some(v => v.extraction === suggested.extraction && v.crossref === suggested.crossref))
            .map((suggestion, idx) => (
              <SmartSuggestionChip
                key={`suggested-${idx}`}
                extractionColumn={suggestion.extraction}
                crossrefColumn={suggestion.crossref}
                onAccept={() => handleAcceptSuggestion(suggestion)}
              />
            ))}
        </div>
      )}

      <div className="space-y-3">
        {value.map((pair, index) => (
          <div key={index} className="flex gap-4 items-center animate-in fade-in slide-in-from-left-2">
            <div className="flex-1">
              <Select
                value={pair.extraction}
                onValueChange={(val) => updateKeyRow(index, "extraction", val)}
              >
                <SelectTrigger className="w-full rounded-full border-[#e0e0e0]">
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

            <div className="text-[#7a7a7a] text-center w-8 shrink-0">
              →
            </div>

            <div className="flex-1">
              <Select
                value={pair.crossref}
                onValueChange={(val) => updateKeyRow(index, "crossref", val)}
              >
                <SelectTrigger className="w-full rounded-full border-[#e0e0e0]">
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

            <Button
              variant="ghost"
              size="icon"
              className="text-[#7a7a7a] hover:text-red-500 rounded-full shrink-0"
              onClick={() => removeKeyRow(index)}
              title="Quitar clave"
            >
              <X size={18} />
            </Button>
          </div>
        ))}
      </div>

      <button
        onClick={addKeyRow}
        className="text-[14px] font-medium text-action-blue hover:underline flex items-center gap-1"
      >
        <Plus size={14} />
        Agregar otra clave
      </button>
    </div>
  );
};

export default MatchKeySelector;
