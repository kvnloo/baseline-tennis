import { useEffect, useMemo, useState } from 'react'
import { Area, AreaChart, Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import { ArrowUpRight, ChartBar, GlobeHemisphereWest, MagnifyingGlass } from '@phosphor-icons/react'
import { AnimatePresence, motion } from 'motion/react'
import { answerQuestion } from './lib/analytics'
import type { MatchRecord, StatisticalAnswer, Surface, Tour } from './lib/types'
import { LiveMatchCenter } from './LiveMatchCenter'
import { TennisBallSymbol } from './TennisBallSymbol'
import { ThemeToggle } from './ThemeToggle'
import { WorldMap } from './WorldMap'
import './index.css'

const examples = ['Who hit the most aces at Wimbledon?', 'What was the longest WTA match?', 'How many matches were played on clay?']

function App() {
  const [matches, setMatches] = useState<MatchRecord[]>([])
  const [tour, setTour] = useState<Tour | 'All'>('All')
  const [surface, setSurface] = useState<Surface | 'All'>('All')
  const [selectedTournament, setSelectedTournament] = useState<string | null>(null)
  const [question, setQuestion] = useState('')
  const [answer, setAnswer] = useState<StatisticalAnswer | null>(null)

  useEffect(() => { fetch('./data/matches-2024.json').then((r) => r.json()).then(setMatches) }, [])

  const filtered = useMemo(() => matches.filter((m) => (tour === 'All' || m.tour === tour) && (surface === 'All' || m.surface === surface) && (!selectedTournament || m.tournament === selectedTournament)), [matches, tour, surface, selectedTournament])
  const venues = useMemo(() => Object.values(filtered.reduce<Record<string, MatchRecord[]>>((acc, m) => ((acc[m.tournament] ||= []).push(m), acc), {})).map((group) => ({ ...group[0], count: group.length, aces: group.reduce((n, m) => n + m.winnerAces + m.loserAces, 0) })), [filtered])
  const surfaceData = useMemo(() => ['Hard', 'Clay', 'Grass'].map((name) => ({ name, matches: filtered.filter((m) => m.surface === name).length })), [filtered])
  const monthlyData = useMemo(() => Array.from({ length: 12 }, (_, i) => ({ name: new Date(2024, i).toLocaleString('en', { month: 'short' }), matches: filtered.filter((m) => Number(m.date.slice(5, 7)) === i + 1).length })), [filtered])
  const players = useMemo(() => new Set(filtered.flatMap((m) => [m.winner, m.loser])).size, [filtered])
  const aces = useMemo(() => filtered.reduce((n, m) => n + m.winnerAces + m.loserAces, 0), [filtered])

  const ask = (prompt = question) => { if (!prompt.trim()) return; setQuestion(prompt); setAnswer(answerQuestion(prompt, filtered.length ? filtered : matches)) }

  return <main className="app-shell">
    <header className="topbar">
      <div className="brand"><span className="brand-mark"><TennisBallSymbol size="sm" motion="hover" label="Baseline tennis ball" /></span><span>Baseline</span><span className="edition">Open tennis atlas</span></div>
      <nav><button className="nav-active">Explore</button><a href="#live">Live</a><button>Reports</button><a href="https://github.com/Aneeshers/tennis-sackmann-archive" target="_blank">Data <ArrowUpRight /></a><ThemeToggle /></nav>
    </header>

    <section className="hero-line">
      <div><p className="kicker">Global match intelligence</p><h1>Every court tells a story.</h1></div>
      <div className="hero-symbol"><TennisBallSymbol size="hero" motion="bounce" label="A textured tennis ball bouncing" /><p>Explore 2,547 ATP and WTA matches across 31 tournaments. Ask a statistical question and trace every answer to open data.</p></div>
    </section>

    <section className="controls" aria-label="Dataset filters">
      <div className="control-group"><span>Tour</span>{(['All', 'ATP', 'WTA'] as const).map((x) => <button key={x} className={tour === x ? 'selected' : ''} onClick={() => setTour(x)}>{x}</button>)}</div>
      <div className="control-group"><span>Surface</span>{(['All', 'Hard', 'Clay', 'Grass'] as const).map((x) => <button key={x} className={surface === x ? 'selected' : ''} onClick={() => setSurface(x)}>{x}</button>)}</div>
      {selectedTournament && <button className="clear-filter" onClick={() => setSelectedTournament(null)}>Clear {selectedTournament}</button>}
    </section>

    <LiveMatchCenter />

    <section className="atlas-grid">
      <div className="map-panel">
        <div className="panel-heading"><div><GlobeHemisphereWest /><span>Tournament map</span></div><span>{venues.length} venues</span></div>
        <WorldMap venues={venues} selected={selectedTournament} onSelect={setSelectedTournament} />
        <div className="map-caption"><span><TennisBallSymbol size="xs" motion="none" /> Marker size</span><b>matches recorded</b></div>
      </div>

      <aside className="metrics-panel">
        <div className="metric"><span>Matches</span><strong>{filtered.length.toLocaleString()}</strong><small>rows in current view</small></div>
        <div className="metric"><span>Players</span><strong>{players.toLocaleString()}</strong><small>unique competitors</small></div>
        <div className="metric"><span>Aces</span><strong>{aces.toLocaleString()}</strong><small>recorded serves</small></div>
        <div className="surface-chart"><div className="panel-heading"><div><ChartBar /><span>Surface mix</span></div></div><ResponsiveContainer width="100%" height={130}><BarChart data={surfaceData}><XAxis dataKey="name" axisLine={false} tickLine={false} tick={{ fill: '#8d9189', fontSize: 11 }} /><YAxis hide /><Tooltip cursor={{ fill: 'rgba(215,255,63,.06)' }} contentStyle={{ background: '#171916', border: '1px solid #30332e', borderRadius: 8 }} /><Bar dataKey="matches" fill="#d7ff3f" radius={[3, 3, 0, 0]} /></BarChart></ResponsiveContainer></div>
      </aside>
    </section>

    <section className="analysis-grid">
      <article className="trend-panel"><div className="panel-heading"><div><ChartBar /><span>Season rhythm</span></div><span>matches by month</span></div><ResponsiveContainer width="100%" height={230}><AreaChart data={monthlyData}><defs><linearGradient id="limeArea" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#d7ff3f" stopOpacity={0.3}/><stop offset="1" stopColor="#d7ff3f" stopOpacity={0}/></linearGradient></defs><CartesianGrid vertical={false} stroke="#262924"/><XAxis dataKey="name" axisLine={false} tickLine={false} tick={{ fill: '#777b74', fontSize: 11 }}/><YAxis hide/><Tooltip contentStyle={{ background: '#171916', border: '1px solid #30332e', borderRadius: 8 }}/><Area type="monotone" dataKey="matches" stroke="#d7ff3f" strokeWidth={2} fill="url(#limeArea)"/></AreaChart></ResponsiveContainer></article>

      <article className="ask-panel">
        <div className="ask-title"><span><TennisBallSymbol size="md" motion="hover" /></span><div><h2>Ask the dataset</h2><p>Plain-language reports with visible methodology.</p></div></div>
        <div className="examples">{examples.map((example) => <button key={example} onClick={() => ask(example)}>{example}</button>)}</div>
        <AnimatePresence mode="wait">{answer && <motion.div className="answer" key={answer.headline} initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }}><span>Report</span><h3>{answer.headline}</h3>{answer.value && <strong>{answer.value}</strong>}<p>{answer.detail}</p><details><summary>Method</summary><p>{answer.method}</p></details></motion.div>}</AnimatePresence>
        <form onSubmit={(e) => { e.preventDefault(); ask() }}><MagnifyingGlass /><input aria-label="Ask a statistical question" value={question} onChange={(e) => setQuestion(e.target.value)} placeholder="Compare ace rates by surface..."/><button type="submit"><TennisBallSymbol size="xs" motion="none" glow={false} /> Run report <ArrowUpRight /></button></form>
      </article>
    </section>

    <footer><span>Data: Jeff Sackmann / Tennis Abstract</span><span>Map: Natural Earth / world-atlas</span><span>CC BY-NC-SA 4.0</span><span>2024 snapshot</span></footer>
  </main>
}
export default App
