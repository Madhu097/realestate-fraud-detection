import React, { useState, useMemo, useRef } from 'react';
import axios from 'axios';
import {
    Chart as ChartJS,
    ArcElement,
    Tooltip,
    Legend,
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    PointElement,
    LineElement,
    ScatterController,
    Filler
} from 'chart.js';
import { Doughnut, Bar, Line, Scatter } from 'react-chartjs-2';

ChartJS.register(
    ArcElement,
    Tooltip,
    Legend,
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    PointElement,
    LineElement,
    ScatterController,
    Filler
);

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

const CsvAnalyze = () => {
    const [file, setFile] = useState(null);
    const [loading, setLoading] = useState(false);
    const [results, setResults] = useState(null);
    const [metrics, setMetrics] = useState(null);
    const [eda, setEda] = useState(null);
    const [error, setError] = useState(null);
    const [searchTerm, setSearchTerm] = useState('');
    const fileInputRef = useRef(null);

    const handleFileChange = (e) => {
        const selectedFile = e.target.files[0];
        if (selectedFile && selectedFile.type === 'text/csv') {
            setFile(selectedFile);
            setError(null);
        } else {
            setError('Please select a valid CSV file.');
            setFile(null);
        }
    };

    const handleUpload = async () => {
        if (!file) return;
        setLoading(true);
        setError(null);
        setResults(null);
        setMetrics(null);

        const formData = new FormData();
        formData.append('file', file);

        console.log(`🚀 Sending request to: ${API_BASE_URL}/api/analyze/bulk`);

        try {
            const response = await axios.post(`${API_BASE_URL}/api/analyze/bulk`, formData, {
                headers: { 'Content-Type': 'multipart/form-data' }
            });
            setResults(response.data.data);
            setMetrics(response.data.metrics);
            setEda(response.data.eda);
        } catch (err) {
            console.error('Upload error:', err);
            const serverError = err.response?.data?.detail || err.response?.data?.message;
            setError(serverError || 'Connection error: Backend server is unreachable.');
        } finally {
            setLoading(false);
        }
    };

    const filteredResults = useMemo(() => {
        if (!results) return [];
        return results.filter(item =>
            Object.values(item).some(val =>
                String(val).toLowerCase().includes(searchTerm.toLowerCase())
            )
        );
    }, [results, searchTerm]);

    // Data for Charts
    const chartData = useMemo(() => {
        if (!results) return null;

        const realCount = results.filter(r => r.prediction === 'Real').length;
        const fakeCount = results.length - realCount;

        return {
            distribution: {
                labels: ['Real Listings', 'Fraudulent Listings'],
                datasets: [{
                    data: [realCount, fakeCount],
                    backgroundColor: ['#10b981', '#ef4444'],
                    borderColor: ['#064e3b', '#7f1d1d'],
                    borderWidth: 1,
                }]
            },
            confidence: {
                labels: results.slice(0, 10).map((_, i) => `L${i + 1}`),
                datasets: [{
                    label: 'Prediction Confidence (%)',
                    data: results.slice(0, 10).map(r => r.confidence),
                    backgroundColor: 'rgba(59, 130, 246, 0.5)',
                    borderColor: '#3b82f6',
                    borderWidth: 2,
                    tension: 0.4,
                    fill: true
                }]
            }
        };
    }, [results]);

    return (
        <div className="max-w-[1440px] mx-auto animate-in fade-in slide-in-from-bottom-4 duration-700">
            {/* Header Area */}
            <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-8 mb-12">
                <div>
                    <div className="flex items-center gap-3 mb-4">
                        <span className="px-3 py-1 bg-blue-500/10 text-blue-500 text-[10px] font-black uppercase tracking-widest rounded-full border border-blue-500/20">
                            Enterprise Engine v2.4
                        </span>
                        <span className="px-3 py-1 bg-emerald-500/10 text-emerald-500 text-[10px] font-black uppercase tracking-widest rounded-full border border-emerald-500/20">
                            Hybrid ExtraTree+ANN
                        </span>
                    </div>
                    <h1 className="text-4xl md:text-6xl font-black text-white mb-4 tracking-tighter">
                        AI <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-500 to-indigo-400">Deep Analysis</span>
                    </h1>
                    <p className="text-slate-400 max-w-xl leading-relaxed text-lg">
                        Processing datasets through 142 neural features to identify pattern-based fraud and pricing manipulation.
                    </p>
                </div>

                <div className="flex flex-col sm:flex-row gap-4 bg-slate-900/50 p-6 rounded-3xl border border-slate-800 backdrop-blur-xl">
                    <input
                        type="file"
                        ref={fileInputRef}
                        onChange={handleFileChange}
                        accept=".csv"
                        className="hidden"
                    />
                    <button
                        onClick={() => fileInputRef.current.click()}
                        className="px-6 py-4 bg-slate-800 border border-slate-700 rounded-2xl font-bold flex items-center gap-3 hover:bg-slate-700 transition-all cursor-pointer group"
                    >
                        <UploadIcon className="text-blue-500 group-hover:scale-110 transition-transform" />
                        <span className="text-slate-200">{file ? file.name.slice(0, 15) + '...' : 'Select Dataset'}</span>
                    </button>

                    <button
                        onClick={handleUpload}
                        disabled={!file || loading}
                        className={`px-8 py-4 bg-blue-600 text-white rounded-2xl font-extrabold flex items-center gap-3 transition-all ${(!file || loading) ? 'opacity-50 cursor-not-allowed' : 'hover:bg-blue-500 hover:shadow-2xl hover:shadow-blue-500/40 active:scale-95 cursor-pointer'}`}
                    >
                        {loading ? <Spinner /> : <ActivityIcon />}
                        {loading ? 'Processing Neural Net...' : 'Run Deep Analysis'}
                    </button>
                </div>
            </div>

            {error && <ErrorBanner message={error} />}

            {results && metrics && (
                <div className="space-y-8">
                    {/* Top Stats Dashboard */}
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                        <MetricCard label="Hybrid System Accuracy" value={`${metrics.model_accuracy}%`} sub="Overall Ensemble Performance" color="blue" />
                        <MetricCard label="Prediction Confidence" value={`${metrics.average_confidence}%`} sub="Avg. Certainty Level" color="indigo" />
                        <MetricCard label="Genuine Listings" value={`${metrics.real_percentage}%`} sub="Verified Safely" color="emerald" />
                        <MetricCard label="Anomalies Found" value={`${metrics.fake_percentage}%`} sub="High Risk Detected" color="red" />
                    </div>

                    {/* NEW: Sub-Model Accuracy Breakdown */}
                    <div className="bg-slate-900/60 border border-slate-800 p-8 rounded-3xl shadow-2xl">
                        <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 gap-4">
                            <div>
                                <h3 className="text-2xl font-black text-white tracking-tight flex items-center gap-3">
                                    <div className="w-2 h-8 bg-gradient-to-b from-blue-500 to-indigo-600 rounded-full"></div>
                                    Model Intelligence Breakdown
                                </h3>
                                <p className="text-slate-500 text-sm mt-1">Individual performance metrics for each neural layer.</p>
                            </div>
                            <div className="flex items-center gap-2 bg-slate-950 px-4 py-2 rounded-xl border border-slate-800">
                                <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></div>
                                <span className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Logic: Weighted Fusion</span>
                            </div>
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                            {metrics.sub_models?.map((m, i) => (
                                <div key={i} className="group p-6 rounded-2xl bg-slate-950/50 border border-slate-800/50 hover:border-blue-500/30 transition-all duration-300">
                                    <div className="flex justify-between items-start mb-4">
                                        <span className="text-[10px] font-black uppercase tracking-widest text-blue-500">{m.status}</span>
                                        <span className="text-xs font-bold text-slate-600">Weight: {m.weight}</span>
                                    </div>
                                    <h4 className="text-white font-bold text-lg mb-2">{m.name}</h4>
                                    <div className="flex items-end gap-2">
                                        <span className="text-3xl font-black text-white group-hover:text-blue-400 transition-colors">{m.accuracy}%</span>
                                        <span className="text-[10px] text-slate-500 mb-1.5 font-bold uppercase tracking-tighter">Accuracy</span>
                                    </div>
                                    <div className="mt-4 h-1.5 bg-slate-900 rounded-full overflow-hidden">
                                        <div
                                            className="h-full bg-gradient-to-r from-blue-600 to-indigo-500 rounded-full transition-all duration-1000 delay-300"
                                            style={{ width: `${m.accuracy}%` }}
                                        ></div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>

                    {/* NEW: EDA Analysis Dashboard */}
                    {eda && (
                        <div className="space-y-8 mt-12">
                            <div className="flex items-center gap-3">
                                <div className="w-2 h-8 bg-emerald-500 rounded-full"></div>
                                <h2 className="text-3xl font-black text-white tracking-tight">Exploratory Data Analysis (EDA)</h2>
                            </div>

                            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                                {/* Monthly Rent Distribution */}
                                <div className="bg-slate-900/40 backdrop-blur-xl border border-slate-800 p-8 rounded-3xl">
                                    <h3 className="text-white font-bold mb-6 flex items-center gap-2">Monthly Rent Distribution</h3>
                                    <div className="h-[250px]">
                                        <Bar
                                            data={{
                                                labels: eda.rent_dist?.labels || [],
                                                datasets: [{
                                                    label: 'Density',
                                                    data: eda.rent_dist?.values || [],
                                                    backgroundColor: 'rgba(16, 185, 129, 0.5)',
                                                    borderColor: '#10b981',
                                                    borderWidth: 1,
                                                }]
                                            }}
                                            options={{ responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } } }}
                                        />
                                    </div>
                                </div>

                                {/* Rooms vs Floors Scatter */}
                                <div className="bg-slate-900/40 backdrop-blur-xl border border-slate-800 p-8 rounded-3xl">
                                    <h3 className="text-white font-bold mb-6 flex items-center gap-2">Rooms vs Floors</h3>
                                    <div className="h-[250px]">
                                        <Scatter
                                            data={{
                                                datasets: [{
                                                    label: 'Properties',
                                                    data: eda.rooms_vs_floors || [],
                                                    backgroundColor: '#3b82f6',
                                                }]
                                            }}
                                            options={{
                                                responsive: true,
                                                maintainAspectRatio: false,
                                                scales: {
                                                    x: { title: { display: true, text: 'Total Floors', color: '#64748b' } },
                                                    y: { title: { display: true, text: 'Number of Rooms', color: '#64748b' } }
                                                }
                                            }}
                                        />
                                    </div>
                                </div>

                                {/* Rent vs Label */}
                                <div className="bg-slate-900/40 backdrop-blur-xl border border-slate-800 p-8 rounded-3xl">
                                    <h3 className="text-white font-bold mb-6 flex items-center gap-2">Rent vs Label</h3>
                                    <div className="h-[250px]">
                                        <Bar
                                            data={{
                                                labels: ['Real Listing', 'Fake Listing'],
                                                datasets: [{
                                                    label: 'Monthly Rent',
                                                    data: [eda.rent_vs_label?.Real || 0, eda.rent_vs_label?.Fake || 0],
                                                    backgroundColor: ['#10b981', '#ef4444'],
                                                }]
                                            }}
                                            options={{ responsive: true, maintainAspectRatio: false }}
                                        />
                                    </div>
                                </div>

                                {/* Correlation Matrix (Custom Grid) */}
                                <div className="lg:col-span-2 bg-slate-900/40 backdrop-blur-xl border border-slate-800 p-8 rounded-3xl">
                                    <h3 className="text-white font-bold mb-6 flex items-center gap-2">Correlation Matrix</h3>
                                    <div className="overflow-x-auto">
                                        <div className="min-w-[500px]">
                                            <div className="grid grid-cols-[120px_repeat(auto-fill,minmax(60px,1fr))]">
                                                <div className="h-10"></div>
                                                {eda.correlation?.labels.map(l => (
                                                    <div key={l} className="text-[10px] text-slate-500 font-bold truncate p-1 rotate-[-45deg]">{l}</div>
                                                ))}
                                                {eda.correlation?.values.map((row, i) => (
                                                    <React.Fragment key={i}>
                                                        <div className="text-[10px] text-slate-400 font-bold p-2 border-b border-slate-800/50 truncate">
                                                            {eda.correlation.labels[i]}
                                                        </div>
                                                        {row.map((val, j) => (
                                                            <div
                                                                key={j}
                                                                className="h-10 flex items-center justify-center text-[10px] font-bold border-b border-r border-slate-800/30"
                                                                style={{
                                                                    backgroundColor: `rgba(59, 130, 246, ${Math.abs(val)})`,
                                                                    color: Math.abs(val) > 0.5 ? 'white' : 'slate-400'
                                                                }}
                                                            >
                                                                {val}
                                                            </div>
                                                        ))}
                                                    </React.Fragment>
                                                ))}
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    )}

                    {/* Visualization Section */}
                    <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                        {/* Doughnut Chart - Distribution */}
                        <div className="lg:col-span-1 bg-slate-900/40 backdrop-blur-xl border border-slate-800 p-8 rounded-3xl">
                            <h3 className="text-white font-bold mb-8 flex items-center gap-2">
                                <div className="w-1.5 h-6 bg-blue-500 rounded-full"></div>
                                Fraud Distribution
                            </h3>
                            <div className="h-[250px] flex items-center justify-center">
                                <Doughnut
                                    data={chartData.distribution}
                                    options={{ cutout: '75%', plugins: { legend: { display: false } } }}
                                />
                            </div>
                            <div className="mt-8 space-y-3">
                                <LegendItem color="#10b981" label="Genuine" value={metrics.real_percentage + '%'} />
                                <LegendItem color="#ef4444" label="Suspicious" value={metrics.fake_percentage + '%'} />
                            </div>
                        </div>

                        {/* Bar Chart - Confidence Samples */}
                        <div className="lg:col-span-2 bg-slate-900/40 backdrop-blur-xl border border-slate-800 p-8 rounded-3xl">
                            <h3 className="text-white font-bold mb-8 flex items-center gap-2">
                                <div className="w-1.5 h-6 bg-indigo-500 rounded-full"></div>
                                Neural Confidence Samples (First 10)
                            </h3>
                            <div className="h-[300px]">
                                <Bar
                                    data={chartData.confidence}
                                    options={{
                                        responsive: true,
                                        maintainAspectRatio: false,
                                        scales: {
                                            y: { beginAtZero: true, max: 100, grid: { color: 'rgba(255,255,255,0.05)' } },
                                            x: { grid: { display: false } }
                                        },
                                        plugins: { legend: { display: false } }
                                    }}
                                />
                            </div>
                        </div>
                    </div>

                    {/* Detailed Data Table */}
                    <div className="bg-slate-900/30 backdrop-blur-sm border border-slate-800 rounded-3xl overflow-hidden shadow-2xl">
                        <div className="p-8 border-b border-slate-800 flex flex-col sm:flex-row justify-between items-center gap-4">
                            <h3 className="text-xl font-bold text-white tracking-tight">Raw Classification Stream</h3>
                            <div className="relative w-full sm:w-80">
                                <input
                                    type="text"
                                    placeholder="Instant Filter..."
                                    value={searchTerm}
                                    onChange={(e) => setSearchTerm(e.target.value)}
                                    className="w-full bg-slate-950/50 border border-slate-700/50 rounded-xl py-2.5 pl-10 pr-4 text-sm text-white focus:outline-none focus:ring-2 focus:ring-blue-500/20 transition-all"
                                />
                                <SearchIcon className="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-500" />
                            </div>
                        </div>
                        <div className="overflow-x-auto">
                            <table className="w-full text-left border-separate border-spacing-0">
                                <thead className="bg-slate-950/40">
                                    <tr>
                                        <th className="px-8 py-5 text-[10px] font-black uppercase tracking-widest text-slate-500 border-b border-slate-800">Status</th>
                                        <th className="px-8 py-5 text-[10px] font-black uppercase tracking-widest text-slate-500 border-b border-slate-800">Confidence</th>
                                        {results.length > 0 && Object.keys(results[0]).filter(k => k !== 'prediction' && k !== 'confidence').map(key => (
                                            <th key={key} className="px-8 py-5 text-[10px] font-black uppercase tracking-widest text-slate-500 border-b border-slate-800">
                                                {key.replace('_', ' ')}
                                            </th>
                                        ))}
                                    </tr>
                                </thead>
                                <tbody>
                                    {filteredResults.map((row, idx) => (
                                        <tr key={idx} className="hover:bg-blue-500/5 transition-colors group">
                                            <td className="px-8 py-6 border-b border-slate-800/50">
                                                <span className={`px-4 py-1.5 rounded-lg text-[10px] font-black uppercase tracking-wider ${row.prediction === 'Real'
                                                    ? 'bg-emerald-900/20 text-emerald-400 border border-emerald-500/20'
                                                    : 'bg-red-900/20 text-red-400 border border-red-500/20'
                                                    }`}>
                                                    {row.prediction}
                                                </span>
                                            </td>
                                            <td className="px-8 py-6 border-b border-slate-800/50">
                                                <div className="flex items-center gap-3">
                                                    <div className="flex-1 h-1.5 w-16 bg-slate-800 rounded-full overflow-hidden">
                                                        <div
                                                            className={`h-full rounded-full ${row.confidence > 80 ? 'bg-emerald-500' : 'bg-blue-500'}`}
                                                            style={{ width: `${row.confidence}%` }}
                                                        ></div>
                                                    </div>
                                                    <span className="text-xs font-bold text-slate-400">{row.confidence}%</span>
                                                </div>
                                            </td>
                                            {Object.entries(row).filter(([k]) => k !== 'prediction' && k !== 'confidence').map(([key, value], i) => (
                                                <td key={i} className="px-8 py-6 border-b border-slate-800/50 text-sm">
                                                    <span className="text-slate-300 group-hover:text-white transition-colors">
                                                        {String(value)}
                                                    </span>
                                                </td>
                                            ))}
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            )}

            {!results && !loading && <EmptyState onSelect={() => fileInputRef.current.click()} />}
        </div>
    );
};

// --- Styled Components ---

const MetricCard = ({ label, value, sub, color }) => {
    const colors = {
        blue: 'text-blue-400 bg-blue-500/10 border-blue-500/20',
        indigo: 'text-indigo-400 bg-indigo-500/10 border-indigo-500/20',
        emerald: 'text-emerald-400 bg-emerald-500/10 border-emerald-500/20',
        red: 'text-red-400 bg-red-500/10 border-red-500/20',
    };
    return (
        <div className="bg-slate-900/60 p-6 rounded-3xl border border-slate-800 shadow-xl">
            <p className="text-slate-500 text-[10px] font-black uppercase tracking-widest mb-3">{label}</p>
            <div className="flex items-end justify-between">
                <div>
                    <h3 className={`text-4xl font-black ${colors[color].split(' ')[0]}`}>{value}</h3>
                    <p className="text-slate-500 text-xs mt-1">{sub}</p>
                </div>
                <div className={`p-2 rounded-xl border ${colors[color]}`}>
                    <ActivityIcon size={20} />
                </div>
            </div>
        </div>
    );
};

const LegendItem = ({ color, label, value }) => (
    <div className="flex items-center justify-between p-3 rounded-xl bg-slate-950/40 border border-slate-800/50">
        <div className="flex items-center gap-3">
            <div className="w-3 h-3 rounded-full" style={{ backgroundColor: color }}></div>
            <span className="text-xs font-bold text-slate-400">{label}</span>
        </div>
        <span className="text-xs font-black text-white">{value}</span>
    </div>
);

const EmptyState = ({ onSelect }) => (
    <div className="py-32 flex flex-col items-center justify-center border-4 border-dashed border-slate-900 rounded-[3rem] bg-slate-950/20 group hover:border-blue-900/30 transition-all cursor-pointer" onClick={onSelect}>
        <div className="w-20 h-20 bg-slate-900 rounded-3xl flex items-center justify-center mb-8 group-hover:bg-blue-600/20 group-hover:scale-110 transition-all duration-500">
            <UploadIcon size={32} className="text-slate-500 group-hover:text-blue-500" />
        </div>
        <p className="text-2xl text-slate-400 font-extrabold tracking-tight">Neural Dataset Upload</p>
        <p className="text-slate-600 mt-2 font-medium">Click to browse or drag & drop CSV files</p>
    </div>
);

const ErrorBanner = ({ message }) => (
    <div className="mb-12 bg-red-950/30 border border-red-500/20 p-6 rounded-3xl text-red-400 flex items-center gap-4 animate-in fade-in zoom-in-95">
        <div className="p-2 bg-red-500/10 rounded-xl"><InfoIcon /></div>
        <div>
            <p className="font-black text-xs uppercase tracking-widest mb-1">Neural Error</p>
            <p className="text-sm font-medium">{message}</p>
        </div>
    </div>
);

// --- Icons & UI Parts ---
const UploadIcon = ({ size = 24, className }) => (
    <svg width={size} height={size} className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" /><polyline points="17 8 12 3 7 8" /><line x1="12" y1="3" x2="12" y2="15" /></svg>
);
const ActivityIcon = ({ size = 24, className }) => (
    <svg width={size} height={size} className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12" /></svg>
);
const SearchIcon = ({ size = 18, className }) => (
    <svg width={size} height={size} className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="11" cy="11" r="8" /><line x1="21" y1="21" x2="16.65" y2="16.65" /></svg>
);
const InfoIcon = () => (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="10" /><line x1="12" y1="8" x2="12" y2="12" /><line x1="12" y1="16" x2="12.01" y2="16" /></svg>
);
const Spinner = () => (
    <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
);

export default CsvAnalyze;
