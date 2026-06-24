import { useState, type FormEvent } from 'react'
import type { ApiConfig } from '../api/client'
import { getQuickAskVisualTag } from '../api/client'

const FALLBACK_ASKS = [
  'What makes a handball deliberate?',
  'When can VAR overturn an on-field decision?',
  'Explain the offside rule in simple terms',
  'What earns a straight red card?',
]
const FALLBACK_LANGS = ['English', 'Spanish', 'Portuguese', 'French', 'Arabic']

interface Props {
  config?: ApiConfig
  mode: 'fan' | 'analyst'
  language: string
  loading: boolean
  maxChars: number
  onAsk: (q: string) => void
  onModeChange: (m: 'fan' | 'analyst') => void
  onLanguageChange: (l: string) => void
}

export function InquiryDesk({
  config,
  mode,
  language,
  loading,
  maxChars,
  onAsk,
  onModeChange,
  onLanguageChange,
}: Props) {
  const [q, setQ] = useState('')
  const quickAsks = config?.quick_asks ?? FALLBACK_ASKS
  const languages = config?.languages ?? FALLBACK_LANGS

  const submit = (e: FormEvent) => {
    e.preventDefault()
    const t = q.trim()
    if (t && !loading) {
      onAsk(t)
      setQ('')
    }
  }

  return (
    <section id="ask" className="dl-ask" aria-label="Put a question to the Laws">
      <div className="section-rule">
        <span className="k">Ask</span>
        <span className="n">Ask a question</span>
        <span className="i">answers come only from the official rulebook, quoted, cited, and honest when unsure</span>
      </div>

      <p className="dl-ask-hint">
        Spatial rules (offside, penalty area, corner kick) may include a labelled pitch schematic when the
        rulebook supports an answer. Other questions return text and citations only.
      </p>

      <div className="dl-controls">
        <div className="dl-seg" role="group" aria-label="Answer register">
          <button
            type="button"
            className={`dl-seg-btn ${mode === 'fan' ? 'is-active' : ''}`}
            aria-pressed={mode === 'fan'}
            onClick={() => onModeChange('fan')}
          >
            Fan register
          </button>
          <button
            type="button"
            className={`dl-seg-btn ${mode === 'analyst' ? 'is-active' : ''}`}
            aria-pressed={mode === 'analyst'}
            onClick={() => onModeChange('analyst')}
          >
            Analyst register
          </button>
        </div>
        <label className="dl-lang">
          <span className="visually-hidden">Answer language</span>
          <select value={language} onChange={(e) => onLanguageChange(e.target.value)} aria-label="Answer language">
            {languages.map((l) => (
              <option key={l} value={l}>{l}</option>
            ))}
          </select>
        </label>
      </div>

      <div className="dl-chips">
        {quickAsks.map((qq) => {
          const tag = getQuickAskVisualTag(qq)
          return (
            <button key={qq} type="button" className="dl-chip" disabled={loading} onClick={() => !loading && onAsk(qq)}>
              <span className="dl-chip-q">{qq}</span>
              {tag ? (
                <span className={`dl-chip-tag is-${tag.kind}`} aria-hidden="true">{tag.label}</span>
              ) : null}
            </button>
          )
        })}
      </div>

      <form className="dl-form" onSubmit={submit}>
        <input
          type="text"
          value={q}
          maxLength={maxChars}
          disabled={loading}
          onChange={(e) => setQ(e.target.value)}
          placeholder="Why was that goal disallowed? Ask any rule or VAR question…"
          aria-label="Your question"
        />
        <button type="submit" className="dl-submit" disabled={loading || !q.trim()}>
          {loading ? (
            'Reading…'
          ) : (
            <>
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                <path d="M5 12h14M13 6l6 6-6 6" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" />
              </svg>
              Ask
            </>
          )}
        </button>
      </form>
    </section>
  )
}
