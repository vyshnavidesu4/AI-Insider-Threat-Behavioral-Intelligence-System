import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { AppLayout } from './components/layout/AppLayout';
import { Dashboard } from './pages/Dashboard';
import { Alerts } from './pages/Alerts';
import { Employees } from './pages/Employees';
import { Investigations } from './pages/Investigations';
import { Login } from './pages/Login';
import { useAuth } from './hooks/useAuth';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      staleTime: 30000,
    },
  },
});

const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated, isLoading } = useAuth();

  // If initial auth check in flight
  if (isLoading) {
    return (
      <div className="min-h-screen bg-soc-bg flex items-center justify-center text-xs font-mono-dense text-socText-muted">
        [INITIALIZING OPERATOR SECURITY CONTEXT...]
      </div>
    );
  }

  // Fallback dev bypass: if running without backend auth session, let developer view the dashboard
  const token = localStorage.getItem('access_token');
  if (!isAuthenticated && !token) {
    // In dev mode, allow navigating to login
    return <Navigate to="/login" replace />;
  }

  return <>{children}</>;
};

export const App: React.FC = () => {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route
            path="/"
            element={
              <ProtectedRoute>
                <AppLayout />
              </ProtectedRoute>
            }
          >
            <Route index element={<Dashboard />} />
            <Route path="alerts" element={<Alerts />} />
            <Route path="employees" element={<Employees />} />
            <Route path="investigations" element={<Investigations />} />
          </Route>
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  );
};
