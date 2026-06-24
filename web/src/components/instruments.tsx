/* Engraved instruments for the decision record.
   - Dial: an evidence-sufficiency gauge (0..100) with brass-style tick work and
     the two CRAG threshold witnesses at 65 (gold) and 75 (green).
   - DecisionEmblem: a circular rubber stamp naming the decision family, roughened
     so it reads as inked onto the page rather than printed.
   - CragRuler: the 0..1 evidence scale with the 0.65 / 0.75 boundaries.
   Colour is passed in so the band, dial, and stamp stay in one decision tone. */
import type { CSSProperties } from 'react'

const LABEL = 'var(--muted)'

function polar(cx: number, cy: number, r: number, deg: number): [number, number] {
  const a = (Math.PI / 180) * deg
  return [cx + r * Math.cos(a), cy + r * Math.sin(a)]
}

/* Evidence-sufficiency dial, 0..100 over a top semicircle.
   Threshold witnesses sit at 65 (abstain below) and 75 (sufficient at/above). */
export function Dial({ pct, color }: { pct: number; color: string }) {
  const cx = 110
  const cy = 116
  const r = 86
  const [bx, by] = polar(cx, cy, r, 180)
  const [ex, ey] = polar(cx, cy, r, 180 + Math.max(pct, 1) * 1.8)

  const ticks = []
  for (let i = 0; i <= 20; i++) {
    const ang = (Math.PI / 180) * (180 + i * 9)
    const major = i % 5 === 0
    const r1 = r - (major ? 12 : 7)
    const x1 = cx + r1 * Math.cos(ang)
    const y1 = cy + r1 * Math.sin(ang)
    const x2 = cx + r * Math.cos(ang)
    const y2 = cy + r * Math.sin(ang)
    ticks.push(
      <line key={`tk${i}`} x1={x1.toFixed(1)} y1={y1.toFixed(1)} x2={x2.toFixed(1)} y2={y2.toFixed(1)}
        stroke="var(--ink)" strokeWidth={major ? 1.6 : 0.9} opacity={major ? 0.9 : 0.5} />,
    )
  }

  const labels = [0, 25, 50, 75, 100].map((v) => {
    const ang = (Math.PI / 180) * (180 + v * 1.8)
    const rx = r - 23
    const x = cx + rx * Math.cos(ang)
    const y = cy + rx * Math.sin(ang) + 3.2
    return (
      <text key={`l${v}`} x={x.toFixed(1)} y={y.toFixed(1)} textAnchor="middle"
        fontFamily="'IBM Plex Mono',monospace" fontSize="9" fill={LABEL}>{v}</text>
    )
  })

  const witnesses = ([[65, 'var(--gold)'], [75, 'var(--good)']] as const).map(([v, c]) => {
    const ang = (Math.PI / 180) * (180 + v * 1.8)
    const [x1, y1] = [cx + (r + 2) * Math.cos(ang), cy + (r + 2) * Math.sin(ang)]
    const [x2, y2] = [cx + (r + 9) * Math.cos(ang), cy + (r + 9) * Math.sin(ang)]
    return <line key={`w${v}`} x1={x1.toFixed(1)} y1={y1.toFixed(1)} x2={x2.toFixed(1)} y2={y2.toFixed(1)} stroke={c} strokeWidth={2.4} />
  })

  return (
    <svg viewBox="0 0 220 142" width="232" className="dl-dial"
      role="img" aria-label={`Evidence sufficiency ${pct} out of 100`}>
      <path d={`M ${bx} ${by} A ${r} ${r} 0 0 1 ${cx + r} ${cy}`} stroke="var(--hair)" strokeWidth="1" fill="none" />
      <path d={`M ${bx} ${by} A ${r} ${r} 0 0 1 ${ex.toFixed(1)} ${ey.toFixed(1)}`}
        stroke={color} strokeWidth="3" fill="none" opacity="0.9" strokeLinecap="round" />
      {ticks}{labels}{witnesses}
      <g className="dl-needle" style={{ '--sweep': `${(pct * 1.8).toFixed(1)}deg` } as CSSProperties}>
        <polygon points="34,116 112,112.6 112,119.4" fill={color} />
        <circle cx={cx} cy={cy} r="5.5" fill="var(--ink)" />
        <circle cx={cx} cy={cy} r="2" fill="var(--paper)" />
      </g>
    </svg>
  )
}

