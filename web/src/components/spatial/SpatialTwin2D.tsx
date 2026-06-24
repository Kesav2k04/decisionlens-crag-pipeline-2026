/* 2D tactical chalkboard: the always-available twin of the 3D inset.
   Shown when WebGL is unavailable, motion is reduced, or the 3D scene errors.
   Drawn with chalk strokes and hand-drawn tactical arrows on the dark stage:
   labelled illustrations of the cited rule, never a reconstruction of a real
   incident. */

const LINE = '#e8f1ea'
const TEXT = '#cfe0d5'
const FAINT = 'rgba(232,241,234,0.28)'
const OFFSIDE = '#e8553a'
const ATTACK = '#e0b357'
const DEFEND = '#83a6d4'
const GOOD = '#5fb07f'

function label(x: number, y: number, t: string, fill = TEXT, anchor: 'start' | 'middle' | 'end' = 'middle') {
  return (
    <text x={x} y={y} textAnchor={anchor} fontFamily="'IBM Plex Mono',monospace" fontSize="9" letterSpacing="0.5" fill={fill}>{t}</text>
  )
}

/* shared chalk defs: a hand-drawn wobble filter and a context-coloured arrowhead */
function ChalkDefs() {
  return (
    <defs>
      <filter id="dl-chalk" x="-5%" y="-5%" width="110%" height="110%">
        <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="1" seed="7" result="n" />
        <feDisplacementMap in="SourceGraphic" in2="n" scale="1.1" />
      </filter>
      <marker id="dl-arrow" viewBox="0 0 10 10" refX="7.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
        <path d="M0,0 L10,5 L0,10 z" fill="context-stroke" />
      </marker>
    </defs>
  )
}

export function SpatialTwin2D({ type }: { type: string }) {
  if (type === 'offside') {
    return (
      <svg viewBox="0 0 320 200" className="dl-twin" role="img" aria-label="Offside geometry: the offside line at the second-last defender, with an attacker beyond it.">
        <ChalkDefs />
        <rect x="24" y="22" width="272" height="156" fill="none" stroke={FAINT} strokeWidth="1" rx="3" />
        <g filter="url(#dl-chalk)" fill="none">
          <line x1="50" y1="22" x2="50" y2="178" stroke={LINE} strokeWidth="2" />
          <rect x="170" y="22" width="100" height="156" fill={OFFSIDE} opacity="0.07" stroke="none" />
          <line x1="170" y1="22" x2="170" y2="178" stroke={OFFSIDE} strokeWidth="2.5" />
          <path d="M126 92 C 150 70, 178 70, 196 84" stroke={ATTACK} strokeWidth="2" strokeDasharray="5 4" markerEnd="url(#dl-arrow)" strokeLinecap="round" />
        </g>
        {label(50, 16, 'goal line')}
        {label(170, 16, 'offside line', OFFSIDE)}
        <circle cx="170" cy="120" r="7" fill={DEFEND} />{label(170, 142, 'defender', DEFEND)}
        <circle cx="120" cy="92" r="7" fill={ATTACK} />{label(116, 80, 'attacker, beyond', ATTACK)}
        {label(248, 110, 'offside side', 'rgba(232,85,58,0.6)')}
      </svg>
    )
  }
  if (type === 'penalty') {
    return (
      <svg viewBox="0 0 320 200" className="dl-twin" role="img" aria-label="Penalty-area geometry: the boundary that separates a penalty from a direct free kick.">
        <ChalkDefs />
        <rect x="24" y="22" width="272" height="156" fill="none" stroke={FAINT} strokeWidth="1" rx="3" />
        <g filter="url(#dl-chalk)" fill="none">
          <line x1="44" y1="22" x2="44" y2="178" stroke={LINE} strokeWidth="2" />
          <rect x="44" y="48" width="120" height="104" stroke={LINE} strokeWidth="2" />
          <rect x="44" y="80" width="44" height="40" stroke={LINE} strokeWidth="1.4" />
          <path d="M 150 78 A 26 26 0 0 1 150 122" stroke={LINE} strokeWidth="1.4" />
          <path d="M128 100 C 104 92, 80 96, 60 100" stroke={GOOD} strokeWidth="2" markerEnd="url(#dl-arrow)" strokeLinecap="round" />
        </g>
        {label(104, 42, 'penalty area')}
        <circle cx="128" cy="100" r="2.8" fill={LINE} />
        <circle cx="96" cy="118" r="7" fill={GOOD} />{label(96, 140, 'inside: penalty', GOOD)}
        <circle cx="232" cy="100" r="7" fill={OFFSIDE} />{label(232, 122, 'outside: free kick', OFFSIDE)}
      </svg>
    )
  }
  if (type === 'corner') {
    return (
      <svg viewBox="0 0 320 200" className="dl-twin" role="img" aria-label="Corner-kick geometry: the quarter-circle arc at the corner where a corner kick is taken.">
        <ChalkDefs />
        <rect x="24" y="22" width="272" height="156" fill="none" stroke={FAINT} strokeWidth="1" rx="3" />
        <g filter="url(#dl-chalk)" fill="none">
          <line x1="44" y1="40" x2="44" y2="170" stroke={LINE} strokeWidth="2" />
          <line x1="44" y1="170" x2="250" y2="170" stroke={LINE} strokeWidth="2" />
          <path d="M 44 142 A 28 28 0 0 0 72 170" stroke={OFFSIDE} strokeWidth="2.5" />
          <line x1="44" y1="170" x2="44" y2="146" stroke={TEXT} strokeWidth="1.6" />
          <path d="M 44 146 l 13 4 l -13 4 z" fill={OFFSIDE} stroke="none" />
          <rect x="40" y="64" width="8" height="40" stroke={LINE} strokeWidth="1.6" />
          <path d="M 64 158 C 120 120, 170 120, 196 132" stroke={ATTACK} strokeWidth="2" strokeDasharray="5 4" markerEnd="url(#dl-arrow)" strokeLinecap="round" />
        </g>
        {label(44, 32, 'goal line')}
        {label(150, 188, 'touchline')}
        {label(98, 150, 'corner arc', OFFSIDE, 'start')}
        <circle cx="58" cy="156" r="5" fill="#f7faf7" />{label(72, 138, 'ball', TEXT, 'start')}
        {label(196, 124, 'delivery', ATTACK, 'start')}
      </svg>
    )
  }
  // var: four nested scope rings
  const rings = [
    { r: 76, c: DEFEND, t: 'goal / no goal' },
    { r: 58, c: GOOD, t: 'penalty / no penalty' },
    { r: 40, c: ATTACK, t: 'direct red card' },
    { r: 22, c: OFFSIDE, t: 'mistaken identity' },
  ]
  return (
    <svg viewBox="0 0 320 200" className="dl-twin" role="img" aria-label="The four categories VAR may review, drawn as nested scope rings.">
      <ChalkDefs />
      <g filter="url(#dl-chalk)" fill="none">
        {rings.map((ring, i) => (
          <circle key={i} cx="104" cy="100" r={ring.r} stroke={ring.c} strokeWidth="2.4" />
        ))}
      </g>
      {rings.map((ring, i) => (
        <text key={`t${i}`} x="206" y={60 + i * 26} fontFamily="'IBM Plex Mono',monospace" fontSize="10" fill={TEXT}>
          <tspan fill={ring.c}>■ </tspan>{ring.t}
        </text>
      ))}
    </svg>
  )
}
