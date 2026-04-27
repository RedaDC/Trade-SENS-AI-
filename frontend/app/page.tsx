import { Button } from "@/components/ui/button";
import Link from "next/link";
import { ArrowRight, BarChart, ShieldCheck, Zap } from "lucide-react";

export default function Home() {
    return (
        <div className="flex flex-col min-h-screen">
            {/* Hero Section */}
            <section className="relative pt-32 pb-20 overflow-hidden">
                <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-blue-900/40 via-slate-950 to-slate-950 z-0"></div>
                <div className="absolute top-0 left-0 w-full h-full bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-20 z-0"></div>

                <div className="container mx-auto px-4 relative z-10 text-center">
                    <div className="inline-block mb-4 px-4 py-1.5 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-400 text-sm font-semibold animate-in fade-in slide-in-from-bottom-4">
                        🚀 The Future of Prop Trading is Here
                    </div>
                    <h1 className="text-6xl md:text-8xl font-black tracking-tighter mb-8 text-white drop-shadow-2xl animate-in fade-in slide-in-from-bottom-6 duration-700">
                        Trade <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 via-blue-200 to-emerald-400 animate-gradient-x">Smarter.</span> <br />
                        Get <span className="text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 via-emerald-200 to-teal-400">Funded.</span>
                    </h1>
                    <p className="text-xl md:text-2xl text-slate-400 max-w-3xl mx-auto mb-12 leading-relaxed animate-in fade-in slide-in-from-bottom-8 duration-900">
                        Join the <span className="text-white font-semibold">elite circle</span> of traders using <span className="text-blue-400">Institutional Grade AI</span> and <span className="text-emerald-400">Premium Data</span> to conquer the markets.
                    </p>

                    <div className="flex flex-col md:flex-row gap-6 justify-center animate-in fade-in slide-in-from-bottom-10 duration-1000">
                        <Link href="/pricing">
                            <Button size="lg" className="h-14 px-10 text-lg rounded-full bg-blue-600 hover:bg-blue-500 shadow-xl shadow-blue-600/20 hover:scale-105 transition-all">
                                Start Challenge <ArrowRight className="ml-2 w-5 h-5" />
                            </Button>
                        </Link>
                        <Link href="/dashboard">
                            <Button variant="outline" size="lg" className="h-14 px-10 text-lg rounded-full border-slate-700 text-slate-300 hover:bg-slate-800 hover:text-white transition-all">
                                View Dashboard
                            </Button>
                        </Link>
                    </div>
                </div>
            </section>

            {/* Features Grid (Bento Box) */}
            <section className="py-24 bg-slate-950 relative z-10">
                <div className="container mx-auto px-4 max-w-6xl">
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                        {/* Large Card */}
                        {/* Large Card */}
                        <div className="md:col-span-2 p-10 bg-slate-900/60 backdrop-blur-md rounded-3xl border border-white/10 hover:border-blue-500/50 transition-all group relative overflow-hidden shadow-2xl ring-1 ring-white/5">
                            <div className="absolute top-0 right-0 w-64 h-64 bg-blue-600/10 rounded-full blur-3xl group-hover:bg-blue-600/20 transition-all"></div>
                            <div className="relative z-10">
                                <div className="w-12 h-12 bg-blue-600/20 rounded-xl flex items-center justify-center mb-6 text-blue-400 shadow-lg shadow-blue-500/20">
                                    <Zap className="w-6 h-6" />
                                </div>
                                <h3 className="text-3xl font-bold mb-4 text-white">AI-Powered Signals</h3>
                                <p className="text-slate-400 text-lg leading-relaxed max-w-md">
                                    Stop guessing. Our <strong>Elite GPT-4o</strong> models analyze market structure, news sentiment, and technical indicators to give you high-probability trade setups in real-time.
                                </p>
                            </div>
                        </div>

                        {/* Tall Card */}
                        {/* Tall Card */}
                        <div className="md:row-span-2 p-10 bg-slate-900/60 backdrop-blur-md rounded-3xl border border-white/10 hover:border-emerald-500/50 transition-all group relative overflow-hidden shadow-2xl ring-1 ring-white/5">
                            <div className="absolute bottom-0 left-0 w-full h-1/2 bg-emerald-600/5 rounded-full blur-3xl"></div>
                            <div className="relative z-10 flex flex-col h-full">
                                <div className="w-12 h-12 bg-emerald-600/20 rounded-xl flex items-center justify-center mb-6 text-emerald-400 shadow-lg shadow-emerald-500/20">
                                    <BarChart className="w-6 h-6" />
                                </div>
                                <h3 className="text-3xl font-bold mb-4 text-white">Global Markets</h3>
                                <p className="text-slate-400 text-lg leading-relaxed mb-8">
                                    Trade the world. Access robust data for:
                                </p>
                                <ul className="space-y-4 font-semibold text-slate-300">
                                    <li className="flex items-center gap-3"><span className="w-2 h-2 rounded-full bg-emerald-400 shadow-[0_0_10px_rgba(52,211,153,0.5)]"></span> US Stocks (Nasdaq/NYSE)</li>
                                    <li className="flex items-center gap-3"><span className="w-2 h-2 rounded-full bg-blue-400 shadow-[0_0_10px_rgba(96,165,250,0.5)]"></span> Forex Majors</li>
                                    <li className="flex items-center gap-3"><span className="w-2 h-2 rounded-full bg-purple-400 shadow-[0_0_10px_rgba(192,132,252,0.5)]"></span> Crypto (BTC/ETH)</li>
                                    <li className="flex items-center gap-3"><span className="w-2 h-2 rounded-full bg-red-400 shadow-[0_0_10px_rgba(248,113,113,0.5)]"></span> Casablanca Exchange</li>
                                </ul>
                            </div>
                        </div>

                        {/* Standard Card */}
                        {/* Standard Card */}
                        <div className="p-10 bg-slate-900/60 backdrop-blur-md rounded-3xl border border-white/10 hover:border-purple-500/50 transition-all group shadow-2xl ring-1 ring-white/5">
                            <div className="w-12 h-12 bg-purple-600/20 rounded-xl flex items-center justify-center mb-6 text-purple-400 shadow-lg shadow-purple-500/20">
                                <ShieldCheck className="w-6 h-6" />
                            </div>
                            <h3 className="text-2xl font-bold mb-3 text-white">Risk Management</h3>
                            <p className="text-slate-400">
                                Automatic draw-down protection and risk alerts to keep you in the game.
                            </p>
                        </div>

                        {/* Standard Card */}
                        {/* Standard Card */}
                        <div className="p-10 bg-slate-900/60 backdrop-blur-md rounded-3xl border border-white/10 hover:border-orange-500/50 transition-all group shadow-2xl ring-1 ring-white/5">
                            <div className="w-12 h-12 bg-orange-600/20 rounded-xl flex items-center justify-center mb-6 text-orange-400 shadow-lg shadow-orange-500/20">
                                <Zap className="w-6 h-6" />
                            </div>
                            <h3 className="text-2xl font-bold mb-3 text-white">Instant Funding</h3>
                            <p className="text-slate-400">
                                Pass the challenge and get funded up to <strong>$100,000</strong> instantly.
                            </p>
                        </div>
                    </div>
                </div>
            </section>
        </div>
    );
}
