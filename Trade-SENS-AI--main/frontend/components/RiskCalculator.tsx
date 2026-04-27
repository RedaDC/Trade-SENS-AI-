"use client";
import { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';

interface RiskCalculatorProps {
    symbol: string;
    currentPrice: number;
    suggestedSL?: number;
}

export function RiskCalculator({ symbol, currentPrice, suggestedSL }: RiskCalculatorProps) {
    const [balance, setBalance] = useState<number>(10000);
    const [riskPercent, setRiskPercent] = useState<number>(1);
    const [stopLoss, setStopLoss] = useState<number>(suggestedSL || currentPrice * 0.99);

    const [positionSize, setPositionSize] = useState<number>(0);
    const [riskAmount, setRiskAmount] = useState<number>(0);

    useEffect(() => {
        if (suggestedSL) setStopLoss(suggestedSL);
    }, [suggestedSL]);

    useEffect(() => {
        const calculate = () => {
            const riskAmt = balance * (riskPercent / 100);
            const priceDiff = Math.abs(currentPrice - stopLoss);

            if (priceDiff > 0) {
                const size = riskAmt / priceDiff;
                setPositionSize(Number(size.toFixed(4)));
                setRiskAmount(Number(riskAmt.toFixed(2)));
            }
        };
        calculate();
    }, [balance, riskPercent, stopLoss, currentPrice]);

    return (
        <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-4 backdrop-blur-md">
            <h3 className="text-blue-400 font-bold mb-4 flex items-center gap-2">
                <span className="text-lg">⚖️</span> Risk & Position Calculator
            </h3>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-4">
                    <div className="space-y-2">
                        <Label className="text-slate-400 text-xs uppercase">Account Balance ($)</Label>
                        <Input
                            type="number"
                            value={balance}
                            onChange={(e: any) => setBalance(Number(e.target.value))}
                            className="bg-slate-950 border-slate-700 text-white"
                        />
                    </div>
                    <div className="space-y-2">
                        <Label className="text-slate-400 text-xs uppercase">Risk Percentage (%)</Label>
                        <Input
                            type="number"
                            value={riskPercent}
                            onChange={(e: any) => setRiskPercent(Number(e.target.value))}
                            className="bg-slate-950 border-slate-700 text-white"
                        />
                    </div>
                    <div className="space-y-2">
                        <Label className="text-slate-400 text-xs uppercase">Stop Loss Price</Label>
                        <Input
                            type="number"
                            value={stopLoss}
                            step="0.0001"
                            onChange={(e: any) => setStopLoss(Number(e.target.value))}
                            className="bg-slate-950 border-slate-700 text-white"
                        />
                        <p className="text-[10px] text-slate-500">Current: {currentPrice.toFixed(4)}</p>
                    </div>
                </div>

                <div className="bg-blue-600/10 border border-blue-500/20 rounded-lg p-4 flex flex-col justify-center items-center text-center">
                    <div className="mb-4">
                        <p className="text-slate-400 text-xs uppercase mb-1">Position Size ({symbol.split('.')[0]})</p>
                        <p className="text-3xl font-black text-white">{positionSize}</p>
                        <p className="text-[10px] text-blue-300 mt-1">Units / Lots</p>
                    </div>
                    <div className="w-full h-px bg-slate-800 my-2" />
                    <div>
                        <p className="text-slate-400 text-xs uppercase mb-1">Risk Amount</p>
                        <p className="text-xl font-bold text-red-400">-${riskAmount}</p>
                    </div>
                </div>
            </div>

            <div className="mt-4 p-2 bg-slate-800/30 rounded text-[10px] text-slate-500 italic">
                * Based on direct price difference. Does not account for leverage or specific broker contract sizes (e.g., 1 lot = 100,000 for Forex).
            </div>
        </div>
    );
}
