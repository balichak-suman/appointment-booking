import React, { useState, useEffect } from 'react';
import {
    UserCheck, UserPlus, Search, Download, Eye, Edit, Trash2,
    X, Mail, Phone, Calendar, Activity
} from 'lucide-react';
import axios from 'axios';
import './Doctors.css'; // Reusing the same styles

const Patients = () => {
    const [patients, setPatients] = useState([]);
    const [filteredPatients, setFilteredPatients] = useState([]);
    const [loading, setLoading] = useState(true);
    const [searchTerm, setSearchTerm] = useState('');
    const [filterGender, setFilterGender] = useState('');
    const [filterStatus, setFilterStatus] = useState('');
    const [currentPage, setCurrentPage] = useState(1);
    const [showModal, setShowModal] = useState(false);
    const [selectedPatient, setSelectedPatient] = useState(null);
    const itemsPerPage = 10;

    useEffect(() => {
        fetchPatients();
    }, []);

    useEffect(() => {
        filterPatients();
    }, [searchTerm, filterGender, filterStatus, patients]);

    const fetchPatients = async () => {
        try {
            const response = await axios.get(`${import.meta.env.VITE_API_URL || 'http://localhost:8001'}/api/patients?limit=250`);
            setPatients(response.data.patients);
            setFilteredPatients(response.data.patients);
            setLoading(false);
        } catch (error) {
            console.error('Error fetching patients:', error);
            setLoading(false);
        }
    };

    const filterPatients = () => {
        let filtered = patients;

        if (searchTerm) {
            filtered = filtered.filter(patient =>
                patient.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                patient.email.toLowerCase().includes(searchTerm.toLowerCase())
            );
        }

        if (filterGender) {
            filtered = filtered.filter(patient => patient.gender === filterGender);
        }

        if (filterStatus) {
            filtered = filtered.filter(patient => patient.status === filterStatus);
        }

        setFilteredPatients(filtered);
        setCurrentPage(1);
    };

    const getStatusClass = (status) => {
        return status === 'Active' ? 'available' : 'on-leave';
    };

    const getInitials = (name) => {
        return name.split(' ').map(n => n[0]).join('').substring(0, 2);
    };

    const handleView = (patient) => {
        setSelectedPatient(patient);
        setShowModal(true);
    };

    const handleEdit = (patient) => {
        console.log('Edit patient:', patient);
    };

    const handleDelete = (patient) => {
        if (window.confirm(`Are you sure you want to delete ${patient.name}?`)) {
            console.log('Delete patient:', patient);
        }
    };

    const exportToCSV = () => {
        console.log('Exporting to CSV...');
    };

    // Pagination
    const indexOfLastItem = currentPage * itemsPerPage;
    const indexOfFirstItem = indexOfLastItem - itemsPerPage;
    const currentPatients = filteredPatients.slice(indexOfFirstItem, indexOfLastItem);
    const totalPages = Math.ceil(filteredPatients.length / itemsPerPage);

    const stats = {
        total: patients.length,
        active: patients.filter(p => p.status === 'Active').length,
        inactive: patients.filter(p => p.status === 'Inactive').length,
        male: patients.filter(p => p.gender === 'Male').length,
        female: patients.filter(p => p.gender === 'Female').length,
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
                    <h1>Patients Management</h1>
                    <p>Manage and monitor all patients in the system</p>
                </div>
                <div className="page-actions">
                    <button className="btn btn-primary" onClick={() => setShowModal(true)}>
                        <UserPlus size={18} />
                        Add New Patient
                    </button>
                </div>
            </div>

            {/* Stats Cards */}
            <div className="stats-cards-row">
                <div className="stat-card">
                    <div className="stat-card-header">
                        <div className="stat-icon">
                            <UserCheck size={20} />
                        </div>
                    </div>
                    <div className="stat-value">{stats.total}</div>
                    <div className="stat-label">Total Patients</div>
                </div>

                <div className="stat-card">
                    <div className="stat-card-header">
                        <div className="stat-icon" style={{ background: 'linear-gradient(135deg, #10B981, #34D399)' }}>
                            <Activity size={20} />
                        </div>
                    </div>
                    <div className="stat-value">{stats.active}</div>
                    <div className="stat-label">Active</div>
                </div>

                <div className="stat-card">
                    <div className="stat-card-header">
                        <div className="stat-icon" style={{ background: 'linear-gradient(135deg, #667eea, #764ba2)' }}>
                            <UserCheck size={20} />
                        </div>
                    </div>
                    <div className="stat-value">{stats.male}</div>
                    <div className="stat-label">Male</div>
                </div>

                <div className="stat-card">
                    <div className="stat-card-header">
                        <div className="stat-icon" style={{ background: 'linear-gradient(135deg, #f093fb, #f5576c)' }}>
                            <UserCheck size={20} />
                        </div>
                    </div>
                    <div className="stat-value">{stats.female}</div>
                    <div className="stat-label">Female</div>
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
                            placeholder="Search by name or email..."
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                        />
                    </div>

                    <div className="filter-group">
                        <label className="filter-label">Gender</label>
                        <select
                            className="filter-select"
                            value={filterGender}
                            onChange={(e) => setFilterGender(e.target.value)}
                        >
                            <option value="">All Genders</option>
                            <option value="Male">Male</option>
                            <option value="Female">Female</option>
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
                            <option value="Active">Active</option>
                            <option value="Inactive">Inactive</option>
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
                    <h2 className="table-title">All Patients ({filteredPatients.length})</h2>
                </div>

                <div className="table-container">
                    <table className="data-table">
                        <thead>
                            <tr>
                                <th>Patient</th>
                                <th>Age / Gender</th>
                                <th>Blood Group</th>
                                <th>Condition</th>
                                <th>Last Visit</th>
                                <th>Status</th>
                                <th>Contact</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {currentPatients.map(patient => (
                                <tr key={patient.id}>
                                    <td>
                                        <div className="doctor-info">
                                            <div className="doctor-avatar" style={{
                                                background: patient.gender === 'Male'
                                                    ? 'linear-gradient(135deg, #667eea, #764ba2)'
                                                    : 'linear-gradient(135deg, #f093fb, #f5576c)'
                                            }}>
                                                {getInitials(patient.name)}
                                            </div>
                                            <div className="doctor-details">
                                                <h4>{patient.name}</h4>
                                                <p>{patient.email}</p>
                                            </div>
                                        </div>
                                    </td>
                                    <td>{patient.age} / {patient.gender}</td>
                                    <td>
                                        <span style={{
                                            padding: '0.25rem 0.5rem',
                                            background: 'rgba(239, 68, 68, 0.1)',
                                            color: '#EF4444',
                                            borderRadius: '4px',
                                            fontSize: '0.75rem',
                                            fontWeight: '600'
                                        }}>
                                            {patient.bloodGroup}
                                        </span>
                                    </td>
                                    <td>{patient.condition}</td>
                                    <td>
                                        <div style={{ display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
                                            <Calendar size={14} />
                                            {patient.lastVisit}
                                        </div>
                                    </td>
                                    <td>
                                        <span className={`status-badge ${getStatusClass(patient.status)}`}>
                                            <span className="status-dot"></span>
                                            {patient.status}
                                        </span>
                                    </td>
                                    <td>
                                        <div style={{ fontSize: '0.75rem' }}>
                                            <div style={{ display: 'flex', alignItems: 'center', gap: '0.25rem', marginBottom: '0.25rem' }}>
                                                <Phone size={12} />
                                                {patient.phone}
                                            </div>
                                            <div style={{ display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
                                                <Mail size={12} />
                                                {patient.email}
                                            </div>
                                        </div>
                                    </td>
                                    <td>
                                        <div className="action-buttons">
                                            <button className="action-btn" onClick={() => handleView(patient)} title="View">
                                                <Eye size={16} />
                                            </button>
                                            <button className="action-btn" onClick={() => handleEdit(patient)} title="Edit">
                                                <Edit size={16} />
                                            </button>
                                            <button className="action-btn delete" onClick={() => handleDelete(patient)} title="Delete">
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
                        Showing {indexOfFirstItem + 1} to {Math.min(indexOfLastItem, filteredPatients.length)} of {filteredPatients.length} patients
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

            {/* View Patient Modal */}
            {showModal && selectedPatient && (
                <div className="modal-overlay" onClick={() => setShowModal(false)}>
                    <div className="modal" onClick={(e) => e.stopPropagation()}>
                        <div className="modal-header">
                            <h2 className="modal-title">Patient Details</h2>
                            <button className="modal-close" onClick={() => setShowModal(false)}>
                                <X size={18} />
                            </button>
                        </div>
                        <div className="modal-body">
                            <div className="form-grid">
                                <div className="form-group">
                                    <label className="form-label">Name</label>
                                    <input className="form-input" value={selectedPatient.name} readOnly />
                                </div>
                                <div className="form-group">
                                    <label className="form-label">Age</label>
                                    <input className="form-input" value={selectedPatient.age} readOnly />
                                </div>
                                <div className="form-group">
                                    <label className="form-label">Gender</label>
                                    <input className="form-input" value={selectedPatient.gender} readOnly />
                                </div>
                                <div className="form-group">
                                    <label className="form-label">Blood Group</label>
                                    <input className="form-input" value={selectedPatient.bloodGroup} readOnly />
                                </div>
                                <div className="form-group">
                                    <label className="form-label">Email</label>
                                    <input className="form-input" value={selectedPatient.email} readOnly />
                                </div>
                                <div className="form-group">
                                    <label className="form-label">Phone</label>
                                    <input className="form-input" value={selectedPatient.phone} readOnly />
                                </div>
                                <div className="form-group">
                                    <label className="form-label">Condition</label>
                                    <input className="form-input" value={selectedPatient.condition} readOnly />
                                </div>
                                <div className="form-group">
                                    <label className="form-label">Last Visit</label>
                                    <input className="form-input" value={selectedPatient.lastVisit} readOnly />
                                </div>
                                <div className="form-group full-width">
                                    <label className="form-label">Address</label>
                                    <input className="form-input" value={selectedPatient.address} readOnly />
                                </div>
                                <div className="form-group full-width">
                                    <label className="form-label">Status</label>
                                    <input className="form-input" value={selectedPatient.status} readOnly />
                                </div>
                            </div>
                        </div>
                        <div className="modal-footer">
                            <button className="btn-secondary" onClick={() => setShowModal(false)}>
                                Close
                            </button>
                            <button className="btn btn-primary" onClick={() => handleEdit(selectedPatient)}>
                                <Edit size={16} />
                                Edit Patient
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Patients;
