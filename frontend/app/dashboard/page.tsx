"use client";
import { useEffect, useState } from 'react';
import { Button } from '@/components/ui/button';
import { ChartComponent } from '@/components/ChartComponent';
import { AIAnalysisPanel } from '@/components/AIAnalysisPanel';
import { MoroccanStocksList } from '@/components/MoroccanStocksList';
import { FinanceAIWidget } from '@/components/FinanceAIWidget';
import { AITradingAnalysis } from '@/components/AITradingAnalysis';
import { fetchMarketData, fetchNews, fetchCalendar, placeTrade } from '@/lib/api';

export default function Dashboard() {
    type ExecutionEntry = {
        time: string;
        source: 'AI' | 'Manual';
        side: 'BUY' | 'SELL';
        symbol: string;
        price?: number;
        explanation: string;
    };
    const [price, setPrice] = useState<number>(0);
    const [symbol, setSymbol] = useState('EURUSD');
    const [autoTrade, setAutoTrade] = useState(false);
    const [toasts, setToasts] = useState<string[]>([]);
    const [news, setNews] = useState<any[]>([]);
    const [executions, setExecutions] = useState<ExecutionEntry[]>([]);
    const [activeTab, setActiveTab] = useState<'trading' | 'ai-analysis'>('trading');

    useEffect(() => {
        // Auto-trading simulation
        let tradeInterval: any;

        if (autoTrade) {
            tradeInterval = setInterval(() => {
                // Randomly decide to place a trade
                if (Math.random() > 0.7) {
                    const action = Math.random() > 0.5 ? "BUY" : "SELL";
                    const msg = `AI Placed ${action} order on ${symbol} @ ${price || 'MARKET'}`;
                    setToasts(prev => [msg, ...prev].slice(0, 5));

                    const entry: ExecutionEntry = {
                        time: new Date().toLocaleTimeString(),
                        source: 'AI',
                        side: action as 'BUY' | 'SELL',
                        symbol,
                        price: price || undefined,
                        explanation: action === 'BUY'
                            ? 'AI detected bullish momentum near support; executed BUY.'
                            : 'AI detected bearish momentum near resistance; executed SELL.'
                    };
                    setExecutions(prev => [entry, ...prev].slice(0, 20));
                }
            }, 3000); // Check every 3 seconds
        }

        return () => clearInterval(tradeInterval);
    }, [autoTrade, symbol, price]);

    const handleTrade = async (side: "BUY" | "SELL") => {
        const trade = {
            challenge_id: 1, // Mock challenge ID
            symbol: symbol,
            side: side,
            volume: 1.0
        };

        try {
            await placeTrade(trade);
            const msg = `Manual ${side} order placed on ${symbol} @ ${price}`;
            setToasts(prev => [msg, ...prev].slice(0, 5));

            const entry: ExecutionEntry = {
                time: new Date().toLocaleTimeString(),
                source: 'Manual',
                side,
                symbol,
                price: price || undefined,
                explanation: 'User triggered execution from Trading Controls.'
            };
            setExecutions(prev => [entry, ...prev].slice(0, 20));
        } catch (e) {
            console.error(e);
            setToasts(prev => ["Failed to place trade", ...prev].slice(0, 5));
        }
    };

    useEffect(() => {
        const interval = setInterval(() => {
            fetchMarketData(symbol).then(data => {
                if (data && data.price) {
                    setPrice(data.price);
                }
            });
        }, 5000); // Polling every 5s

        return () => clearInterval(interval);
    }, [symbol]);

    useEffect(() => {
        // Fetch economic calendar relevant to the symbol
        fetchCalendar(symbol).then((data: any[]) => {
            if (data && data.length > 0) {
                setNews(data);
            } else {
                // If no calendar events, fallback to general news headlines
                fetchNews().then(newsData => {
                    setNews((newsData || []).slice(0, 8));
                });
            }
        }).catch(() => {
            // Fallback to general news on error
            fetchNews().then(newsData => {
                setNews((newsData || []).slice(0, 8));
            });
        });
    }, [symbol]); // Re-fetch when symbol changes

    return (
        <div className="flex h-[calc(100vh-80px)]">
            {/* Sidebar: Asset Selector */}
            <div className="w-64 bg-slate-900 border-r border-slate-800 p-4 flex flex-col">
                <h3 className="text-slate-400 font-bold mb-4">Market Watch</h3>
                <div className="space-y-2 flex-shrink-0">
                    {['EURUSD', 'GBPUSD', 'GOLD', 'TSLA', 'AAPL', 'BTCUSD'].map(s => (
                        <div key={s}
                            onClick={() => setSymbol(s)}
                            className={`p-3 rounded cursor-pointer ${symbol === s ? 'bg-blue-900' : 'hover:bg-slate-800'}`}>
                            {s}
                        </div>
                    ))}
                </div>

                {/* Separator */}
                <div className="h-px bg-slate-800 my-4 flex-shrink-0"></div>

                {/* Moroccan Stocks Panel */}
                <MoroccanStocksList currentSymbol={symbol} onSelect={setSymbol} />
            </div>

            {/* Main Content */}
            <div className="flex-1 flex flex-col">
                {/* Header */}
                <div className="h-16 border-b border-slate-800 flex items-center justify-between px-6 bg-slate-900">
                    <div className="flex gap-4">
                        <button
                            onClick={() => setActiveTab('trading')}
                            className={`px-4 py-2 rounded font-semibold transition-colors ${activeTab === 'trading'
                                ? 'bg-blue-600 text-white'
                                : 'bg-slate-800 text-slate-400 hover:bg-slate-700'
                                }`}
                        >
                            📊 Trading
                        </button>
                        <button
                            onClick={() => setActiveTab('ai-analysis')}
                            className={`px-4 py-2 rounded font-semibold transition-colors ${activeTab === 'ai-analysis'
                                ? 'bg-blue-600 text-white'
                                : 'bg-slate-800 text-slate-400 hover:bg-slate-700'
                                }`}
                        >
                            🤖 AI Analysis
                        </button>
                    </div>
                    <h2 className="text-xl font-bold">{symbol}</h2>
                    <div className="text-2xl font-mono text-emerald-400">
                        {price ? price.toFixed(5) : 'Loading...'}
                    </div>
                </div>

                {/* Toast Container */}
                <div className="absolute top-20 right-6 z-50 flex flex-col gap-2 pointer-events-none">
                    {toasts.map((t, i) => (
                        <div key={i} className="bg-slate-800 border border-emerald-500/50 text-emerald-400 px-4 py-2 rounded shadow-lg animate-in fade-in slide-in-from-right-5">
                            🤖 {t}
                        </div>
                    ))}
                </div>

                {/* Chart Area */}
                {activeTab === 'trading' ? (
                    <>
                        <div className="flex-1 bg-black relative flex items-center justify-center border-b border-slate-800 overflow-hidden">
                            <ChartComponent symbol={symbol} theme="dark" />
                        </div>

                        {/* Bottom Panel: Controls & Signals */}
                        <div className="h-64 bg-slate-900 p-6 flex gap-6">

                            {/* Trading Controls */}
                            <div className="w-1/3 flex flex-col gap-4">
                                <div className="flex gap-4">
                                    <Button
                                        className="flex-1 bg-red-600 hover:bg-red-700 h-16 text-xl"
                                        onClick={() => handleTrade("SELL")}
                                    >
                                        SELL
                                    </Button>
                                    <Button
                                        className="flex-1 bg-emerald-600 hover:bg-emerald-700 h-16 text-xl"
                                        onClick={() => handleTrade("BUY")}
                                    >
                                        BUY
                                    </Button>
                                </div>
                                <div className="flex justify-between text-slate-400 text-sm">
                                    <span>Balance: $10,000.00</span>
                                    <span>Equity: $10,000.00</span>
                                </div>
                            </div>

                            {/* AI Signals */}
                            <div className="flex-1 bg-slate-800 rounded p-4 border border-slate-700 relative overflow-hidden flex flex-col">
                                <div className="flex justify-between items-center mb-4">
                                    <h4 className="font-bold text-blue-400">✨ TradeSense AI</h4>
                                    <div className="flex items-center gap-2">
                                        <span className={`text-xs font-bold ${autoTrade ? 'text-emerald-400 animate-pulse' : 'text-slate-500'}`}>
                                            {autoTrade ? 'AUTO-TRADING ACTIVE' : 'AUTO-TRADING OFF'}
                                        </span>
                                        <label className="relative inline-flex items-center cursor-pointer">
                                            <input type="checkbox" className="sr-only peer" checked={autoTrade} onChange={(e) => setAutoTrade(e.target.checked)} />
                                            <div className="w-11 h-6 bg-slate-700 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-800 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-emerald-600"></div>
                                        </label>
                                    </div>
                                </div>

                                <div className="flex-1 overflow-hidden">
                                    <AIAnalysisPanel symbol={symbol} />
                                </div>
                            </div>

                            {/* Economic Calendar */}
                            <div className="w-1/3 bg-slate-800 rounded p-4 border border-slate-700 overflow-y-auto">
                                <h4 className="font-bold text-slate-300 mb-2">Economic Calendar</h4>
                                {news.length === 0 ? (
                                    <p className="text-slate-500 text-xs">Loading calendar...</p>
                                ) : (
                                    <ul className="text-xs space-y-2">
                                        {news.map((n, i) => (
                                            <li key={i} className={`flex justify-between items-center ${n.impact === 'HIGH' ? 'text-red-400' :
                                                n.impact === 'MEDIUM' ? 'text-yellow-400' :
                                                    'text-slate-400'
                                                }`}>
                                                <div className="flex flex-col">
                                                    <span className="font-bold flex items-center gap-2">
                                                        <span>{n.time}</span>
                                                        {n.currency && (
                                                            <span className="text-[10px] px-2 py-0.5 rounded bg-slate-900 text-slate-300 border border-slate-700">{n.currency}</span>
                                                        )}
                                                    </span>
                                                    <span className="truncate max-w-[180px]">{n.title}</span>
                                                </div>
                                                <div className="text-right">
                                                    <span className="block font-bold">{n.impact}</span>
                                                    {n.actual && <span className="text-slate-500">{n.actual}{n.forecast ? ` vs ${n.forecast}` : ''}</span>}
                                                </div>
                                            </li>
                                        ))}
                                    </ul>
                                )}
                            </div>
                        </div>
                    </>
                ) : (
                    <div className="flex-1 overflow-y-auto p-6 bg-black">
                        <AITradingAnalysis symbol={symbol} />
                    </div>
                )}
                <FinanceAIWidget symbol={symbol} />
            </div>
        </div>
    );
}
