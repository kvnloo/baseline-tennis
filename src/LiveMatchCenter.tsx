import { Broadcast, Circle, MapPin, Pulse } from '@phosphor-icons/react'
import { useEffect, useMemo, useState } from 'react'
import { describePoint, normalizeCourtPoint, type LivePoint } from './lib/live'

const demoPoints: LivePoint[] = [
  { id: 'p1', set: 2, game: 7, point: 1, server: 'home', winner: 'home', result: 'ace', score: '15–0', rallyLength: 1, landing: { x: -2.8, y: 8.7 } },
  { id: 'p2', set: 2, game: 7, point: 2, server: 'home', winner: 'away', result: 'return_winner', score: '15–15', rallyLength: 4, landing: { x: 3.7, y: -9.8 } },
  { id: 'p3', set: 2, game: 7, point: 3, server: 'home', winner: 'away', result: 'forced_error', score: '15–30', rallyLength: 11, landing: { x: -1.2, y: 3.6 } },
  { id: 'p4', set: 2, game: 7, point: 4, server: 'home', winner: 'away', result: 'return_winner', score: '30–40', rallyLength: 6, landing: { x: 3.2, y: -9.4 } },
]

export function LiveMatchCenter() {
  const [active, setActive] = useState(demoPoints.length - 1)
  const [playing, setPlaying] = useState(false)
  const point = demoPoints[active]
  const marker = useMemo(() => point.landing ? normalizeCourtPoint(point.landing) : null, [point])

  useEffect(() => {
    if (!playing) return
    const timer = window.setInterval(() => setActive((value) => (value + 1) % demoPoints.length), 2600)
    return () => window.clearInterval(timer)
  }, [playing])

  return (
    <section className="live-center" id="live" aria-labelledby="live-title">
      <div className="live-heading">
        <div>
          <span className="live-kicker"><Broadcast weight="fill" /> Match center</span>
          <h2 id="live-title">See the point, not just the score.</h2>
        </div>
        <div className="demo-status"><span>Demo replay</span><small>Provider not connected</small></div>
      </div>

      <div className="live-board">
        <div className="score-card">
          <div className="match-meta"><span>Exhibition data contract</span><b>SET 2 · GAME 7</b></div>
          <div className="player-row serving"><span><Circle weight="fill" /> Player A</span><b>4</b><strong>30</strong></div>
          <div className="player-row"><span>Player B</span><b>3</b><strong>40</strong></div>
          <div className="coverage"><Pulse /><span>Point timeline ready</span><MapPin /><span>Coordinates when supplied</span></div>
        </div>

        <div className="mini-court-wrap">
          <div className="mini-court" aria-label="Miniature tennis court showing the selected shot landing position">
            <span className="court-net" />
            <span className="court-service court-service-a" />
            <span className="court-service court-service-b" />
            <span className="court-center court-center-a" />
            <span className="court-center court-center-b" />
            {marker && <span className="shot-pulse" style={{ left: `${marker.x}%`, top: `${marker.y}%` }}><i /></span>}
          </div>
          <div className="court-key"><span><i /> selected landing</span><b>True x/y only</b></div>
        </div>

        <div className="play-feed">
          <div className="feed-head"><span>Point by point</span><button type="button" onClick={() => setPlaying((value) => !value)}>{playing ? 'Pause replay' : 'Play replay'}</button></div>
          <div className="commentary"><small>Point {point.point}</small><p>{describePoint(point)}</p></div>
          <ol>
            {demoPoints.map((event, index) => <li key={event.id} className={index === active ? 'active' : ''}>
              <button type="button" onClick={() => { setActive(index); setPlaying(false) }}>
                <span>P{event.point}</span><p>{describePoint(event)}</p><b>{event.score}</b>
              </button>
            </li>)}
          </ol>
        </div>
      </div>
      <p className="live-disclosure">This is an explicitly labeled interface replay—not a live match. Production mode requires a licensed server-side point feed; shot markers appear only when the provider supplies court coordinates.</p>
    </section>
  )
}
