import React from 'react';

const AnalyzeForm = ({ listingData, handleChange, handleSubmit, loading }) => {
    return (
        <div className="max-w-4xl mx-auto bg-slate-900/40 backdrop-blur-xl border border-slate-800 rounded-[2.5rem] p-8 md:p-12 shadow-2xl relative overflow-hidden group">
            {/* Subtle background glow */}
            <div className="absolute -top-24 -right-24 w-64 h-64 bg-blue-600/10 rounded-full blur-3xl group-hover:bg-blue-600/15 transition-all duration-1000"></div>

            {/* Header */}
            <div className="relative mb-10">
                <div className="inline-block px-3 py-1 bg-blue-600/10 border border-blue-500/20 rounded-full text-[10px] font-black uppercase tracking-[0.2em] text-blue-400 mb-4">
                    Intelligence Input
                </div>
                <h2 className="text-3xl font-black text-white mb-3 tracking-tight">
                    Analyze Property Listing
                </h2>
                <p className="text-slate-400 text-sm leading-relaxed max-w-lg">
                    Input comprehensive property metrics to trigger our hybrid AI fraud detection sequence.
                </p>
            </div>

            {/* Form */}
            <form onSubmit={handleSubmit} className="relative space-y-6">
                {/* Property Title */}
                <div className="group/field">
                    <label className="block text-[10px] font-black uppercase tracking-[0.2em] text-slate-500 mb-2 group-focus-within/field:text-blue-400 transition-colors">
                        Property Title *
                    </label>
                    <input
                        type="text"
                        name="title"
                        value={listingData.title}
                        onChange={handleChange}
                        required
                        placeholder="e.g., Luxury 3BHK Apartment with Sea View"
                        className="w-full bg-slate-800/50 border border-slate-700/50 rounded-2xl px-5 py-4 text-white focus:ring-2 focus:ring-blue-600 focus:border-transparent transition-all outline-none font-medium placeholder:text-slate-600"
                    />
                </div>

                {/* Description */}
                <div className="group/field">
                    <label className="block text-[10px] font-black uppercase tracking-[0.2em] text-slate-500 mb-2 group-focus-within/field:text-blue-400 transition-colors">
                        Comprehensive Description *
                    </label>
                    <textarea
                        name="description"
                        value={listingData.description}
                        onChange={handleChange}
                        required
                        rows="4"
                        placeholder="Detail all amenities, constraints, and specific property features..."
                        className="w-full bg-slate-800/50 border border-slate-700/50 rounded-2xl px-5 py-4 text-white focus:ring-2 focus:ring-blue-600 focus:border-transparent transition-all outline-none resize-none font-medium placeholder:text-slate-600"
                    />
                </div>

                {/* Price and Area */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div className="group/field">
                        <label className="block text-[10px] font-black uppercase tracking-[0.2em] text-slate-500 mb-2 group-focus-within/field:text-blue-400 transition-colors">
                            List Price (₹) *
                        </label>
                        <input
                            type="number"
                            name="price"
                            value={listingData.price}
                            onChange={handleChange}
                            required
                            min="0"
                            step="1"
                            placeholder="5000000"
                            className="w-full bg-slate-800/50 border border-slate-700/50 rounded-2xl px-5 py-4 text-white focus:ring-2 focus:ring-blue-600 focus:border-transparent transition-all outline-none font-bold placeholder:text-slate-600"
                        />
                    </div>
                    <div className="group/field">
                        <label className="block text-[10px] font-black uppercase tracking-[0.2em] text-slate-500 mb-2 group-focus-within/field:text-blue-400 transition-colors">
                            Floor Area (sqft) *
                        </label>
                        <input
                            type="number"
                            name="area_sqft"
                            value={listingData.area_sqft}
                            onChange={handleChange}
                            required
                            min="0"
                            step="1"
                            placeholder="1200"
                            className="w-full bg-slate-800/50 border border-slate-700/50 rounded-2xl px-5 py-4 text-white focus:ring-2 focus:ring-blue-600 focus:border-transparent transition-all outline-none font-bold placeholder:text-slate-600"
                        />
                    </div>
                </div>

                {/* City and Locality */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div className="group/field">
                        <label className="block text-[10px] font-black uppercase tracking-[0.2em] text-slate-500 mb-2 group-focus-within/field:text-blue-400 transition-colors">
                            City *
                        </label>
                        <input
                            type="text"
                            name="city"
                            value={listingData.city}
                            onChange={handleChange}
                            required
                            placeholder="Mumbai"
                            className="w-full bg-slate-800/50 border border-slate-700/50 rounded-2xl px-5 py-4 text-white focus:ring-2 focus:ring-blue-600 focus:border-transparent transition-all outline-none font-medium placeholder:text-slate-600"
                        />
                    </div>
                    <div className="group/field">
                        <label className="block text-[10px] font-black uppercase tracking-[0.2em] text-slate-500 mb-2 group-focus-within/field:text-blue-400 transition-colors">
                            Specific Locality *
                        </label>
                        <input
                            type="text"
                            name="locality"
                            value={listingData.locality}
                            onChange={handleChange}
                            required
                            placeholder="Andheri West"
                            className="w-full bg-slate-800/50 border border-slate-700/50 rounded-2xl px-5 py-4 text-white focus:ring-2 focus:ring-blue-600 focus:border-transparent transition-all outline-none font-medium placeholder:text-slate-600"
                        />
                    </div>
                </div>

                {/* Coordinates */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div className="group/field">
                        <label className="block text-[10px] font-black uppercase tracking-[0.2em] text-slate-500 mb-2 group-focus-within/field:text-blue-400 transition-colors">
                            Latitude *
                        </label>
                        <input
                            type="number"
                            step="any"
                            name="latitude"
                            value={listingData.latitude}
                            onChange={handleChange}
                            required
                            min="-90"
                            max="90"
                            placeholder="19.1334"
                            className="w-full bg-slate-800/50 border border-slate-700/50 rounded-2xl px-5 py-4 text-white focus:ring-2 focus:ring-blue-600 focus:border-transparent transition-all outline-none font-mono text-sm placeholder:text-slate-600"
                        />
                    </div>
                    <div className="group/field">
                        <label className="block text-[10px] font-black uppercase tracking-[0.2em] text-slate-500 mb-2 group-focus-within/field:text-blue-400 transition-colors">
                            Longitude *
                        </label>
                        <input
                            type="number"
                            step="any"
                            name="longitude"
                            value={listingData.longitude}
                            onChange={handleChange}
                            required
                            min="-180"
                            max="180"
                            placeholder="72.8291"
                            className="w-full bg-slate-800/50 border border-slate-700/50 rounded-2xl px-5 py-4 text-white focus:ring-2 focus:ring-blue-600 focus:border-transparent transition-all outline-none font-mono text-sm placeholder:text-slate-600"
                        />
                    </div>
                </div>

                {/* Submit Button */}
                <div className="pt-6">
                    <button
                        type="submit"
                        disabled={loading}
                        className={`w-full py-5 rounded-[1.5rem] font-black text-xs uppercase tracking-[0.3em] text-white transition-all shadow-2xl relative overflow-hidden active:scale-[0.98] ${loading
                                ? 'bg-slate-800 cursor-not-allowed'
                                : 'bg-blue-600 hover:bg-blue-500 shadow-blue-600/20'
                            }`}
                    >
                        {loading ? (
                            <span className="flex items-center justify-center gap-4">
                                <div className="w-5 h-5 border-2 border-white/20 border-t-white rounded-full animate-spin"></div>
                                Running Hybrid Analysis...
                            </span>
                        ) : (
                            'Initialize Fraud Detection Sequence'
                        )}
                    </button>

                    {/* Security Badge */}
                    <p className="text-center text-[9px] text-slate-500 uppercase tracking-widest mt-6 font-bold opacity-50">
                        Secure Transmission • Real-time Validation
                    </p>
                </div>
            </form>
        </div>
    );
};

export default AnalyzeForm;
