//  /src/App.jsx
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import ProtectedRoute from './components/layout/ProtectedRoute';

// We'll create these components next
import Login from './components/auth/Login';
import Register from './components/auth/Register';
import TaskList from './components/tasks/TaskList';

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          {/* Public routes */}
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          
          {/* Protected routes */}
          <Route
            path="/tasks"
            element={
              <ProtectedRoute>
                <TaskList />
              </ProtectedRoute>
            }
          />
          
          {/* Redirect root to tasks if authenticated, otherwise to login */}
          <Route path="/" element={<Navigate to="/tasks" replace />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App; 