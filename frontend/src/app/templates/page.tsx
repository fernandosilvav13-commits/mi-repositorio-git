"use client";

import Link from "next/link";
import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
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
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { api } from "@/lib/api";

interface Column {
  name: string;
  display_name: string;
  data_type: string;
  output_format?: string;
}

const RUT_FORMATS = [
  { value: "con_puntos_y_guion", label: "Con puntos y guión (12.345.678-9)" },
  { value: "solo_guion", label: "Solo guión (12345678-9)" },
  { value: "sin_formato", label: "Sin formato (123456789)" },
];

const DATA_TYPES = ["string", "number", "date", "rut", "email", "phone"];

export default function TemplatesPage() {
  const [columns, setColumns] = useState<Column[]>([]);
  const [templateName, setTemplateName] = useState("");
  const [open, setOpen] = useState(false);
  const [templates, setTemplates] = useState<any[]>([]);
  const [saving, setSaving] = useState(false);

  useEffect(() => { loadTemplates(); }, []);

  const loadTemplates = async () => {
    try { setTemplates(await api.templates.list()); } catch { /* no auth yet */ }
  };

  const addColumn = () => {
    setColumns([...columns, { name: "", display_name: "", data_type: "string" }]);
  };

  const updateColumn = (i: number, field: keyof Column, value: string | null) => {
    if (value === null) return;
    const updated = [...columns];
    (updated[i] as any)[field] = value;
    if (field === "display_name" && !updated[i].name) {
      updated[i].name = value.toLowerCase().replace(/\s+/g, "_");
    }
    setColumns(updated);
  };

  const removeColumn = (i: number) => {
    setColumns(columns.filter((_, idx) => idx !== i));
  };

  const handleSave = async () => {
    if (!templateName.trim()) return;
    if (columns.length === 0) return;
    setSaving(true);
    try {
      await api.templates.create({ name: templateName, columns });
      setTemplateName("");
      setColumns([]);
      setOpen(false);
      await loadTemplates();
    } catch (e: any) {
      alert("Error al guardar: " + e.message);
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col">
      <header className="border-b">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
          <h1 className="text-xl font-bold">Plantillas de Extracción</h1>
          <Link href="/" className="inline-flex items-center justify-center rounded-lg border border-border bg-background hover:bg-muted h-8 px-2.5 text-sm font-medium">← Volver</Link>
        </div>
      </header>
      <main className="flex-1 max-w-7xl mx-auto px-4 py-8 w-full">
        <div className="flex justify-between items-center mb-6">
          <p className="text-muted-foreground">
            Define los esquemas de datos a extraer de los documentos
          </p>
          <Dialog open={open} onOpenChange={setOpen}>
            <DialogTrigger>
              <Button>Nueva Plantilla</Button>
            </DialogTrigger>
            <DialogContent className="max-w-2xl">
              <DialogHeader>
                <DialogTitle>Crear Plantilla</DialogTitle>
              </DialogHeader>
              <div className="space-y-4">
                <div>
                  <Label>Nombre de la plantilla</Label>
                  <Input
                    value={templateName}
                    onChange={(e) => setTemplateName(e.target.value)}
                    placeholder="Ej: Datos Personales"
                  />
                </div>
                <div className="space-y-2">
                  <div className="flex justify-between items-center">
                    <Label>Columnas</Label>
                    <Button variant="outline" size="sm" onClick={addColumn}>
                      + Agregar Columna
                    </Button>
                  </div>
                  {columns.map((col, i) => (
                    <Card key={i}>
                      <CardContent className="pt-4 space-y-2">
                        <div className="grid grid-cols-4 gap-2">
                          <div>
                            <Label className="text-xs">Nombre campo</Label>
                            <Input
                              value={col.name}
                              onChange={(e) => updateColumn(i, "name", e.target.value)}
                              placeholder="nombre"
                            />
                          </div>
                          <div>
                            <Label className="text-xs">Nombre visible</Label>
                            <Input
                              value={col.display_name}
                              onChange={(e) => updateColumn(i, "display_name", e.target.value)}
                              placeholder="Nombre completo"
                            />
                          </div>
                          <div>
                            <Label className="text-xs">Tipo de dato</Label>
                            <Select
                              value={col.data_type}
                              onValueChange={(v) => updateColumn(i, "data_type", v)}
                            >
                              <SelectTrigger>
                                <SelectValue />
                              </SelectTrigger>
                              <SelectContent>
                                {DATA_TYPES.map((t) => (
                                  <SelectItem key={t} value={t}>{t}</SelectItem>
                                ))}
                              </SelectContent>
                            </Select>
                          </div>
                          <div>
                            <Label className="text-xs">Formato de salida</Label>
                            {col.data_type === "rut" ? (
                              <Select
                                value={col.output_format}
                                onValueChange={(v) => updateColumn(i, "output_format", v)}
                              >
                                <SelectTrigger>
                                  <SelectValue placeholder="Seleccionar" />
                                </SelectTrigger>
                                <SelectContent>
                                  {RUT_FORMATS.map((f) => (
                                    <SelectItem key={f.value} value={f.value}>{f.label}</SelectItem>
                                  ))}
                                </SelectContent>
                              </Select>
                            ) : (
                              <Input
                                value={col.output_format || ""}
                                onChange={(e) => updateColumn(i, "output_format", e.target.value)}
                                placeholder="Formato"
                              />
                            )}
                          </div>
                        </div>
                        <Button variant="destructive" size="sm" onClick={() => removeColumn(i)}>
                          Eliminar
                        </Button>
                      </CardContent>
                    </Card>
                  ))}
                </div>
                <Button className="w-full" onClick={handleSave} disabled={saving || !templateName.trim() || columns.length === 0}>
                  {saving ? "Guardando..." : "Guardar Plantilla"}
                </Button>
              </div>
            </DialogContent>
          </Dialog>
        </div>
        <Card>
          <CardHeader>
            <CardTitle>Mis Plantillas</CardTitle>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Nombre</TableHead>
                  <TableHead>Columnas</TableHead>
                  <TableHead>Descripción</TableHead>
                  <TableHead>Acciones</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {templates.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={4} className="text-center text-muted-foreground">
                      No hay plantillas aún. Crea una nueva.
                    </TableCell>
                  </TableRow>
                ) : (
                  templates.map((t: any) => (
                    <TableRow key={t.id}>
                      <TableCell className="font-medium">{t.name}</TableCell>
                      <TableCell>{t.columns?.length ?? 0}</TableCell>
                      <TableCell className="text-muted-foreground">{t.description || "-"}</TableCell>
                      <TableCell>
                        <Button variant="outline" size="sm">Ver</Button>
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
