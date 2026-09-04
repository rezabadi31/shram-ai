/**
 * ShramAI Centralized API Configuration.
 * 
 * In production (Vercel): Uses import.meta.env.VITE_API_BASE_URL (e.g. https://YOUR-RENDER-BACKEND.onrender.com)
 * In local development: Falls back to relative proxy '/api/v1' or configured VITE_API_BASE_URL
 */

// Strip trailing slashes from configured base URL
const envBaseUrl = (import.meta.env.VITE_API_BASE_URL || '').trim().replace(/\/+$/, '');

// Base URL for the backend server root
export const BACKEND_ROOT_URL = envBaseUrl;

// Full URL prefix for API v1 routes
export const API_BASE = envBaseUrl ? `${envBaseUrl}/api/v1` : '/api/v1';

/**
 * Builds an absolute or proxy-relative API URL.
 * Example: getApiUrl('/auth/login') -> 'https://backend.onrender.com/api/v1/auth/login'
 */
export function getApiUrl(endpoint: string): string {
  const cleanEndpoint = endpoint.startsWith('/') ? endpoint : `/${endpoint}`;
  if (cleanEndpoint.startsWith('/api/v1')) {
    return envBaseUrl ? `${envBaseUrl}${cleanEndpoint}` : cleanEndpoint;
  }
  return `${API_BASE}${cleanEndpoint}`;
}
