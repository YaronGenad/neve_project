import React from 'react';
import Box from '@mui/material/Box';
import { Navbar } from './Navbar';

interface AppLayoutProps {
  children: React.ReactNode;
}

export const AppLayout: React.FC<AppLayoutProps> = ({ children }) => {
  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        minHeight: '100vh',
        bgcolor: 'background.default',
      }}
    >
      <Navbar />
      {/* Offset for fixed AppBar (default height 64px) */}
      <Box component="main" sx={{ flexGrow: 1, pt: '64px' }}>
        {children}
      </Box>
    </Box>
  );
};
