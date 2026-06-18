"use client";

import { useState, FormEvent } from "react";
import Link from "next/link";
import { useAuth } from "@/lib/auth-context";
import { useRouter } from "next/navigation";
import { toast } from "sonner";
import { Loader2 } from "lucide-react";

const AUTH_ENABLED = !!(process.env.NEXT_PUBLIC_SUPABASE_URL && process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY);

export default function LoginPage() {
  const { login, user } = useAuth();
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [submitting, setSubmitting] = useState(false);

  if (!AUTH_ENABLED) {
    router.push("/wizard");
    return null;
  }

  if (user) {
    router.push("/wizard");
    return null;
  }

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      await login(email, password);
      toast.success("Sesión iniciada");
    } catch (err: any) {
      toast.error(err.message || "Error al iniciar sesión");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="w-full max-w-sm space-y-6">
      <div className="text-center space-y-2">
        <h1 className="text-[32px] font-semibold tracking-tight text-ink">
          Iniciar sesión
        </h1>
        <p className="text-[15px] text-[#6e6e73]">
          Ingresa con tu cuenta para continuar
        </p>
      </div>

      <div className="space-y-4">
        <div>
          <input
            type="email"
            placeholder="Correo electrónico"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            className="w-full rounded-xl border border-[#d2d2d7] bg-white px-4 py-3 text-[15px] text-ink outline-none transition-colors placeholder:text-[#86868b] focus:border-action-blue"
          />
        </div>
        <div>
          <input
            type="password"
            placeholder="Contraseña"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            className="w-full rounded-xl border border-[#d2d2d7] bg-white px-4 py-3 text-[15px] text-ink outline-none transition-colors placeholder:text-[#86868b] focus:border-action-blue"
          />
        </div>
      </div>

      <button
        type="submit"
        disabled={submitting}
        className="active-scale w-full rounded-pill bg-action-blue px-4 py-3 text-[15px] font-semibold text-white transition-opacity hover:opacity-90 disabled:opacity-50"
      >
        {submitting ? <Loader2 className="mx-auto h-5 w-5 animate-spin" /> : "Iniciar sesión"}
      </button>

      <p className="text-center text-[13px] text-[#6e6e73]">
        ¿No tienes cuenta?{" "}
        <Link href="/signup" className="text-action-blue hover:underline">
          Crear cuenta
        </Link>
      </p>
    </form>
  );
}
