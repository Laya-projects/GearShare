import { useState } from 'react'
import { addCustomer } from '../api/client'
import { useCustomer } from '../context/CustomerContext'

export function validateCustomer(form) {
  const errors = {}
  if (!form.name.trim()) errors.name = 'Name is required.'
  if (!form.email.includes('@') || !form.email.includes('.')) {
    errors.email = 'Email must contain @ and a dot.'
  }
  if (!form.membership_type) errors.membership_type = 'Membership is required.'
  return errors
}

const initialForm = {
  name: '',
  email: '',
  membership_type: '',
}

export default function AddCustomerPage() {
  const { refreshCustomers } = useCustomer()
  const [form, setForm] = useState(initialForm)
  const [serverError, setServerError] = useState('')
  const [success, setSuccess] = useState('')
  const errors = validateCustomer(form)
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
      const customer = await addCustomer(form)
      await refreshCustomers()
      setSuccess(`Added ${customer.name} as ${customer.customer_id}.`)
      setForm(initialForm)
    } catch (error) {
      setServerError(error.message)
    }
  }

  return (
    <div className="max-w-2xl">
      <h1 className="mb-6 text-3xl font-bold text-[var(--color-text)]">Add customer</h1>
      <form onSubmit={handleSubmit} className="grid gap-4">
        <div>
          <label htmlFor="customer-name" className="font-medium text-[var(--color-text)]">Name</label>
          <input
            id="customer-name"
            name="name"
            value={form.name}
            onChange={updateField}
            aria-describedby={errors.name ? 'customer-name-error' : undefined}
            aria-invalid={Boolean(errors.name)}
            className="mt-1 block w-full rounded-md px-3 py-2"
          />
          {errors.name && <p id="customer-name-error" role="alert" className="mt-1 text-[var(--color-error)]">{errors.name}</p>}
        </div>
        <div>
          <label htmlFor="customer-email" className="font-medium text-[var(--color-text)]">Email</label>
          <input
            id="customer-email"
            name="email"
            type="email"
            value={form.email}
            onChange={updateField}
            aria-describedby={errors.email ? 'customer-email-error' : undefined}
            aria-invalid={Boolean(errors.email)}
            className="mt-1 block w-full rounded-md px-3 py-2"
          />
          {errors.email && <p id="customer-email-error" role="alert" className="mt-1 text-[var(--color-error)]">{errors.email}</p>}
        </div>
        <div>
          <label htmlFor="customer-membership" className="font-medium text-[var(--color-text)]">Membership</label>
          <select
            id="customer-membership"
            name="membership_type"
            value={form.membership_type}
            onChange={updateField}
            aria-describedby={errors.membership_type ? 'customer-membership-error' : undefined}
            aria-invalid={Boolean(errors.membership_type)}
            className="mt-1 block w-full rounded-md px-3 py-2"
          >
            <option value="">Select membership</option>
            <option value="Basic">Basic (2 items)</option>
            <option value="Plus">Plus (4 items)</option>
            <option value="Pro">Pro (8 items)</option>
          </select>
          {errors.membership_type && <p id="customer-membership-error" role="alert" className="mt-1 text-[var(--color-error)]">{errors.membership_type}</p>}
        </div>
        {serverError && <p role="alert" className="text-[var(--color-error)]">{serverError}</p>}
        {success && <p role="status" className="text-[var(--color-success)]">{success}</p>}
        <button
          type="submit"
          disabled={!isValid}
          className="rounded-md bg-[var(--color-primary)] px-4 py-2 font-medium text-[var(--color-background)]"
        >
          Submit
        </button>
      </form>
    </div>
  )
}
