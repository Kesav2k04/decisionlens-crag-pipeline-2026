/* The Lineage: a century of World Cup moments, drawn as hand-inked player
   figures in the margin of the page. Each card carries a single-stroke
   illustration in the same ink as the rest of the design. The 1986 "Hand of
   God" is the highlighted card: the four-second incident that, decades later,
   made the case for video review. */

export type MotifName =
  | 'kickoff' | 'prodigy' | 'header' | 'volley' | 'handball' | 'maestro'
  | 'keeper' | 'review' | 'lift' | 'whistle'

/* Hand-inked figure library: loose single-stroke player drawings.
   stroke = currentColor, so each inherits the card's ink or accent colour. */
export const MOTIF_PATHS: Record<MotifName, string> = {
  // a player striking the ball off the ground (kick-off)
  kickoff:
    '<circle cx="22" cy="7.5" r="3"/><path d="M22 11v9l-6 5"/><path d="M22 14l7 4"/><path d="M22 20l-2 9"/><path d="M22 20l6 5 4-2"/><circle cx="13.5" cy="33" r="3.2"/>',
  // a young prodigy, ball balanced at the foot
  prodigy:
    '<circle cx="20" cy="7.5" r="3"/><path d="M20 11v10"/><path d="M20 14l6 3"/><path d="M20 14l-5 4"/><path d="M20 21l-3 8"/><path d="M20 21l4 8"/><circle cx="29" cy="31" r="3.4"/>',
  // a player rising for a header
  header:
    '<circle cx="22" cy="6.5" r="3"/><path d="M16 4l3 2.2M28 4l-3 2.2"/><path d="M22 10v9"/><path d="M22 13l-6-2M22 13l6-2"/><path d="M22 19l-3 9M22 19l3 9"/><circle cx="22" cy="35" r="2.4"/>',
  // a volley, leg swung high
  volley:
    '<circle cx="18" cy="8" r="3"/><path d="M18 11v8"/><path d="M18 13l6 3"/><path d="M18 13l-5 5"/><path d="M18 19l9-3"/><path d="M18 19l-2 9"/><circle cx="31" cy="13.5" r="3.2"/>',
  // the handball: a figure with an outstretched arm to a high ball
  handball:
    '<circle cx="18" cy="9" r="3"/><path d="M18 12v9"/><path d="M18 15l9-6"/><path d="M18 15l-5 4"/><path d="M18 21l-2 9M18 21l4 8"/><circle cx="30" cy="7" r="2.8"/>',
  // a maestro on the turn, ball at feet
  maestro:
    '<circle cx="22" cy="7.5" r="3"/><path d="M22 11c-3 3-3 6 0 9"/><path d="M22 13l-6 1M22 13l6 2"/><path d="M22 20l-4 8M22 20l3 8"/><circle cx="16" cy="31" r="3.2"/>',
  // a diving goalkeeper reaching the ball
  keeper:
    '<circle cx="11" cy="13" r="3"/><path d="M11 16l8 4"/><path d="M11 16l-4 6"/><path d="M14 18l8-5M14 18l7 7"/><path d="M11 22l-4 6"/><circle cx="33" cy="10.5" r="3.4"/>',
  // a pitchside review monitor (VAR era)
  review:
    '<rect x="8" y="11" width="28" height="18" rx="1.5"/><path d="M18 35h8M22 29v6"/><path d="M15 20h6M15 23h10" stroke-width="1.2"/><circle cx="29.5" cy="16.5" r="1.6"/>',
  // a player lifting the trophy aloft
  lift:
    '<circle cx="22" cy="8.5" r="3"/><path d="M22 12v8"/><path d="M22 14l-6-3M22 14l6-3"/><path d="M22 20l-3 9M22 20l3 9"/><path d="M16 6h12M18 6v2.5a4 4 0 0 0 8 0V6M22 3.5V6"/>',
  // referee whistle
  whistle:
    '<path d="M16 14h16a2.5 2.5 0 0 1 2.5 2.5V19l-9.5 3.6A8 8 0 1 1 16 14z"/><circle cx="18.5" cy="28" r="3.2"/><path d="M27 9.5l1.5-3M31.5 10.5l3-2M34 14h4" stroke-width="1.2"/>',
}

export function Motif({ name, size = 46, className = 'lg-motif' }: { name: MotifName; size?: number; className?: string }) {
  return (
    <svg className={className} width={size} height={size} viewBox="0 0 44 44" aria-hidden="true">
      <g fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round"
        dangerouslySetInnerHTML={{ __html: MOTIF_PATHS[name] }} />
    </svg>
  )
}

interface Era {
  year: string
  name: string
  note: string
  motif: MotifName
  hero?: boolean
}

const LINEAGE: Era[] = [
  { year: '1930', name: 'Montevideo', note: 'The first final. One referee, no replays, only his word.', motif: 'kickoff' },
  { year: '1958', name: 'Pelé, seventeen', note: 'A boy lifts the Cup in Sweden, and the whole game tilts toward genius.', motif: 'prodigy' },
  { year: '1966', name: 'Wembley', note: 'Did the ball cross the line? Sixty years of argument, one camera short.', motif: 'header' },
  { year: '1970', name: 'Brazil', note: 'Football in full colour, the most beautiful side ever filmed.', motif: 'volley' },
  { year: '1986', name: 'The Hand of God', note: 'Maradona, Law 12, and the four-second incident that made the case for video review.', motif: 'handball', hero: true },
  { year: '1998', name: 'Zidane in Paris', note: 'Two headers in a final, and a nation redrawn around one man.', motif: 'maestro' },
  { year: '2010', name: "Lampard's ghost goal", note: 'A goal that was not given. Goal-line technology arrives two years later.', motif: 'keeper' },
  { year: '2018', name: 'Moscow', note: 'VAR enters the World Cup. Every verdict now leaves a record.', motif: 'review' },
  { year: '2022', name: 'Messi, at last', note: 'The longest argument in football is settled in Lusail.', motif: 'lift' },
  { year: '2026', name: 'The 48-team Cup', note: 'Three hosts, more decisions than ever, each one explainable, right here.', motif: 'whistle' },
]

export function Lineage() {
  return (
    <section aria-label="A century of World Cup moments">
      <div className="section-rule">
        <span className="k">History</span>
        <span className="n">A century of the World Cup</span>
        <span className="i">the moments that shaped how decisions get made</span>
      </div>
      <div className="lineage">
        {LINEAGE.map((e) => (
          <article className={`lg-card ${e.hero ? 'is-hero' : ''}`} key={e.year}>
            <div className="lg-top">
              <span className="lg-yr">{e.year}</span>
              {e.hero && <span className="lg-tag">turning point</span>}
            </div>
            <Motif name={e.motif} />
            <div className="lg-name">{e.name}</div>
            <div className="lg-note">{e.note}</div>
          </article>
        ))}
      </div>
    </section>
  )
}
