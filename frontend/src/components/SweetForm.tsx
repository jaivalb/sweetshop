import { useState } from 'react'

export interface SweetFormValues {
	name: string
	category: string
	price: number
	quantity: number
}

export default function SweetForm({ initial, onSubmit, submitLabel = 'Save' }: { initial?: Partial<SweetFormValues>, onSubmit: (v: SweetFormValues) => void, submitLabel?: string }) {
	const [name, setName] = useState(initial?.name ?? '')
	const [category, setCategory] = useState(initial?.category ?? '')
	const [price, setPrice] = useState(initial?.price ?? 0)
	const [quantity, setQuantity] = useState(initial?.quantity ?? 0)

	return (
		<form onSubmit={e => { e.preventDefault(); onSubmit({ name, category, price: Number(price), quantity: Number(quantity) }) }} className="form-grid">
			<label>
				<span>Name</span>
				<input placeholder="Name" value={name} onChange={e => setName(e.target.value)} required />
			</label>
			<label>
				<span>Category</span>
				<input placeholder="Category" value={category} onChange={e => setCategory(e.target.value)} required />
			</label>
			<label>
				<span>Price</span>
				<input placeholder="Price" type="number" step="0.01" value={price} onChange={e => setPrice(parseFloat(e.target.value))} required />
			</label>
			<label>
				<span>Quantity</span>
				<input placeholder="Quantity" type="number" value={quantity} onChange={e => setQuantity(parseInt(e.target.value))} required />
			</label>
			<button type="submit">{submitLabel}</button>
		</form>
	)
}
