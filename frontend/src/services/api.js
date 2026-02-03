import axios from 'axios';

// Backend API base URL - uses environment variable for production
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

// Create axios instance with default config
const apiClient = axios.create({
    baseURL: API_BASE_URL,
    timeout: 10000,
    headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    },
    withCredentials: true, // Important for CORS with credentials
});

// Request interceptor for debugging
apiClient.interceptors.request.use(
    (config) => {
        console.log('🚀 API Request:', config.method.toUpperCase(), config.url);
        return config;
    },
    (error) => {
        console.error('❌ Request Error:', error);
        return Promise.reject(error);
    }
);

// Response interceptor for debugging and error handling
apiClient.interceptors.response.use(
    (response) => {
        console.log('✅ API Response:', response.status, response.config.url);
        return response;
    },
    (error) => {
        if (error.response) {
            // Server responded with error status
            console.error('❌ API Error Response:', error.response.status, error.response.data);
        } else if (error.request) {
            // Request made but no response received
            console.error('❌ No Response from Server:', error.message);
            console.error('Check if backend is running on', API_BASE_URL);
        } else {
            // Error in request configuration
            console.error('❌ Request Configuration Error:', error.message);
        }
        return Promise.reject(error);
    }
);

// API Service functions
export const api = {
    // Health check
    healthCheck: async () => {
        const response = await apiClient.get('/');
        return response.data;
    },

    // Detailed health check
    detailedHealth: async () => {
        const response = await apiClient.get('/health');
        return response.data;
    },

    // Analyze listing
    analyzeListing: async (data) => {
        const response = await apiClient.post('/api/analyze', data);
        return response.data;
    },

    // Get analysis status
    getAnalysisStatus: async () => {
        const response = await apiClient.get('/api/analyze/status');
        return response.data;
    },
};

export default api;
