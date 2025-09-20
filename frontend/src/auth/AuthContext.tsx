import React, { createContext, useContext, useEffect, useState } from 'react'

interface UserPublic {
	id: string
	email: string
	full_name?: string
	is_admin?: boolean
}

interface AuthContextType {
	token: string | null
	setToken: (t: string | null) => void
	user: UserPublic | null
	logout: () => void
}

const AuthContext = createContext<AuthContextType>({ token: null, setToken: () => {}, user: null, logout: () => {} })

export function AuthProvider({ children }: { children: React.ReactNode }) {
	const [token, setToken] = useState<string | null>(() => localStorage.getItem('token'))
	const [user, setUser] = useState<UserPublic | null>(null)

	useEffect(() => {
		let cancelled = false
		async function fetchMe() {
			if (!token) return setUser(null)
			localStorage.setItem('token', token)
			try {
				const r = await fetch('/api/auth/me', { headers: { Authorization: `Bearer ${token}` } })
				if (!cancelled && r.ok) setUser(await r.json())
				else if (!cancelled) setUser(null)
			} catch {
				if (!cancelled) setUser(null)
			}
		}
		fetchMe()
		return () => { cancelled = true }
	}, [token])

	function logout() {
		setToken(null)
		localStorage.removeItem('token')
		setUser(null)
	}

	return (
		<AuthContext.Provider value={{ token, setToken, user, logout }}>
			{children}
		</AuthContext.Provider>
	)
}

export function useAuth() {
	return useContext(AuthContext)
}
