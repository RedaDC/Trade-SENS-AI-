"use client";
import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { placeTrade } from '@/lib/api';

interface AIAnalysisProps {
    symbol: string;
}

export function AITradingAnalysis({ symbol }: AIAnalysisProps) {
    const [analysis, setAnalysis] = useState<any>(null);
    const [loading, setLoading] = useState(false);

    const [executing, setExecuting] = useState(false);

    const fetchAnalysis = async () => {
        setLoading(true);
        try {
            const res = await fetch('/api/v1/tradesense/ai-analysis/analyze', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ symbol, timeframe: '1D' })
            });
            const data = await res.json();
            setAnalysis(data);
        } catch (e) {
            console.error(e);
        }
        setLoading(false);
    };

    const handleExecuteTrade = async () => {
        if (!analysis || !analysis.analysis.decision) return;

        const decision = analysis.analysis.decision;
        const recommendation = decision.recommendation;
        const riskMgmt = analysis.analysis.risk_management;

        if (recommendation === 'WAIT') return;

        setExecuting(true);
        try {
            await placeTrade({
                challenge_id: 1, // Mock
                symbol: analysis.symbol,
                side: recommendation,
                volume: 1.0, // Default volume
                stop_loss: riskMgmt.stop_loss,
                take_profit: riskMgmt.take_profit
            });
            alert(`Trade Executed: ${recommendation} ${analysis.symbol}`);
        } catch (e) {
            console.error(e);
            alert("Failed to execute trade");
        }
        setExecuting(false);
    };

    if (!analysis) {
        return (
            <div className="p-6 bg-slate-900 rounded-lg border border-slate-700">
                <div className="text-center">
                    <h2 className="text-2xl font-bold mb-4 text-white">🤖 AI Trading Analysis</h2>
                    <p className="text-slate-400 mb-6">Get comprehensive AI-powered trading recommendations</p>
                    <Button onClick={fetchAnalysis} disabled={loading} className="bg-blue-600 hover:bg-blue-700">
                        {loading ? 'Analyzing...' : 'Analyze ' + symbol}
                    </Button>
                </div>
            </div>
        );
    }

    const { analysis: a } = analysis;
    const decision = a.decision;
    const riskMgmt = a.risk_management;

    // Decision color
    const decisionColor = decision.recommendation === 'BUY' ? 'text-green-400' :
        decision.recommendation === 'SELL' ? 'text-red-400' : 'text-yellow-400';
    const decisionBg = decision.recommendation === 'BUY' ? 'bg-green-900/30 border-green-700' :
        decision.recommendation === 'SELL' ? 'bg-red-900/30 border-red-700' : 'bg-yellow-900/30 border-yellow-700';

    return (
        <div className="space-y-4">
            {/* DEMO MODE Banner */}
            <div className="bg-yellow-900/30 border border-yellow-700 rounded-lg p-3 text-center">
                <span className="text-yellow-400 font-bold">⚠️ DEMO MODE - EDUCATIONAL PURPOSES ONLY</span>
                <p className="text-yellow-200 text-xs mt-1">This is NOT financial advice. Simulated data for demonstration.</p>
            </div>

            {/* Header */}
            <div className="bg-slate-900 rounded-lg border border-slate-700 p-6">
                <div className="flex justify-between items-start mb-4">
                    <div>
                        <h2 className="text-3xl font-bold text-white">{analysis.symbol}</h2>
                        <p className="text-slate-400">Current Price: <span className="text-white font-mono">${analysis.current_price}</span></p>
                    </div>
                    <Button onClick={fetchAnalysis} size="sm" className="bg-slate-700 hover:bg-slate-600">
                        Refresh Analysis
                    </Button>
                </div>

                {/* Main Decision */}
                <div className={`${decisionBg} border rounded-lg p-6 mb-4`}>
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-slate-300 text-sm mb-1">RECOMMENDATION</p>
                            <h3 className={`text-4xl font-bold ${decisionColor}`}>{decision.recommendation}</h3>
                        </div>
                        <div className="text-right">
                            <p className="text-slate-300 text-sm mb-1">CONFIDENCE</p>
                            <p className="text-3xl font-bold text-white">{decision.confidence}%</p>
                        </div>
                    </div>
                    <p className="text-slate-300 mt-4 italic">{decision.reasoning}</p>

                    {decision.recommendation !== 'WAIT' && (
                        <div className="mt-6 flex justify-end">
                            <Button
                                onClick={handleExecuteTrade}
                                disabled={executing}
                                className={`font-bold text-lg h-12 px-8 ${decision.recommendation === 'BUY'
                                        ? 'bg-green-600 hover:bg-green-700 text-white'
                                        : 'bg-red-600 hover:bg-red-700 text-white'
                                    }`}
                            >
                                {executing ? 'Executing...' : `EXECUTE ${decision.recommendation}`}
                            </Button>
                        </div>
                    )}
                </div>

                {/* Risk Management */}
                {decision.recommendation !== 'WAIT' && (
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
                        <div className="bg-slate-800 p-3 rounded">
                            <p className="text-slate-400 text-xs">Entry Zone</p>
                            <p className="text-white font-mono text-sm">{riskMgmt.entry_zone}</p>
                        </div>
                        <div className="bg-slate-800 p-3 rounded">
                            <p className="text-slate-400 text-xs">Stop Loss</p>
                            <p className="text-red-400 font-mono text-sm">${riskMgmt.stop_loss}</p>
                        </div>
                        <div className="bg-slate-800 p-3 rounded">
                            <p className="text-slate-400 text-xs">Take Profit</p>
                            <p className="text-green-400 font-mono text-sm">${riskMgmt.take_profit}</p>
                        </div>
                        <div className="bg-slate-800 p-3 rounded">
                            <p className="text-slate-400 text-xs">R:R Ratio</p>
                            <p className="text-blue-400 font-bold text-sm">1:{riskMgmt.risk_reward_ratio}</p>
                        </div>
                    </div>
                )}

                {/* Risk Level Badge */}
                <div className="flex gap-2">
                    <span className={`px-3 py-1 rounded text-xs font-bold ${riskMgmt.risk_level === 'Low' ? 'bg-green-900 text-green-300' :
                        riskMgmt.risk_level === 'Medium' ? 'bg-yellow-900 text-yellow-300' :
                            'bg-red-900 text-red-300'
                        }`}>
                        Risk: {riskMgmt.risk_level}
                    </span>
                    <span className="px-3 py-1 rounded text-xs font-bold bg-slate-700 text-slate-300">
                        Position Size: {riskMgmt.position_size}
                    </span>
                </div>
            </div>

            {/* Detailed Analysis Sections */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {/* News & Macro */}
                <div className="bg-slate-900 rounded-lg border border-slate-700 p-4">
                    <h4 className="font-bold text-white mb-3 flex items-center gap-2">
                        📰 News & Macro Analysis
                    </h4>
                    <div className="space-y-2 text-sm">
                        <div className="flex justify-between">
                            <span className="text-slate-400">Impact:</span>
                            <span className={`font-bold ${a.news_macro.impact === 'Bullish' ? 'text-green-400' :
                                a.news_macro.impact === 'Bearish' ? 'text-red-400' : 'text-slate-300'
                                }`}>{a.news_macro.impact}</span>
                        </div>
                        <div>
                            <p className="text-slate-400 mb-1">Key Events:</p>
                            <ul className="list-disc list-inside text-slate-300">
                                {a.news_macro.key_events.map((event: string, i: number) => (
                                    <li key={i}>{event}</li>
                                ))}
                            </ul>
                        </div>
                        <div className="flex justify-between">
                            <span className="text-slate-400">Overreaction Risk:</span>
                            <span className="text-slate-300">{a.news_macro.overreaction_risk}</span>
                        </div>
                    </div>
                </div>

                {/* Market Structure */}
                <div className="bg-slate-900 rounded-lg border border-slate-700 p-4">
                    <h4 className="font-bold text-white mb-3 flex items-center gap-2">
                        📊 Market Structure
                    </h4>
                    <div className="space-y-2 text-sm">
                        <div className="flex justify-between">
                            <span className="text-slate-400">Trend:</span>
                            <span className="font-bold text-white">{a.market_structure.trend}</span>
                        </div>
                        <div className="flex justify-between">
                            <span className="text-slate-400">Strength:</span>
                            <span className="text-slate-300">{a.market_structure.trend_strength}</span>
                        </div>
                        <div className="flex justify-between">
                            <span className="text-slate-400">Support:</span>
                            <span className="text-green-400 font-mono">${a.market_structure.support_level}</span>
                        </div>
                        <div className="flex justify-between">
                            <span className="text-slate-400">Resistance:</span>
                            <span className="text-red-400 font-mono">${a.market_structure.resistance_level}</span>
                        </div>
                    </div>
                </div>

                {/* Technical Indicators */}
                <div className="bg-slate-900 rounded-lg border border-slate-700 p-4">
                    <h4 className="font-bold text-white mb-3 flex items-center gap-2">
                        📈 Technical Indicators
                    </h4>
                    <div className="space-y-3 text-sm">
                        <div>
                            <div className="flex justify-between mb-1">
                                <span className="text-slate-400">RSI (14):</span>
                                <span className="font-bold text-white">{a.technical.rsi.value}</span>
                            </div>
                            <div className="w-full bg-slate-800 rounded-full h-2">
                                <div className="bg-blue-500 h-2 rounded-full" style={{ width: `${a.technical.rsi.value}%` }}></div>
                            </div>
                            <p className="text-xs text-slate-400 mt-1">{a.technical.rsi.signal}</p>
                        </div>
                        <div className="flex justify-between">
                            <span className="text-slate-400">MACD:</span>
                            <span className={`font-bold ${a.technical.macd.signal === 'Bullish' ? 'text-green-400' : 'text-red-400'}`}>
                                {a.technical.macd.signal}
                            </span>
                        </div>
                        <div className="flex justify-between">
                            <span className="text-slate-400">EMA Alignment:</span>
                            <span className="font-bold text-white">{a.technical.ema.alignment}</span>
                        </div>
                        <div className="flex justify-between">
                            <span className="text-slate-400">Volume:</span>
                            <span className="text-slate-300">{a.technical.volume.trend}</span>
                        </div>
                    </div>
                </div>

                {/* Sentiment */}
                <div className="bg-slate-900 rounded-lg border border-slate-700 p-4">
                    <h4 className="font-bold text-white mb-3 flex items-center gap-2">
                        🎭 Market Sentiment
                    </h4>
                    <div className="space-y-2 text-sm">
                        <div className="flex justify-between">
                            <span className="text-slate-400">Environment:</span>
                            <span className="font-bold text-white">{a.sentiment.environment}</span>
                        </div>
                        <div>
                            <div className="flex justify-between mb-1">
                                <span className="text-slate-400">Fear & Greed:</span>
                                <span className="font-bold text-white">{a.sentiment.fear_greed_index}</span>
                            </div>
                            <div className="w-full bg-slate-800 rounded-full h-2">
                                <div className={`h-2 rounded-full ${a.sentiment.fear_greed_index < 40 ? 'bg-red-500' :
                                    a.sentiment.fear_greed_index > 60 ? 'bg-green-500' : 'bg-yellow-500'
                                    }`} style={{ width: `${a.sentiment.fear_greed_index}%` }}></div>
                            </div>
                            <p className="text-xs text-slate-400 mt-1">{a.sentiment.sentiment_label}</p>
                        </div>
                        <div className="flex justify-between">
                            <span className="text-slate-400">Positioning:</span>
                            <span className="text-slate-300">{a.sentiment.positioning}</span>
                        </div>
                    </div>
                </div>
            </div>

            {/* Scenarios */}
            <div className="bg-slate-900 rounded-lg border border-slate-700 p-4">
                <h4 className="font-bold text-white mb-4">🎯 Trade Scenarios</h4>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div className="bg-green-900/20 border border-green-700 rounded p-4">
                        <div className="flex justify-between items-center mb-2">
                            <h5 className="font-bold text-green-400">Bullish Case</h5>
                            <span className="text-2xl font-bold text-green-400">{a.scenarios.bullish.probability}%</span>
                        </div>
                        <p className="text-sm text-slate-300 mb-2">{a.scenarios.bullish.case}</p>
                        <p className="text-xs text-slate-400">Target: <span className="text-green-400 font-mono">${a.scenarios.bullish.target}</span></p>
                    </div>
                    <div className="bg-red-900/20 border border-red-700 rounded p-4">
                        <div className="flex justify-between items-center mb-2">
                            <h5 className="font-bold text-red-400">Bearish Case</h5>
                            <span className="text-2xl font-bold text-red-400">{a.scenarios.bearish.probability}%</span>
                        </div>
                        <p className="text-sm text-slate-300 mb-2">{a.scenarios.bearish.case}</p>
                        <p className="text-xs text-slate-400">Target: <span className="text-red-400 font-mono">${a.scenarios.bearish.target}</span></p>
                    </div>
                    <div className="bg-yellow-900/20 border border-yellow-700 rounded p-4">
                        <div className="flex justify-between items-center mb-2">
                            <h5 className="font-bold text-yellow-400">Wait Case</h5>
                            <span className="text-2xl font-bold text-yellow-400">{a.scenarios.wait.probability}%</span>
                        </div>
                        <p className="text-sm text-slate-300 mb-2">{a.scenarios.wait.case}</p>
                        <p className="text-xs text-slate-400">{a.scenarios.wait.reason}</p>
                    </div>
                </div>
            </div>

            {/* Disclaimer */}
            <div className="bg-red-900/20 border border-red-700 rounded-lg p-4 text-center">
                <p className="text-red-300 text-sm font-bold">⚠️ DISCLAIMER</p>
                <p className="text-red-200 text-xs mt-2">
                    This analysis is for educational purposes only and does NOT constitute financial advice.
                    Trading involves substantial risk of loss. Past performance does not guarantee future results.
                    Always consult a licensed financial advisor before making trading decisions.
                </p>
            </div>
        </div>
    );
}
