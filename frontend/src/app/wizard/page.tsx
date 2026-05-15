"use client";

import { useState, useRef, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { api } from "@/lib/api";
import { LucideIcon, Upload, Database, Layout, ShieldCheck, Cpu, FileSpreadsheet, Star, ChevronRight, ChevronLeft, Plus, Check, X } from "lucide-react";
import ConfiguratorCard from "@/components/apple/ConfiguratorCard";
import FrostedContainer from "@/components/apple/FrostedContainer";
import { cn } from "@/lib/utils";

type Step = "upload" | "crossref" | "template" | "rules" | "extract" | "export" | "review";

const STEPS: { key: Step; label: string; icon: any }[] = [
  { key: "upload", label: "Inicio", icon: Upload },
  { key: "crossref", label: "Referencia", icon: Database },
  { key: "template", label: "Estructura", icon: Layout },
  { key: "rules", label: "Inteligencia", icon: ShieldCheck },
  { key: "extract", label: "Procesamiento", icon: Cpu },
  { key: "export", label: "Entrega", icon: FileSpreadsheet },
  { key: "review", label: "Calidad", icon: Star },
];

const PillChip = ({ 
  selected, 
  onClick, 
  children,
  className
}: { 
  selected: boolean; 
  onClick: () => void; 
  children: React.ReactNode;
  className?: string;
}) => (
  <button
    onClick={onClick}
    className={cn(
      "rounded-full px-6 py-3 text-[14px] font-medium transition-all duration-300 active-scale",
      selected 
        ? "border-2 border-action-blue text-action-blue bg-white" 
        : "border border-[#e0e0e0] text-ink bg-white hover:border-[#7a7a7a]",
      className
    )}
  >
    {children}
  </button>
);

export default function WizardPage() {
  const [currentStep, setCurrentStep] = useState<Step>("upload");
  const [subStep, setSubStep] = useState(0);
  const [stepHistory, setStepHistory] = useState<{ step: Step; subStep: number }[]>([]);

  // State Management
  const [uploadFiles, setUploadFiles] = useState<File[]>([]);
  const [uploadedPaths, setUploadedPaths] = useState<string[]>([]);
  const [uploading, setUploading] = useState(false);
  const fileRef = useRef<HTMLInputElement>(null);

  const [enableCrossref, setEnableCrossref] = useState<boolean | null>(null);
  const [crossrefFiles, setCrossrefFiles] = useState<any[]>([]);
  const [selectedCrossrefId, setSelectedCrossrefId] = useState("");
  const [crossrefData, setCrossrefData] = useState<any>(null);
  const [matchColumn, setMatchColumn] = useState("");
  const [crossrefMatchColumn, setCrossrefMatchColumn] = useState("");
  const [outputColumns, setOutputColumns] = useState<string[]>([]);
  
  const [templates, setTemplates] = useState<any[]>([]);
  const [selectedTemplateId, setSelectedTemplateId] = useState("");
  const [templateColumns, setTemplateColumns] = useState<string[]>([]);
  const [newTemplateName, setNewTemplateName] = useState("");
  const [newTemplateColumns, setNewTemplateColumns] = useState<any[]>([]);

  const [rules, setRules] = useState<any[]>([]);
  const [selectedRuleIds, setSelectedRuleIds] = useState<Set<string>>(new Set());

  const [extracting, setExtracting] = useState(false);
  const [extractionResults, setExtractionResults] = useState<any[]>([]);
  const [extractionDone, setExtractionDone] = useState(false);

  const [exporting, setExporting] = useState(false);
  const [exported, setExported] = useState(false);

  const [conforme, setConforme] = useState<boolean | null>(null);
  const [feedbackSent, setFeedbackSent] = useState(false);

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
        setCurrentStep("template");
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
            setCurrentStep("rules");
            setSubStep(0);
            return;
        }
        if (subStep < 1) {
            setSubStep(subStep + 1);
            return;
        }
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
      alert("Error al procesar archivos");
    } finally {
      setUploading(false);
    }
  };

  const handleSelectCrossref = async (id: string) => {
    setSelectedCrossrefId(id);
    const data = await api.crossref.get(id);
    setCrossrefData(data);
    setCrossrefMatchColumn(data.columns?.[0] || "");
    setOutputColumns(data.columns?.slice(1, 3) || []);
    goNext();
  };

  const handleCreateTemplate = async () => {
    const t = await api.templates.create({ name: newTemplateName, columns: newTemplateColumns });
    setSelectedTemplateId(t.id);
    setTemplateColumns(newTemplateColumns.map((c: any) => c.name));
    setCurrentStep("rules");
    setSubStep(0);
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
      alert("Error en la extracción");
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
          match_column: matchColumn,
          crossref_match_column: crossrefMatchColumn,
          output_columns: outputColumns,
        };
      }
      await api.export.excel(payload);
      setExported(true);
      goNext();
    } catch (e) {
      alert("Error al exportar");
    } finally {
      setExporting(false);
    }
  };

  return (
    <div className="min-h-screen bg-parchment flex flex-col items-center pt-[104px] pb-24 overflow-x-hidden">
      {/* Global Nav Placeholder */}
      <div className="fixed top-0 left-0 w-full h-[44px] bg-black z-[100] flex items-center justify-center">
        <span className="text-white text-[12px] font-medium tracking-tight">Proyecto Prueba</span>
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
                onClick={() => fileRef.current?.click()}
                className="w-full aspect-[2/1] rounded-lg border-2 border-dashed border-[#e0e0e0] flex flex-col items-center justify-center gap-4 cursor-pointer hover:border-action-blue group transition-colors bg-white/50"
              >
                <input ref={fileRef} type="file" multiple className="hidden" onChange={(e) => setUploadFiles(Array.from(e.target.files || []))} />
                <div className="w-16 h-16 rounded-full bg-parchment flex items-center justify-center group-hover:bg-action-blue group-hover:text-white transition-all">
                    <Upload size={28} />
                </div>
                <p className="text-[17px] font-semibold text-ink">Seleccionar archivos</p>
                <div className="flex flex-wrap justify-center gap-2 max-w-md px-6">
                    {uploadFiles.slice(0, 5).map((f, i) => (
                        <Badge key={i} variant="secondary" className="bg-parchment text-ink rounded-full px-3 py-1 border-none font-normal text-[12px]">
                            {f.name}
                        </Badge>
                    ))}
                    {uploadFiles.length > 5 && <span className="text-[12px] text-[#7a7a7a]">+{uploadFiles.length - 5} más</span>}
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
                    <PillChip selected={enableCrossref === true} onClick={() => { setEnableCrossref(true); setSubStep(1); }}>
                        Seleccionar
                    </PillChip>
                </div>
              </ConfiguratorCard>
              <ConfiguratorCard 
                title="No, omitir" 
                subtitle="Continuar solo con los datos extraídos de los currículums seleccionados."
              >
                <div className="flex justify-end">
                    <PillChip selected={enableCrossref === false} onClick={() => { setEnableCrossref(false); goNext(); }}>
                        Continuar
                    </PillChip>
                </div>
              </ConfiguratorCard>
            </div>
          )}

          {currentStep === "crossref" && subStep === 1 && (
            <div className="flex flex-col gap-4">
               {crossrefFiles.map((f: any) => (
                  <ConfiguratorCard key={f.id}>
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-[17px] font-semibold text-ink">{f.name}</p>
                            <p className="text-[14px] text-[#7a7a7a]">{f.row_count} registros disponibles</p>
                        </div>
                        <PillChip selected={selectedCrossrefId === f.id} onClick={() => handleSelectCrossref(f.id)}>
                            {selectedCrossrefId === f.id ? "Seleccionado" : "Usar este"}
                        </PillChip>
                    </div>
                  </ConfiguratorCard>
                ))}
            </div>
          )}

          {currentStep === "crossref" && subStep === 2 && (
            <ConfiguratorCard title="Conexión de campos" subtitle="Seleccione la columna de la base maestra que se utilizará como llave de unión.">
                <div className="space-y-6">
                    <div className="space-y-2">
                        <label className="text-[14px] font-semibold text-[#7a7a7a] uppercase tracking-wide">Campo de unión</label>
                        <select 
                            value={crossrefMatchColumn} 
                            onChange={(e) => setCrossrefMatchColumn(e.target.value)} 
                            className="w-full bg-parchment rounded-lg px-4 py-3 text-ink focus:outline-none border border-[#e0e0e0] appearance-none"
                        >
                            {crossrefData?.columns?.map((c: string) => <option key={c} value={c}>{c}</option>)}
                        </select>
                    </div>
                    <button onClick={goNext} className="w-full bg-action-blue text-white rounded-full py-3 text-[17px] font-medium active-scale">
                        Confirmar Enlace
                    </button>
                </div>
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
                        <PillChip selected={selectedTemplateId === t.id} onClick={() => { setSelectedTemplateId(t.id); setTemplateColumns(t.columns.map((c:any) => c.name)); goNext(); }}>
                            Seleccionar
                        </PillChip>
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

          {currentStep === "rules" && (
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
                <div className="mt-8 flex justify-center">
                    <button onClick={goNext} className="bg-action-blue text-white rounded-full px-12 py-3 text-[17px] font-medium active-scale">
                        Continuar
                    </button>
                </div>
            </div>
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
