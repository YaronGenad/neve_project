import { createTheme } from '@mui/material/styles';
import createCache from '@emotion/cache';
import { prefixer } from 'stylis';
import rtlPlugin from 'stylis-plugin-rtl';

// RTL Emotion cache
export const cacheRtl = createCache({
  key: 'muirtl',
  stylisPlugins: [prefixer, rtlPlugin],
});

export const theme = createTheme({
  direction: 'rtl',
  palette: {
    primary: {
      main: '#00796b', // teal-700 — calm educational green
      light: '#48a999',
      dark: '#004c40',
      contrastText: '#ffffff',
    },
    secondary: {
      main: '#26a69a', // teal-400
      light: '#64d8cb',
      dark: '#00766c',
      contrastText: '#ffffff',
    },
    background: {
      default: '#f5f7f6',
      paper: '#ffffff',
    },
    success: {
      main: '#388e3c',
    },
    error: {
      main: '#d32f2f',
    },
    info: {
      main: '#1976d2',
    },
    warning: {
      main: '#f57c00',
    },
  },
  typography: {
    fontFamily: [
      '"Noto Sans Hebrew"',
      '"Noto Sans Arabic"',
      '-apple-system',
      'BlinkMacSystemFont',
      '"Segoe UI"',
      'Roboto',
      'Arial',
      'sans-serif',
    ].join(','),
    h4: {
      fontWeight: 700,
    },
    h5: {
      fontWeight: 600,
    },
    h6: {
      fontWeight: 600,
    },
  },
  shape: {
    borderRadius: 10,
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',
          fontWeight: 600,
          borderRadius: 8,
        },
      },
    },
    MuiTextField: {
      defaultProps: {
        variant: 'outlined',
        fullWidth: true,
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          boxShadow: '0 2px 12px rgba(0,0,0,0.08)',
          borderRadius: 12,
        },
      },
    },
    MuiChip: {
      styleOverrides: {
        root: {
          fontWeight: 600,
        },
      },
    },
    MuiAppBar: {
      styleOverrides: {
        root: {
          boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
        },
      },
    },
  },
});
