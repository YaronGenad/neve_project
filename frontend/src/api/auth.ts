import apiClient from './client';
import { Token, User } from '../types';

export const login = async (email: string, password: string): Promise<Token> => {
  // OAuth2 requires application/x-www-form-urlencoded with `username` field
  const params = new URLSearchParams();
  params.append('username', email);
  params.append('password', password);

  const response = await apiClient.post<Token>('/auth/login', params, {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
  });
  return response.data;
};

export const register = async (
  email: string,
  password: string,
  fullName?: string
): Promise<User> => {
  const response = await apiClient.post<User>('/auth/register', {
    email,
    password,
    ...(fullName ? { full_name: fullName } : {}),
  });
  return response.data;
};

export const refreshToken = async (token: string): Promise<Token> => {
  const response = await apiClient.post<Token>('/auth/refresh', {
    refresh_token: token,
  });
  return response.data;
};

export const getMe = async (): Promise<User> => {
  const response = await apiClient.get<User>('/auth/me');
  return response.data;
};
