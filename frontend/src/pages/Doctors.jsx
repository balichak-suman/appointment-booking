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

import { useAuth } from '../context/AuthContext';

const Doctors = () => {
    const { isAdmin } = useAuth();
    const [summary, setSummary] = useState(null);
    // ... (rest of state)

    // ... (fetchData)

    const handleDelete = async (doctorId) => {
        if (!window.confirm("Are you sure you want to delete this doctor? This action cannot be undone.")) {
            return;
        }

        try {
            await api.delete(`/doctors/${doctorId}`);
            // Optimistic update or refresh
            setDoctors(prev => prev.filter(d => d.id !== doctorId));
            alert("Doctor deleted successfully");
        } catch (err) {
            console.error("Failed to delete doctor:", err);
            alert("Failed to delete doctor");
        }
    };

    // ... (rest of render)
    {/* Doctors List */ }
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
                            <DoctorCard
                                doctor={doctor}
                                onDelete={isAdmin ? handleDelete : undefined}
                            />
                        </Grid>
                    ))}
                </Grid>
            )}
        </CardContent>
    </Card>

    {/* Add Doctor Dialog */ }
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
                <Grid item xs={12}>
                    <TextField
                        fullWidth
                        label="Google Calendar ID (Optional)"
                        value={newDoctor.google_calendar_id || ''}
                        onChange={(e) => setNewDoctor({ ...newDoctor, google_calendar_id: e.target.value })}
                        helperText={
                            <span>
                                Calendar ID (e.g., email@gmail.com).
                                <br />
                                <strong>Important:</strong> Share your calendar with:
                                <code style={{ backgroundColor: '#f5f5f5', padding: '2px 4px', borderRadius: '4px', display: 'block', wordBreak: 'break-all', marginTop: '4px' }}>
                                    appointment-bot@airy-period-486906-a4.iam.gserviceaccount.com
                                </code>
                            </span>
                        }
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
    </Box >
    );
};

// Force rebuild
export default Doctors;
