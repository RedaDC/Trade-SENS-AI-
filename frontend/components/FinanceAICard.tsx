"use client";
import React from 'react';
import { twMerge } from 'tailwind-merge';

interface AnalysisData {
    decision: {
        recommendation: string;
        confidence: number;
        reasoning: string;
    };
    technical: {
        rsi: { value: number; signal: string };
        macd: { signal: string };
        ema: { alignment: string };
    };
    market_structure: {
        trend: string;
        support_level: number;
        resistance_level: number;
    };
    risk_management: {
        entry_zone: string;
        stop_loss: number | null;
        take_profit: number | null;
        risk_reward_ratio: number | null;
    };
}

interface FinanceAICardProps {
    data: AnalysisData;
    symbol: string;
}

export function FinanceAICard({ data, symbol }: FinanceAICardProps) {
    const { decision, technical, market_structure, risk_management } = data;
    const rec = decision.recommendation.toUpperCase();

    const isBuy = rec === "BUY";
    const isSell = rec === "SELL";

    // Dynamic Styles based on Signal
    const borderColor = isBuy ? "border-emerald-500/40" : isSell ? "border-rose-500/40" : "border-slate-500/40";
    const shadowColor = isBuy ? "shadow-emerald-500/10" : isSell ? "shadow-rose-500/10" : "shadow-slate-500/10";
    const textColor = isBuy ? "text-emerald-400" : isSell ? "text-rose-400" : "text-slate-400";
    const gradient = isBuy
        ? "from-emerald-500/20 to-emerald-900/10"
        : isSell
            ? "from-rose-500/20 to-rose-900/10"
            : "from-slate-700/20 to-slate-900/10";

    return (
        <div className={twMerge(
            "w-full max-w-sm rounded-2xl border backdrop-blur-xl overflow-hidden transition-all duration-500 hover:scale-[1.02]",
            "bg-slate-950/40 shadow-2xl ring-1 ring-white/10",
            borderColor,
            shadowColor
        )}>
            {/* Header section with Signal and Confidence */}
            <div className={twMerge("p-6 bg-gradient-to-br border-b border-white/5", gradient)}>
                <div className="flex justify-between items-start">
                    <div className="flex items-center gap-4">
                        <div className={twMerge(
                            "w-12 h-12 rounded-xl flex items-center justify-center shadow-lg ring-1 ring-white/10 transition-transform duration-700 hover:rotate-6",
                            isBuy ? "bg-emerald-500/30" : isSell ? "bg-rose-500/30" : "bg-slate-500/30"
                        )}>
                            <span className="text-2xl">{isBuy ? "▲" : isSell ? "▼" : "◆"}</span>
                        </div>
                        <div>
                            <p className="text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-0.5">Live Intelligence • {symbol}</p>
                            <h2 className={twMerge("text-3xl font-black tracking-tighter", textColor)}>{rec}</h2>
                        </div>
                    </div>
                    <div className="text-right">
                        <div className="text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-1">Scale</div>
                        <div className="flex items-center gap-2">
                            <div className="w-20 h-2 bg-slate-900/80 rounded-full border border-white/5 overflow-hidden">
                                <div
                                    className={twMerge("h-full transition-all duration-1000", isBuy ? "bg-emerald-500" : isSell ? "bg-rose-500" : "bg-slate-500")}
                                    style={{ width: `${decision.confidence}%` }}
                                ></div>
                            </div>
                            <span className="font-mono text-sm font-bold text-white leading-none">{decision.confidence}%</span>
                        </div>
                    </div>
                </div>
            </div>

            {/* Analysis Content */}
            <div className="p-6 space-y-6">
                <div className="relative">
                    <div className="absolute -left-3 top-0 bottom-0 w-0.5 bg-blue-500/50 rounded-full"></div>
                    <p className="text-sm text-slate-300 leading-relaxed font-medium italic">
                        "{decision.reasoning}"
                    </p>
                </div>

                <div className="grid grid-cols-2 gap-3">
                    <InsightBox label="Trend" value={market_structure.trend} icon="🧭" />
                    <InsightBox label="RSI" value={technical.rsi.value.toFixed(1)} sub={technical.rsi.signal} icon="📈" />
                    <InsightBox label="Support" value={market_structure.support_level.toFixed(2)} icon="🛡️" />
                    <InsightBox label="Resist." value={market_structure.resistance_level.toFixed(2)} icon="🏹" />
                </div>

                {rec !== "WAIT" && (
                    <div className="mt-4 p-4 rounded-xl bg-slate-900/60 border border-white/5 space-y-3">
                        <div className="flex items-center gap-2 text-[10px] font-black text-slate-500 uppercase tracking-widest">
                            <span className="w-1.5 h-1.5 bg-blue-500 rounded-full animate-pulse"></span>
                            Risk Matrix Execution
                        </div>
                        <div className="grid grid-cols-3 gap-4">
                            <ExecutionDetail label="Entry" value={risk_management.entry_zone.split("-")[0].trim()} color="text-sky-400" />
                            <ExecutionDetail label="Stop" value={risk_management.stop_loss?.toString() || "-"} color="text-rose-400" />
                            <ExecutionDetail label="Target" value={risk_management.take_profit?.toString() || "-"} color="text-emerald-400" />
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}

function InsightBox({ label, value, sub, icon }: { label: string, value: string, sub?: string, icon: string }) {
    return (
        <div className="bg-white/5 hover:bg-white/10 transition-colors rounded-xl p-3 border border-white/5 flex flex-col items-center text-center">
            <span className="text-xs mb-1 opacity-50">{icon} {label}</span>
            <span className="text-sm font-bold text-slate-100 truncate w-full">{value}</span>
            {sub && <span className="text-[10px] text-blue-400 font-bold uppercase mt-1">{sub}</span>}
        </div>
    );
}

function ExecutionDetail({ label, value, color }: { label: string, value: string, color: string }) {
    return (
        <div className="flex flex-col gap-0.5">
            <span className="text-[9px] font-bold text-slate-500 uppercase tracking-tighter">{label}</span>
            <span className={twMerge("text-sm font-mono font-bold tracking-tight", color)}>{value}</span>
        </div>
    );
}
