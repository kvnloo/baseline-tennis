import { describe, expect, it } from 'vitest'
import { describePoint, normalizeCourtPoint } from './live'

describe('live match event presentation', () => {
  it('grounds commentary in the event result and score', () => {
    expect(describePoint({
      id: 'p1', set: 2, game: 7, point: 4, server: 'home', winner: 'away',
      result: 'return_winner', score: '30–40', rallyLength: 6,
    })).toBe('Return winner after six shots. Break point at 30–40.')
  })

  it('does not invent court coordinates when a feed omits them', () => {
    expect(normalizeCourtPoint({ x: null, y: null })).toBeNull()
    expect(normalizeCourtPoint({ x: 3.2, y: -9.4 })).toEqual({ x: 66, y: 90 })
  })
})
