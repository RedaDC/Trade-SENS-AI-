import type { Metadata } from "next";
import { Inter, Outfit } from "next/font/google"; // Added Outfit for headings
import "./globals.css";
import Navbar from "@/components/Navbar";

const inter = Inter({ subsets: ["latin"], variable: '--font-inter' });
const outfit = Outfit({ subsets: ["latin"], variable: '--font-outfit' });

export const metadata: Metadata = {
  title: "TradeSense AI | Elite Prop Trading Platform",
  description: "Institutional-grade AI signals, real-time market data, and instant funding for serious traders.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className={`${inter.variable} ${outfit.variable} font-sans bg-slate-950 text-white antialiased selection:bg-blue-500/30`}>
        <div className="fixed inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-blue-900/20 via-slate-950 to-slate-950 z-0 pointer-events-none"></div>
        <div className="fixed inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-5 pointer-events-none z-50"></div>
        <Navbar />
        <main className="min-h-screen relative">
          {children}
        </main>
      </body>
    </html>
  );
}
