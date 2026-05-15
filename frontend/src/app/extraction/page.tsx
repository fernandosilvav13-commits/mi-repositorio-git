"use client";

import Link from "next/link";
import { useState, useRef, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Badge } from "@/components/ui/badge";
import { api } from "@/lib/api";

interface Result {
  filename: string;
  status: string;
  data: Record<string, string>;
  error?: string;
}

export default function ExtractionPage() {
  const [files, setFiles] = useState<File[]>([]);
  const [results, setResults] = useState<Result[]>([]);
  const [loading, setLoading] = useState(false);
  const [threshold, setThreshold] = useState(70);
  const [templates, setTemplates] = useState<any[]>([]);
  const [selectedTemplate, setSelectedTemplate] = useState<string>("");
  const [uploading, setUploading] = useState(false);
  const fileRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    api.templates.list().then(setTemplates).catch(() => {});
  }, []);

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    const dropped = Array.from(e.dataTransfer.files);
    setFiles((prev) => [...prev, ...dropped]);
  };

  const runExtraction = async () => {
    if (!selectedTemplate || files.length === 0) return;
    setLoading(true);
    setResults([]);
    try {
      setUploading(true);
      const form = new FormData();
      files.forEach((f) => form.append("files", f));
      const uploaded = await api.ingest.upload(files);
      setUploading(false);

      const res = await api.extraction.extract({
        template_id: selectedTemplate,
        file_paths: uploaded.files,
        fuzzy_threshold: threshold,
      });
      setResults(res);
    } catch (e: any) {
      alert("Error: " + e.message);
    } finally {
      setLoading(false);
      setUploading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col">
      <header className="border-b">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
          <h1 className="text-xl font-bold">Extracción de Datos</h1>
          <Link href="/" className="inline-flex items-center justify-center rounded-lg border border-border bg-background hover:bg-muted h-8 px-2.5 text-sm font-medium">← Volver</Link>
        </div>
      </header>
      <main className="flex-1 max-w-7xl mx-auto px-4 py-8 w-full space-y-6">
        <Card>
          <CardHeader>
            <CardTitle>Subir Documentos</CardTitle>
          </CardHeader>
          <CardContent>
            <div
              onDrop={handleDrop}
              onDragOver={(e) => e.preventDefault()}
              className="border-2 border-dashed rounded-lg p-12 text-center hover:border-primary cursor-pointer"
              onClick={() => fileRef.current?.click()}
            >
              <input
                ref={fileRef}
                type="file"
                multiple
                accept=".pdf,.doc,.docx,.csv,.jpg,.jpeg,.png"
                className="hidden"
                onChange={(e) => setFiles(Array.from(e.target.files || []))}
              />
              <p className="text-lg font-medium">Arrastra archivos aquí</p>
              <p className="text-sm text-muted-foreground mt-1">
                PDF, DOC, DOCX, CSV, JPG, PNG
              </p>
            </div>
            {files.length > 0 && (
              <div className="mt-4">
                <p className="text-sm font-medium mb-2">{files.length} archivo(s)</p>
                <div className="flex flex-wrap gap-2">
                  {files.map((f, i) => (
                    <Badge key={i} variant="secondary">{f.name}</Badge>
                  ))}
                </div>
              </div>
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Configuración</CardTitle>
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
                    <SelectItem key={t.id} value={t.id}>
                      {t.name} ({t.columns?.length ?? 0} columnas)
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div>
              <label className="text-sm font-medium">
                Umbral Fuzzy Matching: {threshold}%
              </label>
              <input
                type="range"
                min="0"
                max="100"
                value={threshold}
                onChange={(e) => setThreshold(Number(e.target.value))}
                className="w-full"
              />
              <div className="flex justify-between text-xs text-muted-foreground">
                <span>0% - Permisivo</span>
                <span>100% - Exacto</span>
              </div>
            </div>
            <Button onClick={runExtraction} disabled={loading || files.length === 0 || !selectedTemplate}>
              {uploading ? "Subiendo archivos..." : loading ? "Extrayendo..." : "Ejecutar Extracción"}
            </Button>
          </CardContent>
        </Card>

        {results.length > 0 && (
          <Card>
            <CardHeader>
              <CardTitle>Resultados</CardTitle>
            </CardHeader>
            <CardContent>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Archivo</TableHead>
                    <TableHead>Estado</TableHead>
                    {Object.keys(results[0].data).map((k) => (
                      <TableHead key={k}>{k}</TableHead>
                    ))}
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {results.map((r, i) => (
                    <TableRow key={i}>
                      <TableCell>{r.filename}</TableCell>
                      <TableCell>
                        <Badge variant={r.status === "ok" ? "default" : "destructive"}>
                          {r.status}
                        </Badge>
                      </TableCell>
                      {Object.values(r.data).map((v, j) => (
                        <TableCell key={j}>
                          {v === "NO ENCONTRADO" ? (
                            <span className="text-destructive font-medium">NO ENCONTRADO</span>
                          ) : (
                            v
                          )}
                        </TableCell>
                      ))}
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        )}
      </main>
    </div>
  );
}
