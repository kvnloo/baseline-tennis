export type Tour = 'ATP' | 'WTA'
export type Surface = 'Hard' | 'Clay' | 'Grass' | 'Carpet'

export interface MatchRecord {
  id: string
  tour: Tour
  tournament: string
  city: string
  country: string
  lat: number
  lng: number
  surface: Surface
  level: string
  date: string
  winner: string
  loser: string
  winnerRank: number | null
  loserRank: number | null
  winnerAces: number
  loserAces: number
  winnerDoubleFaults: number
  loserDoubleFaults: number
  minutes: number | null
}

export interface StatisticalAnswer {
  headline: string
  value?: string
  detail: string
  method: string
  matchCount: number
  limitation?: string
}
