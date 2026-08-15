export type Side = 'home' | 'away'
export type PointResult = 'ace' | 'double_fault' | 'serve_winner' | 'return_winner' | 'forced_error' | 'unforced_error'

export type LivePoint = {
  id: string
  set: number
  game: number
  point: number
  server: Side
  winner: Side
  result: PointResult
  score: string
  rallyLength?: number
  landing?: { x: number | null; y: number | null }
  occurredAt?: string
}

const countWords = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve']

export function describePoint(event: LivePoint): string {
  const shots = event.rallyLength && event.rallyLength < countWords.length
    ? ` after ${countWords[event.rallyLength]} shots`
    : event.rallyLength ? ` after a ${event.rallyLength}-shot rally` : ''
  const result: Record<PointResult, string> = {
    ace: 'Ace',
    double_fault: 'Double fault',
    serve_winner: 'Unreturned serve',
    return_winner: 'Return winner',
    forced_error: 'Forced error',
    unforced_error: 'Unforced error',
  }
  const pressure = event.score === '30–40' || event.score === '40–AD' ? ' Break point' : ' Score'
  return `${result[event.result]}${shots}.${pressure} at ${event.score}.`
}

export function normalizeCourtPoint(point: { x: number | null; y: number | null }): { x: number; y: number } | null {
  if (point.x === null || point.y === null) return null
  const clamp = (value: number) => Math.max(10, Math.min(90, Math.round(value)))
  return { x: clamp(50 + point.x * 5), y: clamp(50 - point.y * 4.25) }
}
