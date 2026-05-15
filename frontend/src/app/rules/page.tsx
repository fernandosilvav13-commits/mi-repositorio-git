"use client";

import Link from "next/link";
import { useState } from "react";
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

const OPERATORS = [
  { value: "==", label: "Igual a" },
  { value: "!=", label: "Distinto de" },
  { value: ">", label: "Mayor que" },
  { value: "<", label: "Menor que" },
  { value: "contains", label: "Contiene" },
  { value: "not_contains", label: "No contiene" },
  { value: "is_empty", label: "Está vacío" },
  { value: "is_not_empty", label: "No está vacío" },
  { value: "count>", label: "Conteo mayor a" },
  { value: "count<", label: "Conteo menor a" },
];

const ACTIONS = [
  { value: "fill_row", label: "Pintar fila", colors: ["GREEN", "YELLOW", "RED"] },
];

export default function RulesPage() {
  const [open, setOpen] = useState(false);
  const [rules, setRules] = useState<any[]>([]);

  const [newRule, setNewRule] = useState({
    name: "",
    field: "",
    operator: "==",
    value: "",
    action_type: "fill_row",
    action_color: "GREEN",
  });

  const addRule = () => {
    setRules([
      ...rules,
      {
        id: crypto.randomUUID(),
        name: newRule.name,
        conditions: [{ field: newRule.field, operator: newRule.operator, value: newRule.value }],
        action: { type: newRule.action_type, params: { color: newRule.action_color } },
        enabled: true,
      },
    ]);
    setOpen(false);
    setNewRule({ name: "", field: "", operator: "==", value: "", action_type: "fill_row", action_color: "GREEN" });
  };

  return (
    <div className="min-h-screen flex flex-col">
      <header className="border-b">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
          <h1 className="text-xl font-bold">Reglas de Negocio</h1>
          <Link href="/" className="inline-flex items-center justify-center rounded-lg border border-border bg-background hover:bg-muted h-8 px-2.5 text-sm font-medium">← Volver</Link>
        </div>
      </header>
      <main className="flex-1 max-w-7xl mx-auto px-4 py-8 w-full">
        <div className="flex justify-between items-center mb-6">
          <p className="text-muted-foreground">
            Define reglas para formatear y colorear los resultados
          </p>
          <Dialog open={open} onOpenChange={setOpen}>
            <DialogTrigger>
              <Button>Nueva Regla</Button>
            </DialogTrigger>
            <DialogContent>
              <DialogHeader>
                <DialogTitle>Crear Regla</DialogTitle>
              </DialogHeader>
              <div className="space-y-4">
                <div>
                  <Label>Nombre de la regla</Label>
                  <Input
                    value={newRule.name}
                    onChange={(e) => setNewRule({ ...newRule, name: e.target.value })}
                    placeholder="Ej: Más de 4 títulos"
                  />
                </div>
                <div className="grid grid-cols-3 gap-2">
                  <div>
                    <Label>Campo</Label>
                    <Input
                      value={newRule.field}
                      onChange={(e) => setNewRule({ ...newRule, field: e.target.value })}
                      placeholder="campo"
                    />
                  </div>
                  <div>
                    <Label>Operador</Label>
                    <Select value={newRule.operator} onValueChange={(v) => setNewRule({ ...newRule, operator: v ?? "" })}>
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        {OPERATORS.map((op) => (
                          <SelectItem key={op.value} value={op.value}>{op.label}</SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                  <div>
                    <Label>Valor</Label>
                    <Input
                      value={newRule.value}
                      onChange={(e) => setNewRule({ ...newRule, value: e.target.value })}
                      placeholder="valor"
                    />
                  </div>
                </div>
                <div className="grid grid-cols-2 gap-2">
                  <div>
                    <Label>Acción</Label>
                    <Select value={newRule.action_type} onValueChange={(v) => setNewRule({ ...newRule, action_type: v ?? "fill_row" })}>
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        {ACTIONS.map((a) => (
                          <SelectItem key={a.value} value={a.value}>{a.label}</SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                  <div>
                    <Label>Color</Label>
                    <Select value={newRule.action_color} onValueChange={(v) => setNewRule({ ...newRule, action_color: v ?? "GREEN" })}>
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        {ACTIONS.find((a) => a.value === newRule.action_type)?.colors.map((c) => (
                          <SelectItem key={c} value={c}>{c}</SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                </div>
                <div className="flex gap-2">
                  <span
                    className="w-6 h-6 rounded-full"
                    style={{ backgroundColor: newRule.action_color === "GREEN" ? "#44FF44" : newRule.action_color === "YELLOW" ? "#FFFF44" : "#FF4444" }}
                  />
                  <span className="text-sm text-muted-foreground self-center">
                    Vista previa del color
                  </span>
                </div>
                <Button className="w-full" onClick={addRule}>Guardar Regla</Button>
              </div>
            </DialogContent>
          </Dialog>
        </div>
        <Card>
          <CardHeader>
            <CardTitle>Mis Reglas</CardTitle>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Nombre</TableHead>
                  <TableHead>Condición</TableHead>
                  <TableHead>Acción</TableHead>
                  <TableHead>Estado</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {rules.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={4} className="text-center text-muted-foreground">
                      No hay reglas aún. Crea una nueva.
                    </TableCell>
                  </TableRow>
                ) : (
                  rules.map((r) => (
                    <TableRow key={r.id}>
                      <TableCell className="font-medium">{r.name}</TableCell>
                      <TableCell>
                        {r.conditions.map((c: any) => `${c.field} ${c.operator} ${c.value}`).join(", ")}
                      </TableCell>
                      <TableCell>
                        <span
                          className="inline-block w-4 h-4 rounded-full mr-2 align-middle"
                          style={{ backgroundColor: r.action.params.color === "GREEN" ? "#44FF44" : r.action.params.color === "YELLOW" ? "#FFFF44" : "#FF4444" }}
                        />
                        {r.action.type === "fill_row" ? "Pintar fila" : r.action.type}
                      </TableCell>
                      <TableCell>
                        <span className="text-emerald-600">Activa</span>
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
