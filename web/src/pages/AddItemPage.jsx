import { useState } from 'react'
import { addGear, getCategories } from '../api/client'
import { useEffect } from 'react'

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
  const [categories, setCategories] = useState([])
  const [categoryStatus, setCategoryStatus] = useState('loading')
  const [categoryRetry, setCategoryRetry] = useState(0)
  const errors = validateItem(form)
  const isValid = Object.keys(errors).length === 0 && Boolean(form.category)

  useEffect(() => {
    const controller = new AbortController()
    setCategoryStatus('loading')
    getCategories(controller.signal)
      .then((rows) => {
        setCategories(rows)
        setCategoryStatus('success')
      })
      .catch((error) => {
        if (error.name !== 'AbortError') setCategoryStatus('error')
      })
    return () => controller.abort()
  }, [categoryRetry])

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

  const fieldClasses = 'mt-1 block w-full rounded-md px-3 py-2'

  return (
    <div className="max-w-2xl">
      <h1 className="mb-6 text-3xl font-bold text-[var(--color-text)]">Add item</h1>
      <form onSubmit={handleSubmit} className="grid gap-4">
        {[
          ['sku', 'SKU', 'text'],
          ['name', 'Name', 'text'],
          ['tags', 'Tags (comma separated)', 'text'],
        ].map(([name, label, type]) => (
          <div key={name}>
            <label htmlFor={name} className="font-medium text-[var(--color-text)]">{label}</label>
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
              <p id={`${name}-error`} role="alert" className="mt-1 text-sm text-[var(--color-error)]">{errors[name]}</p>
            )}
          </div>
        ))}

        <div>
          <label htmlFor="category" className="font-medium text-[var(--color-text)]">Category</label>
          {categoryStatus === 'loading' && <p role="status">Loading categories...</p>}
          {categoryStatus === 'error' && (
            <div role="alert">
              <p>Couldn't load categories.</p>
              <button type="button" onClick={() => setCategoryRetry((value) => value + 1)}>Retry</button>
            </div>
          )}
          <select
            id="category"
            name="category"
            value={form.category}
            onChange={updateField}
            required
            disabled={categoryStatus !== 'success'}
            className={fieldClasses}
          >
            <option value="" disabled>Select a category</option>
            {categories.map((category) => (
              <option key={category.id} value={category.name}>{category.name}</option>
            ))}
          </select>
        </div>

        <div>
          <label htmlFor="itemType" className="font-medium text-[var(--color-text)]">Item type</label>
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
            <label htmlFor={name} className="font-medium text-[var(--color-text)]">{label}</label>
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
              <p id={`${name}-error`} role="alert" className="mt-1 text-sm text-[var(--color-error)]">{errors[name]}</p>
            )}
          </div>
        ))}

        {serverError && <p role="alert" className="text-[var(--color-error)]">{serverError}</p>}
        {success && <p role="status" className="text-[var(--color-success)]">{success}</p>}
        <button
          type="submit"
          disabled={!isValid}
          className="rounded-md bg-[var(--color-primary)] px-4 py-2 font-medium text-[var(--color-background)] disabled:cursor-not-allowed"
        >
          Submit
        </button>
      </form>
    </div>
  )
}
