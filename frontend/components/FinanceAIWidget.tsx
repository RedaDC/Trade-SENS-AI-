"use client";
import React, { useState, useRef, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { chatWithAI } from '@/lib/api';
import { FinanceAICard } from './FinanceAICard';
import ReactMarkdown from 'react-markdown';

interface Message {
    role: 'user' | 'assistant';
    content: string;
    type?: 'text' | 'analysis';
    analysisData?: any;
}

export function FinanceAIWidget({ symbol }: { symbol: string }) {
    const [isOpen, setIsOpen] = useState(false);
    const [messages, setMessages] = useState<Message[]>([
        { role: 'assistant', content: 'Hello! I am Finance with AI. Ask me about **price**, **trend**, or for a **technical analysis**! 🤖', type: 'text' }
    ]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);
    const scrollRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        if (scrollRef.current) {
            scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
        }
    }, [messages, isOpen]);

    const handleSend = async () => {
        if (!input.trim()) return;

        const userText = input;
        setInput('');

        const userMessage: Message = { role: 'user', content: userText, type: 'text' };
        setMessages((prev: Message[]) => [...prev, userMessage]);
        setLoading(true);

        const data = await chatWithAI(userText, { symbol });

        let aiMessage: Message;
        // Handle different response formats (string error vs structured object)
        if (data.response && typeof data.response === 'object') {
            aiMessage = {
                role: 'assistant',
                content: data.response.message || '',
                type: data.response.type || 'text',
                analysisData: data.response.data
            };
        } else {
            aiMessage = { role: 'assistant', content: data.response || "Error connecting to AI.", type: 'text' };
        }

        setMessages((prev: Message[]) => [...prev, aiMessage]);
        setLoading(false);
    };

    return (
        <div className="fixed bottom-6 right-6 z-50 flex flex-col items-end gap-4">
            {isOpen && (
                <div className="w-96 h-[500px] bg-slate-950 border border-slate-800 rounded-xl shadow-2xl flex flex-col overflow-hidden animate-in slide-in-from-bottom-5 backdrop-blur-sm">
                    {/* Header */}
                    <div className="bg-slate-900/50 p-4 border-b border-slate-800 flex justify-between items-center backdrop-blur-md">
                        <h3 className="font-bold text-blue-400 flex items-center gap-2">
                            <span className="text-xl">🤖</span> Finance AI
                        </h3>
                        <button onClick={() => setIsOpen(false)} className="text-slate-400 hover:text-white transition-colors">✕</button>
                    </div>

                    {/* Chat Area */}
                    <div ref={scrollRef} className="flex-1 overflow-y-auto p-4 space-y-4 bg-slate-950/50">
                        {messages.map((m, i) => (
                            <div key={i} className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                                <div className={`max-w-[90%] rounded-2xl px-4 py-3 text-sm shadow-sm ${m.role === 'user'
                                    ? 'bg-blue-600 text-white rounded-br-none'
                                    : 'bg-slate-800 text-slate-200 rounded-bl-none border border-slate-700'
                                    }`}>

                                    {m.type === 'analysis' && m.analysisData ? (
                                        <div className="space-y-3">
                                            <p className="opacity-80 mb-2"><ReactMarkdown>{m.content}</ReactMarkdown></p>
                                            <FinanceAICard data={m.analysisData} symbol={symbol} />
                                        </div>
                                    ) : (
                                        <div className="markdown-content">
                                            <ReactMarkdown
                                                components={{
                                                    strong: ({ ...props }) => <span className="font-bold text-blue-300" {...props} />,
                                                    p: ({ ...props }) => <p className="mb-2 last:mb-0" {...props} />
                                                }}
                                            >
                                                {m.content}
                                            </ReactMarkdown>
                                        </div>
                                    )}
                                </div>
                            </div>
                        ))}
                        {loading && (
                            <div className="flex justify-start">
                                <div className="bg-slate-800 rounded-2xl rounded-bl-none px-4 py-3 text-sm text-slate-400 animate-pulse border border-slate-700">
                                    <span className="flex gap-1">
                                        <span className="animate-bounce delay-0">.</span>
                                        <span className="animate-bounce delay-100">.</span>
                                        <span className="animate-bounce delay-200">.</span>
                                    </span>
                                </div>
                            </div>
                        )}
                    </div>

                    {/* Input Area */}
                    <div className="p-3 bg-slate-900 border-t border-slate-800 flex gap-2">
                        <input
                            type="text"
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
                            placeholder="Ask for analysis, trend, opinion..."
                            className="flex-1 bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-blue-500 transition-colors"
                        />
                        <Button onClick={handleSend} size="sm" className="bg-blue-600 hover:bg-blue-500 text-white rounded-lg px-4">
                            Send
                        </Button>
                    </div>
                </div>
            )}

            {/* Toggle Button */}
            <button
                onClick={() => setIsOpen(!isOpen)}
                className="w-14 h-14 bg-blue-600 hover:bg-blue-500 rounded-full shadow-xl shadow-blue-500/20 flex items-center justify-center text-2xl hover:scale-105 transition-all duration-200 border border-white/10"
            >
                {isOpen ? '✕' : '💬'}
            </button>
        </div>
    );
}
