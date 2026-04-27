"use client";
import React, { useEffect, useState } from 'react';
import { fetchOHLCV } from '@/lib/api';
import {
    LineChart,
    Line,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    ResponsiveContainer
} from 'recharts';

type OHLCV = {
    time: string;
    open: number;
    high: number;
    low: number;
    close: number;
    volume: number;
};

export const OPCVMChart = React.memo(function OPCVMChart({
    symbol = "OPCVM_ATTIJARI_DIV",
    theme = "dark"
}: {
    symbol?: string;
    theme?: "light" | "dark";
}) {
    const [data, setData] = useState<OHLCV[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        setLoading(true);
        fetchOHLCV(symbol).then(historicalData => {
            // Reformat data for recharts if needed, or just use it directly
            // `fetchOHLCV` returns an array of objects with {time, close, ...}
            setData(historicalData || []);
            setLoading(false);
        }).catch(err => {
            console.error("Failed to load OPCVM chart data", err);
            setLoading(false);
        });
    }, [symbol]);

    if (loading) {
        return (
            <div className="flex items-center justify-center h-full w-full text-slate-500 animate-pulse">
                Chargement de l'historique du fonds...
            </div>
        );
    }

    if (data.length === 0) {
        return (
            <div className="flex items-center justify-center h-full w-full text-slate-500">
                Aucune donnée disponible pour {symbol}
            </div>
        );
    }

    // Calculate dynamic Y-axis domain to make the subtle fund movements visible
    const minClose = Math.min(...data.map(d => d.close));
    const maxClose = Math.max(...data.map(d => d.close));
    const padding = (maxClose - minClose) * 0.1 || minClose * 0.01;

    // Custom Tooltip
    const CustomTooltip = ({ active, payload, label }: any) => {
        if (active && payload && payload.length) {
            return (
                <div className="bg-slate-800 border border-slate-700 p-3 rounded shadow-xl">
                    <p className="text-slate-400 text-xs mb-1">{label}</p>
                    <p className="text-emerald-400 font-bold">
                        NAV : {payload[0].value.toFixed(2)} MAD
                    </p>
                </div>
            );
        }
        return null;
    };

    return (
        <div style={{ width: '100%', height: '100%', padding: '20px' }}>
            <ResponsiveContainer width="100%" height="100%">
                <LineChart
                    data={data}
                    margin={{
                        top: 5,
                        right: 30,
                        left: 20,
                        bottom: 5,
                    }}
                >
                    <CartesianGrid strokeDasharray="3 3" stroke="#334155" vertical={false} />
                    <XAxis
                        dataKey="time"
                        stroke="#64748b"
                        tick={{ fill: '#64748b', fontSize: 12 }}
                        tickLine={false}
                        axisLine={false}
                        minTickGap={30}
                    />
                    <YAxis
                        domain={[minClose - padding, maxClose + padding]}
                        stroke="#64748b"
                        tick={{ fill: '#64748b', fontSize: 12 }}
                        tickLine={false}
                        axisLine={false}
                        tickFormatter={(val) => Math.round(val).toString()}
                    />
                    <Tooltip content={<CustomTooltip />} />
                    <Line
                        type="monotone"
                        dataKey="close"
                        stroke="#34d399"
                        strokeWidth={3}
                        dot={false}
                        activeDot={{ r: 6, fill: "#34d399", stroke: "#064e3b", strokeWidth: 2 }}
                        animationDuration={1500}
                    />
                </LineChart>
            </ResponsiveContainer>
        </div>
    );
});
