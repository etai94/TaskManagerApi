import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

// Reusing validation functions from Login component for consistency
const validateUsername = (username) => {
  if (!username) return 'Username is required';
  if (username.length < 3) return 'Username must be at least 3 characters long';
  if (!/^[a-zA-Z0-9_-]+$/.test(username)) {
    return 'Username must contain only letters, numbers, underscores, and hyphens';
  }
  return '';
};

const validatePassword = (password) => {
  if (!password) return 'Password is required';
  if (password.length < 8) return 'Password must be at least 8 characters long';
  if (!/[A-Z]/.test(password)) return 'Password must contain at least one uppercase letter';
  if (!/[a-z]/.test(password)) return 'Password must contain at least one lowercase letter';
  if (!/[0-9]/.test(password)) return 'Password must contain at least one number';
  return '';
};

const Register = () => {
  const navigate = useNavigate();
  const { register } = useAuth();

  // Form state
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    confirmPassword: ''
  });

  // Validation errors state
  const [errors, setErrors] = useState({
    username: '',
    password: '',
    confirmPassword: '',
    form: ''
  });

  // Loading state
  const [isLoading, setIsLoading] = useState(false);

  // Handle input changes
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));

    // Clear field-specific error when user starts typing
    setErrors(prev => ({
      ...prev,
      [name]: '',
      form: ''
    }));

    // Real-time validation
    if (name === 'username') {
      setErrors(prev => ({
        ...prev,
        username: validateUsername(value)
      }));
    }
    if (name === 'password') {
      const passwordError = validatePassword(value);
      setErrors(prev => ({
        ...prev,
        password: passwordError,
        confirmPassword: value !== formData.confirmPassword ? 'Passwords do not match' : ''
      }));
    }
    if (name === 'confirmPassword') {
      setErrors(prev => ({
        ...prev,
        confirmPassword: value !== formData.password ? 'Passwords do not match' : ''
      }));
    }
  };

  // Form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log("inside handleSubmit...");
    // Validate all fields before submission
    const usernameError = validateUsername(formData.username);
    const passwordError = validatePassword(formData.password);
    const confirmPasswordError = formData.password !== formData.confirmPassword ?
      'Passwords do not match' : '';

    if (usernameError || passwordError || confirmPasswordError) {
      setErrors({
        username: usernameError,
        password: passwordError,
        confirmPassword: confirmPasswordError,
        form: ''
      });
      return;
    }

    setIsLoading(true);
    setErrors(prev => ({ ...prev, form: '' }));

    try {
      // const result = await register(formData.username, formData.password);
      await register(formData.username, formData.password);
      console.log("Registration and login successful");
      // if (result) {
      console.log("inside  if (result) {...");
      navigate('/tasks', { replace: true });
      // }
    } catch (error) {
      console.log("inside Registration error");
      console.error('Registration error:', error);
      let errorMessage = 'Registration failed. Please try again.';

      if (error.response) {
        const { status, data } = error.response;

        switch (status) {
          case 400:
            errorMessage = data.detail || 'Username already exists';
            break;
          case 422:
            if (Array.isArray(data.detail)) {
              errorMessage = data.detail.map(err => err.msg).join(', ');
            } else if (data.detail) {
              errorMessage = data.detail;
            }
            break;
          case 500:
            errorMessage = "Server error. Please try again later.";
            break;
          default:
            errorMessage = "An unexpected error occurred. Please try again.";
        }
      }

      setErrors(prev => ({
        ...prev,
        form: errorMessage
      }));
    } finally {
      setIsLoading(false);
    }
  };

  // Determine if form is valid
  const isValid = !errors.username && !errors.password && !errors.confirmPassword &&
    formData.username && formData.password && formData.confirmPassword;

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Create your account
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600">
            Already have an account?{' '}
            <Link to="/login" className="font-medium text-indigo-600 hover:text-indigo-500">
              Sign in
            </Link>
          </p>
        </div>

        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          {/* Show form-level errors */}
          {errors.form && (
            <div className="rounded-md bg-red-50 p-4">
              <div className="text-sm text-red-700">{errors.form}</div>
            </div>
          )}

          <div className="rounded-md shadow-sm -space-y-px">
            {/* Username field */}
            <div>
              <label htmlFor="username" className="sr-only">Username</label>
              <input
                id="username"
                name="username"
                type="text"
                required
                className={`appearance-none rounded-none relative block w-full px-3 py-2 border 
                  ${errors.username ? 'border-red-300' : 'border-gray-300'}
                  placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none 
                  focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm`}
                placeholder="Username"
                value={formData.username}
                onChange={handleChange}
              />
              {errors.username && (
                <p className="mt-2 text-sm text-red-600">{errors.username}</p>
              )}
            </div>

            {/* Password field */}
            <div>
              <label htmlFor="password" className="sr-only">Password</label>
              <input
                id="password"
                name="password"
                type="password"
                required
                className={`appearance-none rounded-none relative block w-full px-3 py-2 border 
                  ${errors.password ? 'border-red-300' : 'border-gray-300'}
                  placeholder-gray-500 text-gray-900 focus:outline-none 
                  focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm`}
                placeholder="Password"
                value={formData.password}
                onChange={handleChange}
              />
              {errors.password && (
                <p className="mt-2 text-sm text-red-600">{errors.password}</p>
              )}
            </div>

            {/* Confirm Password field */}
            <div>
              <label htmlFor="confirmPassword" className="sr-only">Confirm Password</label>
              <input
                id="confirmPassword"
                name="confirmPassword"
                type="password"
                required
                className={`appearance-none rounded-none relative block w-full px-3 py-2 border 
                  ${errors.confirmPassword ? 'border-red-300' : 'border-gray-300'}
                  placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none 
                  focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm`}
                placeholder="Confirm Password"
                value={formData.confirmPassword}
                onChange={handleChange}
              />
              {errors.confirmPassword && (
                <p className="mt-2 text-sm text-red-600">{errors.confirmPassword}</p>
              )}
            </div>
          </div>

          <div>
            <button
              type="submit"
              disabled={!isValid || isLoading}
              className={`group relative w-full flex justify-center py-2 px-4 border border-transparent 
                text-sm font-medium rounded-md text-white 
                ${isValid && !isLoading
                  ? 'bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500'
                  : 'bg-indigo-400 cursor-not-allowed'}
              `}
            >
              {isLoading ? (
                <span className="absolute left-0 inset-y-0 flex items-center pl-3">
                  {/* Loading spinner */}
                  <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                </span>
              ) : null}
              {isLoading ? 'Creating account...' : 'Create account'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Register;