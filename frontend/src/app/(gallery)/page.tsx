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
import { FileText } from "lucide-react";

interface Result {
  id?: string;
  filename: string;
  folder?: string;
  status: string;
  data: Record<string, any>;
  rules?: any[];
  error?: string;
}

export default function GalleryPage() {
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
      {/* Hero Section */}
      <Tile variant="white">
        <h2 className="text-[21px] font-semibold tracking-tight text-ink/60 mb-2">
          Collection
        </h2>
        <h1 className="text-[56px] md:text-[72px] font-bold tracking-tight text-ink leading-[1.05] mb-8">
          Extracted Insights
        </h1>
        
        <div className="flex flex-wrap items-center justify-center gap-4 mt-4 p-4 rounded-2xl bg-near-black/5 backdrop-blur-md">
          <Select value={selectedTemplate} onValueChange={setSelectedTemplate}>
            <SelectTrigger className="w-[200px] bg-white rounded-full border-none shadow-sm h-10 px-4">
              <SelectValue placeholder="Select Template" />
            </SelectTrigger>
            <SelectContent>
              {templates.map((t: any) => (
                <SelectItem key={t.id} value={t.id}>
                  {t.name}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>

          <Button 
            variant="outline" 
            onClick={() => fileRef.current?.click()}
            className="rounded-full bg-white border-none shadow-sm h-10"
          >
            Add Files
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
            className="rounded-full bg-ink text-white h-10 px-6 hover:bg-ink/90 transition-all"
          >
            {loading ? "Analyzing..." : "Process Collection"}
          </Button>
        </div>
        
        {files.length > 0 && (
          <p className="mt-4 text-sm text-ink/40">
            {files.length} items ready for processing
          </p>
        )}
      </Tile>

      {/* Gallery Section */}
      <Tile variant="dark" className="min-h-[600px] !items-start">
        {results.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 w-full max-w-7xl mx-auto">
            {results.map((result, idx) => {
              // Task 2: Data Mapping
              const score = result.data.score || result.data.Score || "Pristine";
              const rut = result.data.RUT || result.data.rut || "Unknown";
              
              return (
                <ProductCard
                  key={result.id || idx}
                  title={result.filename}
                  description={`Condition: ${score}`}
                  className="h-full"
                >
                  <div className="flex flex-col gap-4">
                    <div className="relative w-full aspect-[4/3] bg-near-black-2 rounded-md flex items-center justify-center overflow-hidden">
                       <FileText size={64} className="text-white/10" />
                       <div className="absolute inset-0 bg-gradient-to-tr from-white/5 to-transparent pointer-events-none" />
                    </div>
                    
                    <div className="flex flex-col gap-1">
                      <span className="text-[10px] uppercase tracking-widest text-ink/40 font-bold">
                        Artifact Metadata
                      </span>
                      <div className="flex justify-between items-center py-2 border-b border-ink/5">
                        <span className="text-[13px] text-ink/60">Serial No.</span>
                        <span className="text-[13px] font-mono font-medium">{rut}</span>
                      </div>
                      <div className="flex justify-between items-center py-2">
                        <span className="text-[13px] text-ink/60">Provenance</span>
                        <span className="text-[13px]">{result.folder || "Raíz"}</span>
                      </div>
                    </div>
                  </div>
                </ProductCard>
              );
            })}
          </div>
        ) : (
          <div className="flex flex-col items-center justify-center py-40 w-full text-white/40">
            <p className="text-[21px] font-medium">No artifacts found in collection.</p>
            <p className="text-[17px]">Complete an extraction to see results here.</p>
          </div>
        )}
      </Tile>

      {/* Utility Section */}
      <Tile variant="parchment">
        <div className="flex flex-col items-center gap-6">
          <h3 className="text-[28px] font-semibold tracking-tight">
            Preserve findings.
          </h3>
          <p className="max-w-md text-[17px] text-ink/60 mb-4 text-center">
            Export your collection as a high-fidelity spreadsheet for external analysis.
          </p>
          <Button 
            onClick={handleExport}
            className="rounded-full px-8 py-6 h-auto text-[17px] font-medium bg-ink text-white hover:bg-ink/90 transition-all"
            disabled={results.length === 0}
          >
            Download Collection
          </Button>
        </div>
      </Tile>
    </div>
  );
}
