import React from 'react';
import { Card, CardContent, Box, Typography, IconButton } from '@mui/material';
import { ChevronLeft, ChevronRight } from '@mui/icons-material';

const CalendarWidget = ({ appointments = [] }) => {
    const [currentDate, setCurrentDate] = React.useState(new Date());

    const getDaysInMonth = (date) => {
        const year = date.getFullYear();
        const month = date.getMonth();
        const firstDay = new Date(year, month, 1);
        const lastDay = new Date(year, month + 1, 0);
        const daysInMonth = lastDay.getDate();
        const startingDayOfWeek = firstDay.getDay();

        return { daysInMonth, startingDayOfWeek };
    };

    const { daysInMonth, startingDayOfWeek } = getDaysInMonth(currentDate);
    const monthName = currentDate.toLocaleDateString('en-US', { month: 'long', year: 'numeric' });
    const today = new Date().getDate();
    const isCurrentMonth = currentDate.getMonth() === new Date().getMonth() &&
        currentDate.getFullYear() === new Date().getFullYear();

    const handlePrevMonth = () => {
        setCurrentDate(new Date(currentDate.getFullYear(), currentDate.getMonth() - 1));
    };

    const handleNextMonth = () => {
        setCurrentDate(new Date(currentDate.getFullYear(), currentDate.getMonth() + 1));
    };

    const getAppointmentCount = (day) => {
        const dateStr = `${currentDate.getFullYear()}-${String(currentDate.getMonth() + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
        return appointments.filter(apt => apt.appointmentDate === dateStr).length;
    };

    return (
        <Card sx={{ height: '100%' }}>
            <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                    <Typography variant="h6" fontWeight={700}>
                        {monthName}
                    </Typography>
                    <Box>
                        <IconButton size="small" onClick={handlePrevMonth}>
                            <ChevronLeft />
                        </IconButton>
                        <IconButton size="small" onClick={handleNextMonth}>
                            <ChevronRight />
                        </IconButton>
                    </Box>
                </Box>

                <Box sx={{ display: 'grid', gridTemplateColumns: 'repeat(7, 1fr)', gap: 0.5, mb: 1 }}>
                    {['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].map((day) => (
                        <Box key={day} sx={{ textAlign: 'center', py: 1 }}>
                            <Typography variant="caption" fontWeight={600} color="text.secondary">
                                {day}
                            </Typography>
                        </Box>
                    ))}
                </Box>

                <Box sx={{ display: 'grid', gridTemplateColumns: 'repeat(7, 1fr)', gap: 0.5 }}>
                    {Array.from({ length: startingDayOfWeek }).map((_, index) => (
                        <Box key={`empty-${index}`} sx={{ aspectRatio: '1', p: 0.5 }} />
                    ))}
                    {Array.from({ length: daysInMonth }).map((_, index) => {
                        const day = index + 1;
                        const isToday = isCurrentMonth && day === today;
                        const appointmentCount = getAppointmentCount(day);

                        return (
                            <Box
                                key={day}
                                sx={{
                                    aspectRatio: '1',
                                    p: 0.5,
                                    display: 'flex',
                                    flexDirection: 'column',
                                    alignItems: 'center',
                                    justifyContent: 'center',
                                    borderRadius: 2,
                                    cursor: 'pointer',
                                    position: 'relative',
                                    bgcolor: isToday ? 'primary.main' : 'transparent',
                                    color: isToday ? 'white' : 'text.primary',
                                    '&:hover': {
                                        bgcolor: isToday ? 'primary.dark' : 'grey.100',
                                    },
                                }}
                            >
                                <Typography variant="body2" fontWeight={isToday ? 700 : 500}>
                                    {day}
                                </Typography>
                                {appointmentCount > 0 && (
                                    <Box
                                        sx={{
                                            width: 6,
                                            height: 6,
                                            borderRadius: '50%',
                                            bgcolor: isToday ? 'white' : 'primary.main',
                                            mt: 0.25,
                                        }}
                                    />
                                )}
                            </Box>
                        );
                    })}
                </Box>
            </CardContent>
        </Card>
    );
};

export default CalendarWidget;
