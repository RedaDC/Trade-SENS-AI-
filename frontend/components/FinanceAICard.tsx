"use client";
import React from 'react';
import clsx from 'clsx';
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

    // Dynamic Colors based on Signal
    const borderColor = isBuy ? "border-green-500/50" : isSell ? "border-red-500/50" : "border-slate-500/50";
    const bgColor = isBuy ? "bg-green-500/10" : isSell ? "bg-red-500/10" : "bg-slate-500/10";
    const textColor = isBuy ? "text-green-400" : isSell ? "text-red-400" : "text-slate-400";
    const badgeColor = isBuy ? "bg-green-500 text-white" : isSell ? "bg-red-500 text-white" : "bg-slate-600 text-slate-200";

    return (
        <div className={twMerge("w-full max-w-sm rounded-xl border backdrop-blur-md overflow-hidden transition-all duration-300 hover:shadow-lg", "bg-slate-900/80", borderColor)}>

            {/* Header: Signal & Confidence */}
            <div className={twMerge("p-4 flex justify-between items-center border-b border-white/5", bgColor)}>
                <div>
                    <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider">AI Analysis • {symbol}</h4>
                    <div className={twMerge("text-2xl font-black mt-1", textColor)}>{rec}</div>
                </div>
                <div className="flex flex-col items-end gap-1">
                    <span className="text-xs text-slate-400">Confidence</span>
                    <div className="flex items-center gap-2">
                        <span className="font-bold text-white">{decision.confidence}%</span>
                        {/* Circular Progress or Bar */}
                        <div className="w-12 h-2 bg-slate-700 rounded-full overflow-hidden">
                            <div className={twMerge("h-full rounded-full", isBuy ? "bg-green-500" : isSell ? "bg-red-500" : "bg-slate-500")} style={{ width: `${decision.confidence}%` }}></div>
                        </div>
                    </div>
                </div>
            </div>

            {/* Content Body */}
            <div className="p-4 space-y-4">

                {/* Reasoning */}
                <div className="text-sm text-slate-300 italic leading-relaxed border-l-2 border-slate-600 pl-3">
                    "{decision.reasoning}"
                </div>

                {/* Technical Grid */}
                <div className="grid grid-cols-2 gap-2 text-xs">
                    <StatBox label="Trend" value={market_structure.trend} />
                    <StatBox label="RSI (14)" value={technical.rsi.value.toString()} sub={technical.rsi.signal} />
                    <StatBox label="Support" value={market_structure.support_level.toFixed(2)} />
                    <StatBox label="Resistance" value={market_structure.resistance_level.toFixed(2)} />
                </div>

                {/* Risk Management Section (Only if actionable) */}
                {rec !== "WAIT" && (
                    <div className="bg-slate-800/50 rounded-lg p-3 space-y-2 border border-slate-700/50">
                        <div className="text-xs font-bold text-slate-400 uppercase mb-1">Risk Management</div>
                        <div className="grid grid-cols-3 gap-2 text-center">
                            <RiskBox label="Entry" value={risk_management.entry_zone.split("-")[0].trim()} color="text-yellow-400" />
                            <RiskBox label="Stop Loss" value={risk_management.stop_loss?.toString() || "-"} color="text-red-400" />
                            <RiskBox label="Target" value={risk_management.take_profit?.toString() || "-"} color="text-green-400" />
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}

function StatBox({ label, value, sub }: { label: string, value: string, sub?: string }) {
    return (
        <div className="bg-slate-800/50 rounded p-2 flex flex-col items-center justify-center border border-slate-700/30">
            <span className="text-slate-500 mb-1">{label}</span>
            <span className="font-mono font-bold text-slate-200">{value}</span>
            {sub && <span className="text-[10px] text-slate-400">{sub}</span>}
        </div>
    )
}

function RiskBox({ label, value, color }: { label: string, value: string, color: string }) {
    return (
        <div className="flex flex-col">
            <span className="text-[10px] text-slate-500">{label}</span>
            <span className={clsx("font-mono font-bold text-sm", color)}>{value}</span>
        </div>
    )
}
