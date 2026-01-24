import React from 'react';

const ExplanationList = ({ explanations, fraudTypes }) => {
    // Filter out the summary explanation (first one) as it will be displayed in main dashboard
    const detailedExplanations = explanations.length > 1 ? explanations.slice(1) : [];

    return (
        <div className="space-y-6">
            <div className="flex flex-wrap items-center gap-3">
                {fraudTypes.map((type, idx) => (
                    <span
                        key={idx}
                        className="px-3 py-1 bg-red-500/10 text-red-500 text-[9px] font-black rounded-lg border border-red-500/20 uppercase tracking-widest"
                    >
                        {type.replace('_', ' ')}
                    </span>
                ))}
            </div>

            <div className="space-y-3">
                {detailedExplanations.length > 0 ? (
                    detailedExplanations.map((exp, idx) => (
                        <div
                            key={idx}
                            className="bg-slate-800/30 p-5 rounded-2xl border border-slate-700/30 group hover:border-blue-500/30 transition-all duration-300"
                        >
                            <div className="flex gap-4">
                                <div className="flex-shrink-0 w-8 h-8 rounded-xl bg-slate-700/50 flex items-center justify-center text-slate-400 group-hover:bg-blue-600/10 group-hover:text-blue-400 transition-all">
                                    <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                                        <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
                                    </svg>
                                </div>
                                <p className="text-slate-300 text-sm leading-relaxed whitespace-pre-wrap font-medium">
                                    {exp}
                                </p>
                            </div>
                        </div>
                    ))
                ) : explanations.length <= 1 ? (
                    <div className="bg-emerald-500/5 p-10 rounded-[2rem] border border-dashed border-emerald-500/20 text-center">
                        <div className="w-12 h-12 bg-emerald-500/10 rounded-2xl flex items-center justify-center mx-auto mb-4">
                            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                        </div>
                        <p className="text-emerald-500/60 text-xs font-black uppercase tracking-[0.2em]">All Systems Nominal</p>
                        <p className="text-slate-500 text-[10px] mt-2 italic font-medium">No granular risk exceptions were identified beyond the primary summary.</p>
                    </div>
                ) : null}
            </div>
        </div>
    );
};

export default ExplanationList;
