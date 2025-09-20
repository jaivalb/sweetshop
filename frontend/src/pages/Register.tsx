import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../auth/AuthContext'

export default function Register() {
	const [email, setEmail] = useState('')
	const [password, setPassword] = useState('')
	const [fullName, setFullName] = useState('')
	const [error, setError] = useState<string | null>(null)
	const [loading, setLoading] = useState(false)
	const { setToken } = useAuth()
	const navigate = useNavigate()

	async function onSubmit(e: React.FormEvent) {
		e.preventDefault()
		setError(null)
		setLoading(true)
		const resp = await fetch('/api/auth/register', {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ email, password, full_name: fullName, is_admin: false })
		})
		try {
			if (!resp.ok) {
				const msg = (await resp.json().catch(() => null))?.detail || 'Registration failed'
				setError(typeof msg === 'string' ? msg : 'Registration failed')
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
			<h2>Register</h2>
			<label>
				<span>Full name</span>
				<input placeholder="Full name" value={fullName} onChange={e => setFullName(e.target.value)} />
			</label>
			<label>
				<span>Email</span>
				<input placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} required />
			</label>
			<label>
				<span>Password</span>
				<input placeholder="Password" type="password" value={password} onChange={e => setPassword(e.target.value)} required />
			</label>
			{error && <div className="error">{error}</div>}
			<button type="submit" disabled={loading}>{loading ? 'Creating...' : 'Create account'}</button>
		</form>
	)
}
