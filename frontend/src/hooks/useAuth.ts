import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useState, useEffect } from 'react';
import { authApi, LoginPayload } from '../api/auth';
import { User } from '../types';

export function useAuth() {
  const queryClient = useQueryClient();
  const [token, setToken] = useState<string | null>(() => localStorage.getItem('access_token'));

  useEffect(() => {
    const handleStorageChange = () => {
      setToken(localStorage.getItem('access_token'));
    };
    window.addEventListener('storage', handleStorageChange);
    return () => window.removeEventListener('storage', handleStorageChange);
  }, []);

  const {
    data: user,
    isLoading,
    isError,
    refetch,
  } = useQuery<User>({
    queryKey: ['auth', 'user'],
    queryFn: authApi.getProfile,
    enabled: !!token,
    retry: 1,
    staleTime: 5 * 60 * 1000,
  });

  const loginMutation = useMutation({
    mutationFn: async (payload: LoginPayload) => {
      const tokens = await authApi.login(payload);
      localStorage.setItem('access_token', tokens.access_token);
      localStorage.setItem('refresh_token', tokens.refresh_token);
      setToken(tokens.access_token);
      return tokens;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['auth', 'user'] });
    },
  });

  const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    setToken(null);
    queryClient.setQueryData(['auth', 'user'], null);
  };

  return {
    user,
    isAuthenticated: !!user && !!token,
    isLoading: !!token && isLoading,
    isError,
    login: loginMutation.mutateAsync,
    isLoggingIn: loginMutation.isPending,
    loginError: loginMutation.error,
    logout,
    refetchUser: refetch,
  };
}
