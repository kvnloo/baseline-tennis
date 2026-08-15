// @vitest-environment jsdom

import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import { TennisBallSymbol } from './TennisBallSymbol'

describe('TennisBallSymbol', () => {
  it('serves responsive textured derivatives without exposing the 8K master', () => {
    render(<TennisBallSymbol label="Baseline tennis ball" size="hero" motion="bounce" />)
    const symbol = screen.getByRole('img', { name: 'Baseline tennis ball' })
    const image = symbol.querySelector('img')

    expect(symbol.className).toContain('tennis-ball--bounce')
    expect(image?.getAttribute('src')).toContain('tennis-ball-glow-256.webp')
    expect(image?.getAttribute('srcset')).toContain('tennis-ball-glow-1024.webp 1024w')
    expect(image?.getAttribute('src')).not.toContain('8192')
  })

  it('is decorative by default', () => {
    const { container } = render(<TennisBallSymbol motion="none" />)
    expect(container.querySelector('.tennis-ball')?.getAttribute('aria-hidden')).toBe('true')
  })
})
