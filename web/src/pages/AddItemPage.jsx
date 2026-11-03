import { useState } from 'react'
import { addGear } from '../api/client'

const initialForm = {
  sku: '',
  name: '',
  tags: '',
  category: '',
  itemType: 'Equipment',
  weight: '0',
  price: '0',
  total: '1',
}

export function validateItem(form) {
  const errors = {}
  if (!/^\d{10}$/.test(form.sku)) {
    errors.sku = 'SKU must be exactly 10 digits.'
  }
  if (!form.name.trim()) {
    errors.name = 'Item name is required.'
  }
  if (!Number.isInteger(Number(form.total)) || Number(form.total) < 1) {
    errors.total = 'Total units must be at least 1.'
  }
  return errors
}

export default function AddItemPage() {
  const [form, setForm] = useState(initialForm)
  const [serverError, setServerError] = useState('')
  const [success, setSuccess] = useState('')
  const errors = validateItem(form)
  const isValid = Object.keys(errors).length === 0

  const updateField = (event) => {
    const { name, value } = event.target
    setForm((current) => ({ ...current, [name]: value }))
    setServerError('')
    setSuccess('')
  }

  const handleSubmit = async (event) => {
    event.preventDefault()
    if (!isValid) return

    try {
      await addGear({
        sku: form.sku,
        name: form.name.trim(),
        tags: form.tags.split(',').map((tag) => tag.trim()).filter(Boolean),
        category: form.category,
        item_type: form.itemType,
        weight_g: Number(form.weight),
        total: Number(form.total),
      })
      setSuccess('Item added successfully.')
      setForm(initialForm)
    } catch (error) {
      setServerError(error.message)
    }
  }

  const fieldClasses = 'mt-1 block w-full rounded-md border border-slate-300 px-3 py-2'

  return (
    <div className="max-w-2xl">
      <h1 className="mb-6 text-3xl font-bold text-slate-900">Add item</h1>
      <form onSubmit={handleSubmit} className="grid gap-4">
        {[
          ['sku', 'SKU', 'text'],
          ['name', 'Name', 'text'],
          ['tags', 'Tags (comma separated)', 'text'],
          ['category', 'Category', 'text'],
        ].map(([name, label, type]) => (
          <div key={name}>
            <label htmlFor={name} className="font-medium text-slate-700">{label}</label>
            <input
              id={name}
              name={name}
              type={type}
              value={form[name]}
              onChange={updateField}
              aria-describedby={errors[name] ? `${name}-error` : undefined}
              aria-invalid={Boolean(errors[name])}
              className={fieldClasses}
            />
            {errors[name] && (
              <p id={`${name}-error`} className="mt-1 text-sm text-red-700">{errors[name]}</p>
            )}
          </div>
        ))}

        <div>
          <label htmlFor="itemType" className="font-medium text-slate-700">Item type</label>
          <select
            id="itemType"
            name="itemType"
            value={form.itemType}
            onChange={updateField}
            className={fieldClasses}
          >
            <option>Equipment</option>
            <option>Accessory</option>
            <option>Display</option>
          </select>
        </div>

        {[
          ['weight', 'Weight (g)', 'number'],
          ['price', 'Price', 'number'],
          ['total', 'Total units', 'number'],
        ].map(([name, label, type]) => (
          <div key={name}>
            <label htmlFor={name} className="font-medium text-slate-700">{label}</label>
            <input
              id={name}
              name={name}
              type={type}
              min={name === 'total' ? 1 : 0}
              value={form[name]}
              onChange={updateField}
              aria-describedby={errors[name] ? `${name}-error` : undefined}
              aria-invalid={Boolean(errors[name])}
              className={fieldClasses}
            />
            {errors[name] && (
              <p id={`${name}-error`} className="mt-1 text-sm text-red-700">{errors[name]}</p>
            )}
          </div>
        ))}

        {serverError && <p role="alert" className="text-red-700">{serverError}</p>}
        {success && <p role="status" className="text-green-700">{success}</p>}
        <button
          type="submit"
          disabled={!isValid}
          className="rounded-md bg-blue-700 px-4 py-2 font-medium text-white disabled:cursor-not-allowed disabled:bg-slate-300"
        >
          Submit
        </button>
      </form>
    </div>
  )
}
