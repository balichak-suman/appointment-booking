import React, { useState, useEffect } from 'react';
import {
    TextField,
    Autocomplete,
    InputAdornment,
    Box,
    Typography,
    Chip,
    CircularProgress
} from '@mui/material';
import { Search as SearchIcon } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import api from '../../services/api';

const GlobalSearch = () => {
    const [open, setOpen] = useState(false);
    const [options, setOptions] = useState([]);
    const [loading, setLoading] = useState(false);
    const [inputValue, setInputValue] = useState('');
    const navigate = useNavigate();

    useEffect(() => {
        let active = true;

        if (inputValue.length < 2) {
            setOptions([]);
            return undefined;
        }

        const fetchResults = async () => {
            setLoading(true);
            try {
                const response = await api.get(`/search`, {
                    params: { q: inputValue }
                });
                if (active) {
                    setOptions(response.data);
                }
            } catch (error) {
                console.error("Search failed:", error);
            } finally {
                if (active) {
                    setLoading(false);
                }
            }
        };

        const timer = setTimeout(() => {
            fetchResults();
        }, 500);

        return () => {
            active = false;
            clearTimeout(timer);
        };
    }, [inputValue]);

    return (
        <Autocomplete
            id="global-search"
            sx={{
                width: 300,
                ml: 2,
                display: { xs: 'none', md: 'block' }
            }}
            open={open}
            onOpen={() => {
                if (inputValue.length >= 2) setOpen(true);
            }}
            onClose={() => setOpen(false)}
            isOptionEqualToValue={(option, value) => option.id === value.id && option.type === value.type}
            getOptionLabel={(option) => option.title}
            options={options}
            loading={loading}
            onInputChange={(event, newInputValue) => {
                setInputValue(newInputValue);
                if (newInputValue.length >= 2) {
                    setOpen(true);
                } else {
                    setOpen(false);
                }
            }}
            onChange={(event, newValue) => {
                if (newValue && newValue.link) {
                    navigate(newValue.link);
                    setOpen(false);
                    setInputValue('');
                }
            }}
            renderOption={(props, option) => {
                const { key, ...optionProps } = props;
                return (
                    <Box component="li" key={key} {...optionProps}>
                        <Box sx={{ display: 'flex', flexDirection: 'column', width: '100%' }}>
                            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                                <Typography variant="body2" fontWeight="600">{option.title}</Typography>
                                <Chip
                                    label={option.type}
                                    size="small"
                                    color={
                                        option.type === 'doctor' ? 'primary' :
                                            option.type === 'patient' ? 'secondary' :
                                                option.type === 'appointment' ? 'success' : 'default'
                                    }
                                    sx={{ height: 16, fontSize: '0.6rem', textTransform: 'uppercase' }}
                                />
                            </Box>
                            <Typography variant="caption" color="text.secondary" noWrap>
                                {option.subtitle}
                            </Typography>
                        </Box>
                    </Box>
                );
            }}
            renderInput={(params) => (
                <TextField
                    {...params}
                    placeholder="Search patients, doctors..."
                    size="small"
                    InputProps={{
                        ...params.InputProps,
                        startAdornment: (
                            <InputAdornment position="start">
                                <SearchIcon color="action" />
                            </InputAdornment>
                        ),
                        endAdornment: (
                            <React.Fragment>
                                {loading ? <CircularProgress color="inherit" size={20} /> : null}
                                {params.InputProps.endAdornment}
                            </React.Fragment>
                        ),
                        sx: {
                            borderRadius: '20px',
                            backgroundColor: '#f5f7fa',
                            '& fieldset': { border: 'none' },
                            '&:hover': {
                                backgroundColor: '#e4e7eb'
                            }
                        }
                    }}
                />
            )}
        />
    );
};

export default GlobalSearch;
