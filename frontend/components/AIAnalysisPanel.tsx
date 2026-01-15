"use client";
import { useEffect, useState } from 'react';
import { fetchAnalysis } from '@/lib/api';

type TradeSetup = {
    asset: string;
    bias: "LONG" | "SHORT";
    entry: number;
    stop_loss: number;
    take_profit: number[];
    rr_ratio: number;
    confidence: string;
    duration: string;
};

type AnalysisReport = {
    market_summary: string;
    regime: string;
    news_driver: string;
    trade_setup: TradeSetup;
    risk_assessment: string;
    entry_logic: string;
};

export const AIAnalysisPanel = ({ symbol }: { symbol: string }) => {
    const [report, setReport] = useState<AnalysisReport | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        setLoading(true);
        // In real app, pass symbol to fetchAnalysis
        fetchAnalysis(symbol).then(data => {
            setReport(data);
            setLoading(false);
        });
    }, [symbol]);

    if (loading) return <div className="p-4 text-slate-400 animate-pulse">Analyzing Market Structure...</div>;
    if (!report) return <div className="p-4 text-slate-400">Analysis Unavailable</div>;

    const isLong = report.trade_setup.bias === 'LONG';
    const biasColor = isLong ? 'text-emerald-400' : 'text-red-400';
    const bgColor = isLong ? 'bg-emerald-900/20' : 'bg-red-900/20';
    const borderColor = isLong ? 'border-emerald-500/30' : 'border-red-500/30';

    return (
        <div className="flex flex-col h-full overflow-y-auto pr-2 gap-4">
            {/* Header / Regime */}
            <div className="bg-slate-800 p-3 rounded border border-slate-700">
                <div className="text-xs text-slate-500 uppercase font-bold mb-1">Market Regime</div>
                <div className="text-sm font-medium text-blue-300">{report.regime}</div>
            </div>

            {/* Trade Idea Card */}
            <div className={`p-4 rounded border ${borderColor} ${bgColor} relative overflow-hidden`}>
                <div className="absolute top-0 right-0 p-2 opacity-10">
                    <span className="text-6xl font-black">{report.trade_setup.bias}</span>
                </div>

                <h4 className={`text-lg font-bold ${biasColor} mb-2 flex items-center gap-2`}>
                    {report.trade_setup.bias} {report.trade_setup.asset}
                    <span className="text-xs font-normal text-slate-400 border border-slate-600 px-1 rounded">{report.trade_setup.duration}</span>
                </h4>

                <div className="grid grid-cols-2 gap-4 text-sm mb-4">
                    <div>
                        <div className="text-slate-500 text-xs">Entry Zone</div>
                        <div className="font-mono text-white">{report.trade_setup.entry}</div>
                    </div>
                    <div>
                        <div className="text-slate-500 text-xs">Stop Loss</div>
                        <div className="font-mono text-red-300">{report.trade_setup.stop_loss}</div>
                    </div>
                </div>

                <div className="space-y-1 mb-4">
                    <div className="text-slate-500 text-xs">Take Profit Targets</div>
                    <div className="flex gap-2">
                        {report.trade_setup.take_profit.map((tp, i) => (
                            <span key={i} className="font-mono text-emerald-300 bg-emerald-950/50 px-2 py-0.5 rounded border border-emerald-900 text-xs">
                                TP{i + 1}: {tp}
                            </span>
                        ))}
                    </div>
                </div>

                <div className="text-xs border-t border-slate-700/50 pt-3 mt-3">
                    <span className="text-slate-400 font-bold">Logic: </span>
                    <span className="text-slate-300">{report.entry_logic}</span>
                </div>
            </div>

            {/* Risk & News */}
            <div className="space-y-3">
                <div className="bg-slate-800 p-3 rounded border border-slate-700">
                    <div className="text-xs text-slate-500 uppercase font-bold mb-1">⚠️ Risk Assessment</div>
                    <p className="text-xs text-slate-300 leading-relaxed">{report.risk_assessment}</p>
                </div>

                <div className="bg-slate-800 p-3 rounded border border-slate-700">
                    <div className="text-xs text-slate-500 uppercase font-bold mb-1">📰 Key Driver</div>
                    <p className="text-xs text-slate-300 leading-relaxed">{report.news_driver}</p>
                </div>
            </div>

            <div className="text-[10px] text-center text-slate-600 mt-2">
                Confidence Score: {report.trade_setup.confidence} • RR: 1:{report.trade_setup.rr_ratio}
            </div>
        </div>
    );
};
