"use client";

import Link from "next/link";
import { useState, useRef, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
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
import { api } from "@/lib/api";

type Step = "upload" | "crossref" | "template" | "rules" | "extract" | "export" | "review";

const STEPS: { key: Step; label: string; icon: string }[] = [
  { key: "upload", label: "Subir Archivos", icon: "1" },
  { key: "crossref", label: "Cruzar Datos", icon: "2" },
  { key: "template", label: "Plantilla", icon: "3" },
  { key: "rules", label: "Reglas", icon: "4" },
  { key: "extract", label: "Extracción", icon: "5" },
  { key: "export", label: "Exportar", icon: "6" },
  { key: "review", label: "Revisión", icon: "7" },
];

interface ColumnMapping {
  match_column: string;
  crossref_match_column: string;
  output_columns: string[];
}

export default function WizardPage() {
  const [currentStep, setCurrentStep] = useState<Step>("upload");
  const [stepHistory, setStepHistory] = useState<Step[]>([]);

  // Step 1: Upload
  const [uploadFiles, setUploadFiles] = useState<File[]>([]);
  const [uploadedPaths, setUploadedPaths] = useState<string[]>([]);
  const [uploading, setUploading] = useState(false);
  const fileRef = useRef<HTMLInputElement>(null);

  // Step 2: Crossref
  const [enableCrossref, setEnableCrossref] = useState(false);
  const [crossrefFiles, setCrossrefFiles] = useState<any[]>([]);
  const [selectedCrossrefId, setSelectedCrossrefId] = useState("");
  const [crossrefData, setCrossrefData] = useState<any>(null);
  const [matchColumn, setMatchColumn] = useState("");
  const [crossrefMatchColumn, setCrossrefMatchColumn] = useState("");
  const [outputColumns, setOutputColumns] = useState<string[]>([]);
  const [crossrefUploadFile, setCrossrefUploadFile] = useState<File | null>(null);
  const [uploadingCrossref, setUploadingCrossref] = useState(false);
  const crossrefFileRef = useRef<HTMLInputElement>(null);

  // Step 3: Template
  const [templates, setTemplates] = useState<any[]>([]);
  const [selectedTemplateId, setSelectedTemplateId] = useState("");
  const [templateColumns, setTemplateColumns] = useState<string[]>([]);
  const [showCreateTemplate, setShowCreateTemplate] = useState(false);
  const [newTemplateName, setNewTemplateName] = useState("");
  const [newTemplateColumns, setNewTemplateColumns] = useState<any[]>([]);

  // Step 4: Rules
  const [rules, setRules] = useState<any[]>([]);
  const [selectedRuleIds, setSelectedRuleIds] = useState<Set<string>>(new Set());

  // Step 5: Extract
  const [extracting, setExtracting] = useState(false);
  const [extractionResults, setExtractionResults] = useState<any[]>([]);
  const [extractionDone, setExtractionDone] = useState(false);
  const [fuzzyThreshold, setFuzzyThreshold] = useState(70);

  // Step 6: Export
  const [exporting, setExporting] = useState(false);
  const [exported, setExported] = useState(false);

  // Step 7: Review
  const [conforme, setConforme] = useState<boolean | null>(null);
  const [feedbackText, setFeedbackText] = useState("");
  const [feedbackSent, setFeedbackSent] = useState(false);

  useEffect(() => {
    api.templates.list().then(setTemplates).catch(() => {});
    api.rules.list().then(setRules).catch(() => {});
    api.crossref.list().then(setCrossrefFiles).catch(() => {});
  }, []);

  const canGoNext = (): boolean => {
    switch (currentStep) {
      case "upload": return uploadedPaths.length > 0;
      case "crossref": return !enableCrossref || (!!selectedCrossrefId && !!matchColumn && !!crossrefMatchColumn && outputColumns.length > 0);
      case "template": return !!selectedTemplateId;
      case "rules": return true;
      case "extract": return extractionDone;
      case "export": return exported;
      case "review": return true;
    }
  };

  const goNext = () => {
    const idx = STEPS.findIndex((s) => s.key === currentStep);
    if (idx < STEPS.length - 1) {
      setStepHistory([...stepHistory, currentStep]);
      setCurrentStep(STEPS[idx + 1].key);
    }
  };

  const goBack = () => {
    if (stepHistory.length > 0) {
      const prev = stepHistory[stepHistory.length - 1];
      setStepHistory(stepHistory.slice(0, -1));
      setCurrentStep(prev);
    }
  };

  const goToStep = (step: Step) => {
    const currentIdx = STEPS.findIndex((s) => s.key === currentStep);
    const targetIdx = STEPS.findIndex((s) => s.key === step);
    if (targetIdx <= currentIdx) {
      setCurrentStep(step);
      setStepHistory(stepHistory.filter((_, i) => i < targetIdx));
    }
  };

  // --- Handlers ---

  const handleUploadFiles = async () => {
    if (uploadFiles.length === 0) return;
    setUploading(true);
    try {
      const result = await api.ingest.upload(uploadFiles);
      setUploadedPaths(result.files);
    } catch (e: any) {
      alert("Error al subir: " + e.message);
    } finally {
      setUploading(false);
    }
  };

  const handleUploadCrossref = async () => {
    if (!crossrefUploadFile) return;
    setUploadingCrossref(true);
    try {
      const result = await api.crossref.upload(crossrefUploadFile);
      setSelectedCrossrefId(result.id);
      setCrossrefData(result);
      setCrossrefMatchColumn(result.columns?.[0] || "");
      setOutputColumns(result.columns?.slice(1, 3) || []);
      await api.crossref.list().then(setCrossrefFiles);
      setCrossrefUploadFile(null);
    } catch (e: any) {
      alert("Error al subir: " + e.message);
    } finally {
      setUploadingCrossref(false);
    }
  };

  const handleSelectCrossref = async (id: string) => {
    setSelectedCrossrefId(id);
    if (!id) {
      setCrossrefData(null);
      return;
    }
    try {
      const data = await api.crossref.get(id);
      setCrossrefData(data);
      setCrossrefMatchColumn(data.columns?.[0] || "");
      setOutputColumns(data.columns?.slice(1, 3) || []);
    } catch {
      setCrossrefData(null);
    }
  };

  const handleCreateTemplate = async () => {
    if (!newTemplateName.trim() || newTemplateColumns.length === 0) return;
    try {
      const t = await api.templates.create({
        name: newTemplateName,
        columns: newTemplateColumns,
      });
      setSelectedTemplateId(t.id);
      setTemplateColumns(newTemplateColumns.map((c: any) => c.name));
      setShowCreateTemplate(false);
      setNewTemplateName("");
      setNewTemplateColumns([]);
      await api.templates.list().then(setTemplates);
    } catch (e: any) {
      alert("Error al crear plantilla: " + e.message);
    }
  };

  const handleSelectTemplate = async (id: string) => {
    setSelectedTemplateId(id);
    if (!id) return;
    try {
      const t = await api.templates.get(id);
      setTemplateColumns((t.columns || []).map((c: any) => c.name));
      if (enableCrossref && matchColumn && !t.columns?.some((c: any) => c.name === matchColumn)) {
        setMatchColumn("");
      }
    } catch {
      setTemplateColumns([]);
    }
  };

  const handleExtract = async () => {
    if (!selectedTemplateId || uploadedPaths.length === 0) return;
    setExtracting(true);
    setExtractionDone(false);
    try {
      const res = await api.extraction.extract({
        template_id: selectedTemplateId,
        file_paths: uploadedPaths,
        fuzzy_threshold: fuzzyThreshold,
      });
      setExtractionResults(res);
      setExtractionDone(true);
    } catch (e: any) {
      alert("Error en extracción: " + e.message);
    } finally {
      setExtracting(false);
    }
  };

  const handleExport = async () => {
    if (extractionResults.length === 0) return;
    setExporting(true);
    setExported(false);
    try {
      const payload: any = {
        template_id: selectedTemplateId,
        rows: extractionResults.map((r: any) => r.data),
      };
      if (enableCrossref && selectedCrossrefId && matchColumn) {
        const mapping: ColumnMapping = {
          match_column: matchColumn,
          crossref_match_column: crossrefMatchColumn,
          output_columns: outputColumns,
        };
        payload.crossref_file_id = selectedCrossrefId;
        payload.column_mapping = mapping;
      }
      await api.export.excel(payload);
      setExported(true);
    } catch (e: any) {
      alert("Error al exportar: " + e.message);
    } finally {
      setExporting(false);
    }
  };

  const handleFeedback = async () => {
    setFeedbackSent(true);
  };

  const toggleRule = (id: string) => {
    const next = new Set(selectedRuleIds);
    if (next.has(id)) next.delete(id);
    else next.add(id);
    setSelectedRuleIds(next);
  };

  const toggleOutputColumn = (col: string) => {
    setOutputColumns((prev) =>
      prev.includes(col) ? prev.filter((c) => c !== col) : [...prev, col]
    );
  };

  const stepIdx = STEPS.findIndex((s) => s.key === currentStep);

  return (
    <div className="min-h-screen flex flex-col">
      <header className="border-b">
        <div className="max-w-5xl mx-auto px-4 py-4 flex items-center justify-between">
          <h1 className="text-xl font-bold">Flujo de Trabajo</h1>
          <Link href="/" className="inline-flex items-center justify-center rounded-lg border border-border bg-background hover:bg-muted h-8 px-2.5 text-sm font-medium">← Salir</Link>
        </div>
      </header>

      {/* Step indicators */}
      <div className="border-b bg-muted/20">
        <div className="max-w-5xl mx-auto px-4 py-3 flex items-center gap-1 overflow-x-auto">
          {STEPS.map((s, i) => {
            const isActive = s.key === currentStep;
            const isDone = STEPS.indexOf(s) < stepIdx && s.key !== currentStep;
            return (
              <button
                key={s.key}
                onClick={() => goToStep(s.key)}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-medium whitespace-nowrap transition-colors ${
                  isActive
                    ? "bg-primary text-primary-foreground"
                    : isDone
                    ? "text-primary hover:bg-muted"
                    : "text-muted-foreground"
                }`}
              >
                <span className={`w-5 h-5 rounded-full flex items-center justify-center text-[10px] font-bold ${
                  isActive ? "bg-primary-foreground text-primary" : isDone ? "bg-primary text-primary-foreground" : "bg-muted-foreground/20"
                }`}>
                  {isDone ? "✓" : s.icon}
                </span>
                {s.label}
              </button>
            );
          })}
        </div>
      </div>

      <main className="flex-1 max-w-5xl mx-auto px-4 py-6 w-full">
        {/* Step: Upload */}
        {currentStep === "upload" && (
          <Card>
            <CardHeader>
              <CardTitle>Paso 1: Subir Archivos</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div
                onClick={() => fileRef.current?.click()}
                className="border-2 border-dashed rounded-lg p-10 text-center hover:border-primary cursor-pointer"
              >
                <input
                  ref={fileRef}
                  type="file"
                  multiple
                  accept=".pdf,.doc,.docx,.csv,.jpg,.jpeg,.png"
                  className="hidden"
                  onChange={(e) => setUploadFiles(Array.from(e.target.files || []))}
                />
                <p className="text-lg font-medium">Arrastra archivos aquí</p>
                <p className="text-sm text-muted-foreground mt-1">PDF, DOC, DOCX, CSV, JPG, PNG</p>
              </div>

              {uploadFiles.length > 0 && (
                <div className="space-y-2">
                  <p className="text-sm font-medium">{uploadFiles.length} archivo(s) seleccionados</p>
                  <div className="flex flex-wrap gap-2">
                    {uploadFiles.map((f, i) => (
                      <Badge key={i} variant="secondary">{f.name}</Badge>
                    ))}
                  </div>
                  <Button onClick={handleUploadFiles} disabled={uploading} size="sm">
                    {uploading ? "Subiendo..." : "Subir Archivos"}
                  </Button>
                </div>
              )}

              {uploadedPaths.length > 0 && (
                <div className="bg-emerald-50 border border-emerald-200 rounded-lg p-3 text-sm text-emerald-700">
                  ✓ {uploadedPaths.length} archivo(s) subidos exitosamente
                </div>
              )}
            </CardContent>
          </Card>
        )}

        {/* Step: Crossref */}
        {currentStep === "crossref" && (
          <Card>
            <CardHeader>
              <CardTitle>Paso 2: Cruce de Datos (Opcional)</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <label className="flex items-center gap-3 cursor-pointer">
                <input
                  type="checkbox"
                  checked={enableCrossref}
                  onChange={(e) => {
                    setEnableCrossref(e.target.checked);
                    if (!e.target.checked) setSelectedCrossrefId("");
                  }}
                  className="w-4 h-4 rounded"
                />
                <span className="text-sm font-medium">¿Deseas cruzar datos con un archivo externo?</span>
              </label>

              {enableCrossref && (
                <div className="border rounded-lg p-4 space-y-4 bg-muted/20">
                  <div
                    onClick={() => crossrefFileRef.current?.click()}
                    className="border-2 border-dashed rounded-lg p-6 text-center hover:border-primary cursor-pointer"
                  >
                    <input
                      ref={crossrefFileRef}
                      type="file"
                      accept=".pdf,.csv,.ppt,.pptx,.doc,.docx"
                      className="hidden"
                      onChange={(e) => setCrossrefUploadFile(e.target.files?.[0] || null)}
                    />
                    <p className="text-sm font-medium">Subir archivo de referencia</p>
                    <p className="text-xs text-muted-foreground mt-1">PDF, CSV, PPT, DOCX</p>
                  </div>

                  {crossrefUploadFile && (
                    <div className="flex items-center gap-3">
                      <Badge variant="secondary">{crossrefUploadFile.name}</Badge>
                      <Button onClick={handleUploadCrossref} disabled={uploadingCrossref} size="sm">
                        {uploadingCrossref ? "Subiendo..." : "Subir"}
                      </Button>
                    </div>
                  )}

                  {crossrefFiles.length > 0 && (
                    <div>
                      <Label className="text-xs">O selecciona un archivo ya subido</Label>
                      <Select value={selectedCrossrefId} onValueChange={handleSelectCrossref}>
                        <SelectTrigger>
                          <SelectValue placeholder="Seleccionar archivo..." />
                        </SelectTrigger>
                        <SelectContent>
                          {crossrefFiles.map((f: any) => (
                            <SelectItem key={f.id} value={f.id}>{f.name} ({f.row_count} filas)</SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>
                  )}

                  {crossrefData && templateColumns.length > 0 && (
                    <div className="space-y-3 border-t pt-3">
                      <p className="text-xs text-muted-foreground">Columnas del archivo: {crossrefData.columns?.join(", ")}</p>
                      <div className="grid grid-cols-2 gap-3">
                        <div>
                          <Label className="text-xs">Columna en resultados</Label>
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
                          <Label className="text-xs">Columna en referencia</Label>
                          <Select value={crossrefMatchColumn} onValueChange={setCrossrefMatchColumn}>
                            <SelectTrigger>
                              <SelectValue placeholder="Seleccionar..." />
                            </SelectTrigger>
                            <SelectContent>
                              {crossrefData.columns?.map((c: string) => (
                                <SelectItem key={c} value={c}>{c}</SelectItem>
                              ))}
                            </SelectContent>
                          </Select>
                        </div>
                      </div>
                      <div>
                        <Label className="text-xs">Columnas a agregar al Excel</Label>
                        <div className="flex flex-wrap gap-2 mt-1">
                          {crossrefData.columns
                            ?.filter((c: string) => c !== crossrefMatchColumn)
                            .map((c: string) => (
                              <label key={c} className="flex items-center gap-1.5 text-sm cursor-pointer">
                                <input type="checkbox" checked={outputColumns.includes(c)} onChange={() => toggleOutputColumn(c)} className="rounded" />
                                {c}
                              </label>
                            ))}
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              )}

              {templateColumns.length === 0 && enableCrossref && (
                <p className="text-xs text-amber-600">Define una plantilla primero para ver las columnas disponibles.</p>
              )}
            </CardContent>
          </Card>
        )}

        {/* Step: Template */}
        {currentStep === "template" && (
          <Card>
            <CardHeader>
              <CardTitle>Paso 3: Seleccionar Plantilla</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex gap-3 items-end">
                <div className="flex-1">
                  <Label>Plantilla existente</Label>
                  <Select value={selectedTemplateId} onValueChange={handleSelectTemplate}>
                    <SelectTrigger>
                      <SelectValue placeholder="Selecciona una plantilla" />
                    </SelectTrigger>
                    <SelectContent>
                      {templates.map((t: any) => (
                        <SelectItem key={t.id} value={t.id}>{t.name} ({t.columns?.length ?? 0} col.)</SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
                <Button variant="outline" size="sm" onClick={() => setShowCreateTemplate(!showCreateTemplate)}>
                  {showCreateTemplate ? "Cancelar" : "+ Nueva"}
                </Button>
              </div>

              {showCreateTemplate && (
                <div className="border rounded-lg p-4 space-y-3 bg-muted/20">
                  <Label>Nombre de la plantilla</Label>
                  <Input value={newTemplateName} onChange={(e) => setNewTemplateName(e.target.value)} placeholder="Ej: Datos Personales" />
                  <div className="space-y-2">
                    <div className="flex justify-between items-center">
                      <Label className="text-xs">Columnas</Label>
                      <Button variant="outline" size="sm" onClick={() => setNewTemplateColumns([...newTemplateColumns, { name: "", display_name: "", data_type: "string" }])}>
                        + Agregar
                      </Button>
                    </div>
                    {newTemplateColumns.map((col: any, i: number) => (
                      <div key={i} className="flex gap-2 items-center">
                        <Input
                          value={col.name}
                          onChange={(e) => {
                            const c = [...newTemplateColumns];
                            c[i] = { ...c[i], name: e.target.value, display_name: e.target.value };
                            setNewTemplateColumns(c);
                          }}
                          placeholder="nombre_campo"
                          className="flex-1"
                        />
                        <Button variant="destructive" size="sm" onClick={() => setNewTemplateColumns(newTemplateColumns.filter((_: any, j: number) => j !== i))}>
                          ×
                        </Button>
                      </div>
                    ))}
                  </div>
                  <Button onClick={handleCreateTemplate} disabled={!newTemplateName.trim() || newTemplateColumns.length === 0} className="w-full">
                    Crear Plantilla
                  </Button>
                </div>
              )}

              {templateColumns.length > 0 && (
                <div className="bg-emerald-50 border border-emerald-200 rounded-lg p-3 text-sm text-emerald-700">
                  ✓ Columnas: {templateColumns.join(", ")}
                </div>
              )}
            </CardContent>
          </Card>
        )}

        {/* Step: Rules */}
        {currentStep === "rules" && (
          <Card>
            <CardHeader>
              <CardTitle>Paso 4: Seleccionar Reglas</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {rules.length === 0 ? (
                <p className="text-sm text-muted-foreground">
                  No hay reglas creadas.{" "}
                  <Link href="/rules" className="underline">Crear reglas</Link>
                </p>
              ) : (
                <div className="space-y-2">
                  {rules.map((r: any) => (
                    <label key={r.id} className="flex items-center gap-3 p-3 border rounded-lg cursor-pointer hover:bg-muted/30 transition-colors">
                      <input
                        type="checkbox"
                        checked={selectedRuleIds.has(r.id)}
                        onChange={() => toggleRule(r.id)}
                        className="w-4 h-4 rounded"
                      />
                      <div>
                        <p className="text-sm font-medium">{r.name}</p>
                        <p className="text-xs text-muted-foreground">{r.description || r.conditions?.length + " condición(es)"}</p>
                      </div>
                    </label>
                  ))}
                </div>
              )}

              {selectedRuleIds.size > 0 && (
                <p className="text-xs text-emerald-600">{selectedRuleIds.size} regla(s) seleccionada(s)</p>
              )}
            </CardContent>
          </Card>
        )}

        {/* Step: Extract */}
        {currentStep === "extract" && (
          <Card>
            <CardHeader>
              <CardTitle>Paso 5: Extraer Datos</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="bg-muted/30 rounded-lg p-4 space-y-2 text-sm">
                <p><strong>Archivos:</strong> {uploadedPaths.length}</p>
                <p><strong>Plantilla:</strong> {templates.find((t) => t.id === selectedTemplateId)?.name || selectedTemplateId}</p>
                <p><strong>Reglas:</strong> {selectedRuleIds.size > 0 ? `${selectedRuleIds.size} seleccionada(s)` : "Ninguna"}</p>
                {enableCrossref && selectedCrossrefId && (
                  <p><strong>Cruce:</strong> {crossrefFiles.find((f) => f.id === selectedCrossrefId)?.name}</p>
                )}
              </div>

              <div>
                <Label className="text-sm font-medium">Umbral Fuzzy Matching: {fuzzyThreshold}%</Label>
                <input
                  type="range"
                  min="0" max="100"
                  value={fuzzyThreshold}
                  onChange={(e) => setFuzzyThreshold(Number(e.target.value))}
                  className="w-full"
                />
                <div className="flex justify-between text-xs text-muted-foreground">
                  <span>0% - Permisivo</span>
                  <span>100% - Exacto</span>
                </div>
              </div>

              <Button onClick={handleExtract} disabled={extracting || extractionResults.length > 0} className="w-full">
                {extracting ? "Extrayendo..." : extractionDone ? "✓ Extracción Completa" : "Ejecutar Extracción"}
              </Button>

              {extractionResults.length > 0 && (
                <div className="max-h-60 overflow-auto border rounded-lg">
                  <Table>
                    <TableHeader>
                      <TableRow>
                        <TableHead>Archivo</TableHead>
                        <TableHead>Estado</TableHead>
                        {templateColumns.slice(0, 3).map((c) => (
                          <TableHead key={c}>{c}</TableHead>
                        ))}
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {extractionResults.map((r: any, i: number) => (
                        <TableRow key={i}>
                          <TableCell className="text-xs">{r.filename}</TableCell>
                          <TableCell>
                            <Badge variant={r.status === "ok" ? "default" : "destructive"}>{r.status}</Badge>
                          </TableCell>
                          {templateColumns.slice(0, 3).map((c) => (
                            <TableCell key={c} className="text-xs max-w-[120px] truncate">
                              {r.data?.[c] === "NO ENCONTRADO" ? <span className="text-destructive">N/E</span> : r.data?.[c]}
                            </TableCell>
                          ))}
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </div>
              )}
            </CardContent>
          </Card>
        )}

        {/* Step: Export */}
        {currentStep === "export" && (
          <Card>
            <CardHeader>
              <CardTitle>Paso 6: Exportar a Excel</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="bg-muted/30 rounded-lg p-4 space-y-2 text-sm">
                <p><strong>Resultados:</strong> {extractionResults.length} filas</p>
                {enableCrossref && (
                  <p><strong>Cruce:</strong> {matchColumn} → {crossrefMatchColumn} (agregar: {outputColumns.join(", ") || "ninguna"})</p>
                )}
                <p><strong>Consolidación por RUT:</strong> Automática</p>
              </div>

              <Button onClick={handleExport} disabled={exporting || extractionResults.length === 0} className="w-full">
                {exporting ? "Generando Excel..." : exported ? "✓ Excel Descargado" : "Descargar Excel"}
              </Button>

              {exported && (
                <div className="bg-emerald-50 border border-emerald-200 rounded-lg p-4 text-center">
                  <p className="text-emerald-700 font-medium">✓ Excel descargado exitosamente</p>
                </div>
              )}
            </CardContent>
          </Card>
        )}

        {/* Step: Review */}
        {currentStep === "review" && (
          <Card>
            <CardHeader>
              <CardTitle>Paso 7: ¿Quedaste Conforme?</CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 text-center">
                <p className="text-blue-700 font-medium">El proceso de exportación ha finalizado</p>
                <p className="text-sm text-blue-600 mt-1">¿El resultado cumple con lo que esperabas?</p>
              </div>

              {conforme === null && !feedbackSent && (
                <div className="flex gap-4 justify-center">
                  <Button onClick={() => { setConforme(true); setFeedbackSent(true); }} className="bg-emerald-600 hover:bg-emerald-700 px-8">
                    Sí, estoy conforme ✓
                  </Button>
                  <Button onClick={() => setConforme(false)} variant="outline" className="px-8">
                    No, necesito cambios ✗
                  </Button>
                </div>
              )}

              {conforme === false && !feedbackSent && (
                <div className="space-y-4 border rounded-lg p-4">
                  <Label>Describe qué cambios necesitas</Label>
                  <Textarea
                    value={feedbackText}
                    onChange={(e) => setFeedbackText(e.target.value)}
                    placeholder="Ej: Agregar columna de correo electrónico, cambiar formato de RUT, ajustar reglas..."
                    rows={4}
                  />
                  <div className="flex gap-3">
                    <Button onClick={handleFeedback} disabled={!feedbackText.trim()}>Enviar Feedback</Button>
                    <Button variant="outline" onClick={() => setConforme(null)}>Cancelar</Button>
                  </div>
                  <div className="text-sm text-muted-foreground space-y-2">
                    <p className="font-medium">Según tu feedback, puedes volver a:</p>
                    <div className="flex flex-wrap gap-2">
                      <Button variant="outline" size="sm" onClick={() => goToStep("template")}>✏️ Ajustar plantilla</Button>
                      <Button variant="outline" size="sm" onClick={() => goToStep("rules")}>⚙️ Ajustar reglas</Button>
                      <Button variant="outline" size="sm" onClick={() => { setExtractionDone(false); setExtractionResults([]); goToStep("extract"); }}>
                        🔄 Re-extraer datos
                      </Button>
                      <Button variant="outline" size="sm" onClick={() => { setEnableCrossref(true); goToStep("crossref"); }}>
                        📊 Ajustar cruce de datos
                      </Button>
                    </div>
                  </div>
                </div>
              )}

              {feedbackSent && conforme === true && (
                <div className="text-center space-y-4">
                  <div className="text-4xl">🎉</div>
                  <p className="text-lg font-medium text-emerald-700">¡Proceso completado con éxito!</p>
                  <p className="text-sm text-muted-foreground">Puedes iniciar un nuevo flujo desde el inicio.</p>
                  <Button onClick={() => {
                    setCurrentStep("upload");
                    setStepHistory([]);
                    setUploadFiles([]);
                    setUploadedPaths([]);
                    setExtractionResults([]);
                    setExtractionDone(false);
                    setExported(false);
                    setConforme(null);
                    setFeedbackText("");
                    setFeedbackSent(false);
                    setSelectedTemplateId("");
                    setTemplateColumns([]);
                    setSelectedRuleIds(new Set());
                    setEnableCrossref(false);
                    setSelectedCrossrefId("");
                    setCrossrefData(null);
                  }}>
                    Nuevo Flujo
                  </Button>
                </div>
              )}

              {feedbackSent && conforme === false && (
                <div className="bg-amber-50 border border-amber-200 rounded-lg p-4 text-center">
                  <p className="text-amber-700 font-medium">✓ Feedback enviado</p>
                  <p className="text-sm text-amber-600 mt-1">Selecciona qué paso quieres ajustar usando los botones de arriba.</p>
                </div>
              )}
            </CardContent>
          </Card>
        )}

        {/* Navigation */}
        <div className="flex justify-between mt-6">
          <Button variant="outline" onClick={goBack} disabled={stepHistory.length === 0}>
            ← Atrás
          </Button>
          {currentStep !== "review" && (
            <Button onClick={goNext} disabled={!canGoNext()}>
              {currentStep === "export" ? "Finalizar →" : "Siguiente →"}
            </Button>
          )}
        </div>
      </main>
    </div>
  );
}
