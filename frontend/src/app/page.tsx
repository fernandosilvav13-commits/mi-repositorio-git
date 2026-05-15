import Link from "next/link";

const features = [
  {
    title: "🌐 Flujo Completo",
    description: "Guía paso a paso: subir archivos, cruzar datos, extraer y exportar",
    href: "/wizard",
    color: "bg-violet-600",
  },
  {
    title: "Plantillas",
    description: "Define esquemas de extracción con columnas dinámicas y formatos de salida",
    href: "/templates",
    color: "bg-blue-500",
  },
  {
    title: "Extracción",
    description: "Sube documentos y extrae datos estructurados con IA + Fuzzy Matching",
    href: "/extraction",
    color: "bg-emerald-500",
  },
  {
    title: "Reglas",
    description: "Crea reglas de negocio para formatear y colorear resultados",
    href: "/rules",
    color: "bg-amber-500",
  },
  {
    title: "Exportar",
    description: "Genera Excel con formato condicional y reglas aplicadas",
    href: "/export",
    color: "bg-violet-500",
  },
  {
    title: "Cruzar Datos",
    description: "Sube archivos de referencia (MinEduc, etc.) para enriquecer el Excel final",
    href: "/crossref",
    color: "bg-rose-500",
  },
];

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col">
      <header className="border-b">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
          <h1 className="text-xl font-bold">Automatizacion-Ciclo</h1>
          <span className="text-sm text-muted-foreground">Sistema de Automatización Documental</span>
        </div>
      </header>
      <main className="flex-1 max-w-7xl mx-auto px-4 py-12 w-full">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold tracking-tight">Panel de Control</h2>
          <p className="text-muted-foreground mt-2">
            Gestión de extracción de datos desde documentos con IA
          </p>
        </div>
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {features.map((f) => (
            <Link key={f.href} href={f.href} className="group">
              <div className="rounded-lg border bg-card p-6 hover:shadow-md transition-shadow">
                <div className={`w-10 h-10 rounded-lg ${f.color} mb-4`} />
                <h3 className="font-semibold mb-2">{f.title}</h3>
                <p className="text-sm text-muted-foreground">{f.description}</p>
              </div>
            </Link>
          ))}
        </div>
      </main>
    </div>
  );
}
