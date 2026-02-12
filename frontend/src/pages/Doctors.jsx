import React, { useState, useEffect } from 'react';
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
    EventAvailable,
    MedicalServices
} from '@mui/icons-material';
import api from '../services/api';
import StatCard from '../components/StatCard';
import DoctorCard from '../components/DoctorCard';

const Doctors = () => {
    const [summary, setSummary] = useState(null);
    const [doctors, setDoctors] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    const fetchData = async () => {
        try {
            const [summaryRes, doctorsRes] = await Promise.all([
                api.get('/dashboard/summary'),
                api.get('/doctors')
            ]);

            setSummary(summaryRes.data.data);
            setDoctors(doctorsRes.data.data || []);
            setError('');
        } catch (err) {
            setError('Failed to load doctor data');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchData();
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

    // Combine doctors with their appointment stats from summary
    const doctorsWithStats = doctors.map(doctor => {
        const stats = summary?.doctorSummary?.find(ds => ds.doctorId === doctor.id);
        return {
            ...doctor,
            totalAppointments: stats?.totalAppointments || 0,
            completed: stats?.completed || 0,
            waiting: stats?.waiting || 0
        };
    });

    return (
        <Box>
            <Box sx={{ mb: 4 }}>
                <Typography variant="h4" fontWeight={700} gutterBottom>
                    Doctor Management
                </Typography>
                <Typography variant="body1" color="text.secondary">
                    View doctor information and today's performance
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

            {/* Doctors List */}
            <Card>
                <CardContent>
                    <Typography variant="h6" fontWeight={700} gutterBottom>
                        All Doctors ({doctorsWithStats.length})
                    </Typography>

                    {doctorsWithStats.length === 0 ? (
                        <Box sx={{ py: 8, textAlign: 'center' }}>
                            <Typography variant="body1" color="text.secondary">
                                No doctors found
                            </Typography>
                        </Box>
                    ) : (
                        <Grid container spacing={2} sx={{ mt: 1 }}>
                            {doctorsWithStats.map((doctor) => (
                                <Grid item xs={12} md={6} key={doctor.id}>
                                    <DoctorCard doctor={doctor} />
                                </Grid>
                            ))}
                        </Grid>
                    )}
                </CardContent>
            </Card>
        </Box>
    );
};

export default Doctors;
