export default function LeaderboardPage() {
    const mockTraders = [
        { rank: 1, name: "AtlasTrader", profit: "+24.5%", status: "PASSED" },
        { rank: 2, name: "CasablancaWhale", profit: "+18.2%", status: "PASSED" },
        { rank: 3, name: "ForexKing", profit: "+12.1%", status: "ACTIVE" },
    ];

    return (
        <div className="py-20 px-4 max-w-4xl mx-auto">
            <h1 className="text-3xl font-bold mb-8 text-center">Top Traders</h1>
            <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
                <table className="w-full text-left">
                    <thead className="bg-slate-800 text-slate-300">
                        <tr>
                            <th className="p-4">Rank</th>
                            <th className="p-4">Trader</th>
                            <th className="p-4">Profit</th>
                            <th className="p-4">Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        {mockTraders.map((t) => (
                            <tr key={t.rank} className="border-t border-slate-800">
                                <td className="p-4 font-bold text-blue-400">#{t.rank}</td>
                                <td className="p-4">{t.name}</td>
                                <td className="p-4 text-emerald-400">{t.profit}</td>
                                <td className="p-4">
                                    <span className="bg-emerald-900 text-emerald-300 px-2 py-1 rounded text-xs">{t.status}</span>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}
