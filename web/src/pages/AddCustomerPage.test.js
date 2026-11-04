import { describe, expect, it } from 'vitest'
import { validateCustomer } from './AddCustomerPage.jsx'

describe('validateCustomer', () => {
  it('accepts a complete customer', () => {
    expect(validateCustomer({
      name: 'New Customer',
      email: 'new.customer@example.com',
      membership_type: 'Basic',
    })).toEqual({})
  })

  it('requires a name', () => {
    expect(validateCustomer({
      name: '',
      email: 'new@example.com',
      membership_type: 'Plus',
    }).name).toBe('Name is required.')
  })

  it('requires an email with an @ and a dot', () => {
    expect(validateCustomer({
      name: 'New Customer',
      email: 'new@example',
      membership_type: 'Pro',
    }).email).toBe('Email must contain @ and a dot.')
  })

  it('requires a membership', () => {
    expect(validateCustomer({
      name: 'New Customer',
      email: 'new@example.com',
      membership_type: '',
    }).membership_type).toBe('Membership is required.')
  })
})
