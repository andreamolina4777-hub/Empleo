import "../dashboard/app/globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Contexto económico | Ecuador y el mundo",
  description: "Dashboard académico reproducible"
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return <html lang="es"><body>{children}</body></html>;
}
