"use client";

import { useAuth } from "@/lib/auth-context";
import { useRouter } from "next/navigation";
import { useEffect } from "react";

const AUTH_ENABLED = !!(process.env.NEXT_PUBLIC_SUPABASE_URL && process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY);

export function AuthGuard({ children }: { children: React.ReactNode }) {
  const { user, loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (AUTH_ENABLED && !loading && !user) {
      router.push("/login");
    }
  }, [user, loading, router]);

  if (AUTH_ENABLED && loading) {
    return (
      <div className="flex min-h-[50vh] items-center justify-center">
        <div className="h-6 w-6 animate-spin rounded-full border-2 border-[#d2d2d7] border-t-action-blue" />
      </div>
    );
  }

  if (AUTH_ENABLED && !user) return null;

  return <>{children}</>;
}
