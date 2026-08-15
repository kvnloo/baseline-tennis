import { useEffect, useMemo, useState } from 'react'
import { geoNaturalEarth1, geoPath } from 'd3-geo'
import { feature } from 'topojson-client'
import type { FeatureCollection, Geometry } from 'geojson'
import type { GeometryCollection, Topology } from 'topojson-specification'
import type { MatchRecord } from './lib/types'

interface Venue extends MatchRecord { count: number; aces: number }
interface Props { venues: Venue[]; selected: string | null; onSelect: (name: string) => void }

const projection = geoNaturalEarth1().fitExtent([[18, 18], [882, 502]], { type: 'Sphere' })
const path = geoPath(projection)

export function WorldMap({ venues, selected, onSelect }: Props) {
  const [countries, setCountries] = useState<FeatureCollection<Geometry> | null>(null)
  const [zoom, setZoom] = useState(1)
  useEffect(() => {
    fetch('./data/countries-110m.json').then((r) => r.json()).then((topology: Topology) => {
      const objects = topology.objects as Record<string, GeometryCollection>
      setCountries(feature(topology, objects.countries) as FeatureCollection<Geometry>)
    })
  }, [])
  const dots = useMemo(() => venues.map((v) => ({ v, point: projection([v.lng, v.lat]) })), [venues])
  return <div className="world-map">
    <svg viewBox="0 0 900 520" role="img" aria-label="Interactive world map of tennis tournaments">
      <rect width="900" height="520" fill="#10120f" />
      <g style={{ transform: `scale(${zoom})`, transformOrigin: '450px 260px', transition: 'transform .55s cubic-bezier(.16,1,.3,1)' }}>
        {countries?.features.map((country, index) => <path key={index} d={path(country) ?? ''} fill="#1d201b" stroke="#34382f" strokeWidth={0.6} />)}
        {dots.map(({ v, point }) => point && <g key={v.tournament} transform={`translate(${point[0]} ${point[1]})`} className="venue-dot" onClick={() => onSelect(v.tournament)} role="button" tabIndex={0} aria-label={`${v.tournament}, ${v.count} matches`}>
          <circle r={selected === v.tournament ? 12 : Math.min(10, 4 + Math.sqrt(v.count) / 2.2)} fill={selected === v.tournament ? '#d7ff3f' : '#10120f'} stroke="#d7ff3f" strokeWidth={1.2}/>
          <text y="3" textAnchor="middle" fill={selected === v.tournament ? '#10120f' : '#d7ff3f'}>{v.count}</text>
        </g>)}
      </g>
    </svg>
    <div className="map-zoom"><button onClick={() => setZoom((z) => Math.min(1.8, z + .2))}>+</button><button onClick={() => setZoom((z) => Math.max(1, z - .2))}>−</button></div>
  </div>
}
