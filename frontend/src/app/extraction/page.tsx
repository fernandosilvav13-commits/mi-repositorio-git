"use client";

import React, { useState, useEffect, useRef } from "react";
import Tile from "@/components/apple/Tile";
import ProductCard from "@/components/apple/ProductCard";
import { api } from "@/lib/api";
import { Button } from "@/components/ui/button";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { FileText, Download, Play, Plus, ArrowLeft } from "lucide-react";
import { cn } from "@/lib/utils";
import Link from "next/link";

interface Result {
  id?: string;
  filename: string;
  folder?: string;
  status: string;
  data: Record<string, any>;
  rules?: any[];
  error?: string;
}

export default function ExtractionGalleryPage() {
  const [files, setFiles] = useState<{ file: File; folder: string }[]>([]);
  const [results, setResults] = useState<Result[]>([]);
  const [loading, setLoading] = useState(false);
  const [templates, setTemplates] = useState<any[]>([]);
  const [selectedTemplate, setSelectedTemplate] = useState<string>("");
  const fileRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    api.templates.list().then(setTemplates).catch(() => {});
  }, []);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFiles = Array.from(e.target.files || []);
    const newFiles = selectedFiles.map(f => ({ file: f, folder: "Raíz" }));
    setFiles((prev) => [...prev, ...newFiles]);
  };

  const runExtraction = async () => {
    if (!selectedTemplate || files.length === 0) return;
    setLoading(true);
    setResults([]);
    
    try {
      const uploaded = await api.ingest.upload(files.map(f => f.file));
      const res = await api.extraction.extract({
        template_id: selectedTemplate,
        file_paths: uploaded.files,
      });

      const processedRes = res.map((r: any) => {
        const fileMatch = files.find(f => f.file.name === r.filename);
        return { ...r, folder: fileMatch?.folder || "Raíz" };
      });

      setResults(processedRes);
    } catch (e: any) {
      alert("Error: " + e.message);
    } finally {
      setLoading(false);
    }
  };

  const handleExport = () => {
    if (results.length === 0) return;
    const rowsToExport = results.map(r => ({ ...r.data, Carpeta: r.folder }));
    api.export.excel({ template_id: selectedTemplate, rows: rowsToExport });
  };

  return (
    <div className="flex flex-col w-full bg-white">
      {/* Floating Back Button */}
      <div className="fixed top-8 left-8 z-50">
        <Link href="/">
          <Button variant="ghost" className="rounded-full bg-white/80 backdrop-blur-md shadow-sm hover:bg-white active-scale">
            <ArrowLeft size={20} className="mr-2" />
            Back
          </Button>
        </Link>
      </div>

      {/* Hero Section - White Tile */}
      <Tile variant="white" className="pt-32 pb-20">
        <h2 className="text-[21px] font-semibold tracking-[0.011em] text-ink/60 mb-2 uppercase">
          Collection
        </h2>
        <h1 className="apple-tight text-[56px] md:text-[72px] lg:text-[80px] text-ink leading-[1.05] mb-12 text-center">
          Extracted Insights
        </h1>
        
        {/* Floating Controls Bar */}
        <div className="flex flex-wrap items-center justify-center gap-3 p-2 rounded-full bg-near-black/5 backdrop-blur-xl border border-white/20 shadow-sm">
          <Select value={selectedTemplate} onValueChange={setSelectedTemplate}>
            <SelectTrigger className="w-[180px] bg-white rounded-full border-none shadow-sm h-11 px-5 text-[14px] font-medium active-scale transition-all">
              <SelectValue placeholder="Template" />
            </SelectTrigger>
            <SelectContent className="rounded-2xl border-none shadow-xl">
              {templates.map((t: any) => (
                <SelectItem key={t.id} value={t.id} className="rounded-lg">
                  {t.name}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>

          <Button 
            variant="ghost" 
            onClick={() => fileRef.current?.click()}
            className="rounded-full bg-white/80 hover:bg-white text-ink border-none shadow-sm h-11 px-5 active-scale transition-all flex items-center gap-2"
          >
            <Plus size={18} />
            <span className="text-[14px] font-medium">Add Artifacts</span>
          </Button>
          <input
            ref={fileRef}
            type="file"
            multiple
            className="hidden"
            onChange={handleFileChange}
          />

          <Button 
            onClick={runExtraction} 
            disabled={loading || files.length === 0 || !selectedTemplate}
            className={cn(
              "rounded-full h-11 px-8 active-scale transition-all flex items-center gap-2",
              loading ? "bg-ink/40" : "bg-action-blue text-white hover:bg-action-blue/90"
            )}
          >
            {loading ? (
              <div className="h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent" />
            ) : (
              <Play size={16} fill="currentColor" />
            )}
            <span className="text-[14px] font-medium">{loading ? "Analyzing..." : "Process Collection"}</span>
          </Button>
        </div>
        
        {files.length > 0 && (
          <p className="mt-6 text-[14px] font-medium text-ink/40 animate-in fade-in slide-in-from-top-2 duration-500">
            {files.length} artifact{files.length > 1 ? 's' : ''} staged for extraction
          </p>
        )}
      </Tile>

      {/* Gallery Grid - Dark Tile */}
      <Tile variant="dark" className="min-h-[800px] !items-start overflow-visible">
        {results.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 w-full max-w-7xl mx-auto px-4 md:px-6">
            {results.map((result, idx) => {
              const score = result.data.score || result.data.Score || "Pristine";
              const rut = result.data.RUT || result.data.rut || "Unknown";
              
              return (
                <div key={result.id || idx} className="animate-in fade-in zoom-in-95 duration-700 ease-out fill-mode-both" style={{ animationDelay: `${idx * 50}ms` }}>
                  <ProductCard
                    title={result.filename}
                    description={`Condition: ${score}`}
                    className="h-full group hover:border-ink/20 transition-all duration-500"
                  >
                    <div className="flex flex-col gap-6">
                      <div className="relative w-full aspect-[4/3] bg-near-black-2 rounded-lg flex items-center justify-center overflow-hidden">
                         <FileText size={80} className="text-white/5 transition-transform duration-700 group-hover:scale-110" />
                         <div className="absolute inset-0 bg-gradient-to-tr from-white/5 to-transparent pointer-events-none" />
                         
                         {/* Gloss effect */}
                         <div className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-1000 bg-gradient-to-br from-white/10 via-transparent to-transparent pointer-events-none" />
                      </div>
                      
                      <div className="flex flex-col gap-1">
                        <span className="text-[10px] uppercase tracking-[0.1em] text-ink/30 font-bold">
                          Artifact Metadata
                        </span>
                        <div className="flex justify-between items-center py-3 border-b border-ink/5">
                          <span className="text-[14px] text-ink/50">Serial No.</span>
                          <span className="text-[14px] font-mono font-medium text-ink/80">{rut}</span>
                        </div>
                        <div className="flex justify-between items-center py-3">
                          <span className="text-[14px] text-ink/50">Provenance</span>
                          <span className="text-[14px] text-ink/80">{result.folder || "Raíz"}</span>
                        </div>
                      </div>
                    </div>
                  </ProductCard>
                </div>
              );
            })}
          </div>
        ) : (
          <div className="flex flex-col items-center justify-center py-60 w-full text-white/20">
            <div className="w-20 h-20 rounded-3xl bg-white/5 flex items-center justify-center mb-8">
              <FileText size={32} />
            </div>
            <p className="text-[24px] font-medium tracking-tight mb-2">Collection is currently empty.</p>
            <p className="text-[17px] max-w-sm text-center">Add artifacts and choose a template to begin the museum extraction.</p>
          </div>
        )}
      </Tile>

      {/* Export Section - Parchment Tile */}
      <Tile variant="parchment" className="border-t border-near-black/5">
        <div className="flex flex-col items-center text-center max-w-2xl">
          <h3 className="apple-tight text-[40px] md:text-[48px] text-ink mb-6">
            Preserve findings.
          </h3>
          <p className="text-[19px] md:text-[21px] text-ink/60 mb-10 leading-relaxed font-normal">
            Export your collection as a high-fidelity spreadsheet for secondary analysis and permanent archiving.
          </p>
          <Button 
            onClick={handleExport}
            disabled={results.length === 0}
            className="rounded-full px-10 py-7 h-auto text-[17px] font-medium bg-ink text-white hover:bg-near-black active-scale transition-all flex items-center gap-3 shadow-lg shadow-near-black/10"
          >
            <Download size={20} />
            Download Collection
          </Button>
        </div>
      </Tile>
    </div>
  );
}
