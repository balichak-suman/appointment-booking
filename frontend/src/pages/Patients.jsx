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
    TextField,
    InputAdornment
} from '@mui/material';
import {
    CheckCircle,
    HourglassEmpty,
    EventAvailable,
    MedicalServices,
    Search,
    Phone,
    Email
} from '@mui/icons-material';
import api from '../services/api';
import StatCard from '../components/StatCard';

const Patients = () => {
    const [summary, setSummary] = useState(null);
    const [patients, setPatients] = useState([]);
    const [filteredPatients, setFilteredPatients] = useState([]);
    const [searchTerm, setSearchTerm] = useState('');
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    const fetchData = async () => {
        try {
            const [summaryRes, patientsRes] = await Promise.all([
                api.get('/dashboard/summary'),
                api.get('/patients')
            ]);

            setSummary(summaryRes.data.data);
            setPatients(patientsRes.data.data || []);
            setFilteredPatients(patientsRes.data.data || []);
            setError('');
        } catch (err) {
            setError('Failed to load patient data');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchData();
    }, []);

    useEffect(() => {
        if (searchTerm) {
            const filtered = patients.filter(patient =>
                patient.name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
                patient.mobile?.includes(searchTerm) ||
                patient.email?.toLowerCase().includes(searchTerm.toLowerCase())
            );
            setFilteredPatients(filtered);
        } else {
            setFilteredPatients(patients);
        }
    }, [searchTerm, patients]);

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

    return (
        <Box>
            <Box sx={{ mb: 4 }}>
                <Typography variant="h4" fontWeight={700} gutterBottom>
                    Patient Management
                </Typography>
                <Typography variant="body1" color="text.secondary">
                    View and manage patient records
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

            {/* Patient List */}
            <Card>
                <CardContent>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
                        <Typography variant="h6" fontWeight={700}>
                            All Patients ({filteredPatients.length})
                        </Typography>
                        <TextField
                            placeholder="Search patients..."
                            size="small"
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                            InputProps={{
                                startAdornment: (
                                    <InputAdornment position="start">
                                        <Search />
                                    </InputAdornment>
                                ),
                            }}
                            sx={{ width: 300 }}
                        />
                    </Box>

                    {filteredPatients.length === 0 ? (
                        <Box sx={{ py: 8, textAlign: 'center' }}>
                            <Typography variant="body1" color="text.secondary">
                                {searchTerm ? 'No patients found' : 'No patients registered'}
                            </Typography>
                        </Box>
                    ) : (
                        <Grid container spacing={2}>
                            {filteredPatients.map((patient) => (
                                <Grid item xs={12} md={6} lg={4} key={patient.id}>
                                    <Card
                                        sx={{
                                            border: '1px solid',
                                            borderColor: 'grey.200',
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
                                                        bgcolor: 'primary.main',
                                                        fontSize: '1.25rem',
                                                        fontWeight: 700,
                                                    }}
                                                >
                                                    {patient.name?.charAt(0) || 'P'}
                                                </Avatar>
                                                <Box sx={{ flex: 1 }}>
                                                    <Typography variant="subtitle1" fontWeight={600}>
                                                        {patient.name}
                                                    </Typography>
                                                    <Chip
                                                        label={patient.gender || 'N/A'}
                                                        size="small"
                                                        sx={{ mt: 0.5, bgcolor: 'grey.100' }}
                                                    />

                                                    <Box sx={{ mt: 1.5, display: 'flex', flexDirection: 'column', gap: 0.5 }}>
                                                        {patient.mobile && (
                                                            <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                                                                <Phone sx={{ fontSize: '0.875rem', color: 'text.secondary' }} />
                                                                <Typography variant="caption" color="text.secondary">
                                                                    {patient.mobile}
                                                                </Typography>
                                                            </Box>
                                                        )}
                                                        {patient.email && (
                                                            <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                                                                <Email sx={{ fontSize: '0.875rem', color: 'text.secondary' }} />
                                                                <Typography variant="caption" color="text.secondary">
                                                                    {patient.email}
                                                                </Typography>
                                                            </Box>
                                                        )}
                                                    </Box>
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

export default Patients;
