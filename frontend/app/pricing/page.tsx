"use client";
import { Button } from "@/components/ui/button";
import { useRouter } from 'next/navigation';
import { useState } from 'react';

export default function PricingPage() {
    const router = useRouter();
    const [processing, setProcessing] = useState<string | null>(null);

    const plans = [
        { name: "Starter", price: "$99", fund: "$10,000" },
        { name: "Pro", price: "$199", fund: "$50,000" },
        { name: "Elite", price: "$499", fund: "$100,000" },
    ];

    const handlePayment = async (planName: string, provider: string) => {
        setProcessing(planName);
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 2000));

        // redirect to dashboard
        router.push('/dashboard');
    };

    return (
        <div className="py-20 px-4 text-center">
            <h1 className="text-4xl font-bold mb-10">Choose Your Challenge</h1>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto">
                {plans.map((plan) => (
                    <div key={plan.name} className="bg-slate-900 border border-slate-800 rounded-xl p-8 hover:border-blue-500 transition relative overflow-hidden">
                        {processing === plan.name && (
                            <div className="absolute inset-0 bg-slate-900/90 flex items-center justify-center z-10 flex-col">
                                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-emerald-500 mb-4"></div>
                                <p className="text-emerald-400 font-bold">Processing Payment...</p>
                            </div>
                        )}
                        <h2 className="text-2xl font-bold mb-4">{plan.name}</h2>
                        <div className="text-4xl font-extrabold mb-2">{plan.price}</div>
                        <p className="text-slate-400 mb-6">Funded Account Size: {plan.fund}</p>
                        <ul className="text-left text-sm space-y-3 mb-8 text-slate-300">
                            <li>✅ Profit Split 80/20</li>
                            <li>✅ AI Assistant Included</li>
                            <li>✅ Real-time Data</li>
                        </ul>
                        <div className="flex flex-col gap-3">
                            <Button
                                className="w-full bg-blue-600 hover:bg-blue-700"
                                onClick={() => handlePayment(plan.name, 'PAYPAL')}
                                disabled={!!processing}
                            >
                                Pay with PayPal
                            </Button>
                            <Button
                                className="w-full"
                                variant="outline"
                                onClick={() => handlePayment(plan.name, 'CMI')}
                                disabled={!!processing}
                            >
                                Pay with CMI (Mock)
                            </Button>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}
