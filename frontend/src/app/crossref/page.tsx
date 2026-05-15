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
import { Badge } from "@/components/ui/badge";
import { api } from "@/lib/api";

export default function CrossrefPage() {
  const [files, setFiles] = useState<any[]>([]);
  const [uploading, setUploading] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const fileRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    loadFiles();
  }, []);

  const loadFiles = async () => {
    try {
      setFiles(await api.crossref.list());
    } catch {
      /* no auth yet */
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) return;
    setUploading(true);
    try {
      await api.crossref.upload(selectedFile);
      setSelectedFile(null);
      await loadFiles();
    } catch (e: any) {
      alert("Error al subir: " + e.message);
    } finally {
      setUploading(false);
    }
  };

  const handleDelete = async (id: string) => {
    try {
      await api.crossref.delete(id);
      await loadFiles();
    } catch (e: any) {
      alert("Error al eliminar: " + e.message);
    }
  };

  const formatDate = (d: string) =>
    new Date(d).toLocaleDateString("es-CL", {
      year: "numeric",
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });

  return (
    <div className="min-h-screen flex flex-col">
      <header className="border-b">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
          <h1 className="text-xl font-bold">Cruzar Datos</h1>
          <Link href="/" className="inline-flex items-center justify-center rounded-lg border border-border bg-background hover:bg-muted h-8 px-2.5 text-sm font-medium">← Volver</Link>
        </div>
      </header>
      <main className="flex-1 max-w-7xl mx-auto px-4 py-8 w-full space-y-6">
        <Card>
          <CardHeader>
            <CardTitle>Subir Archivo de Referencia</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div
              onClick={() => fileRef.current?.click()}
              className="border-2 border-dashed rounded-lg p-12 text-center hover:border-primary cursor-pointer"
            >
              <input
                ref={fileRef}
                type="file"
                accept=".pdf,.csv,.ppt,.pptx,.doc,.docx"
                className="hidden"
                onChange={(e) => setSelectedFile(e.target.files?.[0] || null)}
              />
              <p className="text-lg font-medium">Selecciona un archivo</p>
              <p className="text-sm text-muted-foreground mt-1">
                PDF, CSV, PPT, DOCX — Archivos con datos de referencia para cruzar (ej: base MinEduc)
              </p>
            </div>
            {selectedFile && (
              <div className="flex items-center gap-3">
                <Badge variant="secondary">{selectedFile.name}</Badge>
                <Button onClick={handleUpload} disabled={uploading} size="sm">
                  {uploading ? "Subiendo..." : "Subir Archivo"}
                </Button>
              </div>
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Archivos Subidos</CardTitle>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Nombre</TableHead>
                  <TableHead>Tipo</TableHead>
                  <TableHead>Columnas</TableHead>
                  <TableHead>Filas</TableHead>
                  <TableHead>Subido</TableHead>
                  <TableHead>Acciones</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {files.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={6} className="text-center text-muted-foreground">
                      No hay archivos subidos aún.
                    </TableCell>
                  </TableRow>
                ) : (
                  files.map((f: any) => (
                    <TableRow key={f.id}>
                      <TableCell className="font-medium">{f.name}</TableCell>
                      <TableCell>
                        <Badge variant="outline">{f.file_type?.toUpperCase()}</Badge>
                      </TableCell>
                      <TableCell>{f.columns?.length ?? 0}</TableCell>
                      <TableCell>{f.row_count}</TableCell>
                      <TableCell className="text-sm text-muted-foreground">{formatDate(f.created_at)}</TableCell>
                      <TableCell>
                        <Button variant="destructive" size="sm" onClick={() => handleDelete(f.id)}>
                          Eliminar
                        </Button>
                      </TableCell>
                    </TableRow>
                  ))
                )}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      </main>
    </div>
  );
}
