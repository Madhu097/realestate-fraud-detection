import React from 'react';

const FraudScoreCard = ({ probability }) => {
    const percentage = (probability * 100).toFixed(0);

    const getStatusInfo = (p) => {
        if (p >= 0.7) return { label: 'CRITICAL RISK', color: 'text-red-500', bg: 'bg-red-500', glow: 'shadow-red-500/20' };
        if (p >= 0.4) return { label: 'MODERATE RISK', color: 'text-amber-500', bg: 'bg-amber-500', glow: 'shadow-amber-500/20' };
        return { label: 'MINIMAL RISK', color: 'text-emerald-500', bg: 'bg-emerald-500', glow: 'shadow-emerald-500/20' };
    };

    const status = getStatusInfo(probability);

    return (
        <div className="relative overflow-hidden group">
            <h3 className="text-[10px] font-black uppercase tracking-[0.2em] text-slate-500 mb-6 flex items-center gap-2">
                <div className="w-1.5 h-1.5 rounded-full bg-blue-500"></div>
                Overall Fraud Index
            </h3>

            <div className="flex flex-col items-center justify-center py-6">
                <div className="relative mb-6">
                    {/* Radial progress simulator or large text */}
                    <div className={`text-8xl font-black tracking-tighter tabular-nums ${status.color} mb-2`}>
                        {percentage}<span className="text-3xl opacity-50">%</span>
                    </div>
                </div>

                <div className={`px-6 py-2 rounded-full border-2 border-current ${status.color} bg-white/5 font-black text-[10px] uppercase tracking-[0.3em] shadow-2xl ${status.glow}`}>
                    {status.label}
                </div>
            </div>

            <div className="mt-8">
                <div className="flex justify-between text-[9px] font-black uppercase tracking-widest text-slate-500 mb-2">
                    <span>Probability Scale</span>
                    <span>{percentage}%</span>
                </div>
                <div className="w-full bg-slate-800 rounded-full h-1.5 overflow-hidden">
                    <div
                        className={`h-full transition-all duration-1000 ease-out ${status.bg}`}
                        style={{ width: `${percentage}%` }}
                    ></div>
                </div>
            </div>

            <p className="mt-6 text-[10px] text-slate-500 font-medium leading-relaxed italic opacity-70">
                Confidence-weighted fusion of neural text analysis, geospatial price clusters, and metadata validation.
            </p>
        </div>
    );
};

export default FraudScoreCard;
