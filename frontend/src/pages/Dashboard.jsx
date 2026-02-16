import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
    Box,
    Grid,
    Card,
    CardContent,
    Typography,
    CircularProgress,
    Alert,
    Chip
} from '@mui/material';
import {
    CheckCircle,
    HourglassEmpty,
    Cancel,
    PersonOff,
    EventAvailable,
    MedicalServices
} from '@mui/icons-material';
import api from '../services/api';
import { useAuth } from '../context/AuthContext';
import StatCard from '../components/StatCard';
import CalendarWidget from '../components/CalendarWidget';
import DoctorCard from '../components/DoctorCard';

const Dashboard = () => {
    const navigate = useNavigate();
    const [summary, setSummary] = useState(null);
    const [queue, setQueue] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const { user, isDoctor } = useAuth();

    const fetchDashboardData = async () => {
        try {
            const [summaryRes, queueRes] = await Promise.all([
                api.get('/dashboard/summary'),
                api.get('/queue')
            ]);

            setSummary(summaryRes.data.data);
            setQueue(queueRes.data.data);
            setError('');
        } catch (err) {
            setError('Failed to load dashboard data');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchDashboardData();

        // Auto-refresh queue every 15 seconds
        const interval = setInterval(() => {
            fetchDashboardData();
        }, 15000);

        return () => clearInterval(interval);
    }, []);

    if (loading) {
        return (
            <Box sx={{ display: 'flex', justifyContent: 'center', py: 8 }}>
                <CircularProgress />
            </Box>
        );
    }

    if (error) {
        return <Alert severity="error">{error}</Alert>;
    }



    const handleCardClick = (status) => {
        const today = new Date().toISOString().split('T')[0];
        let params = `date=${today}`;

        if (status === 'Total Today') {
            // No status filter, just date
        } else if (status === 'In Progress') {
            params += `&status=Checked In,In Consultation`;
        } else {
            params += `&status=${status}`;
        }

        navigate(`/appointments?${params}`);
    };

    const statusCards = [
        { label: 'Total Today', value: summary?.summary?.total || 0, color: '#38B2AC', icon: <EventAvailable />, onClick: () => handleCardClick('Total Today') },
        { label: 'Completed', value: summary?.summary?.completed || 0, color: '#48BB78', icon: <CheckCircle />, onClick: () => handleCardClick('Completed') },
        { label: 'In Progress', value: (summary?.summary?.checkedIn || 0) + (summary?.summary?.inConsultation || 0), color: '#ED8936', icon: <MedicalServices />, onClick: () => handleCardClick('In Progress') },
        { label: 'Pending', value: summary?.summary?.booked || 0, color: '#4299E1', icon: <HourglassEmpty />, onClick: () => handleCardClick('Booked') }, // Map Pending -> Booked
        { label: 'Cancelled', value: summary?.summary?.cancelled || 0, color: '#A0AEC0', icon: <Cancel />, onClick: () => handleCardClick('Cancelled') },
        { label: 'No Show', value: summary?.summary?.noShow || 0, color: '#F56565', icon: <PersonOff />, onClick: () => handleCardClick('No Show') },
    ];

    const getStatusColor = (status) => {
        const colors = {
            'Booked': '#4299E1',
            'Checked In': '#ED8936',
            'In Consultation': '#9C27B0',
            'Completed': '#48BB78',
            'Cancelled': '#A0AEC0',
            'No Show': '#F56565'
        };
        return colors[status] || '#666';
    };

    return (
        <Box>
            <Box sx={{ mb: 4 }}>
                <Typography variant="h4" fontWeight={700} gutterBottom>
                    Welcome back, {user?.fullName}!
                </Typography>
                <Typography variant="body1" color="text.secondary">
                    Here's what's happening today
                </Typography>
            </Box>

            {/* Summary Cards */}
            <Grid container spacing={3} sx={{ mb: 4 }}>
                {statusCards.map((card, index) => (
                    <Grid item xs={12} sm={6} md={3} key={index}>
                        <StatCard
                            title={card.label}
                            value={card.value}
                            icon={card.icon}
                            color={card.color}
                            subtitle={index === 0 ? 'All appointments' : undefined}
                            onClick={card.onClick}
                        />
                    </Grid>
                ))}
            </Grid>

            {/* Calendar and Doctor Summary Row */}
            <Grid container spacing={3} sx={{ mb: 4 }}>
                {/* Calendar Widget */}
                <Grid item xs={12} md={5}>
                    <CalendarWidget appointments={queue} />
                </Grid>

                {/* Doctor Summary */}
                <Grid item xs={12} md={7}>
                    <Card sx={{ height: '100%' }}>
                        <CardContent>
                            <Typography variant="h6" fontWeight={700} gutterBottom>
                                Doctor-wise Summary
                            </Typography>
                            {!isDoctor && summary?.doctorSummary && summary.doctorSummary.length > 0 ? (
                                <Grid container spacing={2} sx={{ mt: 0.5 }}>
                                    {summary.doctorSummary.map((doc, index) => (
                                        <Grid item xs={12} sm={6} key={index}>
                                            <DoctorCard doctor={{
                                                name: doc.doctor?.name,
                                                department: doc.doctor?.department,
                                                totalAppointments: doc.totalAppointments,
                                                completed: doc.completed,
                                                waiting: doc.waiting
                                            }} />
                                        </Grid>
                                    ))}
                                </Grid>
                            ) : (
                                <Typography variant="body2" color="text.secondary" sx={{ py: 4, textAlign: 'center' }}>
                                    No doctor data available
                                </Typography>
                            )}
                        </CardContent>
                    </Card>
                </Grid>
            </Grid>

            {/* Current Queue */}
            <Card sx={{ borderRadius: 3 }}>
                <CardContent>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                        <Typography variant="h6" fontWeight="700">
                            Current Queue ({queue.length})
                        </Typography>
                        <Chip
                            label="Auto-refreshing every 15s"
                            size="small"
                            color="primary"
                            variant="outlined"
                        />
                    </Box>

                    {queue.length === 0 ? (
                        <Box sx={{ textAlign: 'center', py: 4 }}>
                            <Typography variant="body2" color="text.secondary">
                                No patients in queue
                            </Typography>
                        </Box>
                    ) : (
                        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                            {queue.map((appointment, index) => (
                                <Box
                                    key={appointment.id}
                                    sx={{
                                        p: 2,
                                        borderRadius: 2,
                                        border: '2px solid',
                                        borderColor: `${getStatusColor(appointment.status)}40`,
                                        bgcolor: `${getStatusColor(appointment.status)}10`,
                                        display: 'flex',
                                        alignItems: 'center',
                                        gap: 2
                                    }}
                                >
                                    <Box
                                        sx={{
                                            width: 40,
                                            height: 40,
                                            borderRadius: '50%',
                                            bgcolor: getStatusColor(appointment.status),
                                            color: 'white',
                                            display: 'flex',
                                            alignItems: 'center',
                                            justifyContent: 'center',
                                            fontWeight: '700',
                                            fontSize: '1.2rem'
                                        }}
                                    >
                                        {index + 1}
                                    </Box>
                                    <Box sx={{ flex: 1 }}>
                                        <Typography variant="subtitle2" fontWeight="600">
                                            {appointment.patient?.name}
                                        </Typography>
                                        <Typography variant="caption" color="text.secondary">
                                            {appointment.patient?.mobile}
                                        </Typography>
                                    </Box>
                                    <Box>
                                        <Typography variant="body2" fontWeight="600">
                                            {appointment.doctor?.name}
                                        </Typography>
                                        <Typography variant="caption" color="text.secondary">
                                            {appointment.slotStartTime?.substring(0, 5)}
                                        </Typography>
                                    </Box>
                                    <Chip
                                        label={appointment.status}
                                        size="small"
                                        sx={{
                                            bgcolor: getStatusColor(appointment.status),
                                            color: 'white',
                                            fontWeight: '600'
                                        }}
                                    />
                                    {appointment.source === 'whatsapp' && (
                                        <Chip
                                            label="WhatsApp"
                                            size="small"
                                            color="success"
                                            variant="outlined"
                                        />
                                    )}
                                    {appointment.waitingTime !== null && (
                                        <Chip
                                            label={`${appointment.waitingTime} min`}
                                            size="small"
                                            color="warning"
                                            variant="outlined"
                                        />
                                    )}
                                </Box>
                            ))}
                        </Box>
                    )}
                </CardContent>
            </Card>
        </Box>
    );
};

export default Dashboard;
