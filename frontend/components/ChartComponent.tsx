"use client";
import React, { useEffect, useRef, memo } from 'react';

export const ChartComponent = memo(function ChartComponent({
    symbol = "EURUSD",
    theme = "dark",
    autosize = true,
}: {
    symbol?: string;
    theme?: "light" | "dark";
    autosize?: boolean;
}) {
    const container = useRef<HTMLDivElement>(null);

    useEffect(() => {
        if (!container.current) return;

        // Clear previous script if any (though React usually handles DOM cleanup, script tags are persistent)
        container.current.innerHTML = "";

        const script = document.createElement("script");
        script.src = "https://s3.tradingview.com/external-embedding/embed-widget-advanced-chart.js";
        script.type = "text/javascript";
        script.async = true;

        // Transform symbol for TradingView
        let tvSymbol = symbol;
        if (symbol.endsWith('.MA')) {
            // Moroccan stocks: IAM.MA -> CSEMA:IAM
            tvSymbol = `CSEMA:${symbol.replace('.MA', '')}`;
        }

        script.innerHTML = JSON.stringify({
            "autosize": autosize,
            "symbol": tvSymbol,
            "interval": "D",
            "timezone": "Etc/UTC",
            "theme": theme,
            "style": "1",
            "locale": "en",
            "enable_publishing": false,
            "allow_symbol_change": true,
            "calendar": false,
            "support_host": "https://www.tradingview.com"
        });

        const widgetContainer = document.createElement("div");
        widgetContainer.className = "tradingview-widget-container__widget";
        widgetContainer.style.height = "100%";
        widgetContainer.style.width = "100%";

        container.current.appendChild(widgetContainer);
        container.current.appendChild(script);

    }, [symbol, theme, autosize]);

    return (
        <div className="tradingview-widget-container" ref={container} style={{ height: "100%", width: "100%" }}>
            <div className="tradingview-widget-container__widget" style={{ height: "calc(100% - 32px)", width: "100%" }}></div>
        </div>
    );
});
