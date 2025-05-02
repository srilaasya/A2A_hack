import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useSpring, animated } from '@react-spring/web';
import { useInView } from 'react-intersection-observer';
import { HexColorPicker } from 'react-colorful';
import Confetti from 'react-confetti';
import { useStore } from './store';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { Box, Typography, IconButton, Paper, Grid } from '@mui/material';
import { styled } from '@mui/material/styles';
import SearchIcon from '@mui/icons-material/Search';
import CodeIcon from '@mui/icons-material/Code';
import DataObjectIcon from '@mui/icons-material/DataObject';
import RocketLaunchIcon from '@mui/icons-material/RocketLaunch';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import { loadSlim } from 'tsparticles-slim';
import { Engine } from 'tsparticles-engine';

// Custom theme with futuristic colors
const theme = createTheme({
    palette: {
        mode: 'dark',
        primary: {
            main: '#00ff9d',
        },
        secondary: {
            main: '#00b8ff',
        },
        background: {
            default: '#0a1929',
            paper: '#112240',
        },
    },
    typography: {
        fontFamily: '"Space Mono", monospace',
    },
});

// Styled components
const Container = styled(Box)(({ theme }) => ({
    height: '100vh',
    overflow: 'hidden',
    position: 'relative',
    background: 'linear-gradient(45deg, #0a1929 0%, #112240 100%)',
}));

const GlassPanel = styled(Paper)(({ theme }) => ({
    background: 'rgba(17, 34, 64, 0.7)',
    backdropFilter: 'blur(10px)',
    border: '1px solid rgba(255, 255, 255, 0.1)',
    borderRadius: '20px',
    padding: theme.spacing(3),
}));

const WorkflowStep = styled(motion.div)(({ theme, active }) => ({
    display: 'flex',
    alignItems: 'center',
    gap: theme.spacing(2),
    padding: theme.spacing(2),
    borderRadius: '15px',
    background: active ? 'rgba(0, 255, 157, 0.1)' : 'transparent',
    border: `1px solid ${active ? 'rgba(0, 255, 157, 0.3)' : 'rgba(255, 255, 255, 0.1)'}`,
}));

