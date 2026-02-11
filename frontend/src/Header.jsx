import React from 'react';
import { Search, Bell, Menu } from 'lucide-react';
import './Sidebar.css';

const Header = ({ pageTitle, breadcrumb, onToggleSidebar }) => {
    return (
        <div className="main-header">
            <div className="header-left">
                <button className="sidebar-toggle" onClick={onToggleSidebar}>
                    <Menu size={20} />
                </button>
                <div>
                    <h1 className="page-title">{pageTitle}</h1>
                    {breadcrumb && (
                        <div className="breadcrumb">
                            {breadcrumb.map((item, idx) => (
                                <React.Fragment key={idx}>
                                    {idx > 0 && <span className="breadcrumb-separator">/</span>}
                                    <span>{item}</span>
                                </React.Fragment>
                            ))}
                        </div>
                    )}
                </div>
            </div>

            <div className="header-right">
                <div className="search-box">
                    <Search className="search-icon" size={18} />
                    <input
                        type="text"
                        className="search-input"
                        placeholder="Search patients, doctors, appointments..."
                    />
                </div>

                <button className="notification-btn">
                    <Bell size={20} />
                </button>

                <div className="user-avatar">AD</div>
            </div>
        </div>
    );
};

export default Header;
