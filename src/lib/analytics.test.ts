import { describe, expect, it } from 'vitest'
import { answerQuestion, summarizeTour } from './analytics'
import type { MatchRecord } from './types'

const matches: MatchRecord[] = [
  { id: '1', tour: 'ATP', tournament: 'Australian Open', city: 'Melbourne', country: 'Australia', lat: -37.82, lng: 144.98, surface: 'Hard', level: 'Grand Slam', date: '2024-01-14', winner: 'Jannik Sinner', loser: 'Daniil Medvedev', winnerRank: 4, loserRank: 3, winnerAces: 14, loserAces: 11, winnerDoubleFaults: 5, loserDoubleFaults: 3, minutes: 226 },
  { id: '2', tour: 'WTA', tournament: 'Australian Open', city: 'Melbourne', country: 'Australia', lat: -37.82, lng: 144.98, surface: 'Hard', level: 'Grand Slam', date: '2024-01-27', winner: 'Aryna Sabalenka', loser: 'Qinwen Zheng', winnerRank: 2, loserRank: 15, winnerAces: 3, loserAces: 6, winnerDoubleFaults: 0, loserDoubleFaults: 6, minutes: 76 },
  { id: '3', tour: 'ATP', tournament: 'Roland Garros', city: 'Paris', country: 'France', lat: 48.85, lng: 2.25, surface: 'Clay', level: 'Grand Slam', date: '2024-06-09', winner: 'Carlos Alcaraz', loser: 'Alexander Zverev', winnerRank: 3, loserRank: 4, winnerAces: 9, loserAces: 8, winnerDoubleFaults: 6, loserDoubleFaults: 6, minutes: 259 },
]

describe('summarizeTour', () => {
  it('aggregates matches by surface and tour', () => {
    const summary = summarizeTour(matches)
    expect(summary.totalMatches).toBe(3)
    expect(summary.surface).toEqual({ Hard: 2, Clay: 1 })
    expect(summary.tours).toEqual({ ATP: 2, WTA: 1 })
  })
})

describe('answerQuestion', () => {
  it('answers a constrained statistical question with evidence', () => {
    const answer = answerQuestion('Who hit the most aces at the Australian Open?', matches)
    expect(answer.headline).toContain('Jannik Sinner')
    expect(answer.value).toBe('14 aces')
    expect(answer.matchCount).toBe(2)
    expect(answer.method).toContain('Australian Open')
  })

  it('returns a useful limitation for unsupported questions', () => {
    const answer = answerQuestion('What color shoes did every player wear?', matches)
    expect(answer.limitation).toContain('not available')
  })
})
