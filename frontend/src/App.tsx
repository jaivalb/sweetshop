import { Routes, Route, Link, Navigate, useNavigate } from 'react-router-dom'
import { AuthProvider, useAuth } from './auth/AuthContext'
import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'

function PrivateRoute({ children }: { children: JSX.Element }) {
	const { token } = useAuth()
	return token ? children : <Navigate to="/login" replace />
}

function Header() {
	const { user, logout, token } = useAuth()
	const navigate = useNavigate()
	return (
		<header style={{ display: 'flex', gap: 16, marginBottom: 24, alignItems: 'center' }}>
			<Link to="/">Dashboard</Link>
			<div style={{ marginLeft: 'auto', display: 'flex', gap: 12, alignItems: 'center' }}>
				{token ? (
					<>
						<span>{user?.email}{user?.is_admin ? ' (admin)' : ''}</span>
						<button onClick={() => { logout(); navigate('/login') }}>Logout</button>
					</>
				) : (
					<>
						<Link to="/login">Login</Link>
						<Link to="/register">Register</Link>
					</>
				)}
			</div>
		</header>
	)
}

export default function App() {
	return (
		<AuthProvider>
            <div className="container">
				<Header />
				<Routes>
					<Route path="/" element={<PrivateRoute><Dashboard /></PrivateRoute>} />
					<Route path="/login" element={<Login />} />
					<Route path="/register" element={<Register />} />
				</Routes>
			</div>
		</AuthProvider>
	)
}
