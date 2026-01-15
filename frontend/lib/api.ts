// Use relative URL and Next.js rewrites to avoid CORS issues in dev
const BASE_URL = '/api/v1/tradesense';

export async function fetchMarketData(symbol: string) {
    try {
        const res = await fetch(`${BASE_URL}/market-data/last?symbol=${symbol}`);
        if (!res.ok) throw new Error('Failed to fetch');
        return res.json();
    } catch (e) {
        console.error(e);
        return { price: 0.0 };
    }
}

export async function fetchOHLCV(symbol: string) {
    try {
        const res = await fetch(`${BASE_URL}/market-data/ohlcv?symbol=${symbol}&limit=100`);
        if (!res.ok) throw new Error('Failed to fetch OHLCV');
        return res.json();
    } catch (e) {
        console.error(e);
        return [];
    }
}

export async function fetchNews() {
    try {
        const res = await fetch(`${BASE_URL}/news/`);
        return res.json();
    } catch (e) {
        return [];
    }
}

export async function placeTrade(trade: any) {
    const res = await fetch(`${BASE_URL}/trades/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(trade)
    });
    return res.json();
}

export async function loginUser(email: string, password: string) {
    const res = await fetch(`${BASE_URL}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
    });
    return res.json();
}

export async function fetchAnalysis(symbol: string) {
    try {
        const res = await fetch(`${BASE_URL}/analysis/latest?symbol=${symbol}`);
        if (!res.ok) return null;
        return res.json();
    } catch (e) {
        console.error(e);
        return null;
    }
}

export async function chatWithAI(message: string, context: any) {
    try {
        const res = await fetch(`${BASE_URL}/ai/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message, context })
        });
        if (!res.ok) throw new Error('AI failed');
        return res.json();
    } catch (e) {
        console.error(e);
        return { response: "I'm having trouble connecting. Try again later! 🤖" };
    }
}
