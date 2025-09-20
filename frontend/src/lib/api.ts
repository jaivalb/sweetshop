export async function apiFetch<T = any>(path: string, options: RequestInit = {}, token?: string | null): Promise<Response> {
	const headers = new Headers(options.headers || {})
	if (token) headers.set('Authorization', `Bearer ${token}`)
	if (!headers.has('Content-Type') && options.body) headers.set('Content-Type', 'application/json')
	return fetch(path, { ...options, headers })
}
