import { createContext, useContext, useState, useEffect } from 'react';
import api from '../services/api';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // Check if user is logged in on mount
        const token = localStorage.getItem('token');
        if (token) {
            // TODO: Implement user verification with backend
            setUser({ token });
        }
        setLoading(false);
    }, []);

    const login = async (username, password) => {
        try {
            console.log('=== Login Flow Start ===');
            console.log('Creating FormData...');
            const formData = new URLSearchParams();
            formData.append('username', username);
            formData.append('password', password);
            formData.append('grant_type', 'password');
            console.log('FormData contents:');
            for (let pair of formData.entries()) {
                console.log(pair[0] + ': ' + pair[1]);
            }
            console.log('Sending request to:', '/login');
            const response = await api.post('/login', formData, {
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
            });
            console.log('Response received:', {
                status: response.status,
                statusText: response.statusText,
                headers: response.headers,
                data: response.data
            });
            // Check if we have the expected data structure
            if (!response.data || !response.data.access_token) {
                console.error('Invalid login response:', response.data);
                throw new Error('Invalid login response format');
            }
            const { access_token } = response.data;
            console.log('Access token received, length:', access_token.length);
            localStorage.setItem('token', access_token);
            setUser({ token: access_token });
            console.log('=== Login Flow Complete ===');
            return true;
        } catch (error) {
            console.error('=== Login Flow Error ===');
            console.error('Error type:', error.constructor.name);
            console.error('Error message:', error.message);
            if (error.response) {
                console.error('Response status:', error.response.status);
                console.error('Response headers:', error.response.headers);
                console.error('Response data:', error.response.data);
            }
            if (error.request) {
                console.error('Request config:', {
                    method: error.request.method,
                    url: error.request.url,
                    headers: error.request.headers,
                });
            }
            console.error('=== End Error Details ===');
            throw error;
        }
    };


    const register = async (username, password) => {
        try {
            console.log('Starting registration request with:', { username }); // Don't log password
            const response = await api.post('/register', {
                username,
                password
            });
            console.log('Registration successful');
            // After registration, log the user in
            try {
                const loginSuccess = await login(username, password);
                return loginSuccess;
            } catch (loginError) {
                console.error('Post-registration login failed:', loginError);
                throw loginError;
            }
        } catch (error) {
            console.error('Registration/Login error:', {
                message: error.message,
                response: error.response?.data,
                status: error.response?.status
            });
            throw error;
        }
    };

    const logout = () => {
        localStorage.removeItem('token');
        setUser(null);
    };

    const value = {
        user,
        loading,
        login,
        register,
        logout
    };

    return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
};