/* A circular rubber stamp for the decision family, roughened with a turbulence
   displacement so the ink looks pressed onto the parchment. */
export function DecisionEmblem({ label, color }: { label: string; color: string }) {
  const slug = label.replace(/\s+/g, '-').toLowerCase()
  const arcId = `stamp-arc-${slug}`
  const roughId = `stamp-rough-${slug}`
  const words = label.split(' ')
  const center =
    words.length >= 2 ? (
      <>
        <text x="75" y="71" textAnchor="middle" fontFamily="'Fraunces',serif" fontSize="15.5" fontWeight="650" letterSpacing="2" fill={color}>{words[0]}</text>
        <text x="75" y="89" textAnchor="middle" fontFamily="'Fraunces',serif" fontSize="15.5" fontWeight="650" letterSpacing="2" fill={color}>{words.slice(1).join(' ')}</text>
        <circle cx="75" cy="47" r="1.6" fill={color} />
        <circle cx="75" cy="101" r="1.6" fill={color} />
      </>
    ) : (
      <>
        <text x="75" y="81" textAnchor="middle" fontFamily="'Fraunces',serif" fontSize="16.5" fontWeight="650" letterSpacing="2.5" fill={color}>{label}</text>
        <circle cx="75" cy="55" r="1.6" fill={color} />
        <circle cx="75" cy="95" r="1.6" fill={color} />
      </>
    )

  return (
    <svg viewBox="0 0 150 150" width="146" className="dl-badge" role="img" aria-label={`Decision stamp: ${label}`}>
      <defs>
        <path id={arcId} d="M 75 75 m -57 0 a 57 57 0 1 1 114 0 a 57 57 0 1 1 -114 0" />
        <filter id={roughId}>
          <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="1" result="n" />
          <feDisplacementMap in="SourceGraphic" in2="n" scale="2.2" />
        </filter>
      </defs>
      <g filter={`url(#${roughId})`}>
        <circle cx="75" cy="75" r="70" fill="none" stroke={color} strokeWidth="3" />
        <circle cx="75" cy="75" r="46" fill="none" stroke={color} strokeWidth="1.4" />
        <text fontFamily="'IBM Plex Mono',monospace" fontSize="9.2" letterSpacing="2.6" fill={color}>
          <textPath href={`#${arcId}`}>LAWS OF THE GAME · I.F.A.B. · DECISIONLENS · 2026 · </textPath>
        </text>
        {center}
      </g>
    </svg>
  )
}

/* CRAG evidence-score scale: zones (abstain / borderline / sufficient), fixed
   marks at 0.65 and 0.75, and a pin at the actual score. */
export function CragRuler({ score }: { score: number }) {
  const pos = Math.max(0, Math.min(1, score)) * 100
  return (
    <div className="dl-ruler" role="img" aria-label={`Evidence score ${score.toFixed(3)} on a 0 to 1 scale; the engine abstains below 0.65 and answers at or above 0.75`}>
      <div className="dl-ruler-bar">
        <span className="dl-zone z-poor" />
        <span className="dl-zone z-mid" />
        <span className="dl-zone z-good" />
        <span className="dl-mark" style={{ left: '65%' }} />
        <span className="dl-mark" style={{ left: '75%' }} />
        <span className="dl-pin" style={{ left: `${pos.toFixed(1)}%` }} />
      </div>
      <div className="dl-ruler-lab">
        <span>0</span>
        <span style={{ left: '65%' }}>0.65</span>
        <span style={{ left: '75%' }}>0.75</span>
        <span>1.0</span>
      </div>
    </div>
  )
}
