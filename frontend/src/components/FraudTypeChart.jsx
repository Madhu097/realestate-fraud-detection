import React from 'react';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend,
} from 'chart.js';
import { Bar } from 'react-chartjs-2';

ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend
);

const FraudTypeChart = ({ scores }) => {
    const data = {
        labels: Object.keys(scores),
        datasets: [
            {
                label: 'Fraud Score',
                data: Object.values(scores).map(s => (s * 100).toFixed(1)),
                backgroundColor: Object.values(scores).map(s => {
                    if (s >= 0.8) return 'rgba(239, 68, 68, 0.8)'; // red
                    if (s >= 0.6) return 'rgba(249, 115, 22, 0.8)'; // orange
                    if (s >= 0.4) return 'rgba(234, 179, 8, 0.8)'; // yellow
                    return 'rgba(34, 197, 94, 0.8)'; // green
                }),
                borderColor: Object.values(scores).map(s => {
                    if (s >= 0.8) return 'rgb(239, 68, 68)';
                    if (s >= 0.6) return 'rgb(249, 115, 22)';
                    if (s >= 0.4) return 'rgb(234, 179, 8)';
                    return 'rgb(34, 197, 94)';
                }),
                borderWidth: 1,
                borderRadius: 4,
            },
        ],
    };

    const options = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: false,
            },
            title: {
                display: false,
            },
            tooltip: {
                callbacks: {
                    label: (context) => `Probability: ${context.raw}%`,
                },
                backgroundColor: 'rgba(15, 23, 42, 0.9)',
                titleColor: '#94a3b8',
                bodyColor: '#f1f5f9',
                padding: 12,
                cornerRadius: 8,
            }
        },
        scales: {
            y: {
                beginAtZero: true,
                max: 100,
                grid: {
                    color: 'rgba(51, 65, 85, 0.5)',
                },
                ticks: {
                    color: '#94a3b8',
                    callback: (value) => `${value}%`,
                },
            },
            x: {
                grid: {
                    display: false,
                },
                ticks: {
                    color: '#94a3b8',
                },
            },
        },
    };

    return (
        <div className="bg-slate-800 p-6 rounded-xl shadow-lg border border-slate-700 h-[300px]">
            <h3 className="text-slate-400 text-sm font-medium mb-6 uppercase tracking-wider">Module Score Breakdown</h3>
            <div className="h-[200px]">
                <Bar data={data} options={options} />
            </div>
        </div>
    );
};

export default FraudTypeChart;
