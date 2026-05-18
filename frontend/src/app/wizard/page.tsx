"use client";

import { useState, useRef, useEffect, useCallback } from "react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { api } from "@/lib/api";
import { LucideIcon, Upload, Database, Layout, ShieldCheck, Cpu, FileSpreadsheet, Star, ChevronRight, ChevronLeft, Plus, Check, X, AlertCircle, Loader2 } from "lucide-react";
import { toast } from "sonner";
import ConfiguratorCard from "@/components/apple/ConfiguratorCard";
import PillChip from "@/components/apple/PillChip";
import FrostedContainer from "@/components/apple/FrostedContainer";
import MatchKeySelector from "@/components/apple/MatchKeySelector";
import OutputColumnPicker from "@/components/apple/OutputColumnPicker";
import MatchSummaryBar from "@/components/apple/MatchSummaryBar";
import MatchTable from "@/components/apple/MatchTable";
import { cn } from "@/lib/utils";

type Step = "upload" | "crossref" | "template" | "rules" | "extract" | "export" | "review";

const STEPS: { key: Step; label: string; icon: any }[] = [
  { key: "upload", label: "Inicio", icon: Upload },
  { key: "template", label: "Estructura", icon: Layout },
  { key: "crossref", label: "Referencia", icon: Database },
  { key: "rules", label: "Inteligencia", icon: ShieldCheck },
  { key: "extract", label: "Procesamiento", icon: Cpu },
  { key: "export", label: "Entrega", icon: FileSpreadsheet },
  { key: "review", label: "Calidad", icon: Star },
];

