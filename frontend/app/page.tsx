import { Button } from "@/components/ui/button";
import Link from "next/link";

export default function Home() {
    return (
        <div className="flex flex-col items-center justify-center min-h-[80vh] text-center px-4">
            <h1 className="text-6xl font-extrabold tracking-tight mb-6">
                Unleash Your Trading Potential with <br />
                <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-500 to-purple-500">
                    TradeSense AI
                </span>
            </h1>
            <p className="text-xl text-slate-400 max-w-2xl mb-10">
                The ultimate simulation platform for Prop Traders. Experience real-time US & Morocco markets,
                AI-powered signals, and built-in economic calendars. Prove your skills and get funded.
            </p>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-16 text-left max-w-5xl">
                <div className="p-6 bg-slate-900 rounded-xl border border-slate-800">
                    <h3 className="text-xl font-bold mb-2">🤖 AI Assistance</h3>
                    <p className="text-slate-400">Real-time buy/sell signals and risk alerts driven by advanced ML models.</p>
                </div>
                <div className="p-6 bg-slate-900 rounded-xl border border-slate-800">
                    <h3 className="text-xl font-bold mb-2">🌍 Global Markets</h3>
                    <p className="text-slate-400">Trade US Stocks, Crypto, and exclusive Casablanca Stock Exchange tickers.</p>
                </div>
                <div className="p-6 bg-slate-900 rounded-xl border border-slate-800">
                    <h3 className="text-xl font-bold mb-2">📰 News Hub</h3>
                    <p className="text-slate-400">Integrated economic calendar to stay ahead of high-impact events.</p>
                </div>
            </div>

            <div className="flex gap-6">
                <Link href="/pricing">
                    <Button size="lg" className="px-8 text-lg">Start Challenge</Button>
                </Link>
                <Link href="/leaderboard">
                    <Button variant="outline" size="lg" className="px-8 text-lg">View Leaderboard</Button>
                </Link>
            </div>
        </div>
    );
}
