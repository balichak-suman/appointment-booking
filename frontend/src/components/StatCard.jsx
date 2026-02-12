import React from 'react';
import { Card, CardContent, Box, Typography } from '@mui/material';

const StatCard = ({ title, value, icon, color = '#38B2AC', trend, subtitle }) => {
    return (
        <Card
            sx={{
                height: '100%',
                background: `linear-gradient(135deg, ${color}10 0%, ${color}20 100%)`,
                border: `1px solid ${color}30`,
                transition: 'transform 0.2s, box-shadow 0.2s',
                '&:hover': {
                    transform: 'translateY(-4px)',
                    boxShadow: '0px 8px 24px rgba(0, 0, 0, 0.12)',
                },
            }}
        >
            <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', mb: 2 }}>
                    <Box>
                        <Typography variant="caption" color="text.secondary" fontWeight={600} sx={{ textTransform: 'uppercase', letterSpacing: '0.5px' }}>
                            {title}
                        </Typography>
                        <Typography variant="h4" fontWeight={700} sx={{ color, mt: 0.5 }}>
                            {value}
                        </Typography>
                        {subtitle && (
                            <Typography variant="caption" color="text.secondary" sx={{ mt: 0.5, display: 'block' }}>
                                {subtitle}
                            </Typography>
                        )}
                    </Box>
                    <Box
                        sx={{
                            width: 48,
                            height: 48,
                            borderRadius: '12px',
                            background: color,
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            color: 'white',
                        }}
                    >
                        {icon}
                    </Box>
                </Box>
                {trend && (
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                        <Typography
                            variant="caption"
                            sx={{
                                color: trend.value >= 0 ? '#48BB78' : '#F56565',
                                fontWeight: 600,
                            }}
                        >
                            {trend.value >= 0 ? '↑' : '↓'} {Math.abs(trend.value)}%
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                            {trend.label}
                        </Typography>
                    </Box>
                )}
            </CardContent>
        </Card>
    );
};

export default StatCard;