const App = () => {
    const [showConfetti, setShowConfetti] = useState(false);
    const [workflowStep, setWorkflowStep] = useState(0);
    const [searchQuery, setSearchQuery] = useState('');
    const [properties, setProperties] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [ref, inView] = useInView({ threshold: 0.5 });

    // Spring animations
    const searchSpring = useSpring({
        transform: `scale(${isLoading ? 1.1 : 1})`,
        config: { tension: 300, friction: 20 },
    });

    // Particle effects
    const particlesInit = async (engine) => {
        await loadSlim(engine);
    };

    // Workflow steps
    const workflowSteps = [
        {
            id: 1,
            title: 'User Input',
            icon: <SearchIcon />,
            description: 'Enter property search criteria',
        },
        {
            id: 2,
            title: 'A2A Processing',
            icon: <CodeIcon />,
            description: 'Agent processes the request',
        },
        {
            id: 3,
            title: 'API Integration',
            icon: <DataObjectIcon />,
            description: 'Fetching real-time property data',
        },
        {
            id: 4,
            title: 'Results',
            icon: <CheckCircleIcon />,
            description: 'Displaying property matches',
        },
    ];

    const handleSearch = async () => {
        if (!searchQuery.trim()) return;

        setIsLoading(true);
        setWorkflowStep(1);

        try {
            // Simulate A2A workflow steps
            for (let i = 1; i <= 4; i++) {
                setWorkflowStep(i);
                await new Promise(resolve => setTimeout(resolve, 1000));
            }

            // Make API request
            const response = await fetch('http://localhost:10002/execute', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    task_id: `search-${Date.now()}`,
                    task_type: 'property_search',
                    parameters: {
                        location: searchQuery,
                        price_range: '$500k-$1M',
                        bedrooms: 2,
                        bathrooms: 2,
                        property_type: 'condo',
                    },
                }),
            });

            const data = await response.json();
            setProperties(data.result);
            setShowConfetti(true);
            setTimeout(() => setShowConfetti(false), 5000);
        } catch (error) {
            console.error('Error:', error);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <ThemeProvider theme={theme}>
            <CssBaseline />
            <Container>
                {/* Particles */}
                <Engine
                    id="tsparticles"
                    init={particlesInit}
                    options={{
                        particles: {
                            number: {
                                value: 80,
                                density: {
                                    enable: true,
                                    value_area: 800,
                                },
                            },
                            color: {
                                value: '#00ff9d',
                            },
                            shape: {
                                type: 'circle',
                            },
                            opacity: {
                                value: 0.5,
                                random: true,
                            },
                            size: {
                                value: 3,
                                random: true,
                            },
                            line_linked: {
                                enable: true,
                                distance: 150,
                                color: '#00ff9d',
                                opacity: 0.4,
                                width: 1,
                            },
                            move: {
                                enable: true,
                                speed: 2,
                                direction: 'none',
                                random: true,
                                straight: false,
                                out_mode: 'out',
                                bounce: false,
                            },
                        },
                        interactivity: {
                            detect_on: 'canvas',
                            events: {
                                onhover: {
                                    enable: true,
                                    mode: 'grab',
                                },
                                onclick: {
                                    enable: true,
                                    mode: 'push',
                                },
                                resize: true,
                            },
                        },
                        retina_detect: true,
                    }}
                />

                {/* Main Content */}
                <Grid container spacing={4} sx={{ p: 4, position: 'relative', zIndex: 1 }}>
                    {/* Left Panel - Workflow Visualization */}
                    <Grid item xs={12} md={4}>
                        <GlassPanel>
                            <Typography variant="h5" gutterBottom sx={{ color: 'primary.main' }}>
                                A2A Workflow
                            </Typography>
                            {workflowSteps.map((step, index) => (
                                <WorkflowStep
                                    key={step.id}
                                    active={workflowStep === step.id}
                                    initial={{ opacity: 0, x: -20 }}
                                    animate={{ opacity: 1, x: 0 }}
                                    transition={{ delay: index * 0.2 }}
                                >
                                    <IconButton sx={{ color: 'primary.main' }}>
                                        {step.icon}
                                    </IconButton>
                                    <Box>
                                        <Typography variant="subtitle1">{step.title}</Typography>
                                        <Typography variant="body2" color="text.secondary">
                                            {step.description}
                                        </Typography>
                                    </Box>
                                </WorkflowStep>
                            ))}
                        </GlassPanel>
                    </Grid>

                    {/* Right Panel - Search and Results */}
                    <Grid item xs={12} md={8}>
                        <GlassPanel>
                            <animated.div style={searchSpring}>
                                <Box sx={{ display: 'flex', gap: 2, mb: 4 }}>
                                    <input
                                        type="text"
                                        value={searchQuery}
                                        onChange={(e) => setSearchQuery(e.target.value)}
                                        placeholder="Enter property address..."
                                        style={{
                                            flex: 1,
                                            padding: '12px',
                                            borderRadius: '10px',
                                            background: 'rgba(255, 255, 255, 0.1)',
                                            border: '1px solid rgba(255, 255, 255, 0.2)',
                                            color: 'white',
                                            fontSize: '16px',
                                        }}
                                    />
                                    <IconButton
                                        onClick={handleSearch}
                                        disabled={isLoading}
                                        sx={{
                                            background: 'linear-gradient(45deg, #00ff9d 30%, #00b8ff 90%)',
                                            '&:hover': {
                                                background: 'linear-gradient(45deg, #00b8ff 30%, #00ff9d 90%)',
                                            },
                                        }}
                                    >
                                        <RocketLaunchIcon />
                                    </IconButton>
                                </Box>
                            </animated.div>

                            {/* Results */}
                            <AnimatePresence>
                                {properties.length > 0 && (
                                    <motion.div
                                        initial={{ opacity: 0, y: 20 }}
                                        animate={{ opacity: 1, y: 0 }}
                                        exit={{ opacity: 0, y: -20 }}
                                    >
                                        <Grid container spacing={2}>
                                            {properties.map((property, index) => (
                                                <Grid item xs={12} sm={6} key={index}>
                                                    <motion.div
                                                        initial={{ opacity: 0, scale: 0.8 }}
                                                        animate={{ opacity: 1, scale: 1 }}
                                                        transition={{ delay: index * 0.1 }}
                                                    >
                                                        <GlassPanel>
                                                            <Typography variant="h6" gutterBottom>
                                                                {property.address}
                                                            </Typography>
                                                            <Typography variant="body2" color="text.secondary">
                                                                Price: {property.price}
                                                            </Typography>
                                                            <Typography variant="body2" color="text.secondary">
                                                                {property.bedrooms} beds • {property.bathrooms} baths
                                                            </Typography>
                                                        </GlassPanel>
                                                    </motion.div>
                                                </Grid>
                                            ))}
                                        </Grid>
                                    </motion.div>
                                )}
                            </AnimatePresence>
                        </GlassPanel>
                    </Grid>
                </Grid>

                {/* Confetti Effect */}
                {showConfetti && (
                    <Confetti
                        width={window.innerWidth}
                        height={window.innerHeight}
                        recycle={false}
                        numberOfPieces={500}
                    />
                )}
            </Container>
        </ThemeProvider>
    );
};

export default App; 