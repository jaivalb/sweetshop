import { useEffect, useMemo, useState } from 'react'
import { useAuth } from '../auth/AuthContext'
import SweetForm, { SweetFormValues } from '../components/SweetForm'
import { apiFetch } from '../lib/api'

interface Sweet { id: string; name: string; category: string; price: number; quantity: number }

export default function Dashboard() {
	const { token, user } = useAuth()
	const [items, setItems] = useState<Sweet[]>([])
	const [q, setQ] = useState('')
	const [category, setCategory] = useState('')
	const [minPrice, setMinPrice] = useState('')
	const [maxPrice, setMaxPrice] = useState('')
	const [showAdd, setShowAdd] = useState(false)
	const [editId, setEditId] = useState<string | null>(null)
	const [restockQty, setRestockQty] = useState<Record<string, number>>({})
	const isAdmin = !!user?.is_admin

	async function load() {
		const params = new URLSearchParams()
		if (q) params.set('q', q)
		if (category) params.set('category', category)
		if (minPrice) params.set('min_price', minPrice)
		if (maxPrice) params.set('max_price', maxPrice)
		const url = params.toString() ? `/api/sweets/search?${params.toString()}` : '/api/sweets'
		const resp = await apiFetch(url, {}, token)
		if (resp.ok) setItems(await resp.json())
	}

	useEffect(() => { load() }, [token])

	async function purchase(id: string, quantity: number) {
		const resp = await apiFetch(`/api/sweets/${id}/purchase?quantity=${quantity}`, { method: 'POST' }, token)
		if (resp.ok) load()
	}

	async function restock(id: string, quantity: number) {
		const resp = await apiFetch(`/api/sweets/${id}/restock?quantity=${quantity}`, { method: 'POST' }, token)
		if (resp.ok) load()
	}

	async function addSweet(values: SweetFormValues) {
		const resp = await apiFetch(`/api/sweets/`, { method: 'POST', body: JSON.stringify(values) }, token)
		if (resp.ok) { setShowAdd(false); load() }
	}

	async function updateSweet(id: string, price: number) {
		const resp = await apiFetch(`/api/sweets/${id}`, { method: 'PUT', body: JSON.stringify({ price }) }, token)
		if (resp.ok) { setEditId(null); load() }
	}

	async function deleteSweet(id: string) {
		const ok = window.confirm('Delete sweet?')
		if (!ok) return
		const resp = await apiFetch(`/api/sweets/${id}`, { method: 'DELETE' }, token)
		if (resp.ok) load()
	}

	return (
		<div className="grid gap-16">
			<h2>Sweet Shop</h2>
			<div className="toolbar">
				<input placeholder="Search" value={q} onChange={e => setQ(e.target.value)} />
				<input placeholder="Category" value={category} onChange={e => setCategory(e.target.value)} />
				<input placeholder="Min price" value={minPrice} onChange={e => setMinPrice(e.target.value)} />
				<input placeholder="Max price" value={maxPrice} onChange={e => setMaxPrice(e.target.value)} />
				<button onClick={load}>Filter</button>
				{isAdmin && <button onClick={() => setShowAdd(s => !s)}>{showAdd ? 'Cancel' : 'Add Sweet'}</button>}
			</div>
			{isAdmin && showAdd && (
				<div className="card">
					<h3>Add Sweet</h3>
					<SweetForm onSubmit={addSweet} submitLabel="Create" />
				</div>
			)}
			<ul className="list">
				{items.map(it => (
					<li key={it.id} className="list-item">
						<div className="row">
							<div>
								<div style={{ fontWeight: 600 }}>{it.name}</div>
								<div>{it.category}</div>
								<div>${it.price.toFixed(2)} — Qty: {it.quantity}</div>
							</div>
							<div className="actions">
								<button disabled={it.quantity <= 0} onClick={() => purchase(it.id, 1)}>Purchase</button>
								{isAdmin && (
									<>
										<input className="small" type="number" min={1} value={restockQty[it.id] ?? 5} onChange={e => setRestockQty(s => ({ ...s, [it.id]: parseInt(e.target.value) }))} />
										<button onClick={() => restock(it.id, restockQty[it.id] ?? 5)}>Restock</button>
										{editId === it.id ? (
											<>
												<input className="small" type="number" step={0.01} defaultValue={it.price} onKeyDown={e => { if (e.key === 'Enter') updateSweet(it.id, parseFloat((e.target as HTMLInputElement).value)) }} />
												<button onClick={() => updateSweet(it.id, parseFloat((document.activeElement as HTMLInputElement)?.value || String(it.price)))}>Save</button>
												<button onClick={() => setEditId(null)}>Cancel</button>
											</>
										) : (
											<button onClick={() => setEditId(it.id)}>Edit Price</button>
										)}
										<button onClick={() => deleteSweet(it.id)}>Delete</button>
									</>
								)}
							</div>
						</div>
					</li>
				))}
			</ul>
		</div>
	)
}
