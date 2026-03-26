import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import IconButton from '@mui/material/IconButton';
import Box from '@mui/material/Box';
import Avatar from '@mui/material/Avatar';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import Tooltip from '@mui/material/Tooltip';
import Divider from '@mui/material/Divider';
import GrassIcon from '@mui/icons-material/Grass';
import DashboardIcon from '@mui/icons-material/Dashboard';
import AddCircleOutlineIcon from '@mui/icons-material/AddCircleOutline';
import LogoutIcon from '@mui/icons-material/Logout';
import { useAuth } from '../../contexts/AuthContext';

export const Navbar: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { user, logout } = useAuth();
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);

  const handleMenuOpen = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  const handleLogout = () => {
    handleMenuClose();
    logout();
    navigate('/login');
  };

  const isActive = (path: string) => location.pathname === path;

  const initials = user?.full_name
    ? user.full_name.charAt(0).toUpperCase()
    : user?.email.charAt(0).toUpperCase() ?? '?';

  return (
    <AppBar position="fixed" color="primary" elevation={2}>
      <Toolbar sx={{ gap: 1 }}>
        {/* Logo / Brand */}
        <GrassIcon sx={{ ml: 0, mr: 1 }} />
        <Typography
          variant="h6"
          component="div"
          sx={{ fontWeight: 700, cursor: 'pointer', mr: 2 }}
          onClick={() => navigate('/dashboard')}
        >
          Al-Hasade | الحصاد
        </Typography>

        {/* Navigation links */}
        <Box sx={{ display: 'flex', gap: 1, flexGrow: 1 }}>
          <Button
            color="inherit"
            startIcon={<DashboardIcon />}
            onClick={() => navigate('/dashboard')}
            sx={{
              fontWeight: isActive('/dashboard') ? 700 : 400,
              borderBottom: isActive('/dashboard') ? '2px solid white' : 'none',
              borderRadius: 0,
              pb: '2px',
            }}
          >
            לוח בקרה / لوحة التحكم
          </Button>
          <Button
            color="inherit"
            startIcon={<AddCircleOutlineIcon />}
            onClick={() => navigate('/generate')}
            sx={{
              fontWeight: isActive('/generate') ? 700 : 400,
              borderBottom: isActive('/generate') ? '2px solid white' : 'none',
              borderRadius: 0,
              pb: '2px',
            }}
          >
            יצירה חדשה / إنشاء جديد
          </Button>
        </Box>

        {/* User avatar + menu */}
        <Tooltip title={user?.email ?? ''}>
          <IconButton onClick={handleMenuOpen} sx={{ p: 0.5 }}>
            <Avatar
              sx={{ bgcolor: 'secondary.main', width: 36, height: 36, fontSize: 16 }}
            >
              {initials}
            </Avatar>
          </IconButton>
        </Tooltip>

        <Menu
          anchorEl={anchorEl}
          open={Boolean(anchorEl)}
          onClose={handleMenuClose}
          transformOrigin={{ horizontal: 'right', vertical: 'top' }}
          anchorOrigin={{ horizontal: 'right', vertical: 'bottom' }}
          PaperProps={{ sx: { minWidth: 200 } }}
        >
          <Box sx={{ px: 2, py: 1 }}>
            {user?.full_name && (
              <Typography variant="subtitle2" fontWeight={600}>
                {user.full_name}
              </Typography>
            )}
            <Typography variant="body2" color="text.secondary">
              {user?.email}
            </Typography>
          </Box>
          <Divider />
          <MenuItem onClick={handleLogout} sx={{ gap: 1, color: 'error.main' }}>
            <LogoutIcon fontSize="small" />
            התנתק / تسجيل الخروج
          </MenuItem>
        </Menu>
      </Toolbar>
    </AppBar>
  );
};
