import React, { useState } from 'react';
import {
    LayoutDashboard, Users, UserCheck, Calendar, MapPin,
    Stethoscope, Award, Package, Settings, LogOut,
    ChevronDown, Bell, Search, Menu
} from 'lucide-react';
import './Sidebar.css';

const Sidebar = ({ activeMenu, setActiveMenu }) => {
    const [isOpen, setIsOpen] = useState(true);

    const menuItems = [
        {
            section: 'Main Menu',
            items: [
                { id: 'dashboard', label: 'Dashboard (CLEAN)', icon: LayoutDashboard, active: true },
                { id: 'doctors', label: 'Doctors (CLEAN)', icon: Users },
                { id: 'patients', label: 'Patients (CLEAN)', icon: UserCheck },
                { id: 'appointments', label: 'Appointments (CLEAN)', icon: Calendar },
            ]
        },
        {
            section: 'Settings',
            items: [
                { id: 'settings', label: 'Settings', icon: Settings },
            ]
        }
    ];

    return (
        <div className={`sidebar ${isOpen ? 'open' : ''}`}>
            {/* Sidebar Header */}
            <div className="sidebar-header">
                <div className="sidebar-logo">
                    <div className="sidebar-logo-icon">
                        <Stethoscope size={24} />
                    </div>
                    <div className="sidebar-logo-text">
                        <h2>Preclinic</h2>
                        <p>Trustcare Clinic</p>
                    </div>
                </div>
            </div>

            {/* Sidebar Menu */}
            <div className="sidebar-menu">
                {menuItems.map((section, idx) => (
                    <div key={idx} className="menu-section">
                        <div className="menu-section-title">{section.section}</div>
                        <ul className="menu-items">
                            {section.items.map((item) => {
                                const Icon = item.icon;
                                return (
                                    <li key={item.id} className="menu-item">
                                        <div
                                            className={`menu-link ${activeMenu === item.id ? 'active' : ''}`}
                                            onClick={() => setActiveMenu(item.id)}
                                        >
                                            <Icon className="menu-icon" size={20} />
                                            <span>{item.label}</span>
                                            {item.badge && <span className="menu-badge">{item.badge}</span>}
                                        </div>
                                    </li>
                                );
                            })}
                        </ul>
                    </div>
                ))}
            </div>

            {/* Sidebar Footer */}
            <div className="sidebar-footer">
                <div className="user-profile">
                    <div className="user-avatar">AD</div>
                    <div className="user-info">
                        <p className="user-name">Dr. Admin</p>
                        <p className="user-role">Administrator</p>
                    </div>
                    <ChevronDown className="user-menu-icon" size={16} />
                </div>
            </div>
        </div>
    );
};

export default Sidebar;
