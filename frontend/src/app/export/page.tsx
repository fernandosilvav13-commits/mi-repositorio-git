"use client";

import Link from "next/link";
import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { api, API_BASE } from "@/lib/api";

export default function ExportPage() {
  const [templates, setTemplates] = useState<any[]>([]);
  const [selectedTemplate, setSelectedTemplate] = useState<string>("");
  const [results, setResults] = useState<any[]>([]);
  const [exporting, setExporting] = useState(false);
  const [exported, setExported] = useState(false);

  const [crossrefFiles, setCrossrefFiles] = useState<any[]>([]);
  const [selectedCrossref, setSelectedCrossref] = useState<string>("");
  const [selectedCrossrefData, setSelectedCrossrefData] = useState<any>(null);
  const [matchColumn, setMatchColumn] = useState<string>("");
  const [crossrefMatchColumn, setCrossrefMatchColumn] = useState<string>("");
  const [outputColumns, setOutputColumns] = useState<string[]>([]);

  useEffect(() => {
    api.templates.list().then(setTemplates).catch(() => {});
    api.crossref.list().then(setCrossrefFiles).catch(() => {});
  }, []);

  const loadResults = async (templateId: string) => {
    try {
      const res = await fetch(`${API_BASE}/api/extraction/results/${templateId}`);
      if (res.ok) setResults(await res.json());
      else setResults([]);
    } catch {
      setResults([]);
    }
  };

  const loadCrossrefFile = async (fileId: string) => {
    if (!fileId) {
      setSelectedCrossrefData(null);
      setMatchColumn("");
      setCrossrefMatchColumn("");
      setOutputColumns([]);
      return;
    }
    try {
      const data = await api.crossref.get(fileId);
      setSelectedCrossrefData(data);
      setCrossrefMatchColumn(data.columns?.[0] || "");
      setOutputColumns(data.columns?.slice(1, 3) || []);
    } catch {
      setSelectedCrossrefData(null);
    }
  };

  useEffect(() => {
    if (selectedTemplate) {
      loadResults(selectedTemplate);
      setExported(false);
    }
  }, [selectedTemplate, loadResults]);

  useEffect(() => {
    loadCrossrefFile(selectedCrossref);
    setExported(false);
  }, [selectedCrossref, loadCrossrefFile]);

  const templateColumns =
    results.length > 0 ? Object.keys(results[0].data) : [];

  const toggleOutputColumn = (col: string) => {
    setOutputColumns((prev) =>
      prev.includes(col) ? prev.filter((c) => c !== col) : [...prev, col]
    );
  };

  const handleExport = async () => {
    if (!selectedTemplate || results.length === 0) return;
    setExporting(true);
    setExported(false);
    try {
      const payload: any = {
        template_id: selectedTemplate,
        rows: results.map((r: any) => r.data),
      };

      if (selectedCrossref && selectedCrossrefData && matchColumn) {
        payload.crossref_file_id = selectedCrossref;
        payload.column_mapping = {
          match_column: matchColumn,
          crossref_match_column: crossrefMatchColumn,
          output_columns: outputColumns,
        };
      }

      await api.export.excel(payload);
      setExported(true);
    } catch (e: any) {
      alert("Error al exportar: " + e.message);
    } finally {
      setExporting(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col">
      <header className="border-b">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
          <h1 className="text-xl font-bold">Exportar Resultados</h1>
          <Link href="/" className="inline-flex items-center justify-center rounded-lg border border-border bg-background hover:bg-muted h-8 px-2.5 text-sm font-medium">← Volver</Link>
        </div>
      </header>
      <main className="flex-1 max-w-7xl mx-auto px-4 py-8 w-full space-y-6">
        <Card>
          <CardHeader>
            <CardTitle>Exportar a Excel</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <label className="text-sm font-medium">Plantilla</label>
              <Select value={selectedTemplate} onValueChange={setSelectedTemplate}>
                <SelectTrigger>
                  <SelectValue placeholder="Selecciona una plantilla" />
                </SelectTrigger>
                <SelectContent>
                  {templates.map((t: any) => (
                    <SelectItem key={t.id} value={t.id}>{t.name}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            {selectedTemplate && results.length > 0 && (
              <div className="max-h-60 overflow-auto border rounded-lg">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Archivo</TableHead>
                      <TableHead>Estado</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {results.map((r: any, i: number) => (
                      <TableRow key={i}>
                        <TableCell>{r.filename}</TableCell>
                        <TableCell>
                          <Badge variant={r.status === "ok" ? "default" : "destructive"}>
                            {r.status}
                          </Badge>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>
            )}

            {selectedTemplate && results.length === 0 && (
              <p className="text-sm text-muted-foreground">No hay resultados para esta plantilla.</p>
            )}

            {selectedTemplate && results.length > 0 && (
              <>
                <hr className="my-2" />
                <div className="space-y-4">
                  <h3 className="font-semibold text-sm">Cruzar con datos externos (opcional)</h3>

                  <div>
                    <label className="text-sm font-medium">Archivo de referencia</label>
                    <Select value={selectedCrossref} onValueChange={setSelectedCrossref}>
                      <SelectTrigger>
                        <SelectValue placeholder="Seleccionar archivo..." />
                      </SelectTrigger>
                      <SelectContent>
                        {crossrefFiles.map((f: any) => (
                          <SelectItem key={f.id} value={f.id}>
                            {f.name} ({f.row_count} filas)
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>

                  {selectedCrossrefData && (
                    <div className="border rounded-lg p-4 space-y-3 bg-muted/30">
                      <p className="text-xs text-muted-foreground">
                        Columnas del archivo: {selectedCrossrefData.columns?.join(", ")}
                      </p>

                      <div className="grid grid-cols-2 gap-3">
                        <div>
                          <label className="text-xs font-medium">Columna en resultados</label>
                          <Select value={matchColumn} onValueChange={setMatchColumn}>
                            <SelectTrigger>
                              <SelectValue placeholder="Seleccionar..." />
                            </SelectTrigger>
                            <SelectContent>
                              {templateColumns.map((c) => (
                                <SelectItem key={c} value={c}>{c}</SelectItem>
                              ))}
                            </SelectContent>
                          </Select>
                        </div>
                        <div>
                          <label className="text-xs font-medium">Columna en referencia</label>
                          <Select value={crossrefMatchColumn} onValueChange={setCrossrefMatchColumn}>
                            <SelectTrigger>
                              <SelectValue placeholder="Seleccionar..." />
                            </SelectTrigger>
                            <SelectContent>
                              {selectedCrossrefData.columns?.map((c: string) => (
                                <SelectItem key={c} value={c}>{c}</SelectItem>
                              ))}
                            </SelectContent>
                          </Select>
                        </div>
                      </div>

                      <div>
                        <label className="text-xs font-medium">Columnas a agregar al Excel</label>
                        <div className="flex flex-wrap gap-2 mt-1">
                          {selectedCrossrefData.columns
                            ?.filter((c: string) => c !== crossrefMatchColumn)
                            .map((c: string) => (
                              <label key={c} className="flex items-center gap-1.5 text-sm cursor-pointer">
                                <input
                                  type="checkbox"
                                  checked={outputColumns.includes(c)}
                                  onChange={() => toggleOutputColumn(c)}
                                  className="rounded"
                                />
                                {c}
                              </label>
                            ))}
                        </div>
                      </div>

                      {matchColumn && crossrefMatchColumn && outputColumns.length > 0 && (
                        <p className="text-xs text-emerald-600">
                          Se cruzará &ldquo;{matchColumn}&rdquo; → &ldquo;{crossrefMatchColumn}&rdquo; y se agregarán: {outputColumns.join(", ")}
                        </p>
                      )}
                    </div>
                  )}

                  {crossrefFiles.length === 0 && (
                    <p className="text-xs text-muted-foreground">
                      No hay archivos de referencia.{" "}
                      <Link href="/crossref" className="underline">Sube uno aquí</Link>.
                    </p>
                  )}
                </div>
              </>
            )}

            <Button
              onClick={handleExport}
              disabled={exporting || !selectedTemplate || results.length === 0}
              className="w-full"
            >
              {exporting ? "Generando Excel..." : "Exportar a Excel"}
            </Button>
            {exported && (
              <div className="text-center text-sm text-emerald-600 font-medium">
                ✓ Excel descargado
              </div>
            )}
          </CardContent>
        </Card>
      </main>
    </div>
  );
}
