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
  // Auto-select suggested columns on mount if nothing selected yet
  useEffect(() => {
    if (selected.length === 0 && suggested.length > 0) {
      onChange(suggested);
    }
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

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
        <p className="text-[14px] font-semibold uppercase tracking-wide text-ink">
          Columnas a incluir
        </p>
        <p className="text-[14px] text-[#7a7a7a]">No hay columnas disponibles</p>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      <div>
        <p className="text-[14px] font-semibold uppercase tracking-wide text-ink">
          Columnas a incluir
        </p>
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
                "rounded-full px-4 py-2 text-[14px] font-medium transition-all cursor-pointer",
                isSelected
                  ? "bg-action-blue text-white"
                  : "border border-[#e0e0e0] text-ink bg-white hover:border-[#7a7a7a]",
              )}
            >
              {column}
              {isSuggested && !isSelected && (
                <span className="ml-1.5 text-[11px] text-[#7a7a7a] font-normal">
                  Sugerido
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
