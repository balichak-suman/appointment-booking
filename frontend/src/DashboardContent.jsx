import React, { useState, useEffect } from 'react';
import {
    BarChart, Bar, XAxis, YAxis, CartesianGrid,
    Tooltip, Legend, ResponsiveContainer, Area, AreaChart
} from 'recharts';
import {
    Users, UserCheck, Calendar, DollarSign,
    TrendingUp, TrendingDown, ChevronLeft, ChevronRight
} from 'lucide-react';
import './Dashboard.css';
import axios from 'axios';

const DashboardContent = () => {
    const [activeTab, setActiveTab] = useState('admin');
    const [dashboardData, setDashboardData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [currentMonth, setCurrentMonth] = useState(new Date());

    useEffect(() => {
        fetchDashboardData();
    }, []);

    const fetchDashboardData = async () => {
        try {
            const response = await axios.get(`${import.meta.env.VITE_API_URL || 'http://localhost:8001'}/api/dashboard`);
            setDashboardData(response.data);
            setLoading(false);
        } catch (error) {
            console.error('Error fetching dashboard data:', error);
            setLoading(false);
        }
    };

    const getMockData = () => {
        return {
            summary: {
                doctors: { count: 247, change: '+5%', period: 'in last 7 Days' },
                patients: { count: 4178, change: '+25%', period: 'in last 7 Days' },
                appointments: { count: 12178, change: '-8%', period: 'in last 7 Days' },
                revenue: { amount: '$55,1240', change: '+3%', period: 'in last 7 Days' }
            },
            appointmentStats: {
                total: 6314,
                cancelled: 456,
                rescheduled: 745,
                completed: 4578,
                walkIn: 234
            },
            monthlyData: [
                { month: 'Jan', completed: 420, ongoing: 150, rescheduled: 80 },
                { month: 'Feb', completed: 380, ongoing: 120, rescheduled: 65 },
                { month: 'Mar', completed: 450, ongoing: 180, rescheduled: 90 },
                { month: 'Apr', completed: 480, ongoing: 200, rescheduled: 95 },
                { month: 'May', completed: 520, ongoing: 160, rescheduled: 75 },
                { month: 'Jun', completed: 390, ongoing: 140, rescheduled: 70 },
                { month: 'Jul', completed: 410, ongoing: 170, rescheduled: 85 },
                { month: 'Aug', completed: 490, ongoing: 190, rescheduled: 100 },
                { month: 'Sep', completed: 510, ongoing: 210, rescheduled: 88 },
                { month: 'Oct', completed: 470, ongoing: 175, rescheduled: 92 }
            ]
        };
    };

    const generateMiniChartData = () => {
        return Array.from({ length: 7 }, (_, i) => ({
            day: i + 1,
            value: Math.floor(Math.random() * 100) + 50
        }));
    };

    const renderCalendar = () => {
        const year = currentMonth.getFullYear();
        const month = currentMonth.getMonth();
        const firstDay = new Date(year, month, 1).getDay();
        const daysInMonth = new Date(year, month + 1, 0).getDate();
        const today = new Date();

        const days = [];
        const dayHeaders = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

        dayHeaders.forEach(day => {
            days.push(
                <div key={`header-${day}`} className="calendar-day-header">
                    {day}
                </div>
            );
        });

        for (let i = 0; i < firstDay; i++) {
            days.push(<div key={`empty-${i}`} className="calendar-day"></div>);
        }

        for (let day = 1; day <= daysInMonth; day++) {
            const isToday =
                day === today.getDate() &&
                month === today.getMonth() &&
                year === today.getFullYear();

            const hasAppointments = Math.random() > 0.5;

            days.push(
                <div
                    key={`day-${day}`}
                    className={`calendar-day ${isToday ? 'today' : ''} ${hasAppointments ? 'has-appointments' : ''}`}
                >
                    {day}
                </div>
            );
        }

        return days;
    };

    const changeMonth = (direction) => {
        setCurrentMonth(prev => {
            const newDate = new Date(prev);
            newDate.setMonth(prev.getMonth() + direction);
            return newDate;
        });
    };

    if (loading || !dashboardData) {
        return (
            <div className="loading">
                <div className="spinner"></div>
            </div>
        );
    }

    const { summary, appointmentStats, monthlyData } = dashboardData;

    return (
        <div className="dashboard">
            <div className="dashboard-container">
                {/* Navigation Tabs */}
                <nav className="dashboard-nav">
                    <div
                        className={`nav-item ${activeTab === 'admin' ? 'active' : ''}`}
                        onClick={() => setActiveTab('admin')}
                    >
                        Admin Dashboard
                    </div>
                    <div
                        className={`nav-item ${activeTab === 'doctor' ? 'active' : ''}`}
                        onClick={() => setActiveTab('doctor')}
                    >
                        Doctor Dashboard
                    </div>
                    <div
                        className={`nav-item ${activeTab === 'patient' ? 'active' : ''}`}
                        onClick={() => setActiveTab('patient')}
                    >
                        Patient Dashboard
                    </div>
                </nav>

                {/* Summary Cards */}
                <div className="summary-cards">
                    <div className="summary-card">
                        <div className="card-header">
                            <div>
                                <div className="card-label">Doctors</div>
                                <div className="card-period">{summary.doctors.period}</div>
                            </div>
                            <div className="card-icon icon-doctors">
                                <Users size={24} />
                            </div>
                        </div>
                        <div className="card-value">{summary.doctors.count}</div>
                        <div className="card-footer">
                            <div className={`trend-indicator ${summary.doctors.change.startsWith('+') ? 'trend-up' : 'trend-down'}`}>
                                {summary.doctors.change.startsWith('+') ? <TrendingUp size={16} /> : <TrendingDown size={16} />}
                                {summary.doctors.change}
                            </div>
                            <div className="mini-chart">
                                <ResponsiveContainer width="100%" height="100%">
                                    <AreaChart data={generateMiniChartData()}>
                                        <Area type="monotone" dataKey="value" stroke="#667eea" fill="#667eea" fillOpacity={0.3} />
                                    </AreaChart>
                                </ResponsiveContainer>
                            </div>
                        </div>
                    </div>

                    <div className="summary-card">
                        <div className="card-header">
                            <div>
                                <div className="card-label">Patients</div>
                                <div className="card-period">{summary.patients.period}</div>
                            </div>
                            <div className="card-icon icon-patients">
                                <UserCheck size={24} />
                            </div>
                        </div>
                        <div className="card-value">{summary.patients.count}</div>
                        <div className="card-footer">
                            <div className={`trend-indicator ${summary.patients.change.startsWith('+') ? 'trend-up' : 'trend-down'}`}>
                                {summary.patients.change.startsWith('+') ? <TrendingUp size={16} /> : <TrendingDown size={16} />}
                                {summary.patients.change}
                            </div>
                            <div className="mini-chart">
                                <ResponsiveContainer width="100%" height="100%">
                                    <AreaChart data={generateMiniChartData()}>
                                        <Area type="monotone" dataKey="value" stroke="#f5576c" fill="#f5576c" fillOpacity={0.3} />
                                    </AreaChart>
                                </ResponsiveContainer>
                            </div>
                        </div>
                    </div>

                    <div className="summary-card">
                        <div className="card-header">
                            <div>
                                <div className="card-label">Appointment</div>
                                <div className="card-period">{summary.appointments.period}</div>
                            </div>
                            <div className="card-icon icon-appointments">
                                <Calendar size={24} />
                            </div>
                        </div>
                        <div className="card-value">{summary.appointments.count}</div>
                        <div className="card-footer">
                            <div className={`trend-indicator ${summary.appointments.change.startsWith('+') ? 'trend-up' : 'trend-down'}`}>
                                {summary.appointments.change.startsWith('+') ? <TrendingUp size={16} /> : <TrendingDown size={16} />}
                                {summary.appointments.change}
                            </div>
                            <div className="mini-chart">
                                <ResponsiveContainer width="100%" height="100%">
                                    <AreaChart data={generateMiniChartData()}>
                                        <Area type="monotone" dataKey="value" stroke="#00f2fe" fill="#00f2fe" fillOpacity={0.3} />
                                    </AreaChart>
                                </ResponsiveContainer>
                            </div>
                        </div>
                    </div>

                    <div className="summary-card">
                        <div className="card-header">
                            <div>
                                <div className="card-label">Revenue</div>
                                <div className="card-period">{summary.revenue.period}</div>
                            </div>
                            <div className="card-icon icon-revenue">
                                <DollarSign size={24} />
                            </div>
                        </div>
                        <div className="card-value">{summary.revenue.amount}</div>
                        <div className="card-footer">
                            <div className={`trend-indicator ${summary.revenue.change.startsWith('+') ? 'trend-up' : 'trend-down'}`}>
                                {summary.revenue.change.startsWith('+') ? <TrendingUp size={16} /> : <TrendingDown size={16} />}
                                {summary.revenue.change}
                            </div>
                            <div className="mini-chart">
                                <ResponsiveContainer width="100%" height="100%">
                                    <AreaChart data={generateMiniChartData()}>
                                        <Area type="monotone" dataKey="value" stroke="#38f9d7" fill="#38f9d7" fillOpacity={0.3} />
                                    </AreaChart>
                                </ResponsiveContainer>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Stats Section */}
                <div className="stats-section">
                    <div className="stats-card">
                        <div className="stats-header">
                            <h2 className="stats-title">Appointment Statistics</h2>
                            <select className="stats-filter">
                                <option>Monthly</option>
                                <option>Weekly</option>
                                <option>Daily</option>
                            </select>
                        </div>

                        <div className="stats-metrics">
                            <div className="metric">
                                <div className="metric-label">
                                    <span className="metric-dot dot-all"></span>
                                    All Appointments
                                </div>
                                <div className="metric-value">{appointmentStats.total}</div>
                            </div>
                            <div className="metric">
                                <div className="metric-label">
                                    <span className="metric-dot dot-cancelled"></span>
                                    Cancelled
                                </div>
                                <div className="metric-value">{appointmentStats.cancelled}</div>
                            </div>
                            <div className="metric">
                                <div className="metric-label">
                                    <span className="metric-dot dot-rescheduled"></span>
                                    Rescheduled
                                </div>
                                <div className="metric-value">{appointmentStats.rescheduled}</div>
                            </div>
                            <div className="metric">
                                <div className="metric-label">
                                    <span className="metric-dot dot-completed"></span>
                                    Completed
                                </div>
                                <div className="metric-value">{appointmentStats.completed}</div>
                            </div>
                        </div>

                        <div className="chart-container">
                            <ResponsiveContainer width="100%" height="100%">
                                <BarChart data={monthlyData}>
                                    <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                                    <XAxis dataKey="month" stroke="#94a3b8" />
                                    <YAxis stroke="#94a3b8" />
                                    <Tooltip
                                        contentStyle={{
                                            background: 'white',
                                            border: '1px solid #e2e8f0',
                                            borderRadius: '8px',
                                            boxShadow: '0 4px 6px rgba(0,0,0,0.1)'
                                        }}
                                    />
                                    <Legend />
                                    <Bar dataKey="completed" fill="#06B6D4" radius={[8, 8, 0, 0]} />
                                    <Bar dataKey="ongoing" fill="#4F46E5" radius={[8, 8, 0, 0]} />
                                    <Bar dataKey="rescheduled" fill="#8B5CF6" radius={[8, 8, 0, 0]} />
                                </BarChart>
                            </ResponsiveContainer>
                        </div>
                    </div>

                    {/* Calendar */}
                    <div className="calendar-card">
                        <div className="stats-header">
                            <h2 className="stats-title">Appointments</h2>
                            <select className="stats-filter">
                                <option>All Type</option>
                                <option>Walk-in</option>
                                <option>Scheduled</option>
                            </select>
                        </div>

                        <div className="calendar-header">
                            <div className="calendar-month">
                                {currentMonth.toLocaleDateString('en-US', { month: 'long', year: 'numeric' })}
                            </div>
                            <div className="calendar-nav">
                                <button onClick={() => changeMonth(-1)}>
                                    <ChevronLeft size={16} />
                                </button>
                                <button onClick={() => changeMonth(1)}>
                                    <ChevronRight size={16} />
                                </button>
                            </div>
                        </div>

                        <div className="calendar-grid">
                            {renderCalendar()}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default DashboardContent;
