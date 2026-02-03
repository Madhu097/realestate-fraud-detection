import React, { useState } from 'react';
import axios from 'axios';
import AnalyzeForm from './components/AnalyzeForm';
import ResultDashboard from './components/ResultDashboard';
import HistoryView from './components/HistoryView';
import './index.css';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

function App() {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [fraudReport, setFraudReport] = useState(null);
    const [currentView, setCurrentView] = useState('analyze'); // 'analyze' or 'history'
    const [listingData, setListingData] = useState({
        title: '',
        description: '',
        price: '',
        area_sqft: '',
        city: '',
        locality: '',
        latitude: '',
        longitude: ''
    });

    const handleChange = (e) => {
        const { name, value } = e.target;
        setListingData(prev => ({ ...prev, [name]: value }));
        // Clear error when user starts typing
        if (error) setError(null);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);
        setFraudReport(null);

        const payload = {
            listing_data: {
                ...listingData,
                price: parseFloat(listingData.price),
                area_sqft: parseFloat(listingData.area_sqft),
                latitude: parseFloat(listingData.latitude),
                longitude: parseFloat(listingData.longitude)
            }
        };

        try {
            const response = await axios.post(`${API_BASE_URL}/api/analyze`, payload);

            // Handle both old and new response formats
            const reportData = response.data.data || response.data;
            setFraudReport(reportData);

            // AUTO-SAVE to History
            try {
                await axios.post(`${API_BASE_URL}/api/history`, {
                    listing_data: payload.listing_data,
                    analysis_results: reportData
                });
            } catch (historyErr) {
                console.warn('Failed to save to history:', historyErr);
                // Don't show error to user, history save is non-critical
            }
        } catch (err) {
            console.error('Analysis error:', err);

            // Handle different error response formats
            let errorMessage = 'Analysis service error. Please try again.';

            if (err.response?.data) {
                const errorData = err.response.data;
                if (errorData.message) {
                    errorMessage = errorData.message;
                } else if (errorData.detail) {
                    errorMessage = errorData.detail;
                } else if (errorData.validation_errors) {
                    errorMessage = errorData.validation_errors
                        .map(e => `${e.field}: ${e.message}`)
                        .join(', ');
                }
            } else if (err.message) {
                errorMessage = err.message;
            }

            setError(errorMessage);
        } finally {
            setLoading(false);
        }
    };

    const handleBack = () => {
        setFraudReport(null);
        setError(null);
    };

    const handleViewChange = (view) => {
        setCurrentView(view);
        setFraudReport(null);
        setError(null);
    };

    return (
        <div className="min-h-screen bg-slate-950 text-slate-200 font-sans selection:bg-blue-500/30">
            {/* Header */}
            <header className="border-b border-slate-800 bg-slate-950/80 backdrop-blur-md sticky top-0 z-50">
                <div className="max-w-[1440px] mx-auto px-4 sm:px-8 h-20 flex items-center justify-between">
                    <div className="flex items-center gap-2">
                        <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center font-bold text-white shadow-lg shadow-blue-500/20">
                            T
                        </div>
                        <span className="text-lg font-bold tracking-tight text-white italic">
                            Truth<span className="text-blue-500">In</span>Listings
                        </span>
                    </div>

                    <nav className="hidden md:flex items-center gap-10 text-[10px] font-black uppercase tracking-[0.2em] text-slate-500">
                        <button
                            className={`${currentView === 'analyze'
                                ? 'text-blue-500 border-b-2 border-blue-600'
                                : 'hover:text-white'
                                } cursor-pointer transition-all pb-2 focus:outline-none`}
                            onClick={() => handleViewChange('analyze')}
                        >
                            Real Estate Analytics
                        </button>
                        <button
                            className={`${currentView === 'history'
                                ? 'text-blue-500 border-b-2 border-blue-600'
                                : 'hover:text-white'
                                } cursor-pointer transition-all pb-2 focus:outline-none`}
                            onClick={() => handleViewChange('history')}
                        >
                            Fraud Database
                        </button>
                    </nav>
                </div>
            </header>

            {/* Main Content */}
            <main className="max-w-[1440px] mx-auto py-8 sm:py-16 px-4 sm:px-8">
                {currentView === 'analyze' ? (
                    !fraudReport ? (
                        <div className="animate-in fade-in slide-in-from-bottom-4 duration-700">
                            {/* Hero Section */}
                            <div className="text-center mb-12">
                                <h1 className="text-4xl md:text-5xl font-black text-white mb-4 tracking-tight">
                                    Expose Real Estate <span className="text-blue-500">Fraud</span>
                                </h1>
                                <p className="text-slate-400 max-w-xl mx-auto leading-relaxed">
                                    Our hybrid AI engine analyzes price distribution, description manipulation,
                                    image metadata, and geospatial accuracy to protect your investment.
                                </p>
                            </div>

                            {/* Form */}
                            <AnalyzeForm
                                listingData={listingData}
                                handleChange={handleChange}
                                handleSubmit={handleSubmit}
                                loading={loading}
                            />

                            {/* Error Message */}
                            {error && (
                                <div className="max-w-2xl mx-auto mt-6 bg-red-900/20 border border-red-800/50 p-4 rounded-xl flex items-start gap-3 text-red-400 animate-in fade-in slide-in-from-top-2 duration-300">
                                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 flex-shrink-0 mt-0.5" viewBox="0 0 20 20" fill="currentColor">
                                        <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                                    </svg>
                                    <div className="flex-1">
                                        <p className="text-sm font-medium">{error}</p>
                                    </div>
                                    <button
                                        onClick={() => setError(null)}
                                        className="text-red-400 hover:text-red-300 transition-colors focus:outline-none"
                                        aria-label="Dismiss error"
                                    >
                                        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                                            <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
                                        </svg>
                                    </button>
                                </div>
                            )}
                        </div>
                    ) : (
                        <ResultDashboard
                            result={fraudReport}
                            listingData={listingData}
                            onBack={handleBack}
                        />
                    )
                ) : (
                    <HistoryView
                        onBack={() => handleViewChange('analyze')}
                        apiBaseUrl={API_BASE_URL}
                    />
                )}
            </main>

            {/* Footer */}
            <footer className="mt-20 border-t border-slate-900 py-12 text-center text-slate-600 max-w-[1440px] mx-auto px-8">
                <p className="text-[10px] uppercase tracking-[0.4em] font-bold opacity-50">
                    Hybrid AI Fraud Detection System v2.1.0 • Built for Academic Evaluation
                </p>
            </footer>
        </div>
    );
}

export default App;
