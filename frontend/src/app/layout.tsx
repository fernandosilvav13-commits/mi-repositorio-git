import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { Toaster } from "sonner";
import GlobalNav from "@/components/layout/GlobalNav";
import SubNav from "@/components/layout/SubNav";

const inter = Inter({
  subsets: ["latin"],
  display: "swap",
});

export const metadata: Metadata = {
  title: "Proyecto Prueba | Apple Design",
  description: "Extracción inteligente de CVs con diseño de alta gama.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="es" className={`${inter.className} antialiased`}>
      <body className="min-h-screen bg-white text-ink">
        <GlobalNav />
        <SubNav />
        <main>
          {children}
        </main>
        <Toaster richColors position="top-right" />
      </body>
    </html>
  );
}
