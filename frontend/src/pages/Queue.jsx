import React, { useState, useEffect } from 'react';
import {
    Box,
    Grid,
    Card,
    CardContent,
    Typography,
    CircularProgress,
    Alert,
    Chip,
    Avatar,
    Stack
} from '@mui/material';
import {
    CheckCircle,
    HourglassEmpty,
    Cancel,
    PersonOff,
    EventAvailable,
    MedicalServices,
    AccessTime
} from '@mui/icons-material';
import api from '../services/api';
import { useAuth } from '../context/AuthContext';
import StatCard from '../components/StatCard';

const Queue = () => {
    const [summary, setSummary] = useState(null);
    const [queue, setQueue] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const { user } = useAuth();

    const fetchQueueData = async () => {
        try {
            const [summaryRes, queueRes] = await Promise.all([
                api.get('/dashboard/summary'),
                api.get('/queue')
            ]);

            setSummary(summaryRes.data.data);
            setQueue(queueRes.data.data);
            setError('');
        } catch (err) {
            setError('Failed to load queue data');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchQueueData();

        // Auto-refresh every 15 seconds
        const interval = setInterval(() => {
            fetchQueueData();
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

    const statusCards = [
        { label: 'Total Today', value: summary?.summary?.total || 0, color: '#38B2AC', icon: <EventAvailable /> },
        { label: 'Completed', value: summary?.summary?.completed || 0, color: '#48BB78', icon: <CheckCircle /> },
        { label: 'In Progress', value: (summary?.summary?.checkedIn || 0) + (summary?.summary?.inConsultation || 0), color: '#ED8936', icon: <MedicalServices /> },
        { label: 'Pending', value: summary?.summary?.booked || 0, color: '#4299E1', icon: <HourglassEmpty /> },
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

    const getStatusLabel = (status) => {
        const labels = {
            'Booked': 'Waiting',
            'Checked In': 'Checked In',
            'In Consultation': 'In Progress'
        };
        return labels[status] || status;
    };

    return (
        <Box>
            <Box sx={{ mb: 4 }}>
                <Typography variant="h4" fontWeight={700} gutterBottom>
                    Current Queue
                </Typography>
                <Typography variant="body1" color="text.secondary">
                    Live patient queue - Auto-refreshes every 15 seconds
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
                        />
                    </Grid>
                ))}
            </Grid>

            {/* Queue List */}
            <Card>
                <CardContent>
                    <Typography variant="h6" fontWeight={700} gutterBottom>
                        Patients in Queue ({queue.length})
                    </Typography>

                    {queue.length === 0 ? (
                        <Box sx={{ py: 8, textAlign: 'center' }}>
                            <Typography variant="body1" color="text.secondary">
                                No patients in queue
                            </Typography>
                        </Box>
                    ) : (
                        <Grid container spacing={2} sx={{ mt: 1 }}>
                            {queue.map((appointment, index) => (
                                <Grid item xs={12} md={6} key={appointment.id}>
                                    <Card
                                        sx={{
                                            border: '1px solid',
                                            borderColor: 'grey.200',
                                            bgcolor: `${getStatusColor(appointment.status)}08`,
                                            transition: 'transform 0.2s, box-shadow 0.2s',
                                            '&:hover': {
                                                transform: 'translateY(-2px)',
                                                boxShadow: 3,
                                            },
                                        }}
                                    >
                                        <CardContent>
                                            <Box sx={{ display: 'flex', alignItems: 'flex-start', gap: 2 }}>
                                                <Avatar
                                                    sx={{
                                                        width: 48,
                                                        height: 48,
                                                        bgcolor: getStatusColor(appointment.status),
                                                        fontSize: '1.25rem',
                                                        fontWeight: 700,
                                                    }}
                                                >
                                                    {index + 1}
                                                </Avatar>
                                                <Box sx={{ flex: 1 }}>
                                                    <Typography variant="subtitle1" fontWeight={600}>
                                                        {appointment.patient?.name}
                                                    </Typography>
                                                    <Typography variant="caption" color="text.secondary" display="block">
                                                        {appointment.doctor?.name} • {appointment.doctor?.department}
                                                    </Typography>

                                                    <Stack direction="row" spacing={1} sx={{ mt: 1.5 }}>
                                                        <Chip
                                                            label={getStatusLabel(appointment.status)}
                                                            size="small"
                                                            sx={{
                                                                bgcolor: getStatusColor(appointment.status),
                                                                color: 'white',
                                                                fontWeight: 600,
                                                            }}
                                                        />
                                                        <Chip
                                                            icon={<AccessTime sx={{ fontSize: '1rem' }} />}
                                                            label={appointment.slotStartTime?.substring(0, 5)}
                                                            size="small"
                                                            variant="outlined"
                                                        />
                                                        {appointment.waitingTime !== null && (
                                                            <Chip
                                                                label={`Waiting ${appointment.waitingTime} min`}
                                                                size="small"
                                                                color="warning"
                                                                variant="outlined"
                                                            />
                                                        )}
                                                    </Stack>

                                                    {appointment.reasonForVisit && (
                                                        <Typography variant="caption" color="text.secondary" sx={{ mt: 1, display: 'block' }}>
                                                            Reason: {appointment.reasonForVisit}
                                                        </Typography>
                                                    )}
                                                </Box>
                                            </Box>
                                        </CardContent>
                                    </Card>
                                </Grid>
                            ))}
                        </Grid>
                    )}
                </CardContent>
            </Card>
        </Box>
    );
};

export default Queue;
