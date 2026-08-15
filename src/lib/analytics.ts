import type { MatchRecord, StatisticalAnswer } from './types'

export function summarizeTour(matches: MatchRecord[]) {
  const surface: Record<string, number> = {}
  const tours: Record<string, number> = {}
  for (const match of matches) {
    surface[match.surface] = (surface[match.surface] ?? 0) + 1
    tours[match.tour] = (tours[match.tour] ?? 0) + 1
  }
  return { totalMatches: matches.length, surface, tours }
}

function scopedMatches(question: string, matches: MatchRecord[]) {
  const q = question.toLowerCase()
  return matches.filter((m) => {
    const tournamentWords = m.tournament.toLowerCase()
    if (q.includes('australian open') && !tournamentWords.includes('australian open')) return false
    if ((q.includes('roland garros') || q.includes('french open')) && !tournamentWords.includes('roland garros')) return false
    if (q.includes('wimbledon') && !tournamentWords.includes('wimbledon')) return false
    if ((q.includes('us open') || q.includes('u.s. open')) && !tournamentWords.includes('us open')) return false
    if (q.includes('clay') && m.surface !== 'Clay') return false
    if (q.includes('grass') && m.surface !== 'Grass') return false
    if (q.includes('hard court') && m.surface !== 'Hard') return false
    if (q.includes('wta') && m.tour !== 'WTA') return false
    if (q.includes('atp') && m.tour !== 'ATP') return false
    return true
  })
}

export function answerQuestion(question: string, matches: MatchRecord[]): StatisticalAnswer {
  const q = question.trim().toLowerCase()
  const scoped = scopedMatches(q, matches)
  const scopeLabel = scoped.length === matches.length ? 'the selected dataset' : [...new Set(scoped.map((m) => m.tournament))].join(', ')

  if (q.includes('ace')) {
    const totals = new Map<string, number>()
    for (const m of scoped) {
      totals.set(m.winner, (totals.get(m.winner) ?? 0) + m.winnerAces)
      totals.set(m.loser, (totals.get(m.loser) ?? 0) + m.loserAces)
    }
    const leader = [...totals].sort((a, b) => b[1] - a[1])[0]
    if (leader) return {
      headline: `${leader[0]} leads the ace count`,
      value: `${leader[1]} aces`,
      detail: `Computed across ${scoped.length.toLocaleString()} matches in ${scopeLabel}.`,
      method: `Sum of recorded winner and loser ace fields for ${scopeLabel}.`,
      matchCount: scoped.length,
    }
  }

  if (q.includes('longest') || q.includes('duration') || q.includes('minutes')) {
    const longest = scoped.filter((m) => m.minutes !== null).sort((a, b) => (b.minutes ?? 0) - (a.minutes ?? 0))[0]
    if (longest) return {
      headline: `${longest.winner} vs ${longest.loser}`,
      value: `${longest.minutes} minutes`,
      detail: `${longest.tournament} on ${longest.surface.toLowerCase()} in ${longest.city}.`,
      method: `Maximum recorded match duration for ${scopeLabel}.`,
      matchCount: scoped.length,
    }
  }

  if (q.includes('match') || q.includes('how many')) return {
    headline: `${scoped.length.toLocaleString()} matches`,
    detail: `The current filters cover ${new Set(scoped.map((m) => m.tournament)).size} tournaments.`,
    method: `Row count for ${scopeLabel}.`,
    matchCount: scoped.length,
  }

  return {
    headline: 'That field is not available in this dataset',
    detail: 'Try asking about aces, match duration, surfaces, tours, tournaments, or match counts.',
    method: 'The answer engine only reports statistics supported by the loaded source columns.',
    matchCount: scoped.length,
    limitation: 'Requested information is not available in the open match records.',
  }
}
