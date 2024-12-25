import axios from 'axios';

// Create axios instance with custom config
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});


// Add request logging
api.interceptors.request.use(
  (config) => {
    console.log('=== API Request Interceptor ===');
    console.log('Request URL:', config.url);
    console.log('Request Method:', config.method);
    console.log('Request Headers:', config.headers);
    console.log('Request Data Type:', typeof config.data);
    if (config.data instanceof FormData) {
      console.log('FormData contents:');
      for (let pair of config.data.entries()) {
        console.log(pair[0] + ': ' + pair[1]);
      }
    } else {
      console.log('Request Data:', config.data);
    }

    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
      console.log('Added Authorization header');
    }
    return config;
  },
  (error) => {
    console.error('❌ Request Error:', error);
    return Promise.reject(error);
  }
);
// Add response logging
api.interceptors.response.use(
  (response) => {
    console.log('=== API Response Interceptor ===');
    console.log('Response Status:', response.status);
    console.log('Response Headers:', response.headers);
    console.log('Response Data:', response.data);
    return response;
  },
  (error) => {
    console.error('=== API Response Error ===');
    if (error.response) {
      console.error('Error Status:', error.response.status);
      console.error('Error Headers:', error.response.headers);
      console.error('Error Data:', error.response.data);
    } else if (error.request) {
      console.error('No response received:', error.request);
    } else {
      console.error('Error setting up request:', error.message);
    }
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Add a request interceptor to add  token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add a response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized access
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;