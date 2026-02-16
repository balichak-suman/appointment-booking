import { IconButton, Tooltip } from '@mui/material';
import { Delete as DeleteIcon } from '@mui/icons-material';

const DoctorCard = ({ doctor, onDelete }) => {
    if (!doctor) return null;
    const { id, name, department, totalAppointments = 0, completed = 0, waiting = 0 } = doctor;

    const completionRate = totalAppointments > 0 ? Math.round((completed / totalAppointments) * 100) : 0;

    return (
        <Card
            sx={{
                height: '100%',
                position: 'relative',
                transition: 'transform 0.2s, box-shadow 0.2s',
                '&:hover': {
                    transform: 'translateY(-2px)',
                    boxShadow: '0px 8px 20px rgba(0, 0, 0, 0.1)',
                },
            }}
        >
            {onDelete && (
                <Tooltip title="Delete Doctor">
                    <IconButton
                        size="small"
                        onClick={(e) => {
                            e.stopPropagation();
                            onDelete(id);
                        }}
                        sx={{
                            position: 'absolute',
                            top: 8,
                            right: 8,
                            color: 'text.secondary',
                            '&:hover': { color: 'error.main', bgcolor: 'error.lighter' }
                        }}
                    >
                        <DeleteIcon fontSize="small" />
                    </IconButton>
                </Tooltip>
            )}
            <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'flex-start', gap: 2 }}>
                    <Avatar
                        sx={{
                            width: 56,
                            height: 56,
                            bgcolor: 'primary.main',
                            fontSize: '1.5rem',
                            fontWeight: 700,
                        }}
                    >
                        {name?.charAt(0) || 'D'}
                    </Avatar>
                    <Box sx={{ flex: 1 }}>
                        <Typography variant="subtitle1" fontWeight={600}>
                            {name}
                        </Typography>
                        <Typography variant="caption" color="text.secondary" display="block">
                            {department}
                        </Typography>
                        <Box sx={{ display: 'flex', gap: 1, mt: 1.5, flexWrap: 'wrap' }}>
                            <Chip
                                label={`${totalAppointments} Total`}
                                size="small"
                                sx={{ bgcolor: 'grey.100', fontWeight: 500 }}
                            />
                            <Chip
                                label={`${completed} Done`}
                                size="small"
                                color="success"
                                variant="outlined"
                                sx={{ fontWeight: 500 }}
                            />
                            <Chip
                                label={`${waiting} Waiting`}
                                size="small"
                                color="warning"
                                variant="outlined"
                                sx={{ fontWeight: 500 }}
                            />
                        </Box>
                        {totalAppointments > 0 && (
                            <Box sx={{ mt: 2 }}>
                                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.5 }}>
                                    <Typography variant="caption" color="text.secondary">
                                        Completion Rate
                                    </Typography>
                                    <Typography variant="caption" fontWeight={600} color="primary.main">
                                        {completionRate}%
                                    </Typography>
                                </Box>
                                <Box
                                    sx={{
                                        height: 6,
                                        borderRadius: 3,
                                        bgcolor: 'grey.200',
                                        overflow: 'hidden',
                                    }}
                                >
                                    <Box
                                        sx={{
                                            height: '100%',
                                            width: `${completionRate}%`,
                                            bgcolor: 'primary.main',
                                            transition: 'width 0.3s ease',
                                        }}
                                    />
                                </Box>
                            </Box>
                        )}
                    </Box>
                </Box>
            </CardContent>
        </Card>
    );
};

export default DoctorCard;
