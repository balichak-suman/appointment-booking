import React, { useState, useEffect } from 'react';
import {
    Users, UserPlus, Search, Filter, Download, Eye, Edit, Trash2,
    Star, X, Mail, Phone, Award
} from 'lucide-react';
import axios from 'axios';
import './Doctors.css';

const Doctors = () => {
    const [doctors, setDoctors] = useState([]);
    const [filteredDoctors, setFilteredDoctors] = useState([]);
    const [loading, setLoading] = useState(true);
    const [searchTerm, setSearchTerm] = useState('');
    const [filterSpecialization, setFilterSpecialization] = useState('');
    const [filterStatus, setFilterStatus] = useState('');
    const [currentPage, setCurrentPage] = useState(1);
    const [showModal, setShowModal] = useState(false);
    const [selectedDoctor, setSelectedDoctor] = useState(null);
    const itemsPerPage = 10;

    useEffect(() => {
        fetchDoctors();
    }, []);

    useEffect(() => {
        filterDoctors();
    }, [searchTerm, filterSpecialization, filterStatus, doctors]);

    const fetchDoctors = async () => {
        try {
            const response = await axios.get(`${import.meta.env.VITE_API_URL || 'http://localhost:8001'}/api/doctors?limit=250`);
            setDoctors(response.data.doctors);
            setFilteredDoctors(response.data.doctors);
            setLoading(false);
        } catch (error) {
            console.error('Error fetching doctors:', error);
            setLoading(false);
        }
    };

    const filterDoctors = () => {
        let filtered = doctors;

        if (searchTerm) {
            filtered = filtered.filter(doctor =>
                doctor.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                doctor.specialization.toLowerCase().includes(searchTerm.toLowerCase())
            );
        }

        if (filterSpecialization) {
            filtered = filtered.filter(doctor =>
                doctor.specialization === filterSpecialization
            );
        }

        if (filterStatus) {
            filtered = filtered.filter(doctor =>
                doctor.status === filterStatus
            );
        }

        setFilteredDoctors(filtered);
        setCurrentPage(1);
    };

    const getSpecializations = () => {
        const specializations = [...new Set(doctors.map(d => d.specialization))];
        return specializations.sort();
    };

    const getStatusClass = (status) => {
        switch (status) {
            case 'Available':
                return 'available';
            case 'Busy':
                return 'busy';
            case 'On Leave':
                return 'on-leave';
            default:
                return '';
        }
    };

    const getInitials = (name) => {
        return name.split(' ').map(n => n[0]).join('').substring(0, 2);
    };

    const handleView = (doctor) => {
        setSelectedDoctor(doctor);
        setShowModal(true);
    };

    const handleEdit = (doctor) => {
        // TODO: Implement edit functionality
        console.log('Edit doctor:', doctor);
    };

    const handleDelete = (doctor) => {
        // TODO: Implement delete functionality
        if (window.confirm(`Are you sure you want to delete ${doctor.name}?`)) {
            console.log('Delete doctor:', doctor);
        }
    };

    const exportToCSV = () => {
        // TODO: Implement CSV export
        console.log('Exporting to CSV...');
    };

    // Pagination
    const indexOfLastItem = currentPage * itemsPerPage;
    const indexOfFirstItem = indexOfLastItem - itemsPerPage;
    const currentDoctors = filteredDoctors.slice(indexOfFirstItem, indexOfLastItem);
    const totalPages = Math.ceil(filteredDoctors.length / itemsPerPage);

    const stats = {
        total: doctors.length,
        available: doctors.filter(d => d.status === 'Available').length,
        busy: doctors.filter(d => d.status === 'Busy').length,
        onLeave: doctors.filter(d => d.status === 'On Leave').length,
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
                    <h1>Doctors Management</h1>
                    <p>Manage and monitor all doctors in the system</p>
                </div>
                <div className="page-actions">
                    <button className="btn btn-primary" onClick={() => setShowModal(true)}>
                        <UserPlus size={18} />
                        Add New Doctor
                    </button>
                </div>
            </div>

            {/* Stats Cards */}
            <div className="stats-cards-row">
                <div className="stat-card">
                    <div className="stat-card-header">
                        <div className="stat-icon">
                            <Users size={20} />
                        </div>
                    </div>
                    <div className="stat-value">{stats.total}</div>
                    <div className="stat-label">Total Doctors</div>
                </div>

                <div className="stat-card">
                    <div className="stat-card-header">
                        <div className="stat-icon" style={{ background: 'linear-gradient(135deg, #10B981, #34D399)' }}>
                            <Users size={20} />
                        </div>
                    </div>
                    <div className="stat-value">{stats.available}</div>
                    <div className="stat-label">Available</div>
                </div>

                <div className="stat-card">
                    <div className="stat-card-header">
                        <div className="stat-icon" style={{ background: 'linear-gradient(135deg, #F59E0B, #FBBF24)' }}>
                            <Users size={20} />
                        </div>
                    </div>
                    <div className="stat-value">{stats.busy}</div>
                    <div className="stat-label">Busy</div>
                </div>

                <div className="stat-card">
                    <div className="stat-card-header">
                        <div className="stat-icon" style={{ background: 'linear-gradient(135deg, #EF4444, #F87171)' }}>
                            <Users size={20} />
                        </div>
                    </div>
                    <div className="stat-value">{stats.onLeave}</div>
                    <div className="stat-label">On Leave</div>
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
                            placeholder="Search by name or specialization..."
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                        />
                    </div>

                    <div className="filter-group">
                        <label className="filter-label">Specialization</label>
                        <select
                            className="filter-select"
                            value={filterSpecialization}
                            onChange={(e) => setFilterSpecialization(e.target.value)}
                        >
                            <option value="">All Specializations</option>
                            {getSpecializations().map(spec => (
                                <option key={spec} value={spec}>{spec}</option>
                            ))}
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
                            <option value="Available">Available</option>
                            <option value="Busy">Busy</option>
                            <option value="On Leave">On Leave</option>
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
                    <h2 className="table-title">All Doctors ({filteredDoctors.length})</h2>
                </div>

                <div className="table-container">
                    <table className="data-table">
                        <thead>
                            <tr>
                                <th>Doctor</th>
                                <th>Specialization</th>
                                <th>Experience</th>
                                <th>Patients</th>
                                <th>Rating</th>
                                <th>Status</th>
                                <th>Contact</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {currentDoctors.map(doctor => (
                                <tr key={doctor.id}>
                                    <td>
                                        <div className="doctor-info">
                                            <div className="doctor-avatar">
                                                {getInitials(doctor.name)}
                                            </div>
                                            <div className="doctor-details">
                                                <h4>{doctor.name}</h4>
                                                <p>{doctor.email}</p>
                                            </div>
                                        </div>
                                    </td>
                                    <td>
                                        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                                            <Award size={16} color="#667eea" />
                                            {doctor.specialization}
                                        </div>
                                    </td>
                                    <td>{doctor.experience} years</td>
                                    <td>{doctor.patients}</td>
                                    <td>
                                        <div className="rating">
                                            <span className="rating-value">{doctor.rating}</span>
                                            <Star size={14} className="rating-stars" fill="#F59E0B" />
                                        </div>
                                    </td>
                                    <td>
                                        <span className={`status-badge ${getStatusClass(doctor.status)}`}>
                                            <span className="status-dot"></span>
                                            {doctor.status}
                                        </span>
                                    </td>
                                    <td>
                                        <div style={{ fontSize: '0.75rem' }}>
                                            <div style={{ display: 'flex', alignItems: 'center', gap: '0.25rem', marginBottom: '0.25rem' }}>
                                                <Phone size={12} />
                                                {doctor.phone}
                                            </div>
                                            <div style={{ display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
                                                <Mail size={12} />
                                                {doctor.email}
                                            </div>
                                        </div>
                                    </td>
                                    <td>
                                        <div className="action-buttons">
                                            <button className="action-btn" onClick={() => handleView(doctor)} title="View">
                                                <Eye size={16} />
                                            </button>
                                            <button className="action-btn" onClick={() => handleEdit(doctor)} title="Edit">
                                                <Edit size={16} />
                                            </button>
                                            <button className="action-btn delete" onClick={() => handleDelete(doctor)} title="Delete">
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
                        Showing {indexOfFirstItem + 1} to {Math.min(indexOfLastItem, filteredDoctors.length)} of {filteredDoctors.length} doctors
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

            {/* View Doctor Modal */}
            {showModal && selectedDoctor && (
                <div className="modal-overlay" onClick={() => setShowModal(false)}>
                    <div className="modal" onClick={(e) => e.stopPropagation()}>
                        <div className="modal-header">
                            <h2 className="modal-title">Doctor Details</h2>
                            <button className="modal-close" onClick={() => setShowModal(false)}>
                                <X size={18} />
                            </button>
                        </div>
                        <div className="modal-body">
                            <div className="form-grid">
                                <div className="form-group">
                                    <label className="form-label">Name</label>
                                    <input className="form-input" value={selectedDoctor.name} readOnly />
                                </div>
                                <div className="form-group">
                                    <label className="form-label">Specialization</label>
                                    <input className="form-input" value={selectedDoctor.specialization} readOnly />
                                </div>
                                <div className="form-group">
                                    <label className="form-label">Experience</label>
                                    <input className="form-input" value={`${selectedDoctor.experience} years`} readOnly />
                                </div>
                                <div className="form-group">
                                    <label className="form-label">Rating</label>
                                    <input className="form-input" value={selectedDoctor.rating} readOnly />
                                </div>
                                <div className="form-group">
                                    <label className="form-label">Email</label>
                                    <input className="form-input" value={selectedDoctor.email} readOnly />
                                </div>
                                <div className="form-group">
                                    <label className="form-label">Phone</label>
                                    <input className="form-input" value={selectedDoctor.phone} readOnly />
                                </div>
                                <div className="form-group">
                                    <label className="form-label">Total Patients</label>
                                    <input className="form-input" value={selectedDoctor.patients} readOnly />
                                </div>
                                <div className="form-group">
                                    <label className="form-label">Total Appointments</label>
                                    <input className="form-input" value={selectedDoctor.appointments} readOnly />
                                </div>
                                <div className="form-group full-width">
                                    <label className="form-label">Status</label>
                                    <input className="form-input" value={selectedDoctor.status} readOnly />
                                </div>
                            </div>
                        </div>
                        <div className="modal-footer">
                            <button className="btn-secondary" onClick={() => setShowModal(false)}>
                                Close
                            </button>
                            <button className="btn btn-primary" onClick={() => handleEdit(selectedDoctor)}>
                                <Edit size={16} />
                                Edit Doctor
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Doctors;
