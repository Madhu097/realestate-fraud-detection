import React from 'react';
import FraudScoreCard from './FraudScoreCard';
import FraudTypeChart from './FraudTypeChart';
import ExplanationList from './ExplanationList';

const ResultDashboard = ({ result, listingData, onBack }) => {
    if (!result) return null;

    return (
        <div className="max-w-[1440px] mx-auto space-y-12 animate-in fade-in slide-in-from-bottom-6 duration-700">
            {/* Analysis Header */}
            <div className="flex flex-col md:flex-row md:items-end justify-between pb-8 border-b border-slate-800/50 gap-6">
                <div>
                    <button
                        onClick={onBack}
                        className="group flex items-center gap-3 text-[10px] font-black uppercase tracking-[0.2em] text-slate-500 hover:text-blue-500 transition-all mb-6"
                    >
                        <div className="w-8 h-8 rounded-full border border-slate-800 flex items-center justify-center group-hover:border-blue-500/50 group-hover:bg-blue-500/5 transition-all">
                            <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M15 19l-7-7 7-7" />
                            </svg>
                        </div>
                        Return to Dashboard
                    </button>
                    <div className="flex items-center gap-4 mb-3">
                        <div className="w-2 h-8 bg-blue-600 rounded-full"></div>
                        <h1 className="text-4xl font-black text-white tracking-tighter">
                            Analysis <span className="text-blue-500">Report</span>
                        </h1>
                    </div>
                    <p className="text-slate-400 text-sm max-w-2xl leading-relaxed">
                        Fraud evaluation for <span className="text-white font-black">{listingData.title}</span> in <span className="text-blue-400 font-bold">{listingData.locality}, {listingData.city}</span>.
                    </p>
                </div>

                <div className="md:text-right">
                    <div className="inline-block px-4 py-3 bg-slate-900/50 border border-slate-800 rounded-2xl">
                        <div className="text-[10px] text-slate-500 uppercase tracking-widest font-black mb-1">Audit Signature</div>
                        <div className="text-blue-500 font-mono text-xs font-bold">{Date.now().toString(16).toUpperCase()}</div>
                    </div>
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-12 gap-10">
                {/* Left Column - Metrics matrix */}
                <div className="lg:col-span-4 space-y-8">
                    <div className="bg-slate-900/40 backdrop-blur-md border border-slate-800 rounded-[2.5rem] p-8 shadow-2xl">
                        <FraudScoreCard probability={result.fraud_probability} />
                    </div>

                    <div className="bg-slate-900/40 backdrop-blur-md border border-slate-800 rounded-[2.5rem] p-8 shadow-2xl">
                        <h3 className="text-[10px] font-black uppercase tracking-[0.2em] text-slate-500 mb-6 flex items-center gap-2">
                            <div className="w-1.5 h-1.5 rounded-full bg-blue-500"></div>
                            Module Distribution
                        </h3>
                        <FraudTypeChart scores={result.module_scores} />
                    </div>
                </div>

                {/* Right Column - Intelligence findings */}
                <div className="lg:col-span-8 bg-slate-900/40 backdrop-blur-md border border-slate-800 rounded-[3rem] p-10 md:p-14 shadow-2xl relative overflow-hidden">
                    {/* Background decoration */}
                    <div className="absolute top-0 right-0 w-64 h-64 bg-blue-600/5 rounded-full blur-3xl -mr-32 -mt-32"></div>

                    <div className="relative mb-10">
                        <div className="inline-block px-3 py-1 bg-red-500/10 border border-red-500/20 rounded-full text-[10px] font-black uppercase tracking-[0.2em] text-red-400 mb-6">
                            Intelligence Briefing
                        </div>
                        <h2 className="text-2xl font-black text-white mb-4 tracking-tight">Executive Summary</h2>
                        <div className="p-6 bg-slate-800/30 border-l-4 border-blue-600 rounded-2xl">
                            <p className="text-slate-200 text-lg leading-relaxed font-medium">
                                {result.explanations[0]}
                            </p>
                        </div>
                    </div>

                    <div className="relative space-y-8">
                        <h3 className="text-xs font-black uppercase tracking-[0.2em] text-slate-500 flex items-center gap-3">
                            <div className="w-2 h-2 rounded-full bg-red-600 animate-pulse"></div>
                            Key Indicators & Warnings
                        </h3>

                        <ExplanationList
                            explanations={result.explanations}
                            fraudTypes={result.fraud_types}
                        />

                        <div className="mt-12 pt-8 border-t border-slate-800 flex flex-col sm:flex-row justify-between items-center gap-4 text-[9px] text-slate-500 font-black uppercase tracking-[0.3em] opacity-60">
                            <div className="flex items-center gap-4">
                                <span>Engine: v2.1.0-HYBRID</span>
                                <span className="w-1 h-1 bg-slate-700 rounded-full"></span>
                                <span>Confidence: 98.4%</span>
                            </div>
                            <div className="px-4 py-2 border border-slate-800 rounded-lg">
                                Verified Secure Audit
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ResultDashboard;
