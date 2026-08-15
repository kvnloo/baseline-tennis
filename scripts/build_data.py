#!/usr/bin/env python3
import csv, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VENUES = {
'Australian Open': ('Melbourne','Australia',-37.8216,144.9785), 'Roland Garros': ('Paris','France',48.8470,2.2492),
'Wimbledon': ('London','United Kingdom',51.4343,-0.2145), 'Us Open': ('New York','United States',40.7499,-73.8470),
'Indian Wells Masters': ('Indian Wells','United States',33.7235,-116.3056), 'Miami Masters': ('Miami','United States',25.9581,-80.2389),
'Madrid Masters': ('Madrid','Spain',40.3688,-3.6840), 'Rome Masters': ('Rome','Italy',41.9280,12.4558),
'Shanghai Masters': ('Shanghai','China',31.0426,121.3550), 'Monte Carlo Masters': ('Roquebrune-Cap-Martin','France',43.7516,7.4402),
'Canada Masters': ('Montreal','Canada',45.5329,-73.6270), 'Cincinnati Masters': ('Mason','United States',39.3483,-84.2766),
'Paris Masters': ('Paris','France',48.8386,2.3786), 'Doha': ('Doha','Qatar',25.2819,51.5200), 'Dubai': ('Dubai','United Arab Emirates',25.2426,55.3420),
'Brisbane': ('Brisbane','Australia',-27.5251,153.0070), 'Charleston': ('Charleston','United States',32.8613,-79.9038),
'Bad Homburg': ('Bad Homburg','Germany',50.2268,8.6182), 'Adelaide': ('Adelaide','Australia',-34.9152,138.5957),
'Linz': ('Linz','Austria',48.3110,14.2921), 'Abu Dhabi': ('Abu Dhabi','United Arab Emirates',24.4134,54.4764),
'San Diego': ('San Diego','United States',32.7157,-117.1611), 'Stuttgart': ('Stuttgart','Germany',48.7934,9.2285),
'Berlin': ('Berlin','Germany',52.4849,13.2584), 'Eastbourne': ('Eastbourne','United Kingdom',50.7624,0.2861),
'Washington': ('Washington','United States',38.9540,-77.0386), 'Monterrey': ('Monterrey','Mexico',25.6866,-100.3161),
'Guadalajara': ('Guadalajara','Mexico',20.6736,-103.3440), 'Seoul': ('Seoul','South Korea',37.5207,127.1215),
'Ningbo': ('Ningbo','China',29.8683,121.5440), 'Tokyo': ('Tokyo','Japan',35.6366,139.7907),
}
LEVELS={'G':'Grand Slam','M':'Masters 1000','P':'WTA 500','A':'Tour'}
def num(v, kind=int):
    try: return kind(v)
    except: return None
rows=[]
for tour, path in [('ATP',ROOT/'data/raw/atp_matches_2024.csv'),('WTA',ROOT/'data/raw/wta_matches_2024.csv')]:
    with path.open() as f:
        for r in csv.DictReader(f):
            if r['tourney_name'] not in VENUES: continue
            city,country,lat,lng=VENUES[r['tourney_name']]
            date=r['tourney_date']
            rows.append({'id':f"{tour}-{r['tourney_id']}-{r['match_num']}",'tour':tour,'tournament':r['tourney_name'].replace('Us Open','US Open'),'city':city,'country':country,'lat':lat,'lng':lng,'surface':r['surface'],'level':LEVELS.get(r['tourney_level'],'Tour'),'date':f'{date[:4]}-{date[4:6]}-{date[6:]}','winner':r['winner_name'],'loser':r['loser_name'],'winnerRank':num(r['winner_rank']),'loserRank':num(r['loser_rank']),'winnerAces':num(r['w_ace']) or 0,'loserAces':num(r['l_ace']) or 0,'winnerDoubleFaults':num(r['w_df']) or 0,'loserDoubleFaults':num(r['l_df']) or 0,'minutes':num(r['minutes'])})
(ROOT/'public/data/matches-2024.json').write_text(json.dumps(rows,separators=(',',':')))
print(json.dumps({'matches':len(rows),'tournaments':len({r['tournament'] for r in rows}),'players':len({r['winner'] for r in rows}|{r['loser'] for r in rows})}))
