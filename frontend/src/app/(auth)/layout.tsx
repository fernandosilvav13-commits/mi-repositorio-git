export default function AuthLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex min-h-[calc(100vh-6rem)] items-center justify-center bg-parchment px-4">
      {children}
    </div>
  );
}
