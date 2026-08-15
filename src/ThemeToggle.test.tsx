// @vitest-environment jsdom

import { cleanup, fireEvent, render, screen } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { ThemeToggle } from './ThemeToggle'

const matchMedia = (dark: boolean) => vi.fn().mockImplementation(() => ({
  matches: dark,
  media: '(prefers-color-scheme: dark)',
  onchange: null,
  addEventListener: vi.fn(),
  removeEventListener: vi.fn(),
  addListener: vi.fn(),
  removeListener: vi.fn(),
  dispatchEvent: vi.fn(),
}))

function memoryStorage(): Storage {
  const values = new Map<string, string>()
  return {
    get length() { return values.size },
    clear: () => values.clear(),
    getItem: (key) => values.get(key) ?? null,
    key: (index) => [...values.keys()][index] ?? null,
    removeItem: (key) => { values.delete(key) },
    setItem: (key, value) => { values.set(key, value) },
  }
}

describe('ThemeToggle', () => {
  beforeEach(() => {
    vi.stubGlobal('localStorage', memoryStorage())
    document.documentElement.removeAttribute('data-theme')
    Object.defineProperty(window, 'matchMedia', { writable: true, value: matchMedia(true) })
  })

  afterEach(() => {
    cleanup()
    vi.unstubAllGlobals()
    vi.restoreAllMocks()
  })

  it('uses system preference until the visitor selects a theme', () => {
    render(<ThemeToggle />)
    expect(document.documentElement.dataset.theme).toBe('dark')
    expect(screen.getByRole('button', { name: 'Switch to light mode' })).toBeTruthy()
  })

  it('persists a manual theme selection', () => {
    render(<ThemeToggle />)
    fireEvent.click(screen.getByRole('button', { name: 'Switch to light mode' }))
    expect(document.documentElement.dataset.theme).toBe('light')
    expect(localStorage.getItem('baseline-theme')).toBe('light')
    expect(screen.getByRole('button', { name: 'Switch to dark mode' })).toBeTruthy()
  })
})
