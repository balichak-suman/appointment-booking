import React, { useState, useEffect } from 'react';
import {
    Box,
    Card,
    CardContent,
    Typography,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    Chip,
    IconButton,
    TextField,
    MenuItem,
    Grid,
    Button,
    Dialog,
    DialogTitle,
    DialogContent,
    DialogActions,
    Menu,
    MenuItem as MenuOption,
    CircularProgress,
    Alert
} from '@mui/material';
import { MoreVert, WhatsApp, Phone, Person, Add } from '@mui/icons-material';
import api from '../services/api';
import { useAuth } from '../context/AuthContext';

const AppointmentList = () => {
    const [appointments, setAppointments] = useState([]);
    const [doctors, setDoctors] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [filters, setFilters] = useState({
        date: new Date().toISOString().split('T')[0],
        doctorId: '',
        status: ''
    });
    const [anchorEl, setAnchorEl] = useState(null);
    const [selectedAppointment, setSelectedAppointment] = useState(null);
    const { isStaff } = useAuth();

    // Manual Appointment State
    const [openDialog, setOpenDialog] = useState(false);
    const [selectedDepartment, setSelectedDepartment] = useState('');
    const [newAppointment, setNewAppointment] = useState({
        patient_name: '',
        patient_phone: '',
        doctor_id: '',
        date: new Date().toISOString().split('T')[0],
        time: '09:00',
        reason: ''
    });

    // Get unique departments
    const departments = [...new Set(doctors.map(d => d.specialization))];

    // Filter doctors by department
    const filteredDoctors = selectedDepartment
        ? doctors.filter(d => d.specialization === selectedDepartment)
        : doctors;

    const fetchData = async () => {
        try {
            setLoading(true);
            const params = {};
            if (filters.date) params.date = filters.date;
            if (filters.doctorId) params.doctorId = filters.doctorId;
            if (filters.status) params.status = filters.status;

            const [appointmentsRes, doctorsRes] = await Promise.all([
                api.get('/appointments', { params }),
                api.get('/doctors')
            ]);

            setAppointments(appointmentsRes.data.data);
            setDoctors(doctorsRes.data.data);
            setError('');
        } catch (err) {
            setError('Failed to load appointments');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchData();
    }, [filters]);

    const handleMenuOpen = (event, appointment) => {
        setAnchorEl(event.currentTarget);
        setSelectedAppointment(appointment);
    };

    const handleMenuClose = () => {
        setAnchorEl(null);
        setSelectedAppointment(null);
    };

    const handleStatusChange = async (newStatus) => {
        try {
            await api.put(`/appointments/${selectedAppointment.id}/status`, { status: newStatus });
            fetchData();
            handleMenuClose();
        } catch (err) {
            console.error('Failed to update status:', err);
            alert(err.response?.data?.message || 'Failed to update status');
        }
    };

    const getStatusColor = (status) => {
        const colors = {
            'Booked': 'primary',
            'Confirmed': 'primary',
            'Checked In': 'warning',
            'In Consultation': 'secondary',
            'Completed': 'success',
            'Cancelled': 'default',
            'No Show': 'error'
        };
        return colors[status] || 'default';
    };

    const getSourceIcon = (source) => {
        if (source === 'whatsapp') return <WhatsApp fontSize="small" />;
        if (source === 'phone') return <Phone fontSize="small" />;
        return <Person fontSize="small" />;
    };

    const getAvailableStatusTransitions = (currentStatus) => {
        const transitions = {
            'Booked': ['Checked In', 'Cancelled', 'No Show'],
            'Checked In': ['In Consultation', 'Cancelled'],
            'In Consultation': ['Completed']
        };
        return transitions[currentStatus] || [];
    };

    const handleCreateOpen = () => setOpenDialog(true);
    const handleCreateClose = () => setOpenDialog(false);

    const handleCreateSubmit = async () => {
        try {
            await api.post('/appointments', newAppointment);
            setOpenDialog(false);
            fetchData(); // Refresh list
            alert('Appointment created successfully!');
            // Reset form
            setNewAppointment({
                patient_name: '',
                patient_phone: '',
                doctor_id: '',
                date: new Date().toISOString().split('T')[0],
                time: '09:00',
                reason: ''
            });
            setSelectedDepartment('');
        } catch (err) {
            console.error('Failed to create appointment:', err);
            alert(err.response?.data?.detail || 'Failed to create appointment');
        }
    };

    if (loading) {
        return (
            <Box sx={{ display: 'flex', justifyContent: 'center', py: 8 }}>
                <CircularProgress />
            </Box>
        );
    }

    return (
        <Box>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
                <Typography variant="h5" fontWeight="700">
                    Appointments
                </Typography>
                <Button
                    variant="contained"
                    startIcon={<Add />}
                    onClick={handleCreateOpen}
                    sx={{ borderRadius: 2 }}
                >
                    New Appointment
                </Button>
            </Box>

            {/* Filters */}
            <Card sx={{ mb: 3, borderRadius: 3 }}>
                <CardContent>
                    <Grid container spacing={2}>
                        <Grid item xs={12} sm={4}>
                            <TextField
                                fullWidth
                                label="Date"
                                type="date"
                                value={filters.date}
                                onChange={(e) => setFilters({ ...filters, date: e.target.value })}
                                InputLabelProps={{ shrink: true }}
                            />
                        </Grid>
                        <Grid item xs={12} sm={4}>
                            <TextField
                                fullWidth
                                select
                                label="Doctor"
                                value={filters.doctorId}
                                onChange={(e) => setFilters({ ...filters, doctorId: e.target.value })}
                            >
                                <MenuItem value="">All Doctors</MenuItem>
                                {doctors.map((doctor) => (
                                    <MenuItem key={doctor.id} value={doctor.id}>
                                        {doctor.name}
                                    </MenuItem>
                                ))}
                            </TextField>
                        </Grid>
                        <Grid item xs={12} sm={4}>
                            <TextField
                                fullWidth
                                select
                                label="Status"
                                value={filters.status}
                                onChange={(e) => setFilters({ ...filters, status: e.target.value })}
                            >
                                <MenuItem value="">All Statuses</MenuItem>
                                <MenuItem value="Booked">Booked</MenuItem>
                                <MenuItem value="Confirmed">Confirmed</MenuItem>
                                <MenuItem value="Checked In">Checked In</MenuItem>
                                <MenuItem value="In Consultation">In Consultation</MenuItem>
                                <MenuItem value="Completed">Completed</MenuItem>
                                <MenuItem value="Cancelled">Cancelled</MenuItem>
                                <MenuItem value="No Show">No Show</MenuItem>
                            </TextField>
                        </Grid>
                    </Grid>
                </CardContent>
            </Card>

            {/* Appointments Table */}
            <Card sx={{ borderRadius: 3 }}>
                <CardContent>
                    {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

                    <TableContainer>
                        <Table>
                            <TableHead>
                                <TableRow>
                                    <TableCell><strong>Time</strong></TableCell>
                                    <TableCell><strong>Patient</strong></TableCell>
                                    <TableCell><strong>Doctor</strong></TableCell>
                                    <TableCell><strong>Reason</strong></TableCell>
                                    <TableCell><strong>Source</strong></TableCell>
                                    <TableCell><strong>Status</strong></TableCell>
                                    <TableCell align="center"><strong>Actions</strong></TableCell>
                                </TableRow>
                            </TableHead>
                            <TableBody>
                                {appointments.length === 0 ? (
                                    <TableRow>
                                        <TableCell colSpan={7} align="center">
                                            <Typography variant="body2" color="text.secondary" py={4}>
                                                No appointments found
                                            </Typography>
                                        </TableCell>
                                    </TableRow>
                                ) : (
                                    appointments.map((appointment) => (
                                        <TableRow key={appointment.id} hover>
                                            <TableCell>
                                                <Typography variant="body2" fontWeight="600">
                                                    {appointment.slotStartTime?.substring(0, 5)}
                                                </Typography>
                                                <Typography variant="caption" color="text.secondary">
                                                    {appointment.appointmentDate}
                                                </Typography>
                                            </TableCell>
                                            <TableCell>
                                                <Typography variant="body2" fontWeight="600">
                                                    {appointment.patient?.name}
                                                </Typography>
                                                <Typography variant="caption" color="text.secondary">
                                                    {appointment.patient?.mobile}
                                                </Typography>
                                            </TableCell>
                                            <TableCell>
                                                <Typography variant="body2">
                                                    {appointment.doctor?.name}
                                                </Typography>
                                                <Typography variant="caption" color="text.secondary">
                                                    {appointment.doctor?.department}
                                                </Typography>
                                            </TableCell>
                                            <TableCell>
                                                <Typography variant="body2" noWrap sx={{ maxWidth: 200 }}>
                                                    {appointment.reasonForVisit || '-'}
                                                </Typography>
                                            </TableCell>
                                            <TableCell>
                                                <Chip
                                                    icon={getSourceIcon(appointment.source)}
                                                    label={appointment.source}
                                                    size="small"
                                                    variant="outlined"
                                                    color={appointment.source === 'whatsapp' ? 'success' : 'default'}
                                                />
                                            </TableCell>
                                            <TableCell>
                                                <Chip
                                                    label={appointment.status}
                                                    size="small"
                                                    color={getStatusColor(appointment.status)}
                                                />
                                            </TableCell>
                                            <TableCell align="center">
                                                <IconButton
                                                    size="small"
                                                    onClick={(e) => handleMenuOpen(e, appointment)}
                                                >
                                                    <MoreVert />
                                                </IconButton>
                                            </TableCell>
                                        </TableRow>
                                    ))
                                )}
                            </TableBody>
                        </Table>
                    </TableContainer>
                </CardContent>
            </Card>

            {/* Status Update Menu */}
            <Menu
                anchorEl={anchorEl}
                open={Boolean(anchorEl)}
                onClose={handleMenuClose}
            >
                {selectedAppointment && getAvailableStatusTransitions(selectedAppointment.status).map((status) => (
                    <MenuOption key={status} onClick={() => handleStatusChange(status)}>
                        Update to: {status}
                    </MenuOption>
                ))}
                {selectedAppointment && getAvailableStatusTransitions(selectedAppointment.status).length === 0 && (
                    <MenuOption disabled>No actions available</MenuOption>
                )}
            </Menu>
            {/* Manual Appointment Dialog */}
            <Dialog open={openDialog} onClose={handleCreateClose} maxWidth="sm" fullWidth>
                <DialogTitle>New Appointment</DialogTitle>
                <DialogContent>
                    <Grid container spacing={2} sx={{ mt: 1 }}>
                        <Grid item xs={12} sm={6}>
                            <TextField
                                fullWidth
                                label="Patient Name"
                                value={newAppointment.patient_name}
                                onChange={(e) => setNewAppointment({ ...newAppointment, patient_name: e.target.value })}
                            />
                        </Grid>
                        <Grid item xs={12} sm={6}>
                            <TextField
                                fullWidth
                                label="Phone Number"
                                value={newAppointment.patient_phone}
                                onChange={(e) => setNewAppointment({ ...newAppointment, patient_phone: e.target.value })}
                            />
                        </Grid>
                        <Grid item xs={12}>
                            <TextField
                                fullWidth
                                select
                                label="Department"
                                value={selectedDepartment}
                                onChange={(e) => {
                                    setSelectedDepartment(e.target.value);
                                    setNewAppointment({ ...newAppointment, doctor_id: '' }); // Reset doctor
                                }}
                            >
                                <MenuItem value="">All Departments</MenuItem>
                                {departments.map((dept) => (
                                    <MenuItem key={dept} value={dept}>
                                        {dept}
                                    </MenuItem>
                                ))}
                            </TextField>
                        </Grid>
                        <Grid item xs={12}>
                            <TextField
                                fullWidth
                                select
                                label="Doctor"
                                value={newAppointment.doctor_id}
                                onChange={(e) => setNewAppointment({ ...newAppointment, doctor_id: e.target.value })}
                                disabled={!selectedDepartment && departments.length > 0}
                            >
                                {filteredDoctors.map((doctor) => (
                                    <MenuItem key={doctor.id} value={doctor.id}>
                                        {doctor.name} - {doctor.specialization}
                                    </MenuItem>
                                ))}
                            </TextField>
                        </Grid>
                        <Grid item xs={12} sm={6}>
                            <TextField
                                fullWidth
                                label="Date"
                                type="date"
                                value={newAppointment.date}
                                onChange={(e) => setNewAppointment({ ...newAppointment, date: e.target.value })}
                                InputLabelProps={{ shrink: true }}
                            />
                        </Grid>
                        <Grid item xs={12} sm={6}>
                            <TextField
                                fullWidth
                                label="Time"
                                type="time"
                                value={newAppointment.time}
                                onChange={(e) => setNewAppointment({ ...newAppointment, time: e.target.value })}
                                InputLabelProps={{ shrink: true }}
                            />
                        </Grid>
                        <Grid item xs={12}>
                            <TextField
                                fullWidth
                                label="Reason (Optional)"
                                value={newAppointment.reason}
                                onChange={(e) => setNewAppointment({ ...newAppointment, reason: e.target.value })}
                            />
                        </Grid>
                    </Grid>
                </DialogContent>
                <DialogActions>
                    <Button onClick={handleCreateClose}>Cancel</Button>
                    <Button onClick={handleCreateSubmit} variant="contained" disabled={!newAppointment.patient_name || !newAppointment.doctor_id}>
                        Book Appointment
                    </Button>
                </DialogActions>
            </Dialog>
        </Box>
    );
};

export default AppointmentList;
