import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { AuthProvider } from './context/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';
import MainLayout from './components/Layout/MainLayout';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import AppointmentList from './pages/AppointmentList';
import Queue from './pages/Queue';
import Patients from './pages/Patients';
import Doctors from './pages/Doctors';

const theme = createTheme({
    palette: {
        mode: 'light',
        primary: {
            main: '#38B2AC',
            light: '#4FD1C5',
            dark: '#319795',
        },
        secondary: {
            main: '#4299E1',
            light: '#63B3ED',
        },
        background: {
            default: '#F7FAFC',
            paper: '#FFFFFF',
        },
        text: {
            primary: '#2D3748',
            secondary: '#4A5568',
        },
        success: { main: '#48BB78' },
        warning: { main: '#ED8936' },
        error: { main: '#F56565' },
    },
    typography: {
        fontFamily: '"Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", "Roboto", sans-serif',
        h4: { fontWeight: 700, fontSize: '1.5rem' },
        h5: { fontWeight: 600, fontSize: '1.25rem' },
        h6: { fontWeight: 600, fontSize: '1rem' },
        button: { fontWeight: 600, textTransform: 'none' },
    },
    shape: {
        borderRadius: 12,
    },
    shadows: [
        'none',
        '0px 2px 4px rgba(0, 0, 0, 0.05)',
        '0px 4px 6px rgba(0, 0, 0, 0.07)',
        '0px 5px 15px rgba(0, 0, 0, 0.08)',
        '0px 10px 24px rgba(0, 0, 0, 0.1)',
        ...Array(20).fill('0px 10px 24px rgba(0, 0, 0, 0.1)'),
    ],
    components: {
        MuiCard: {
            styleOverrides: {
                root: {
                    boxShadow: '0px 2px 8px rgba(0, 0, 0, 0.06)',
                    borderRadius: 16,
                },
            },
        },
        MuiButton: {
            styleOverrides: {
                root: {
                    borderRadius: 10,
                    padding: '10px 24px',
                    fontWeight: 600,
                    textTransform: 'none',
                },
                contained: {
                    boxShadow: 'none',
                    '&:hover': {
                        boxShadow: '0px 4px 12px rgba(56, 178, 172, 0.3)',
                    },
                },
            },
        },
        MuiChip: {
            styleOverrides: {
                root: {
                    borderRadius: 8,
                    fontWeight: 500,
                },
            },
        },
    },
});

function App() {
    return (
        <ThemeProvider theme={theme}>
            <CssBaseline />
            <AuthProvider>
                <BrowserRouter>
                    <Routes>
                        <Route path="/login" element={<Login />} />
                        <Route
                            path="/"
                            element={
                                <ProtectedRoute>
                                    <MainLayout />
                                </ProtectedRoute>
                            }
                        >
                            <Route index element={<Dashboard />} />
                            <Route path="appointments" element={<AppointmentList />} />
                            <Route path="queue" element={<Queue />} />
                            <Route path="patients" element={<Patients />} />
                            <Route path="doctors" element={<Doctors />} />
                        </Route>
                        <Route path="*" element={<Navigate to="/" replace />} />
                    </Routes>
                </BrowserRouter>
            </AuthProvider>
        </ThemeProvider>
    );
}

export default App;
