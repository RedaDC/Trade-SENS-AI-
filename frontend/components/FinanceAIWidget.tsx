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
        const newMessages = [...messages, userMessage];
        setMessages(newMessages);
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

        setMessages([...newMessages, aiMessage]);
        setLoading(false);
    };

    return (
        <div className="fixed bottom-6 right-6 z-50 flex flex-col items-end gap-4">
            {isOpen && (
                <div className="w-96 h-[600px] bg-slate-900/90 backdrop-blur-xl border border-white/10 rounded-2xl shadow-2xl flex flex-col overflow-hidden animate-in slide-in-from-bottom-5 duration-300 ring-1 ring-white/5">
                    {/* Header */}
                    <div className="bg-gradient-to-r from-blue-900/40 to-slate-900/40 p-4 border-b border-white/5 flex justify-between items-center backdrop-blur-md">
                        <div className="flex items-center gap-3">
                            <div className="w-10 h-10 rounded-full bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center shadow-lg shadow-blue-500/30 ring-2 ring-white/10">
                                <span className="text-lg">💎</span>
                            </div>
                            <div>
                                <h3 className="font-extrabold text-white text-sm tracking-tight">Finance AI <span className="text-blue-400">Elite</span></h3>
                                <p className="text-[10px] text-emerald-400 font-bold flex items-center gap-1">
                                    <span className="w-1.5 h-1.5 bg-emerald-500 rounded-full animate-pulse"></span>
                                    Mentor Online
                                </p>
                            </div>
                        </div>
                        <button onClick={() => setIsOpen(false)} className="text-slate-400 hover:text-white transition-colors bg-white/5 hover:bg-white/10 p-1.5 rounded-full">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="18" x2="6" y1="6" y2="18" /><line x1="6" x2="18" y1="6" y2="18" /></svg>
                        </button>
                    </div>

                    {/* Chat Area */}
                    <div ref={scrollRef} className="flex-1 overflow-y-auto p-4 space-y-6 bg-transparent custom-scrollbar">
                        {messages.map((m, i) => (
                            <div key={i} className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'} animate-in fade-in slide-in-from-bottom-2 duration-300`}>
                                <div className={`max-w-[85%] rounded-2xl p-4 text-sm shadow-sm ${m.role === 'user'
                                    ? 'bg-blue-600 text-white rounded-br-sm'
                                    : 'bg-slate-800/80 backdrop-blur-sm text-slate-200 rounded-bl-sm border border-white/5'
                                    }`}>

                                    {m.type === 'analysis' && m.analysisData ? (
                                        <div className="space-y-4">
                                            <div className="prose prose-invert prose-sm max-w-none">
                                                <p className="opacity-90 leading-relaxed"><ReactMarkdown>{m.content}</ReactMarkdown></p>
                                            </div>
                                            <FinanceAICard data={m.analysisData} symbol={symbol} />
                                        </div>
                                    ) : (
                                        <div className="prose prose-invert prose-sm max-w-none prose-p:leading-relaxed prose-pre:bg-slate-900 prose-pre:border prose-pre:border-white/10">
                                            <ReactMarkdown
                                                components={{
                                                    strong: ({ ...props }) => <span className="font-bold text-blue-300" {...props} />,
                                                    ul: ({ ...props }) => <ul className="list-disc list-outside ml-4 space-y-1 my-2 text-slate-300 marker:text-blue-500" {...props} />,
                                                    li: ({ ...props }) => <li className="pl-1" {...props} />,
                                                    h3: ({ ...props }) => <h3 className="text-base font-bold text-emerald-400 mb-2 mt-3 border-b border-white/5 pb-1" {...props} />,
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
                                <div className="bg-slate-800/50 backdrop-blur-sm rounded-2xl rounded-bl-sm px-4 py-3 border border-white/5">
                                    <div className="flex gap-1.5">
                                        <div className="w-1.5 h-1.5 bg-blue-400 rounded-full animate-bounce [animation-delay:-0.3s]"></div>
                                        <div className="w-1.5 h-1.5 bg-blue-400 rounded-full animate-bounce [animation-delay:-0.15s]"></div>
                                        <div className="w-1.5 h-1.5 bg-blue-400 rounded-full animate-bounce"></div>
                                    </div>
                                </div>
                            </div>
                        )}
                    </div>

                    {/* Input Area */}
                    <div className="p-4 bg-slate-900/60 backdrop-blur-md border-t border-white/5">
                        <div className="relative flex items-center gap-2">
                            <input
                                type="text"
                                value={input}
                                onChange={(e) => setInput(e.target.value)}
                                onKeyDown={(e) => e.key === 'Enter' && handleSend()}
                                placeholder="Ask for analysis..."
                                className="w-full bg-slate-800/50 border border-white/10 rounded-xl px-4 py-3 text-sm text-white placeholder:text-slate-500 focus:outline-none focus:border-blue-500/50 focus:ring-1 focus:ring-blue-500/50 transition-all pr-12 shadow-inner"
                            />
                            <button
                                onClick={handleSend}
                                disabled={!input.trim() || loading}
                                className="absolute right-2 p-1.5 bg-blue-600 hover:bg-blue-500 text-white rounded-lg transition-colors disabled:opacity-50 disabled:hover:bg-blue-600 shadow-lg shadow-blue-600/20"
                            >
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="transform -rotate-45 mb-0.5 ml-0.5"><line x1="22" y1="2" x2="11" y2="13" /><polygon points="22 2 15 22 11 13 2 9 22 2" /></svg>
                            </button>
                        </div>
                    </div>
                </div>
            )}

            {/* Toggle Button */}
            <button
                onClick={() => setIsOpen(!isOpen)}
                className="group relative w-14 h-14 rounded-full shadow-2xl shadow-blue-600/30 flex items-center justify-center transition-all duration-300 hover:scale-110 active:scale-95 z-50"
            >
                <div className="absolute inset-0 bg-gradient-to-br from-blue-600 to-indigo-600 rounded-full animate-pulse-slow group-hover:animate-none"></div>
                <div className="absolute inset-0 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-full opacity-0 group-hover:opacity-100 transition-opacity duration-300 border border-white/20"></div>

                <span className="relative z-10 text-2xl text-white drop-shadow-md transform transition-transform duration-300 group-hover:rotate-12">
                    {isOpen ? '✕' : '💬'}
                </span>

                {!isOpen && (
                    <span className="absolute -top-1 -right-1 flex h-4 w-4">
                        <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                        <span className="relative inline-flex rounded-full h-4 w-4 bg-emerald-500 border-2 border-slate-900"></span>
                    </span>
                )}
            </button>
        </div>
    );
}
