import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../auth/AuthContext'

export default function Login() {
	const [email, setEmail] = useState('')
	const [password, setPassword] = useState('')
	const [error, setError] = useState<string | null>(null)
	const [loading, setLoading] = useState(false)
	const { setToken } = useAuth()
	const navigate = useNavigate()

	async function onSubmit(e: React.FormEvent) {
		e.preventDefault()
		setError(null)
		setLoading(true)
		const resp = await fetch('/api/auth/login', {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ email, password })
		})
		try {
			if (!resp.ok) {
				const msg = (await resp.json().catch(() => null))?.detail || 'Login failed'
				setError(typeof msg === 'string' ? msg : 'Login failed')
				return
			}
			const data = await resp.json()
			setToken(data.access_token)
			navigate('/')
		} finally {
			setLoading(false)
		}
	}

	return (
		<form onSubmit={onSubmit} className="card">
			<h2>Login</h2>
			<label>
				<span>Email</span>
				<input placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} required />
			</label>
			<label>
				<span>Password</span>
				<input placeholder="Password" type="password" value={password} onChange={e => setPassword(e.target.value)} required />
			</label>
			{error && <div className="error">{error}</div>}
			<button type="submit" disabled={loading}>{loading ? 'Logging in...' : 'Login'}</button>
		</form>
	)
}
