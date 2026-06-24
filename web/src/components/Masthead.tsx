import type { Metrics, Health } from '../api/client'

function Mark() {
  return (
    <span className="brand-mark" aria-hidden="true">
      <svg viewBox="0 0 24 24" fill="none">
        <circle cx="12" cy="12" r="8" stroke="currentColor" strokeWidth="1.6" />
        <ellipse cx="12" cy="12" rx="3.4" ry="8" stroke="currentColor" strokeWidth="1.1" />
        <ellipse cx="12" cy="12" rx="8" ry="3.4" stroke="currentColor" strokeWidth="1.1" />
        <circle cx="12" cy="12" r="1.5" fill="currentColor" />
      </svg>
    </span>
  )
}

/* Plate I. A vintage laced football drawn as a natural-history engraving,
   inked in gilt and cream over the night pitch. The two Law 2 figures are
   real: circumference 68 to 70 cm, weight 410 to 450 g. */
function HeroPlate() {
  return (
    <svg className="hero-plate" viewBox="0 0 880 330" role="img" aria-label="Engraved plate of a vintage laced football, with Law 2 dimensions">
      <defs>
        <pattern id="heroHatch" width="5" height="5" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
          <line x1="0" y1="0" x2="0" y2="5" stroke="rgba(242,234,215,0.18)" strokeWidth="0.65" />
        </pattern>
        <clipPath id="heroBallClip"><circle cx="440" cy="166" r="116" /></clipPath>
        <radialGradient id="heroBallShade" cx="40%" cy="34%" r="78%">
          <stop offset="0%" stopColor="rgba(242,234,215,0.18)" />
          <stop offset="58%" stopColor="rgba(242,234,215,0.04)" />
          <stop offset="100%" stopColor="rgba(7,24,17,0)" />
        </radialGradient>
      </defs>
      <ellipse cx="440" cy="300" rx="104" ry="8" fill="url(#heroHatch)" opacity="0.4" />
      <g clipPath="url(#heroBallClip)">
        <rect x="322" y="48" width="236" height="236" fill="url(#heroHatch)" opacity="0.5" />
        <circle cx="440" cy="166" r="116" fill="url(#heroBallShade)" />
      </g>
      <circle cx="440" cy="166" r="116" fill="none" stroke="var(--hero-gold)" strokeWidth="2.4" />
      <ellipse cx="440" cy="166" rx="52" ry="112" fill="none" stroke="var(--hero-ink)" strokeWidth="1.3" opacity="0.65" />
      <ellipse cx="440" cy="166" rx="112" ry="42" fill="none" stroke="var(--hero-ink)" strokeWidth="1.3" opacity="0.65" />
      <path d="M414 84 H466" stroke="var(--hero-gold)" strokeWidth="2.6" strokeLinecap="round" />
      <path d="M424 77 l8 14 M438 77 l8 14 M452 77 l8 14" stroke="var(--hero-gold)" strokeWidth="1.7" strokeLinecap="round" />
      <g fontFamily="'IBM Plex Mono',monospace" fontSize="10.5" fill="var(--hero-ink-2)" letterSpacing="1.5">
        <text x="252" y="84" textAnchor="end">fig. 1 . the lace, hand bound</text>
        <text x="240" y="192" textAnchor="end">fig. 2 . the seam, hand stitched</text>
        <text x="628" y="118" fontSize="11.5" fill="var(--hero-ink)" letterSpacing="2.5">LAW 2 . THE BALL</text>
        <text x="628" y="178">circumference, 68 to 70 cm</text>
        <text x="628" y="234">weight at kick off, 410 to 450 g</text>
      </g>
      <g stroke="var(--hero-ink-2)" strokeWidth="0.8" opacity="0.85" fill="none">
        <path d="M262 80 L408 82" /><circle cx="408" cy="82" r="1.8" fill="var(--hero-ink-2)" stroke="none" />
        <path d="M250 188 L390 206" /><circle cx="390" cy="206" r="1.8" fill="var(--hero-ink-2)" stroke="none" />
        <path d="M620 174 L552 186" /><circle cx="552" cy="186" r="1.8" fill="var(--hero-ink-2)" stroke="none" />
        <path d="M620 230 L522 244" /><circle cx="522" cy="244" r="1.8" fill="var(--hero-ink-2)" stroke="none" />
      </g>
    </svg>
  )
}

export function Masthead({
  metrics,
  health,
  languageCount,
}: {
  metrics?: Metrics
  health?: Health
  languageCount: number
}) {
  const chunks = metrics?.chunks_indexed ?? 593
  const citation = metrics?.citation_accuracy_pct ?? 100
  const total = metrics?.total_questions ?? 50
  const online = health ? health.ollama_reachable && health.granite_loaded : undefined

  const statusText =
    online === false
      ? 'Engine at rest. Start Ollama with granite3.1-dense:8b'
      : online === true
        ? 'Rule engine in session. Local and private'
        : 'Local engine. Private by design'

  return (
    <header className="hero">
      <div className="hero-inner">
        <div className="hero-top">
          <div className="brand">
            <Mark />
            Decision<em>Lens</em>
          </div>
          <div className="hero-status" role="status" aria-live="polite">
            <span className={`hero-status-dot ${online === false ? 'is-off' : ''}`} aria-hidden="true" />
            {statusText}
          </div>
        </div>

        <div className="hero-ruleline">
          <span>The Laws of the Game · IFAB, since 1863</span>
          <span>2026 World Cup edition</span>
        </div>

        <div className="hero-plate-wrap">
          <HeroPlate />
        </div>
        <div className="hero-plate-cap">The ball, drawn in the style of the 1930 final</div>

        <p className="hero-kicker">VAR &amp; referee decisions · FIFA World Cup 2026</p>
        <h1 className="hero-title">
          The Laws of the Game, <em>illuminated</em>
        </h1>
        <p className="hero-sub">
          Ask why a goal was disallowed or a penalty given. DecisionLens finds the exact passage in the
          official IFAB Laws of the Game and VAR Protocol, explains it in plain language, and says how
          strongly the rulebook backs the answer, or states plainly when it cannot know.
        </p>

        <div className="hero-plaque">
          <div className="hstat">
            <div className="hstat-v"><em>{chunks}</em></div>
            <div className="hstat-k">rule passages, parsed by IBM Docling</div>
          </div>
          <div className="hstat">
            <div className="hstat-v">Granite&nbsp;<em>3.1</em><span className="hstat-tag">IBM</span></div>
            <div className="hstat-k">8B · IBM Granite via Ollama</div>
          </div>
          <div className="hstat">
            <div className="hstat-v"><em>{Math.round(citation)}%</em></div>
            <div className="hstat-k">answers cite the rulebook · {total}-question suite</div>
          </div>
          <div className="hstat">
            <div className="hstat-v"><em>{languageCount}</em>&nbsp;tongues</div>
            <div className="hstat-k">fan &amp; analyst registers</div>
          </div>
        </div>
      </div>
    </header>
  )
}
