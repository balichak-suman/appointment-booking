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
    Button,
    Dialog,
    DialogTitle,
    DialogContent,
    DialogActions,
    DialogActions,
    TextField,
    MenuItem
} from '@mui/material';
import {
    CheckCircle,
    HourglassEmpty,
    EventAvailable,
    MedicalServices,
    Add
} from '@mui/icons-material';
import api from '../services/api';
import StatCard from '../components/StatCard';
import DoctorCard from '../components/DoctorCard';

const Doctors = () => {
    const [summary, setSummary] = useState(null);
    const [doctors, setDoctors] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    // Add Doctor State
    const [openDialog, setOpenDialog] = useState(false);
    const [newDoctor, setNewDoctor] = useState({
        name: '',
        specialization: '',
        email: '',
        phone: '',
        experience: 0
    });

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

    const handleCreateOpen = () => setOpenDialog(true);
    const handleCreateClose = () => setOpenDialog(false);

    const handleCreateSubmit = async () => {
        try {
            await api.post('/doctors', newDoctor);
            setOpenDialog(false);
            fetchData(); // Refresh list
            alert('Doctor added successfully!');
            setNewDoctor({
                name: '',
                specialization: '',
                email: '',
                phone: '',
                experience: 0
            });
        } catch (err) {
            console.error('Failed to add doctor:', err);
            alert(err.response?.data?.detail || 'Failed to add doctor');
        }
    };

    return (
        <Box>
            <Box sx={{ mb: 4, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <Box>
                    <Typography variant="h4" fontWeight={700} gutterBottom>
                        Doctor Management
                    </Typography>
                    <Typography variant="body1" color="text.secondary">
                        View doctor information and today's performance
                    </Typography>
                </Box>
                <Button
                    variant="contained"
                    startIcon={<Add />}
                    onClick={handleCreateOpen}
                    sx={{ borderRadius: 2 }}
                >
                    Add Doctor
                </Button>
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

            {/* Add Doctor Dialog */}
            <Dialog open={openDialog} onClose={handleCreateClose} maxWidth="sm" fullWidth>
                <DialogTitle>Add New Doctor</DialogTitle>
                <DialogContent>
                    <Grid container spacing={2} sx={{ mt: 1 }}>
                        <Grid item xs={12}>
                            <TextField
                                fullWidth
                                label="Doctor Name"
                                value={newDoctor.name}
                                onChange={(e) => setNewDoctor({ ...newDoctor, name: e.target.value })}
                            />
                        </Grid>
                        <Grid item xs={12} sm={6}>
                            <TextField
                                fullWidth
                                select
                                label="Specialization (Department)"
                                value={newDoctor.specialization}
                                onChange={(e) => setNewDoctor({ ...newDoctor, specialization: e.target.value })}
                                SelectProps={{
                                    native: false,
                                }}
                            >
                                {/* Extract unique departments from doctors list */}
                                {[...new Set(doctors.map(d => d.specialization))].sort().map((dept) => (
                                    <MenuItem key={dept} value={dept}>
                                        {dept}
                                    </MenuItem>
                                ))}
                                <MenuItem value="General Physician">General Physician</MenuItem>
                                <MenuItem value="Cardiologist">Cardiologist</MenuItem>
                                <MenuItem value="Dermatologist">Dermatologist</MenuItem>
                                <MenuItem value="Pediatrician">Pediatrician</MenuItem>
                                <MenuItem value="Neurologist">Neurologist</MenuItem>
                                <MenuItem value="Orthopedic">Orthopedic</MenuItem>
                            </TextField>
                        </Grid>
                        <Grid item xs={12} sm={6}>
                            <TextField
                                fullWidth
                                label="Experience (Years)"
                                type="number"
                                value={newDoctor.experience}
                                onChange={(e) => setNewDoctor({ ...newDoctor, experience: parseInt(e.target.value) || 0 })}
                            />
                        </Grid>
                        <Grid item xs={12} sm={6}>
                            <TextField
                                fullWidth
                                label="Email"
                                type="email"
                                value={newDoctor.email}
                                onChange={(e) => setNewDoctor({ ...newDoctor, email: e.target.value })}
                            />
                        </Grid>
                        <Grid item xs={12} sm={6}>
                            <TextField
                                fullWidth
                                label="Phone"
                                value={newDoctor.phone}
                                onChange={(e) => setNewDoctor({ ...newDoctor, phone: e.target.value })}
                            />
                        </Grid>
                    </Grid>
                </DialogContent>
                <DialogActions>
                    <Button onClick={handleCreateClose}>Cancel</Button>
                    <Button onClick={handleCreateSubmit} variant="contained" disabled={!newDoctor.name || !newDoctor.specialization || !newDoctor.email}>
                        Add Doctor
                    </Button>
                </DialogActions>
            </Dialog>
        </Box>
    );
};

export default Doctors;
