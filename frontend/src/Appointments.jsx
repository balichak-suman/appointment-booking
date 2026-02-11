import React, { useState, useEffect } from 'react';
import {
    Calendar as CalendarIcon, Plus, Search, Download, Eye, Edit, Trash2,
    X, Clock, User, Stethoscope, FileText
} from 'lucide-react';
import axios from 'axios';
import './Doctors.css';

const Appointments = () => {
    const [appointments, setAppointments] = useState([]);
    const [filteredAppointments, setFilteredAppointments] = useState([]);
    const [loading, setLoading] = useState(true);
    const [searchTerm, setSearchTerm] = useState('');
    const [filterStatus, setFilterStatus] = useState('');
    const [filterType, setFilterType] = useState('');
    const [currentPage, setCurrentPage] = useState(1);
    const [showModal, setShowModal] = useState(false);
    const [selectedAppointment, setSelectedAppointment] = useState(null);
    const itemsPerPage = 10;

    useEffect(() => {
        fetchAppointments();
    }, []);

    useEffect(() => {
        filterAppointments();
    }, [searchTerm, filterStatus, filterType, appointments]);

    const fetchAppointments = async () => {
        try {
            const response = await axios.get(`${import.meta.env.VITE_API_URL || 'http://localhost:8001'}/api/appointments?limit=250`);
            setAppointments(response.data.appointments);
            setFilteredAppointments(response.data.appointments);
            setLoading(false);
        } catch (error) {
            console.error('Error fetching appointments:', error);
            setLoading(false);
        }
    };

    const filterAppointments = () => {
        let filtered = appointments;

        if (searchTerm) {
            filtered = filtered.filter(apt =>
                apt.patientName.toLowerCase().includes(searchTerm.toLowerCase()) ||
                apt.doctorName.toLowerCase().includes(searchTerm.toLowerCase())
            );
        }

        if (filterStatus) {
            filtered = filtered.filter(apt => apt.status === filterStatus);
        }

        if (filterType) {
            filtered = filtered.filter(apt => apt.type === filterType);
        }

        setFilteredAppointments(filtered);
        setCurrentPage(1);
    };

    const getStatusClass = (status) => {
        switch (status) {
            case 'Scheduled':
            case 'In Progress':
                return 'available';
            case 'Completed':
                return 'available';
            case 'Cancelled':
                return 'on-leave';
            case 'Rescheduled':
                return 'busy';
            default:
                return '';
        }
    };

    const getTypeColor = (type) => {
        switch (type) {
            case 'Emergency':
                return '#EF4444';
            case 'Walk-in':
                return '#F59E0B';
            case 'Scheduled':
                return '#10B981';
            case 'Follow-up':
                return '#667eea';
            default:
                return '#94A3B8';
        }
    };

    const handleView = (appointment) => {
        setSelectedAppointment(appointment);
        setShowModal(true);
    };

    const handleEdit = (appointment) => {
        console.log('Edit appointment:', appointment);
    };

    const handleDelete = (appointment) => {
        if (window.confirm(`Are you sure you want to delete this appointment?`)) {
            console.log('Delete appointment:', appointment);
        }
    };

    const exportToCSV = () => {
        console.log('Exporting to CSV...');
    };

    // Pagination
    const indexOfLastItem = currentPage * itemsPerPage;
    const indexOfFirstItem = indexOfLastItem - itemsPerPage;
    const currentAppointments = filteredAppointments.slice(indexOfFirstItem, indexOfLastItem);
    const totalPages = Math.ceil(filteredAppointments.length / itemsPerPage);

    const stats = {
        total: appointments.length,
        scheduled: appointments.filter(a => a.status === 'Scheduled').length,
        completed: appointments.filter(a => a.status === 'Completed').length,
        cancelled: appointments.filter(a => a.status === 'Cancelled').length,
    };

    if (loading) {
        return (
            <div className="loading">
                <div className="spinner"></div>
            </div>
        );
    }

    return (
        <div className="doctors-page">
            {/* Page Header */}
            <div className="page-header">
                <div className="page-header-left">
                    <h1>Appointments Management</h1>
                    <p>Manage and schedule all appointments</p>
                </div>
                <div className="page-actions">
                    <button className="btn btn-primary" onClick={() => setShowModal(true)}>
                        <Plus size={18} />
                        New Appointment
                    </button>
                </div>
            </div>

            {/* Stats Cards */}
            <div className="stats-cards-row">
                <div className="stat-card">
                    <div className="stat-card-header">
                        <div className="stat-icon">
                            <CalendarIcon size={20} />
                        </div>
                    </div>
                    <div className="stat-value">{stats.total}</div>
                    <div className="stat-label">Total Appointments</div>
                </div>

                <div className="stat-card">
                    <div className="stat-card-header">
                        <div className="stat-icon" style={{ background: 'linear-gradient(135deg, #667eea, #764ba2)' }}>
                            <Clock size={20} />
                        </div>
                    </div>
                    <div className="stat-value">{stats.scheduled}</div>
                    <div className="stat-label">Scheduled</div>
                </div>

                <div className="stat-card">
                    <div className="stat-card-header">
                        <div className="stat-icon" style={{ background: 'linear-gradient(135deg, #10B981, #34D399)' }}>
                            <CalendarIcon size={20} />
                        </div>
                    </div>
                    <div className="stat-value">{stats.completed}</div>
                    <div className="stat-label">Completed</div>
                </div>

                <div className="stat-card">
                    <div className="stat-card-header">
                        <div className="stat-icon" style={{ background: 'linear-gradient(135deg, #EF4444, #F87171)' }}>
                            <X size={20} />
                        </div>
                    </div>
                    <div className="stat-value">{stats.cancelled}</div>
                    <div className="stat-label">Cancelled</div>
                </div>
            </div>

            {/* Filters */}
            <div className="filters-section">
                <div className="filters-grid">
                    <div className="filter-group">
                        <label className="filter-label">Search</label>
                        <input
                            type="text"
                            className="filter-input"
                            placeholder="Search by patient or doctor..."
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                        />
                    </div>

                    <div className="filter-group">
                        <label className="filter-label">Type</label>
                        <select
                            className="filter-select"
                            value={filterType}
                            onChange={(e) => setFilterType(e.target.value)}
                        >
                            <option value="">All Types</option>
                            <option value="Walk-in">Walk-in</option>
                            <option value="Scheduled">Scheduled</option>
                            <option value="Emergency">Emergency</option>
                            <option value="Follow-up">Follow-up</option>
                        </select>
                    </div>

                    <div className="filter-group">
                        <label className="filter-label">Status</label>
                        <select
                            className="filter-select"
                            value={filterStatus}
                            onChange={(e) => setFilterStatus(e.target.value)}
                        >
                            <option value="">All Status</option>
                            <option value="Scheduled">Scheduled</option>
                            <option value="Completed">Completed</option>
                            <option value="Cancelled">Cancelled</option>
                            <option value="Rescheduled">Rescheduled</option>
                            <option value="In Progress">In Progress</option>
                        </select>
                    </div>

                    <div className="filter-group">
                        <label className="filter-label">&nbsp;</label>
                        <button className="btn btn-primary" onClick={exportToCSV}>
                            <Download size={18} />
                            Export CSV
                        </button>
                    </div>
                </div>
            </div>

            {/* Table */}
            <div className="table-section">
                <div className="table-header">
                    <h2 className="table-title">All Appointments ({filteredAppointments.length})</h2>
                </div>

                <div className="table-container">
                    <table className="data-table">
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Patient</th>
                                <th>Doctor</th>
                                <th>Date & Time</th>
                                <th>Type</th>
                                <th>Department</th>
                                <th>Reason</th>
                                <th>Status</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {currentAppointments.map(appointment => (
                                <tr key={appointment.id}>
                                    <td>#{appointment.id}</td>
                                    <td>
                                        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                                            <User size={16} color="#667eea" />
                                            {appointment.patientName}
                                        </div>
                                    </td>
                                    <td>
                                        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                                            <Stethoscope size={16} color="#10B981" />
                                            {appointment.doctorName}
                                        </div>
                                    </td>
                                    <td>
                                        <div>
                                            <div style={{ fontWeight: '600', marginBottom: '0.25rem' }}>
                                                {appointment.date}
                                            </div>
                                            <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
                                                <Clock size={12} />
                                                {appointment.time}
                                            </div>
                                        </div>
                                    </td>
                                    <td>
                                        <span style={{
                                            padding: '0.25rem 0.5rem',
                                            background: `${getTypeColor(appointment.type)}15`,
                                            color: getTypeColor(appointment.type),
                                            borderRadius: '4px',
                                            fontSize: '0.75rem',
                                            fontWeight: '600'
                                        }}>
                                            {appointment.type}
                                        </span>
                                    </td>
                                    <td>{appointment.department}</td>
                                    <td>
                                        <div style={{ display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
                                            <FileText size={14} />
                                            {appointment.reason}
                                        </div>
                                    </td>
                                    <td>
                                        <span className={`status-badge ${getStatusClass(appointment.status)}`}>
                                            <span className="status-dot"></span>
                                            {appointment.status}
                                        </span>
                                    </td>
                                    <td>
                                        <div className="action-buttons">
                                            <button className="action-btn" onClick={() => handleView(appointment)} title="View">
                                                <Eye size={16} />
                                            </button>
                                            <button className="action-btn" onClick={() => handleEdit(appointment)} title="Edit">
                                                <Edit size={16} />
                                            </button>
                                            <button className="action-btn delete" onClick={() => handleDelete(appointment)} title="Delete">
                                                <Trash2 size={16} />
                                            </button>
                                        </div>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>

                {/* Pagination */}
                <div className="pagination">
                    <div className="pagination-info">
                        Showing {indexOfFirstItem + 1} to {Math.min(indexOfLastItem, filteredAppointments.length)} of {filteredAppointments.length} appointments
                    </div>
                    <div className="pagination-controls">
                        <button
                            className="pagination-btn"
                            onClick={() => setCurrentPage(prev => Math.max(prev - 1, 1))}
                            disabled={currentPage === 1}
                        >
                            Previous
                        </button>
                        {[...Array(Math.min(5, totalPages))].map((_, idx) => {
                            const pageNum = idx + 1;
                            return (
                                <button
                                    key={pageNum}
                                    className={`pagination-btn ${currentPage === pageNum ? 'active' : ''}`}
                                    onClick={() => setCurrentPage(pageNum)}
                                >
                                    {pageNum}
                                </button>
                            );
                        })}
                        <button
                            className="pagination-btn"
                            onClick={() => setCurrentPage(prev => Math.min(prev + 1, totalPages))}
                            disabled={currentPage === totalPages}
                        >
                            Next
                        </button>
                    </div>
                </div>
            </div>

            {/* View Appointment Modal */}
            {showModal && selectedAppointment && (
                <div className="modal-overlay" onClick={() => setShowModal(false)}>
                    <div className="modal" onClick={(e) => e.stopPropagation()}>
                        <div className="modal-header">
                            <h2 className="modal-title">Appointment Details</h2>
                            <button className="modal-close" onClick={() => setShowModal(false)}>
                                <X size={18} />
                            </button>
                        </div>
                        <div className="modal-body">
                            <div className="form-grid">
                                <div className="form-group">
                                    <label className="form-label">Appointment ID</label>
                                    <input className="form-input" value={`#${selectedAppointment.id}`} readOnly />
                                </div>
                                <div className="form-group">
                                    <label className="form-label">Patient Name</label>
                                    <input className="form-input" value={selectedAppointment.patientName} readOnly />
                                </div>
                                <div className="form-group">
                                    <label className="form-label">Doctor Name</label>
                                    <input className="form-input" value={selectedAppointment.doctorName} readOnly />
                                </div>
                                <div className="form-group">
                                    <label className="form-label">Department</label>
                                    <input className="form-input" value={selectedAppointment.department} readOnly />
                                </div>
                                <div className="form-group">
                                    <label className="form-label">Date</label>
                                    <input className="form-input" value={selectedAppointment.date} readOnly />
                                </div>
                                <div className="form-group">
                                    <label className="form-label">Time</label>
                                    <input className="form-input" value={selectedAppointment.time} readOnly />
                                </div>
                                <div className="form-group">
                                    <label className="form-label">Type</label>
                                    <input className="form-input" value={selectedAppointment.type} readOnly />
                                </div>
                                <div className="form-group">
                                    <label className="form-label">Status</label>
                                    <input className="form-input" value={selectedAppointment.status} readOnly />
                                </div>
                                <div className="form-group full-width">
                                    <label className="form-label">Reason</label>
                                    <input className="form-input" value={selectedAppointment.reason} readOnly />
                                </div>
                            </div>
                        </div>
                        <div className="modal-footer">
                            <button className="btn-secondary" onClick={() => setShowModal(false)}>
                                Close
                            </button>
                            <button className="btn btn-primary" onClick={() => handleEdit(selectedAppointment)}>
                                <Edit size={16} />
                                Edit Appointment
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Appointments;
