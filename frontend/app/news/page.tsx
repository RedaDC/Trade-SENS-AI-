"use client";
import { useEffect, useState } from 'react';
import { Button } from '@/components/ui/button';

interface NewsItem {
    id: number;
    source: string;
    headline: string;
    summary: string;
    category: string;
    impact: string;
    timestamp: string;
    time_ago: string;
}

const SOURCE_COLORS: Record<string, string> = {
    'Reuters': 'bg-orange-600',
    'Bloomberg': 'bg-blue-600',
    'TheStreet': 'bg-green-600',
    'Forex Factory': 'bg-purple-600',
    'ADVFN': 'bg-red-600'
};

const IMPACT_COLORS: Record<string, string> = {
    'HIGH': 'text-red-400 border-red-500',
    'MEDIUM': 'text-yellow-400 border-yellow-500',
    'LOW': 'text-green-400 border-green-500'
};

export default function NewsPage() {
    const [news, setNews] = useState<NewsItem[]>([]);
    const [loading, setLoading] = useState(true);
    const [selectedSource, setSelectedSource] = useState<string | null>(null);
    const [selectedCategory, setSelectedCategory] = useState<string | null>(null);
    const [searchQuery, setSearchQuery] = useState('');

    const sources = ['Reuters', 'Bloomberg', 'TheStreet', 'Forex Factory', 'ADVFN'];
    const categories = ['Markets', 'Forex', 'Stocks', 'Commodities'];

    useEffect(() => {
        fetchNews();
    }, [selectedSource, selectedCategory]);

    const fetchNews = async () => {
        setLoading(true);
        let url = '/api/v1/tradesense/news/';
        const params = new URLSearchParams();
        if (selectedSource) params.append('source', selectedSource);
        if (selectedCategory) params.append('category', selectedCategory);
        if (params.toString()) url += '?' + params.toString();

        try {
            const res = await fetch(url);
            const data = await res.json();
            setNews(data);
        } catch (e) {
            console.error(e);
        }
        setLoading(false);
    };

    const filteredNews = news.filter(item =>
        item.headline.toLowerCase().includes(searchQuery.toLowerCase()) ||
        item.summary.toLowerCase().includes(searchQuery.toLowerCase())
    );

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950">
            {/* Header */}
            <div className="bg-slate-900/50 border-b border-slate-800 backdrop-blur-sm sticky top-0 z-10">
                <div className="max-w-7xl mx-auto px-6 py-6">
                    <h1 className="text-4xl font-bold text-white mb-2">📰 Financial News</h1>
                    <p className="text-slate-400">Real-time market updates from leading sources</p>
                </div>
            </div>

            <div className="max-w-7xl mx-auto px-6 py-8">
                {/* Filters */}
                <div className="mb-8 space-y-4">
                    {/* Search */}
                    <input
                        type="text"
                        placeholder="Search news..."
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                        className="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:border-blue-500"
                    />

                    {/* Source Filters */}
                    <div>
                        <h3 className="text-slate-400 text-sm font-bold mb-2">Sources</h3>
                        <div className="flex flex-wrap gap-2">
                            <Button
                                onClick={() => setSelectedSource(null)}
                                size="sm"
                                className={`${!selectedSource ? 'bg-blue-600' : 'bg-slate-700'} hover:bg-blue-700`}
                            >
                                All Sources
                            </Button>
                            {sources.map(source => (
                                <Button
                                    key={source}
                                    onClick={() => setSelectedSource(source)}
                                    size="sm"
                                    className={`${selectedSource === source ? SOURCE_COLORS[source] : 'bg-slate-700'} hover:opacity-80`}
                                >
                                    {source}
                                </Button>
                            ))}
                        </div>
                    </div>

                    {/* Category Filters */}
                    <div>
                        <h3 className="text-slate-400 text-sm font-bold mb-2">Categories</h3>
                        <div className="flex flex-wrap gap-2">
                            <Button
                                onClick={() => setSelectedCategory(null)}
                                size="sm"
                                className={`${!selectedCategory ? 'bg-blue-600' : 'bg-slate-700'} hover:bg-blue-700`}
                            >
                                All Categories
                            </Button>
                            {categories.map(cat => (
                                <Button
                                    key={cat}
                                    onClick={() => setSelectedCategory(cat)}
                                    size="sm"
                                    className={`${selectedCategory === cat ? 'bg-blue-600' : 'bg-slate-700'} hover:bg-blue-700`}
                                >
                                    {cat}
                                </Button>
                            ))}
                        </div>
                    </div>
                </div>

                {/* News Grid */}
                {loading ? (
                    <div className="text-center py-20">
                        <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-blue-500 border-t-transparent"></div>
                        <p className="text-slate-400 mt-4">Loading news...</p>
                    </div>
                ) : (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        {filteredNews.map(item => (
                            <div key={item.id} className="bg-slate-800/50 border border-slate-700 rounded-lg p-5 hover:border-blue-500 transition-all hover:shadow-lg hover:shadow-blue-500/20">
                                {/* Source Badge */}
                                <div className="flex items-center justify-between mb-3">
                                    <span className={`${SOURCE_COLORS[item.source]} text-white text-xs font-bold px-3 py-1 rounded-full`}>
                                        {item.source}
                                    </span>
                                    <span className="text-slate-500 text-xs">{item.time_ago}</span>
                                </div>

                                {/* Headline */}
                                <h3 className="text-white font-bold text-lg mb-2 line-clamp-2">
                                    {item.headline}
                                </h3>

                                {/* Summary */}
                                <p className="text-slate-400 text-sm mb-4 line-clamp-2">
                                    {item.summary}
                                </p>

                                {/* Footer */}
                                <div className="flex items-center justify-between">
                                    <span className="text-blue-400 text-xs font-medium bg-blue-950 px-2 py-1 rounded">
                                        {item.category}
                                    </span>
                                    <span className={`text-xs font-bold border px-2 py-1 rounded ${IMPACT_COLORS[item.impact]}`}>
                                        {item.impact}
                                    </span>
                                </div>
                            </div>
                        ))}
                    </div>
                )}

                {filteredNews.length === 0 && !loading && (
                    <div className="text-center py-20">
                        <p className="text-slate-400 text-lg">No news found matching your filters.</p>
                    </div>
                )}
            </div>
        </div>
    );
}
