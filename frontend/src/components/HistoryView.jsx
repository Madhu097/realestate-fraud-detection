import React, { useState, useEffect } from 'react';
import axios from 'axios';

const HistoryView = ({ apiBaseUrl, onBack }) => {
    const [history, setHistory] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [selectedHistory, setSelectedHistory] = useState(null);

    useEffect(() => {
        fetchHistory();
    }, []);

    const fetchHistory = async () => {
        setLoading(true);
        setError(null);
        try {
            const response = await axios.get(`${apiBaseUrl}/api/history`);
            setHistory(response.data);
        } catch (err) {
            console.error('Fetch history error:', err);
            setError('Failed to load analysis history. Please ensure the backend is running.');
        } finally {
            setLoading(false);
        }
    };

    const fetchDetail = async (id) => {
        try {
            const response = await axios.get(`${apiBaseUrl}/api/history/${id}`);
            setSelectedHistory(response.data);
        } catch (err) {
            console.error('Failed to load detail', err);
        }
    };

    const formatDate = (dateString) => {
        return new Date(dateString).toLocaleString('en-US', {
            month: 'short',
            day: 'numeric',
            year: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    };

    const getBadgeStyle = (prob) => {
        if (prob >= 0.7) return 'bg-red-500/10 text-red-400 border-red-500/20';
        if (prob >= 0.4) return 'bg-amber-500/10 text-amber-400 border-amber-500/20';
        return 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20';
    };

    if (loading) return (
        <div className="flex flex-col items-center justify-center py-32 gap-6 scale-up-center">
            <div className="relative">
                <div className="w-16 h-16 border-4 border-blue-500/10 border-t-blue-500 rounded-full animate-spin"></div>
                <div className="absolute inset-0 w-16 h-16 border-4 border-blue-400/5 rounded-full animate-ping"></div>
            </div>
            <div className="text-center">
                <p className="text-white font-bold text-lg tracking-tight">Syncing Database</p>
                <p className="text-slate-500 text-sm">Retrieving historical fraud records...</p>
            </div>
        </div>
    );

    return (
        <div className="max-w-[1440px] mx-auto animate-in fade-in slide-in-from-bottom-6 duration-700">
            <div className="flex flex-col md:flex-row md:items-end justify-between mb-10 gap-4">
                <div>
                    <div className="flex items-center gap-3 mb-2">
                        <button
                            onClick={onBack}
                            className="p-2 -ml-2 hover:bg-slate-800 rounded-full transition-colors text-slate-400 hover:text-white md:hidden"
                        >
                            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                            </svg>
                        </button>
                        <h2 className="text-4xl font-black text-white tracking-tighter">Fraud <span className="text-blue-500">Database</span></h2>
                    </div>
                    <p className="text-slate-400 text-sm max-w-md leading-relaxed">
                        A comprehensive audit trail of all analyzed real estate listings, identifying patterns in historical fraud signals.
                    </p>
                </div>
                <div className="flex items-center gap-3">
                    <button
                        onClick={fetchHistory}
                        className="flex items-center gap-2 px-4 py-2 bg-slate-800 hover:bg-slate-700 border border-slate-700/50 rounded-xl transition-all text-xs font-bold uppercase tracking-widest text-slate-300 hover:text-white"
                    >
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                        </svg>
                        Refresh Data
                    </button>
                </div>
            </div>

            {error && (
                <div className="bg-red-500/10 border border-red-500/20 p-6 rounded-2xl text-red-400 mb-8 flex items-center gap-4 animate-shake">
                    <div className="w-10 h-10 bg-red-500/20 rounded-full flex items-center justify-center flex-shrink-0">
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                            <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                        </svg>
                    </div>
                    <div>
                        <p className="font-bold">Connection Error</p>
                        <p className="text-sm opacity-80">{error}</p>
                    </div>
                </div>
            )}

            {!history.length && !error ? (
                <div className="bg-slate-900/40 backdrop-blur-md border border-slate-800 rounded-[2.5rem] p-24 text-center">
                    <div className="relative w-24 h-24 mx-auto mb-8">
                        <div className="absolute inset-0 bg-blue-500/10 rounded-[2rem] rotate-6 animate-pulse"></div>
                        <div className="relative w-full h-full bg-slate-800 border-2 border-slate-700 rounded-[2rem] flex items-center justify-center">
                            <svg xmlns="http://www.w3.org/2000/svg" className="h-10 w-10 text-slate-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
                            </svg>
                        </div>
                    </div>
                    <h3 className="text-2xl font-black text-white mb-3">Database is Empty</h3>
                    <p className="text-slate-400 max-w-sm mx-auto leading-relaxed">
                        No property listings have been analyzed yet. Start a new analysis to see results populated here.
                    </p>
                    <button
                        onClick={onBack}
                        className="mt-8 px-8 py-3 bg-blue-600 hover:bg-blue-500 text-white font-bold rounded-2xl transition-all hover:scale-105 active:scale-95 shadow-xl shadow-blue-600/20"
                    >
                        Analyze First Listing
                    </button>
                </div>
            ) : (
                <div className="bg-slate-900/40 backdrop-blur-md border border-slate-800 rounded-[2.5rem] overflow-hidden shadow-2xl">
                    <div className="overflow-x-auto">
                        <table className="w-full text-left border-collapse">
                            <thead>
                                <tr className="border-b border-slate-800/50 bg-slate-800/20">
                                    <th className="px-8 py-5 text-[10px] font-black uppercase tracking-[0.2em] text-slate-500">Date Analytics</th>
                                    <th className="px-8 py-5 text-[10px] font-black uppercase tracking-[0.2em] text-slate-500">Listing Identification</th>
                                    <th className="px-8 py-5 text-[10px] font-black uppercase tracking-[0.2em] text-slate-500">Geographic Data</th>
                                    <th className="px-8 py-5 text-[10px] font-black uppercase tracking-[0.2em] text-slate-500 text-center">Risk Score</th>
                                    <th className="px-8 py-5 text-[10px] font-black uppercase tracking-[0.2em] text-slate-500 text-right">Action</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-slate-800/50">
                                {history.map((record) => (
                                    <tr
                                        key={record.id}
                                        className="hover:bg-blue-500/5 transition-all group cursor-pointer"
                                        onClick={() => fetchDetail(record.id)}
                                    >
                                        <td className="px-8 py-6">
                                            <div className="text-xs font-bold text-slate-500">{formatDate(record.timestamp).split(',')[0]}</div>
                                            <div className="text-[10px] text-slate-600 uppercase tracking-widest">{formatDate(record.timestamp).split(',')[1]}</div>
                                        </td>
                                        <td className="px-8 py-6">
                                            <div className="text-sm font-bold text-white group-hover:text-blue-400 transition-colors line-clamp-1 mb-1">
                                                {record.title}
                                            </div>
                                            <div className="flex gap-2">
                                                {record.fraud_types.slice(0, 2).map((type, i) => (
                                                    <span key={i} className="text-[8px] px-1.5 py-0.5 rounded-md bg-slate-800 text-slate-400 uppercase font-black border border-slate-700/50">
                                                        {type.split('_')[0]}
                                                    </span>
                                                ))}
                                                {record.fraud_types.length > 2 && <span className="text-[8px] text-slate-500">+{record.fraud_types.length - 2} more</span>}
                                            </div>
                                        </td>
                                        <td className="px-8 py-6">
                                            <div className="text-xs font-medium text-slate-300">{record.locality}</div>
                                            <div className="text-[10px] text-slate-500 opacity-70">{record.city}</div>
                                        </td>
                                        <td className="px-8 py-6 text-center">
                                            <div className={`text-xl font-black ${(record.fraud_probability * 100).toFixed(0) >= 70 ? 'text-red-500' : (record.fraud_probability * 100).toFixed(0) >= 40 ? 'text-amber-500' : 'text-emerald-500'} tabular-nums`}>
                                                {(record.fraud_probability * 100).toFixed(0)}%
                                            </div>
                                            <div className="w-12 h-1 bg-slate-800 mx-auto mt-1 rounded-full overflow-hidden">
                                                <div
                                                    className={`h-full ${(record.fraud_probability * 100).toFixed(0) >= 70 ? 'bg-red-500' : (record.fraud_probability * 100).toFixed(0) >= 40 ? 'bg-amber-500' : 'bg-emerald-500'}`}
                                                    style={{ width: `${record.fraud_probability * 100}%` }}
                                                ></div>
                                            </div>
                                        </td>
                                        <td className="px-8 py-6 text-right">
                                            <button className="px-4 py-2 bg-slate-800 group-hover:bg-blue-600 transition-all text-[10px] font-black uppercase tracking-widest text-white rounded-lg">
                                                View Report
                                            </button>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>
            )}

            {/* Modal for Details with Glassmorphism */}
            {selectedHistory && (
                <div className="fixed inset-0 z-[100] flex items-center justify-center p-6 bg-slate-950/90 backdrop-blur-md">
                    <div className="bg-slate-900 border border-slate-800 rounded-[3rem] w-full max-w-4xl max-h-[90vh] overflow-y-auto shadow-[0_0_100px_-20px_rgba(30,64,175,0.3)] animate-in zoom-in-95 duration-300">
                        <div className="sticky top-0 bg-slate-900/80 backdrop-blur-xl px-10 py-8 border-b border-slate-800 flex items-center justify-between z-10">
                            <div>
                                <h3 className="text-3xl font-black text-white tracking-tighter">Analysis <span className="text-blue-500">Report</span></h3>
                                <p className="text-slate-500 text-xs font-bold uppercase tracking-widest mt-1">Audit Log ID: #{selectedHistory.id} • Precision Analysis</p>
                            </div>
                            <button
                                onClick={() => setSelectedHistory(null)}
                                className="w-12 h-12 bg-slate-800 hover:bg-red-500 text-white rounded-2xl flex items-center justify-center transition-all hover:rotate-90"
                            >
                                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M6 18L18 6M6 6l12 12" />
                                </svg>
                            </button>
                        </div>

                        <div className="p-10 space-y-12">
                            {/* Analytics Header */}
                            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                                <div className={`col-span-1 border-2 rounded-[2.5rem] p-8 flex flex-col items-center justify-center text-center ${getBadgeStyle(selectedHistory.fraud_probability)}`}>
                                    <div className="text-[10px] font-black uppercase tracking-[0.2em] opacity-60 mb-3">Fraud Probability</div>
                                    <div className="text-7xl font-black tracking-tighter tabular-nums">
                                        {(selectedHistory.fraud_probability * 100).toFixed(0)}%
                                    </div>
                                    <div className="mt-6 text-[10px] font-black uppercase tracking-widest bg-white/10 px-6 py-2 rounded-full border border-white/10">
                                        {selectedHistory.fraud_probability >= 0.7 ? 'High Risk Alert' : selectedHistory.fraud_probability >= 0.4 ? 'Verification Recommended' : 'Verified Secure'}
                                    </div>
                                </div>

                                <div className="col-span-1 lg:col-span-2 bg-slate-800/30 border border-slate-700/50 rounded-[2.5rem] p-8">
                                    <h4 className="text-white text-xs font-black uppercase tracking-[0.2em] mb-6 flex items-center gap-2">
                                        <div className="w-1.5 h-1.5 rounded-full bg-blue-500"></div>
                                        Property Meta-Data
                                    </h4>
                                    <div className="space-y-6">
                                        <div>
                                            <div className="text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-1">Title</div>
                                            <div className="text-xl font-bold text-white leading-tight">{selectedHistory.title}</div>
                                        </div>
                                        <div className="grid grid-cols-2 gap-8 pt-4 border-t border-slate-700/50">
                                            <div>
                                                <div className="text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-1">Valuation</div>
                                                <div className="text-2xl font-black text-white tracking-tight">₹{selectedHistory.price.toLocaleString()}</div>
                                            </div>
                                            <div>
                                                <div className="text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-1">Locality</div>
                                                <div className="text-lg font-bold text-slate-200">{selectedHistory.locality}, {selectedHistory.city}</div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            {/* Signal Breakdown */}
                            <div>
                                <h4 className="text-white text-xs font-black uppercase tracking-[0.2em] mb-6 flex items-center gap-2">
                                    <div className="w-1.5 h-1.5 rounded-full bg-red-500"></div>
                                    Detected Fraud Signals
                                </h4>
                                {selectedHistory.explanations.length > 0 ? (
                                    <div className="space-y-3">
                                        {selectedHistory.explanations.map((exp, i) => (
                                            <div key={i} className="bg-slate-800/40 border border-slate-700/50 p-5 rounded-2xl flex items-start gap-4 group hover:border-red-500/30 transition-colors">
                                                <div className="mt-1 w-8 h-8 bg-red-500/10 rounded-xl flex items-center justify-center flex-shrink-0 group-hover:bg-red-500/20 transition-all">
                                                    <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                                                        <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                                                    </svg>
                                                </div>
                                                <p className="text-slate-300 text-sm leading-relaxed font-medium">{exp}</p>
                                            </div>
                                        ))}
                                    </div>
                                ) : (
                                    <div className="bg-emerald-500/5 border border-emerald-500/10 p-10 rounded-3xl text-center">
                                        <div className="w-12 h-12 bg-emerald-500/10 rounded-2xl flex items-center justify-center mx-auto mb-4">
                                            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                                            </svg>
                                        </div>
                                        <p className="text-emerald-400 font-bold uppercase tracking-widest text-xs">No fraud signals detected</p>
                                    </div>
                                )}
                            </div>

                            {/* Multi-Module Matrix */}
                            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                                {Object.entries(selectedHistory.module_scores).map(([name, score]) => (
                                    <div key={name} className="relative bg-slate-800/50 border border-slate-700/50 p-6 rounded-3xl overflow-hidden group">
                                        <div className="relative z-10">
                                            <div className="text-[10px] font-black uppercase tracking-widest text-slate-500 mb-2">{name} Module</div>
                                            <div className={`text-3xl font-black tabular-nums transition-all ${score >= 0.7 ? 'text-red-500' : score >= 0.4 ? 'text-amber-500' : 'text-emerald-500'}`}>
                                                {(score * 100).toFixed(0)}%
                                            </div>
                                        </div>
                                        <div className="absolute bottom-0 left-0 h-1 bg-slate-700 w-full">
                                            <div
                                                className={`h-full transition-all duration-1000 ${score >= 0.7 ? 'bg-red-500' : score >= 0.4 ? 'bg-amber-500' : 'bg-emerald-500'}`}
                                                style={{ width: `${score * 100}%` }}
                                            ></div>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>

                        <div className="p-10 bg-slate-800/30 flex justify-end">
                            <button
                                onClick={() => setSelectedHistory(null)}
                                className="px-10 py-4 bg-white text-slate-950 font-black rounded-2xl transition-all hover:bg-slate-200 uppercase tracking-widest text-xs shadow-xl active:scale-95"
                            >
                                Secure Close
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default HistoryView;
