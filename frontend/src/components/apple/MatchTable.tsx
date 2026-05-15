"use client";

import React from "react";
import { cn } from "@/lib/utils";
import FrostedContainer from "@/components/apple/FrostedContainer";
import { 
  Table, 
  TableBody, 
  TableCell, 
  TableHead, 
  TableHeader, 
  TableRow 
} from "@/components/ui/table";

interface MatchTableProps {
  columns: string[]; // all columns (extraction + crossref)
  rows: Record<string, string>[];
  variant: "matched" | "unmatched";
  extractionColumnCount: number; // how many columns are extraction vs crossref
}

const MatchTable = ({
  columns,
  rows,
  variant,
  extractionColumnCount,
}: MatchTableProps) => {
  const isMatched = variant === "matched";
  const headerBg = isMatched ? "bg-[#34c759]/5" : "bg-[#ff9500]/5";
  
  const extractionCols = columns.slice(0, extractionColumnCount);
  const crossrefCols = columns.slice(extractionColumnCount);

  return (
    <div className="w-full overflow-x-auto">
      <FrostedContainer className="rounded-xl overflow-hidden border border-[#e0e0e0]">
        <Table>
          <TableHeader className={cn("border-b-0", headerBg)}>
            {/* Group Header Row */}
            <TableRow className="hover:bg-transparent border-b-0">
              {extractionCols.length > 0 && (
                <TableHead 
                  colSpan={extractionCols.length} 
                  className="text-center border-r border-[#e0e0e0]/50 h-8 text-[12px] font-bold uppercase tracking-wider text-[#7a7a7a]"
                >
                  Datos extraídos
                </TableHead>
              )}
              {crossrefCols.length > 0 && (
                <TableHead 
                  colSpan={crossrefCols.length} 
                  className="text-center h-8 text-[12px] font-bold uppercase tracking-wider text-[#7a7a7a]"
                >
                  Datos de referencia
                </TableHead>
              )}
            </TableRow>
            {/* Column Names Row */}
            <TableRow className="hover:bg-transparent">
              {columns.map((col, idx) => (
                <TableHead 
                  key={col} 
                  className={cn(
                    "text-[13px] font-semibold text-ink h-12",
                    idx === extractionColumnCount - 1 ? "border-r border-[#e0e0e0]/50" : ""
                  )}
                >
                  {col.replace(/^xref_/, "")}
                </TableHead>
              ))}
            </TableRow>
          </TableHeader>
          <TableBody>
            {rows.length === 0 ? (
              <TableRow>
                <TableCell colSpan={columns.length} className="text-center py-8 text-[#7a7a7a]">
                  No hay registros
                </TableCell>
              </TableRow>
            ) : (
              rows.map((row, rowIdx) => (
                <TableRow 
                  key={rowIdx}
                  className={cn(
                    "hover:bg-muted/30 transition-colors",
                    rowIdx % 2 === 0 ? "bg-white/50" : "bg-transparent"
                  )}
                >
                  {columns.map((col, colIdx) => {
                    const value = row[col];
                    const isNoData = value === "NO ENCONTRADO" || value === "" || value === undefined || value === null;
                    
                    return (
                      <TableCell 
                        key={colIdx} 
                        className={cn(
                          "text-[14px]",
                          colIdx === extractionColumnCount - 1 ? "border-r border-[#e0e0e0]/50" : ""
                        )}
                      >
                        <div className="max-w-[200px] truncate" title={String(value || "")}>
                          {isNoData ? (
                            <span className="text-[#7a7a7a]">—</span>
                          ) : (
                            String(value)
                          )}
                        </div>
                      </TableCell>
                    );
                  })}
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </FrostedContainer>
    </div>
  );
};

export default MatchTable;