export default function WizardPage() {
  const [currentStep, setCurrentStep] = useState<Step>("upload");
  const [subStep, setSubStep] = useState(0);
  const [stepHistory, setStepHistory] = useState<{ step: Step; subStep: number }[]>([]);

  // State Management
  const [uploadFiles, setUploadFiles] = useState<{ file: File; folder: string }[]>([]);
  const [uploadedPaths, setUploadedPaths] = useState<string[]>([]);
  const [uploading, setUploading] = useState(false);
  const fileRef = useRef<HTMLInputElement>(null);
  const folderRef = useRef<HTMLInputElement>(null);
  const crossrefFileRef = useRef<HTMLInputElement>(null);

  const [enableCrossref, setEnableCrossref] = useState<boolean | null>(null);
  const [crossrefFiles, setCrossrefFiles] = useState<any[]>([]);
  const [uploadingCrossref, setUploadingCrossref] = useState(false);
  const [selectedCrossrefId, setSelectedCrossrefId] = useState("");
  const [crossrefData, setCrossrefData] = useState<any>(null);
  const [matchKeys, setMatchKeys] = useState<{ extraction: string; crossref: string }[]>([]);
  const [suggestedMatchKeys, setSuggestedMatchKeys] = useState<{ extraction: string; crossref: string }[]>([]);
  const [outputColumns, setOutputColumns] = useState<string[]>([]);
  const [crossrefStatus, setCrossrefStatus] = useState<"idle" | "loading" | "ready" | "mapped">("idle");
  const [crossrefError, setCrossrefError] = useState<string | null>(null);
  const [crossrefStepError, setCrossrefStepError] = useState<string | null>(null);
  
  const [templates, setTemplates] = useState<any[]>([]);
  const [selectedTemplateId, setSelectedTemplateId] = useState("");
  const [templateColumns, setTemplateColumns] = useState<string[]>([]);
  const [newTemplateName, setNewTemplateName] = useState("");
  const [newTemplateColumns, setNewTemplateColumns] = useState<any[]>([]);
  const [editingTemplateId, setEditingTemplateId] = useState<string | null>(null);
  const [editTemplateName, setEditTemplateName] = useState("");
  const [editTemplateColumns, setEditTemplateColumns] = useState<any[]>([]);

  const [rules, setRules] = useState<any[]>([]);
  const [selectedRuleIds, setSelectedRuleIds] = useState<Set<string>>(new Set());
  const [newRule, setNewRule] = useState({
    name: "",
    description: "",
    field: "",
    operator: "==",
    value: "",
    action_type: "fill_row",
    action_color: "GREEN",
  });

  const [extracting, setExtracting] = useState(false);
  const [extractionResults, setExtractionResults] = useState<any[]>([]);
  const [extractionDone, setExtractionDone] = useState(false);

  const [exporting, setExporting] = useState(false);
  const [exported, setExported] = useState(false);

  const [conforme, setConforme] = useState<boolean | null>(null);
  const [feedbackSent, setFeedbackSent] = useState(false);

  // Match Preview State
  const [matchPreview, setMatchPreview] = useState<{
    matched: Record<string, string>[];
    unmatched: Record<string, string>[];
    matchedCount: number;
    unmatchedCount: number;
  } | null>(null);
  const [matchPreviewLoading, setMatchPreviewLoading] = useState(false);
  const [previewExpanded, setPreviewExpanded] = useState<"matched" | "unmatched" | null>(null);
  const [previewError, setPreviewError] = useState<string | null>(null);
  const [mappingVersion, setMappingVersion] = useState(0);

  useEffect(() => {
    api.templates.list().then(setTemplates).catch(() => {});
    api.rules.list().then(setRules).catch(() => {});
    api.crossref.list().then(setCrossrefFiles).catch(() => {});
  }, []);

  const goNext = () => {
    setStepHistory([...stepHistory, { step: currentStep, subStep }]);
    
    // Logic for complex steps
    if (currentStep === "crossref") {
      if (enableCrossref === false) {
        setCurrentStep("rules");
        setSubStep(0);
        return;
      }
      if (subStep < 2) {
        setSubStep(subStep + 1);
        return;
      }
    }

    if (currentStep === "template") {
        if (subStep === 0 && selectedTemplateId) {
            setCurrentStep("crossref");
            setSubStep(0);
            return;
        }
        if (subStep === 1) {
            setSubStep(0);
            return;
        }
        if (subStep === 2) {
            setSubStep(0);
            return;
        }
        if (subStep < 1) {
            setSubStep(subStep + 1);
            return;
        }
    }

    if (currentStep === "rules") {
      // Avanza directamente al siguiente paso, sin obligar a crear reglas
    }

    const idx = STEPS.findIndex((s) => s.key === currentStep);
    if (idx < STEPS.length - 1) {
      setCurrentStep(STEPS[idx + 1].key);
      setSubStep(0);
    }
  };

  const goBack = () => {
    if (stepHistory.length > 0) {
      const last = stepHistory[stepHistory.length - 1];
      setStepHistory(stepHistory.slice(0, -1));
      setCurrentStep(last.step);
      setSubStep(last.subStep);
    }
  };

  // Handlers
  const handleUpload = async () => {
    setUploading(true);
    try {
      const result = await api.ingest.upload(uploadFiles);
      setUploadedPaths(result.files);
      goNext();
    } catch (e) {
      toast.error("Error al procesar archivos");
    } finally {
      setUploading(false);
    }
  };

  const computeSuggestedMatchKeys = (crossrefColumns: string[], extractionCols: string[]) => {
    const suggestions: { extraction: string; crossref: string }[] = [];
    for (const extCol of extractionCols) {
      const match = crossrefColumns.find(
        (c: string) => c.trim().toLowerCase() === extCol.trim().toLowerCase()
      );
      if (match) {
        suggestions.push({ extraction: extCol, crossref: match });
      }
    }
    return suggestions;
  };

  const computeSuggestedOutputColumns = (crossrefColumns: string[], extractionCols: string[]) => {
    const templateColLower = extractionCols.map((c: string) => c.trim().toLowerCase());
    return crossrefColumns.filter(
      (c: string) => !templateColLower.includes(c.trim().toLowerCase())
    );
  };

  const handleUploadCrossref = async (files: FileList | null) => {
    if (!files || files.length === 0) return;
    setUploadingCrossref(true);
    setCrossrefStepError(null);
    setCrossrefStatus("loading");
    try {
      const result = await api.crossref.upload(files[0]);
      const updated = await api.crossref.list();
      setCrossrefFiles(updated);
      setSelectedCrossrefId(result.id);
      setCrossrefData(result);

      // Compute auto-suggestions
      const columns = result.columns || [];
      const suggestions = computeSuggestedMatchKeys(columns, templateColumns);
      setSuggestedMatchKeys(suggestions);
      if (matchKeys.length === 0) {
        setMatchKeys(suggestions.length > 0 ? suggestions : []);
      }
      setOutputColumns(computeSuggestedOutputColumns(columns, templateColumns));

      setCrossrefStatus("ready");
      setSubStep(2);
    } catch (e: unknown) {
      console.error("CrossRef upload error:", e);
      setCrossrefStepError("Error al subir archivo. Verifique el formato e intente nuevamente");
      setCrossrefStatus("idle");
    } finally {
      setUploadingCrossref(false);
    }
  };

  const handleSelectCrossref = async (id: string) => {
    setSelectedCrossrefId(id);
    setCrossrefStatus("loading");
    setCrossrefStepError(null);
    try {
      const data = await api.crossref.get(id);
      setCrossrefData(data);

      // Compute auto-suggestions
      const columns = data.columns || [];
      const suggestions = computeSuggestedMatchKeys(columns, templateColumns);
      setSuggestedMatchKeys(suggestions);
      setMatchKeys(suggestions.length > 0 ? suggestions : []);
      setOutputColumns(computeSuggestedOutputColumns(columns, templateColumns));

      setCrossrefStatus("ready");
      setSubStep(2);
    } catch (e: unknown) {
      console.error("CrossRef column load error:", e);
      setCrossrefStepError("Error al cargar columnas del archivo. Intente nuevamente o seleccione otro archivo.");
      setCrossrefStatus("idle");
    }
  };

  const handleCreateTemplate = async () => {
    try {
      const t = await api.templates.create({ name: newTemplateName, columns: newTemplateColumns });
      setSelectedTemplateId(t.id);
      setTemplateColumns(newTemplateColumns.map((c: any) => c.name));
      setCurrentStep("crossref");
      setSubStep(0);
    } catch {
      alert("Error al crear plantilla");
    }
  };

  const handleExtract = async () => {
    setExtracting(true);
    try {
      const res = await api.extraction.extract({
        template_id: selectedTemplateId,
        file_paths: uploadedPaths,
      });
      setExtractionResults(res);
      setExtractionDone(true);
      goNext();
    } catch (e) {
      toast.error("Error en la extracción");
    } finally {
      setExtracting(false);
    }
  };

  const handleExport = async () => {
    setExporting(true);
    try {
      const payload: any = {
        template_id: selectedTemplateId,
        rows: extractionResults.map((r: any) => r.data),
      };
      if (enableCrossref && selectedCrossrefId) {
        payload.crossref_file_id = selectedCrossrefId;
        payload.column_mapping = {
          match_column: matchKeys[0]?.extraction || "",
          crossref_match_column: matchKeys[0]?.crossref || "",
          output_columns: outputColumns,
        };
      }
      await api.export.excel(payload);
      setExported(true);
      goNext();
    } catch (e) {
      toast.error("Error al exportar");
    } finally {
      setExporting(false);
    }
  };

  const handleUpdateTemplate = async () => {
    if (!editingTemplateId) return;
    try {
      await api.templates.update(editingTemplateId, {
        name: editTemplateName,
        columns: editTemplateColumns,
      });
      toast.success("Plantilla actualizada");
      const updated = await api.templates.list();
      setTemplates(updated);
      setEditingTemplateId(null);
      setSubStep(0);
    } catch (e: unknown) {
      const msg = e instanceof Error ? e.message : "Error al actualizar plantilla";
      toast.error(msg);
    }
  };

  const handleCreateRule = async () => {
    try {
      const payload = {
        name: newRule.name,
        description: newRule.description,
        conditions: [{ field: newRule.field, operator: newRule.operator, value: newRule.value }],
        action: { type: newRule.action_type, params: { color: newRule.action_color } },
        enabled: true,
      };
      const res = await api.rules.create(payload);
      toast.success("Regla creada");
      const updated = await api.rules.list();
      setRules(updated);
      setSelectedRuleIds(new Set([...selectedRuleIds, res.id]));
      setSubStep(0);
      setNewRule({ name: "", description: "", field: "", operator: "==", value: "", action_type: "fill_row", action_color: "GREEN" });
    } catch (e) {
      toast.error("Error al crear regla");
    }
  };

  const fetchMatchPreview = useCallback(async () => {
    if (!enableCrossref || !selectedCrossrefId || !crossrefData || matchKeys.length === 0 || extractionResults.length === 0) return;
    
    setMatchPreviewLoading(true);
    setPreviewError(null);
    try {
      // Fetch full crossref data
      const fullData = await api.crossref.get(selectedCrossrefId);
      
      const extractionRows = extractionResults.map(r => r.data);
      const crossrefRows = fullData.data || [];
      
      const primaryKey = matchKeys[0];
      if (primaryKey) {
        const extKey = primaryKey.extraction;
        const crefKey = primaryKey.crossref;
        
        // Build lookup from crossref data
        const lookup = new Map<string, Record<string, string>>();
        for (const row of crossrefRows) {
          const val = String(row[crefKey] || "").trim().toLowerCase();
          if (val) lookup.set(val, row);
        }
        
        const matched: Record<string, string>[] = [];
        const unmatched: Record<string, string>[] = [];
        
        for (const row of extractionRows) {
          const matchVal = String(row[extKey] || "").trim().toLowerCase();
          const matchedRow = lookup.get(matchVal);
          
          if (matchedRow) {
            // Merge extraction + crossref data
            const merged = { ...row };
            for (const col of outputColumns) {
              merged[`xref_${col}`] = matchedRow[col] || "";
            }
            matched.push(merged);
          } else {
            // Show extraction data with blank crossref columns
            const unmerged = { ...row };
            for (const col of outputColumns) {
              unmerged[`xref_${col}`] = "NO ENCONTRADO";
            }
            unmatched.push(unmerged);
          }
        }
        
        setMatchPreview({
          matched,
          unmatched,
          matchedCount: matched.length,
          unmatchedCount: unmatched.length,
        });
      }
    } catch (e) {
      console.error("Fetch match preview error:", e);
      setPreviewError("Error al generar vista previa de validación. Revise la configuración de cruce e intente nuevamente.");
    } finally {
      setMatchPreviewLoading(false);
    }
  }, [enableCrossref, selectedCrossrefId, crossrefData, matchKeys, outputColumns, extractionResults]);

  // Re-fetch match preview when user enters review step or mapping changes
  useEffect(() => {
    if (currentStep === "review" && enableCrossref && selectedCrossrefId) {
      fetchMatchPreview();
    }
  }, [currentStep, mappingVersion, enableCrossref, selectedCrossrefId, fetchMatchPreview]);

  // Track mapping changes
  useEffect(() => {
    setMappingVersion(v => v + 1);
  }, [matchKeys, outputColumns]);

  return (
    <div className="min-h-screen bg-parchment flex flex-col items-center pt-[104px] pb-24 overflow-x-hidden">
      {/* Global Nav Placeholder */}
      <div className="fixed top-0 left-0 w-full h-[44px] bg-black z-[100] flex items-center justify-center">
        <span className="text-white text-[12px] font-medium tracking-tight">CicloAI</span>
      </div>

      {/* SubNav (frosted) */}
      <FrostedContainer 
        variant="parchment" 
        className="fixed top-[44px] left-0 w-full h-[52px] z-[90] border-b border-[#e0e0e0] px-6 flex items-center justify-between"
      >
        <div className="flex items-center gap-2">
            <span className="text-[21px] font-semibold tracking-tight text-ink">Configurador</span>
        </div>
        <div className="flex items-center gap-4">
            {stepHistory.length > 0 && (
                <button onClick={goBack} className="text-action-blue text-[14px] font-medium hover:underline flex items-center gap-1 active-scale">
                   <ChevronLeft size={16} /> Atrás
                </button>
            )}
            <button 
                onClick={goNext}
                className="bg-action-blue text-white rounded-full px-4 py-1 text-[14px] font-medium active-scale"
            >
                {currentStep === "review" ? "Terminar" : "Siguiente"}
            </button>
        </div>
      </FrostedContainer>

      <main className="w-full max-w-4xl flex flex-col items-center px-6">
        {/* Header */}
        <div className="text-center mb-12 flex flex-col items-center">
            <span className="text-[14px] font-semibold text-[#7a7a7a] uppercase tracking-wide mb-2">
                {STEPS.find(s => s.key === currentStep)?.label}
            </span>
            <h1 className="text-[34px] font-semibold tracking-apple-tight text-ink leading-tight max-w-xl">
                {currentStep === "upload" && "Comencemos seleccionando los documentos que desea procesar."}
                {currentStep === "crossref" && "¿Desea validar o completar los datos con una base de referencia?"}
                {currentStep === "template" && "¿Qué información específica desea extraer de los documentos?"}
                {currentStep === "rules" && "Aplique reglas de negocio automáticas a la extracción."}
                {currentStep === "extract" && "La IA está lista para analizar sus documentos."}
                {currentStep === "export" && "Sus resultados han sido consolidados con éxito."}
                {currentStep === "review" && "¿Está satisfecho con la precisión de los resultados?"}
            </h1>
        </div>

        {/* Content Area */}
        <div className="w-full flex flex-col gap-6">
          {currentStep === "upload" && (
            <ConfiguratorCard>
              <div 
                className="w-full aspect-[2/1] rounded-lg border-2 border-dashed border-[#e0e0e0] flex flex-col items-center justify-center gap-4 cursor-pointer hover:border-action-blue group transition-colors bg-white/50"
              >
                <input ref={fileRef} type="file" multiple className="hidden" onChange={(e) => {
                  const files = Array.from(e.target.files || []);
                  setUploadFiles((prev) => [...prev, ...files.map(f => ({ file: f, folder: "Raíz" }))]);
                }} />
                <div className="w-16 h-16 rounded-full bg-parchment flex items-center justify-center group-hover:bg-action-blue group-hover:text-white transition-all">
                    <Upload size={28} />
                </div>
                <p className="text-[17px] font-semibold text-ink">Seleccionar archivos</p>
                <Button
                  variant="outline"
                  onClick={(e) => { e.stopPropagation(); folderRef.current?.click(); }}
                  className="rounded-full border border-[#e0e0e0] bg-white text-[#333] hover:bg-[#f5f5f5] h-11 px-5 text-[14px] gap-2"
                >
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/></svg>
                  Subir Carpeta
                </Button>
                <input
                  ref={folderRef}
                  type="file"
                  {...({webkitdirectory: ""} as any)}
                  className="hidden"
                  onChange={(e) => {
                    const files = Array.from(e.target.files || []);
                    const newFiles = files.map(f => {
                      const parts = f.webkitRelativePath.split("/");
                      const folder = parts.length > 1 ? parts[0] : "Raíz";
                      return { file: f, folder };
                    });
                    setUploadFiles((prev) => [...prev, ...newFiles]);
                  }}
                />
                <div className="flex flex-wrap justify-center gap-2 max-w-md px-6">
                    {uploadFiles.slice(0, 5).map((f, i) => (
                        <Badge key={i} variant="secondary" className="bg-parchment text-ink rounded-full px-3 py-1 border-none font-normal text-[12px]">
                            {f.file.name}
                        </Badge>
                    ))}
                    {uploadFiles.length > 5 && <span className="text-[12px] text-[#7a7a7a]">+{uploadFiles.length - 5} archivos más</span>}
                </div>
              </div>
              
              {uploadFiles.length > 0 && (
                <div className="mt-8 flex justify-center">
                    <button 
                        onClick={handleUpload} 
                        disabled={uploading} 
                        className="bg-action-blue text-white rounded-full px-8 py-3 text-[17px] font-medium active-scale w-full sm:w-auto"
                    >
                        {uploading ? "Procesando..." : "Subir y continuar"}
                    </button>
                </div>
              )}
            </ConfiguratorCard>
          )}

          {currentStep === "crossref" && subStep === 0 && (
            <div className="flex flex-col gap-4">
              <ConfiguratorCard 
                title="Sí, cruzar datos" 
                subtitle="Vincular con bases de datos externas para validación de RUT, títulos o experiencia."
              >
                <div className="flex justify-end">
                    <PillChip selected={enableCrossref === true} onClick={() => { setEnableCrossref(true); setCrossrefStepError(null); setSubStep(1); }}>
                        Seleccionar
                    </PillChip>
                </div>
              </ConfiguratorCard>
              <ConfiguratorCard 
                title="No, omitir" 
                subtitle="Continuar solo con los datos extraídos de los currículums seleccionados."
              >
                <div className="flex justify-end">
                            <PillChip selected={enableCrossref === false} onClick={() => {
                                        setEnableCrossref(false);
                                        setStepHistory((prev) => [...prev, { step: currentStep, subStep }]);
                                        setCurrentStep("rules");
                                        setSubStep(0);
                                    }}>
                        Continuar
                    </PillChip>
                </div>
              </ConfiguratorCard>
            </div>
          )}

          {currentStep === "crossref" && subStep === 1 && (
            <div className="flex flex-col gap-4">
              {/* Error banner */}
              {crossrefStepError && (
                <ConfiguratorCard className="!border-red-400/50 !bg-red-50/50">
                  <div className="flex items-start gap-3">
                    <AlertCircle size={20} className="text-red-500 mt-0.5 shrink-0" />
                    <div className="flex-1">
                      <p className="text-[15px] font-medium text-red-800">{crossrefStepError}</p>
                    </div>
                    <button
                      onClick={() => setCrossrefStepError(null)}
                      className="text-red-400 hover:text-red-600 transition-colors"
                    >
                      <X size={18} />
                    </button>
                  </div>
                </ConfiguratorCard>
              )}

              {/* Upload Section */}
              <ConfiguratorCard title="Subir archivo de referencia" subtitle="CSV, PDF, DOCX o PPT con datos maestros para validación.">
                <div className="flex flex-col items-center py-4 gap-4">
                  <input
                    ref={crossrefFileRef}
                    type="file"
                    accept=".csv,.pdf,.docx,.ppt,.pptx"
                    className="hidden"
                    onChange={(e) => handleUploadCrossref(e.target.files)}
                  />
                  <div
                    onClick={() => !uploadingCrossref && crossrefFileRef.current?.click()}
                    className="w-full aspect-[3/1] rounded-lg border-2 border-dashed border-[#e0e0e0] flex flex-col items-center justify-center gap-2 cursor-pointer hover:border-action-blue transition-colors bg-white/50"
                  >
                    {uploadingCrossref ? (
                      <>
                        <Loader2 size={24} className="text-action-blue animate-spin" />
                        <p className="text-[14px] font-medium text-action-blue">Subiendo...</p>
                      </>
                    ) : (
                      <>
                        <Upload size={24} className="text-[#7a7a7a]" />
                        <p className="text-[14px] font-medium text-[#7a7a7a]">Haga clic para seleccionar archivo</p>
                      </>
                    )}
                  </div>
                </div>
              </ConfiguratorCard>

              {/* Available Files Section */}
              {crossrefFiles.length > 0 && (
                <>
                  <p className="text-[14px] font-semibold text-[#7a7a7a] uppercase tracking-wide px-1">
                    Archivos disponibles
                  </p>
                  {crossrefFiles.map((f: any) => (
                    <ConfiguratorCard key={f.id}>
                      <div className="flex items-center justify-between">
                        <div>
                          <p className="text-[17px] font-semibold text-ink">{f.name}</p>
                          <p className="text-[14px] text-[#7a7a7a]">{f.row_count} registros</p>
                        </div>
                        <PillChip selected={selectedCrossrefId === f.id} onClick={() => handleSelectCrossref(f.id)}>
                          {selectedCrossrefId === f.id ? "Seleccionado" : "Usar este"}
                        </PillChip>
                      </div>
                    </ConfiguratorCard>
                  ))}
                </>
              )}

              {/* Empty State */}
              {crossrefFiles.length === 0 && !uploadingCrossref && (
                <ConfiguratorCard>
                  <div className="flex flex-col items-center py-8 gap-3">
                    <Database size={32} className="text-[#7a7a7a] opacity-40" />
                    <p className="text-[17px] font-medium text-ink">Suba un archivo de referencia para comenzar</p>
                    <p className="text-[14px] text-[#7a7a7a]">Los formatos compatibles son CSV, PDF, DOCX y PPT</p>
                  </div>
                </ConfiguratorCard>
              )}
            </div>
          )}

          {currentStep === "crossref" && subStep === 2 && (
            <ConfiguratorCard title="Columnas de cruce" subtitle="Configure cómo se relacionan los datos extraídos con los de referencia.">
              {!crossrefData ? (
                <div className="flex items-center justify-center py-8">
                  <p className="text-[14px] text-[#7a7a7a]">Cargando columnas...</p>
                </div>
              ) : (
                <div className="space-y-6">
                  {/* Match Key Selector */}
                  <MatchKeySelector
                    columns={crossrefData?.columns || []}
                    extractionColumns={templateColumns}
                    suggestedKeys={suggestedMatchKeys}
                    value={matchKeys}
                    onChange={setMatchKeys}
                  />

                  {/* Divider */}
                  <hr className="my-6 border-[#e0e0e0]" />

                  {/* Output Column Picker */}
                  <OutputColumnPicker
                    columns={crossrefData?.columns || []}
                    selected={outputColumns}
                    suggested={computeSuggestedOutputColumns(crossrefData?.columns || [], templateColumns)}
                    onChange={setOutputColumns}
                  />

                  {/* Confirm Button */}
                  <button
                    onClick={() => {
                      if (matchKeys.length === 0 || !matchKeys[0]?.extraction || !matchKeys[0]?.crossref) {
                        return;
                      }
                      setCrossrefStatus("mapped");
                      goNext();
                    }}
                    className="w-full bg-action-blue text-white rounded-full py-3 text-[17px] font-medium active-scale"
                  >
                    Confirmar correspondencia
                  </button>
                  {matchKeys.length === 0 && (
                    <p className="text-[12px] text-red-500 text-center">
                      Seleccione al menos una clave de coincidencia
                    </p>
                  )}
                </div>
              )}
            </ConfiguratorCard>
          )}

          {currentStep === "template" && subStep === 0 && (
            <div className="flex flex-col gap-4">
              {templates.map((t: any) => (
                  <ConfiguratorCard key={t.id}>
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-[17px] font-semibold text-ink">{t.name}</p>
                            <p className="text-[14px] text-[#7a7a7a]">{t.columns?.length} campos configurados</p>
                        </div>
                        <div className="flex gap-2">
                            <PillChip selected={selectedTemplateId === t.id} onClick={() => {
                                const newCols = t.columns.map((c:any) => c.name);
                                if (selectedTemplateId === t.id) {
                                    setTemplateColumns(newCols);
                                    setStepHistory((prev) => [...prev, { step: currentStep, subStep }]);
                                    setCurrentStep("crossref");
                                    setSubStep(0);
                                    return;
                                }
                                if (matchKeys.length > 0) {
                                    const confirmed = window.confirm("Cambiar la plantilla eliminará la configuración actual de cruce de datos. ¿Desea continuar?");
                                    if (!confirmed) return;
                                    setMatchKeys([]);
                                    setOutputColumns([]);
                                }
                                setSelectedTemplateId(t.id);
                                setTemplateColumns(newCols);
                                setStepHistory((prev) => [...prev, { step: currentStep, subStep }]);
                                setCurrentStep("crossref");
                                setSubStep(0);
                            }}>
                                Seleccionar
                            </PillChip>
                            <button
                                onClick={() => {
                                    setEditingTemplateId(t.id);
                                    setEditTemplateName(t.name);
                                    setEditTemplateColumns(t.columns?.map((c:any) => ({...c})) || []);
                                    setSubStep(2);
                                }}
                                className="text-[14px] font-medium text-action-blue hover:underline ml-2"
                            >
                                Editar
                            </button>
                        </div>
                    </div>
                  </ConfiguratorCard>
                ))}
                <button 
                    onClick={() => setSubStep(1)} 
                    className="w-full py-6 border-2 border-dashed border-[#e0e0e0] rounded-lg text-[#7a7a7a] hover:border-action-blue hover:text-action-blue transition-all flex items-center justify-center gap-2 font-medium"
                >
                    <Plus size={20} /> Crear nueva plantilla
                </button>
            </div>
          )}

          {currentStep === "template" && subStep === 1 && (
            <ConfiguratorCard title="Nueva Estructura" subtitle="Defina los campos que la IA debe identificar en cada documento.">
                <div className="space-y-8">
                    <div className="space-y-2">
                        <label className="text-[14px] font-semibold text-[#7a7a7a] uppercase tracking-wide">Nombre de Plantilla</label>
                        <input 
                            value={newTemplateName} 
                            onChange={(e) => setNewTemplateName(e.target.value)} 
                            placeholder="Ej: Reclutamiento IT 2024" 
                            className="w-full border-b border-[#e0e0e0] py-2 text-[21px] font-semibold focus:outline-none focus:border-action-blue transition-colors" 
                        />
                    </div>
                    <div className="space-y-4">
                        <div className="flex justify-between items-center">
                            <label className="text-[14px] font-semibold text-[#7a7a7a] uppercase tracking-wide">Columnas de salida</label>
                            <button onClick={() => setNewTemplateColumns([...newTemplateColumns, {name: "", data_type: "string"}])} className="text-action-blue hover:underline text-[14px] font-medium">
                                + Agregar
                            </button>
                        </div>
                        <div className="space-y-3">
                            {newTemplateColumns.map((col, i) => (
                                <div key={i} className="flex gap-4 items-center animate-in fade-in slide-in-from-left-2">
                                    <input 
                                        value={col.name} 
                                        onChange={(e) => {
                                            const c = [...newTemplateColumns];
                                            c[i].name = e.target.value;
                                            setNewTemplateColumns(c);
                                        }} 
                                        placeholder="Nombre del campo" 
                                        className="flex-1 bg-parchment rounded-md px-4 py-2 text-ink focus:outline-none border border-[#e0e0e0]" 
                                    />
                                    <button 
                                        onClick={() => setNewTemplateColumns(newTemplateColumns.filter((_, idx) => idx !== i))}
                                        className="text-[#7a7a7a] hover:text-red-500"
                                    >
                                        <X size={20} />
                                    </button>
                                </div>
                            ))}
                        </div>
                    </div>
                    <button onClick={handleCreateTemplate} className="w-full bg-action-blue text-white rounded-full py-3 text-[17px] font-medium active-scale">
                        Guardar Plantilla
                    </button>
                </div>
            </ConfiguratorCard>
          )}

          {currentStep === "template" && subStep === 2 && editingTemplateId && (
            <ConfiguratorCard title="Editar Plantilla" subtitle="Modifique los campos de la plantilla existente.">
                <div className="space-y-8">
                    <div className="space-y-2">
                        <label className="text-[14px] font-semibold text-[#7a7a7a] uppercase tracking-wide">Nombre de Plantilla</label>
                        <input 
                            value={editTemplateName} 
                            onChange={(e) => setEditTemplateName(e.target.value)} 
                            placeholder="Ej: Reclutamiento IT 2024" 
                            className="w-full border-b border-[#e0e0e0] py-2 text-[21px] font-semibold focus:outline-none focus:border-action-blue transition-colors" 
                        />
                    </div>
                    <div className="space-y-4">
                        <div className="flex justify-between items-center">
                            <label className="text-[14px] font-semibold text-[#7a7a7a] uppercase tracking-wide">Columnas de salida</label>
                            <button onClick={() => setEditTemplateColumns([...editTemplateColumns, {name: "", data_type: "string"}])} className="text-action-blue hover:underline text-[14px] font-medium">
                                + Agregar
                            </button>
                        </div>
                        <div className="space-y-3">
                            {editTemplateColumns.map((col, i) => (
                                <div key={i} className="flex gap-4 items-center animate-in fade-in slide-in-from-left-2">
                                    <input 
                                        value={col.name} 
                                        onChange={(e) => {
                                            const c = [...editTemplateColumns];
                                            c[i].name = e.target.value;
                                            setEditTemplateColumns(c);
                                        }} 
                                        placeholder="Nombre del campo" 
                                        className="flex-1 bg-parchment rounded-md px-4 py-2 text-ink focus:outline-none border border-[#e0e0e0]" 
                                    />
                                    <button 
                                        onClick={() => setEditTemplateColumns(editTemplateColumns.filter((_, idx) => idx !== i))}
                                        className="text-[#7a7a7a] hover:text-red-500"
                                    >
                                        <X size={20} />
                                    </button>
                                </div>
                            ))}
                        </div>
                    </div>
                    <div className="flex gap-3">
                        <button onClick={handleUpdateTemplate} className="flex-1 bg-action-blue text-white rounded-full py-3 text-[17px] font-medium active-scale">
                            Guardar Cambios
                        </button>
                        <button onClick={() => { setEditingTemplateId(null); setSubStep(0); }} className="flex-1 border border-[#e0e0e0] text-[#7a7a7a] rounded-full py-3 text-[17px] font-medium active-scale">
                            Cancelar
                        </button>
                    </div>
                </div>
            </ConfiguratorCard>
          )}

          {currentStep === "rules" && subStep === 0 && (
            <div className="flex flex-col gap-4">
                {rules.map((r: any) => (
                  <ConfiguratorCard key={r.id}>
                    <div className="flex items-center justify-between">
                        <div className="flex items-center gap-4">
                            <div className={cn("w-10 h-10 rounded-full flex items-center justify-center transition-colors", selectedRuleIds.has(r.id) ? "bg-action-blue text-white" : "bg-parchment text-[#7a7a7a]")}>
                                <ShieldCheck size={20} />
                            </div>
                            <div>
                                <p className="text-[17px] font-semibold text-ink">{r.name}</p>
                                <p className="text-[14px] text-[#7a7a7a]">{r.description || "Regla de validación automática"}</p>
                            </div>
                        </div>
                        <PillChip 
                            selected={selectedRuleIds.has(r.id)} 
                            onClick={() => {
                                const next = new Set(selectedRuleIds);
                                if (next.has(r.id)) next.delete(r.id);
                                else next.add(r.id);
                                setSelectedRuleIds(next);
                            }}
                        >
                            {selectedRuleIds.has(r.id) ? "Activada" : "Activar"}
                        </PillChip>
                    </div>
                  </ConfiguratorCard>
                ))}
                <button 
                    onClick={() => setSubStep(1)} 
                    className="w-full py-6 border-2 border-dashed border-[#e0e0e0] rounded-lg text-[#7a7a7a] hover:border-action-blue hover:text-action-blue transition-all flex items-center justify-center gap-2 font-medium"
                >
                    <Plus size={20} /> Crear nueva regla
                </button>
                <button
                    onClick={goNext}
                    className="w-full py-3 text-[#7a7a7a] hover:text-action-blue transition-all text-[15px] font-medium text-center"
                >
                    No necesito crear reglas, continuar de todas formas →
                </button>
                <div className="flex justify-center">
                    <button onClick={goNext} className="bg-action-blue text-white rounded-full px-12 py-3 text-[17px] font-medium active-scale">
                        Continuar
                    </button>
                </div>
            </div>
          )}

          {currentStep === "rules" && subStep === 1 && (
            <ConfiguratorCard title="Nueva Regla" subtitle="Defina una condición y acción para la regla de negocio.">
                <div className="space-y-6">
                    <div className="space-y-2">
                        <label className="text-[14px] font-semibold text-[#7a7a7a] uppercase tracking-wide">Nombre</label>
                        <input 
                            value={newRule.name} 
                            onChange={(e) => setNewRule({...newRule, name: e.target.value})} 
                            placeholder="Ej: Más de 4 títulos" 
                            className="w-full border-b border-[#e0e0e0] py-2 text-[17px] focus:outline-none focus:border-action-blue transition-colors" 
                        />
                    </div>
                    <div className="space-y-2">
                        <label className="text-[14px] font-semibold text-[#7a7a7a] uppercase tracking-wide">Descripción</label>
                        <input 
                            value={newRule.description} 
                            onChange={(e) => setNewRule({...newRule, description: e.target.value})} 
                            placeholder="Describa el propósito de la regla" 
                            className="w-full border-b border-[#e0e0e0] py-2 text-[17px] focus:outline-none focus:border-action-blue transition-colors" 
                        />
                    </div>
                    <div className="grid grid-cols-3 gap-4">
                        <div className="space-y-2">
                            <label className="text-[14px] font-semibold text-[#7a7a7a] uppercase tracking-wide">Campo</label>
                            <input 
                                value={newRule.field} 
                                onChange={(e) => setNewRule({...newRule, field: e.target.value})} 
                                placeholder="ej: titulos" 
                                className="w-full bg-parchment rounded-md px-4 py-2 text-ink focus:outline-none border border-[#e0e0e0]" 
                            />
                        </div>
                        <div className="space-y-2">
                            <label className="text-[14px] font-semibold text-[#7a7a7a] uppercase tracking-wide">Operador</label>
                            <select 
                                value={newRule.operator} 
                                onChange={(e) => setNewRule({...newRule, operator: e.target.value})}
                                className="w-full bg-parchment rounded-md px-4 py-2 text-ink focus:outline-none border border-[#e0e0e0]"
                            >
                                <option value="==">Igual a</option>
                                <option value="!=">Distinto de</option>
                                <option value=">">Mayor que</option>
                                <option value="<">Menor que</option>
                                <option value="contains">Contiene</option>
                                <option value="not_contains">No contiene</option>
                                <option value="is_empty">Está vacío</option>
                                <option value="is_not_empty">No está vacío</option>
                                <option value="count>">Conteo mayor a</option>
                                <option value="count<">Conteo menor a</option>
                            </select>
                        </div>
                        <div className="space-y-2">
                            <label className="text-[14px] font-semibold text-[#7a7a7a] uppercase tracking-wide">Valor</label>
                            <input 
                                value={newRule.value} 
                                onChange={(e) => setNewRule({...newRule, value: e.target.value})} 
                                placeholder="valor" 
                                className="w-full bg-parchment rounded-md px-4 py-2 text-ink focus:outline-none border border-[#e0e0e0]" 
                            />
                        </div>
                    </div>
                    <div className="grid grid-cols-2 gap-4">
                        <div className="space-y-2">
                            <label className="text-[14px] font-semibold text-[#7a7a7a] uppercase tracking-wide">Acción</label>
                            <select 
                                value={newRule.action_type} 
                                onChange={(e) => setNewRule({...newRule, action_type: e.target.value})}
                                className="w-full bg-parchment rounded-md px-4 py-2 text-ink focus:outline-none border border-[#e0e0e0]"
                            >
                                <option value="fill_row">Pintar fila</option>
                            </select>
                        </div>
                        <div className="space-y-2">
                            <label className="text-[14px] font-semibold text-[#7a7a7a] uppercase tracking-wide">Color</label>
                            <div className="flex gap-2">
                                {["GREEN", "YELLOW", "RED"].map((c) => (
                                    <button
                                        key={c}
                                        onClick={() => setNewRule({...newRule, action_color: c})}
                                        className={cn(
                                            "w-10 h-10 rounded-full border-2 transition-all",
                                            newRule.action_color === c ? "border-ink scale-110" : "border-transparent"
                                        )}
                                        style={{ backgroundColor: c === "GREEN" ? "#44FF44" : c === "YELLOW" ? "#FFFF44" : "#FF4444" }}
                                    />
                                ))}
                            </div>
                        </div>
                    </div>
                    <button onClick={handleCreateRule} className="w-full bg-action-blue text-white rounded-full py-3 text-[17px] font-medium active-scale">
                        Guardar Regla
                    </button>
                </div>
            </ConfiguratorCard>
          )}

          {currentStep === "extract" && (
            <ConfiguratorCard>
                <div className="flex flex-col items-center py-8 gap-8">
                  <div className={cn("w-24 h-24 rounded-full bg-parchment flex items-center justify-center text-action-blue", extracting ? "animate-pulse" : "")}>
                    <Cpu size={48} />
                  </div>
                  <div className="text-center space-y-2">
                    <p className="text-[24px] font-semibold text-ink">{uploadedPaths.length} Documentos listos</p>
                    <p className="text-[17px] text-[#7a7a7a]">Plantilla: {templates.find(t => t.id === selectedTemplateId)?.name}</p>
                  </div>
                  <button onClick={handleExtract} disabled={extracting} className="bg-action-blue text-white rounded-full px-12 py-3 text-[17px] font-medium active-scale w-full max-w-xs">
                    {extracting ? "Analizando..." : "Iniciar Extracción"}
                  </button>
                </div>
            </ConfiguratorCard>
          )}

          {currentStep === "export" && (
            <ConfiguratorCard>
                <div className="flex flex-col items-center py-8 gap-8">
                  <div className="w-24 h-24 rounded-full bg-[#f2f2f7] flex items-center justify-center text-action-blue">
                    <FileSpreadsheet size={48} />
                  </div>
                  <div className="text-center space-y-2">
                    <p className="text-[24px] font-semibold text-ink">{extractionResults.length} Registros procesados</p>
                    <p className="text-[17px] text-[#7a7a7a]">El archivo Excel ha sido generado con éxito.</p>
                  </div>
                  <button onClick={handleExport} disabled={exporting} className="bg-action-blue text-white rounded-full px-12 py-3 text-[17px] font-medium active-scale w-full max-w-xs">
                    {exporting ? "Generando..." : "Descargar Excel"}
                  </button>
                </div>
            </ConfiguratorCard>
          )}

          {currentStep === "review" && (
            <div className="flex flex-col gap-6">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <ConfiguratorCard className="flex flex-col items-center text-center py-10 hover:border-emerald-500/30 transition-all cursor-pointer group">
                    <div className="w-16 h-16 rounded-full bg-emerald-50 text-emerald-600 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform"><Check size={32} /></div>
                    <p className="text-[21px] font-semibold text-ink">Excelente</p>
                    <button onClick={() => setFeedbackSent(true)} className="mt-6 text-action-blue font-medium hover:underline">Enviar calificación</button>
                </ConfiguratorCard>
                <ConfiguratorCard className="flex flex-col items-center text-center py-10 hover:border-amber-500/30 transition-all cursor-pointer group">
                    <div className="w-16 h-16 rounded-full bg-amber-50 text-amber-600 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform"><X size={32} /></div>
                    <p className="text-[21px] font-semibold text-ink">Necesita Ajustes</p>
                    <button onClick={() => setFeedbackSent(true)} className="mt-6 text-action-blue font-medium hover:underline">Enviar feedback</button>
                </ConfiguratorCard>
              </div>

              {/* Match Preview Section */}
              {(enableCrossref && selectedCrossrefId && matchKeys.length > 0) && (
                <ConfiguratorCard title="Validación de datos" subtitle="Resultados del cruce con la base de referencia">
                  {previewError ? (
                    <div className="p-4 rounded-lg bg-red-50/50 border border-red-400/50 text-[14px] text-red-700">
                      {previewError}
                    </div>
                  ) : (
                    <div className="space-y-4">
                      <MatchSummaryBar
                        matchedCount={matchPreview?.matchedCount ?? 0}
                        unmatchedCount={matchPreview?.unmatchedCount ?? 0}
                        expandedSection={previewExpanded}
                        onToggleMatch={() => setPreviewExpanded(previewExpanded === "matched" ? null : "matched")}
                        onToggleUnmatched={() => setPreviewExpanded(previewExpanded === "unmatched" ? null : "unmatched")}
                        loading={matchPreviewLoading}
                      />

                      {matchPreviewLoading && (
                        <div className="animate-pulse space-y-3">
                          <div className="h-8 bg-gray-100 rounded" />
                          <div className="h-8 bg-gray-100 rounded w-3/4" />
                        </div>
                      )}

                      {!matchPreviewLoading && previewExpanded === "matched" && matchPreview && (
                        <div className="animate-in fade-in slide-in-from-top-2 duration-300">
                          <div className="flex items-center gap-2 mb-3">
                            <span className="text-[14px] font-semibold text-[#34c759]">Concordancia</span>
                            <PillChip variant="status" statusType="matched">
                              {matchPreview.matchedCount} registros validados correctamente
                            </PillChip>
                          </div>
                          <MatchTable
                            columns={[...templateColumns, ...outputColumns.map(c => `xref_${c}`)]}
                            rows={matchPreview.matched}
                            variant="matched"
                            extractionColumnCount={templateColumns.length}
                          />
                        </div>
                      )}

                      {!matchPreviewLoading && previewExpanded === "unmatched" && matchPreview && (
                        <div className="animate-in fade-in slide-in-from-top-2 duration-300">
                          <div className="flex items-center gap-2 mb-3">
                            <span className="text-[14px] font-semibold text-[#ff9500]">Sin concordancia</span>
                            <PillChip variant="status" statusType="unmatched">
                              {matchPreview.unmatchedCount} registros sin validar
                            </PillChip>
                          </div>
                          <MatchTable
                            columns={[...templateColumns, ...outputColumns.map(c => `xref_${c}`)]}
                            rows={matchPreview.unmatched}
                            variant="unmatched"
                            extractionColumnCount={templateColumns.length}
                          />
                        </div>
                      )}
                    </div>
                  )}
                </ConfiguratorCard>
              )}

              {feedbackSent && (
                <div className="fixed inset-0 bg-parchment/95 backdrop-blur-md z-[100] flex flex-col items-center justify-center gap-8 animate-in fade-in duration-500">
                     <div className="text-8xl animate-bounce">✨</div>
                     <h2 className="text-[40px] font-semibold tracking-apple-tight text-ink">¡Configuración Completa!</h2>
                     <p className="text-[21px] text-[#7a7a7a] max-w-md text-center">Su flujo ha sido procesado con los más altos estándares de calidad.</p>
                     <button onClick={() => window.location.reload()} className="bg-action-blue text-white rounded-full px-8 py-3 text-[17px] font-medium active-scale mt-8">
                        Comenzar de nuevo
                     </button>
                </div>
              )}
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
