import Link from 'next/link';
import { Button } from './ui/button';

export default function Navbar() {
    return (
        <nav className="sticky top-0 z-40 flex items-center justify-between p-6 bg-slate-900/80 backdrop-blur-md border-b border-white/5 supports-[backdrop-filter]:bg-slate-900/50">
            <div className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-emerald-400 text-transparent bg-clip-text">
                TradeSense AI
            </div>
            <div className="flex gap-6">
                <Link href="/" className="hover:text-blue-400 transition">Home</Link>
                <Link href="/pricing" className="hover:text-blue-400 transition">Pricing</Link>
                <Link href="/news" className="hover:text-blue-400 transition">News</Link>
                <Link href="/leaderboard" className="hover:text-blue-400 transition">Leaderboard</Link>
                <Link href="/dashboard" className="hover:text-blue-400 transition">Dashboard</Link>
            </div>
            <div className="flex gap-4">
                <Link href="/login">
                    <Button variant="ghost">Login</Button>
                </Link>
                <Link href="/pricing">
                    <Button>Get Funded</Button>
                </Link>
            </div>
        </nav>
    );
}
