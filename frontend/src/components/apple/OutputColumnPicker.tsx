"use client";

import { useEffect } from "react";
import { cn } from "@/lib/utils";

interface OutputColumnPickerProps {
  columns: string[];
  selected: string[];
  suggested: string[]; // columns suggested (those NOT in extraction template)
  onChange: (selected: string[]) => void;
}

const OutputColumnPicker = ({
  columns,
  selected,
  suggested,
  onChange,
}: OutputColumnPickerProps) => {
  // Auto-select suggested on mount if empty
  useEffect(() => {
    if (selected.length === 0 && suggested.length > 0) {
      onChange(suggested);
    }
  }, []);

  const toggleColumn = (column: string) => {
    if (selected.includes(column)) {
      onChange(selected.filter((c) => c !== column));
    } else {
      onChange([...selected, column]);
    }
  };

  if (columns.length === 0) {
    return (
      <div className="space-y-3">
        <h4 className="text-[14px] font-semibold uppercase tracking-wide text-ink">
          Columnas a incluir
        </h4>
        <p className="text-[14px] text-[#7a7a7a]">
          No hay columnas disponibles
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      <div>
        <h4 className="text-[14px] font-semibold uppercase tracking-wide text-ink">
          Columnas a incluir
        </h4>
        <p className="text-[14px] text-[#7a7a7a] mt-1">
          Seleccione los campos adicionales que desea incorporar desde la referencia
        </p>
      </div>

      <div className="flex flex-wrap gap-2">
        {columns.map((column) => {
          const isSelected = selected.includes(column);
          const isSuggested = suggested.includes(column);

          return (
            <button
              key={column}
              onClick={() => toggleColumn(column)}
              className={cn(
                "rounded-full px-4 py-2 text-[14px] font-medium transition-all duration-300 relative",
                isSelected
                  ? "bg-action-blue text-white shadow-sm"
                  : "border border-[#e0e0e0] text-ink bg-white hover:border-[#7a7a7a]"
              )}
            >
              {column}
              {isSuggested && !isSelected && (
                <span className="absolute -top-1 -right-1 flex h-2 w-2">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-action-blue opacity-75"></span>
                  <span className="relative inline-flex rounded-full h-2 w-2 bg-action-blue"></span>
                </span>
              )}
            </button>
          );
        })}
      </div>
    </div>
  );
};

export default OutputColumnPicker;
