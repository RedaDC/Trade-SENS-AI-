"use client";
import { useEffect, useState } from 'react';
import { Button } from '@/components/ui/button';
import { OPCVMChart } from '@/components/OPCVMChart';
import { AIAnalysisPanel } from '@/components/AIAnalysisPanel';
import { FinanceAIWidget } from '@/components/FinanceAIWidget';
import { fetchMarketData } from '@/lib/api';

const OPCVM_FUNDS = [
    { symbol: 'OPCVM_ATTIJARI_DIV', name: 'Attijari Diversifié' },
    { symbol: 'OPCVM_BMCE_ACTIONS', name: 'BMCE Capital Actions' },
    { symbol: 'OPCVM_WAFA_OBLIG', name: 'WafaGestion Obligataire' },
    { symbol: 'OPCVM_CDG_MONETAIRE', name: 'CDG Capital Monétaire' }
];

export default function OPCVMPage() {
    const [price, setPrice] = useState<number>(0);
    const [symbol, setSymbol] = useState(OPCVM_FUNDS[0].symbol);
    const [toasts, setToasts] = useState<string[]>([]);

    // Simple polling for simulated NAV (Net Asset Value / Valeur Liquidative)
    useEffect(() => {
        const interval = setInterval(() => {
            fetchMarketData(symbol).then(data => {
                if (data && data.price) {
                    setPrice(data.price);
                }
            });
        }, 8000); // Polling every 8s for lower volatility funds

        // Initial fetch
        fetchMarketData(symbol).then(data => {
            if (data && data.price) {
                setPrice(data.price);
            }
        });

        return () => clearInterval(interval);
    }, [symbol]);

    return (
        <div className="flex h-[calc(100vh-80px)]">
            {/* Sidebar: Fund Selector */}
            <div className="w-80 bg-slate-900 border-r border-slate-800 p-4 flex flex-col">
                <h3 className="text-slate-400 font-bold mb-4">Fonds OPCVM Marocains</h3>
                <div className="space-y-2 flex-shrink-0">
                    {OPCVM_FUNDS.map(fund => (
                        <div key={fund.symbol}
                            onClick={() => setSymbol(fund.symbol)}
                            className={`p-3 rounded cursor-pointer transition-colors ${symbol === fund.symbol ? 'bg-blue-900 border border-blue-500/30' : 'bg-slate-800/50 hover:bg-slate-800'}`}>
                            <div className="font-bold text-sm text-slate-200">{fund.name}</div>
                            <div className="text-xs text-slate-500 mt-1">{fund.symbol.replace('OPCVM_', '')}</div>
                        </div>
                    ))}
                </div>

                <div className="mt-8 p-4 bg-blue-900/20 rounded border border-blue-500/20">
                    <h4 className="text-sm font-bold text-blue-400 mb-2">ℹ️ Note sur l'IA</h4>
                    <p className="text-xs text-slate-400 leading-relaxed">
                        Les recommandations pour les OPCVM se basent sur l'analyse macro-économique marocaine, les décisions de Bank Al-Maghrib et la tendance des rendements.
                    </p>
                </div>
            </div>

            {/* Main Content */}
            <div className="flex-1 flex flex-col overflow-hidden">
                {/* Header */}
                <div className="h-20 border-b border-slate-800 flex items-center justify-between px-8 bg-slate-900">
                    <div>
                        <h2 className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-emerald-400 text-transparent bg-clip-text">
                            {OPCVM_FUNDS.find(f => f.symbol === symbol)?.name}
                        </h2>
                        <div className="text-sm text-slate-500 mt-1">Valeur Liquidative (MAD)</div>
                    </div>
                    <div className="text-3xl font-mono text-emerald-400 font-bold">
                        {price ? price.toFixed(2) : 'Loading...'}
                        <span className="text-sm text-slate-500 ml-2">MAD</span>
                    </div>
                </div>

                {/* Content Split */}
                <div className="flex-1 flex flex-col lg:flex-row overflow-hidden">
                    {/* Left: Chart */}
                    <div className="flex-[2] bg-black relative flex flex-col border-r border-slate-800 overflow-hidden">
                        <div className="p-4 bg-slate-900 border-b border-slate-800">
                            <h3 className="font-bold text-slate-300">Historique de Performance</h3>
                        </div>
                        <div className="flex-1 relative">
                            {/* Uses the custom chart component for simulated data */}
                            <OPCVMChart symbol={symbol} theme="dark" />
                        </div>
                    </div>

                    {/* Right: AI Analysis Panel */}
                    <div className="flex-1 bg-slate-900 flex flex-col overflow-hidden border-l border-white/5">
                        <div className="p-4 bg-slate-800 border-b border-slate-700 flex justify-between items-center">
                            <h4 className="font-bold text-blue-400 flex items-center gap-2">
                                <span>🧠</span> Analyse IA OPCVM
                            </h4>
                        </div>

                        <div className="flex-1 overflow-y-auto p-2">
                            {/* Reuses the AI Analysis Panel adapted with the dynamic reasons from the backend */}
                            <AIAnalysisPanel symbol={symbol} />
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
