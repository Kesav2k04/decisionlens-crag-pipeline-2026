import { Suspense, lazy } from 'react'
import type { ExplainResult } from '../api/client'
import { DECISION_META, pickScene } from '../api/client'
import { Dial, DecisionEmblem } from './instruments'

const SpatialInset = lazy(() =>
  import('./spatial/SpatialInset').then((m) => ({ default: m.SpatialInset })),
)

function band(pct: number): { color: string; text: string; status: string } {
  if (pct >= 75) return { color: 'var(--good-ink)', text: 'Answered from the rulebook', status: 'SUFFICIENT' }
  if (pct >= 40) return { color: 'var(--gold-2)', text: 'Partial evidence. The answer may be incomplete', status: 'PARTIAL' }
  return { color: 'var(--red)', text: 'Not enough evidence. The engine declines to guess', status: 'DECLINED' }
}

export function VerdictRecord({ question, result, index }: { question: string; result: ExplainResult; index: number }) {
  const confidence = Number(result.confidence || 0)
  const pct = Math.round(confidence * 100)
  const decisionType = result.decision_type || 'unknown'
  const meta = DECISION_META[decisionType] ?? DECISION_META.unknown
  const b = band(pct)
  const citations = result.rule_citations ?? []
  const steps = result.decision_steps ?? []
  const missing = result.missing_evidence ?? []
  const showMissing = missing.length > 0 && (confidence < 0.5 || decisionType === 'unknown')
  const scene = pickScene(question, decisionType)
  const showSpatial = scene !== null && !!result.retrieval_debug && confidence > 0
  const answer = result.answer || 'No answer recorded.'
  const hasCap = !!result.answer && answer.length > 60
  const sources = result.sources?.length
    ? result.sources
    : ['IFAB Laws of the Game 2025/26', 'IFAB VAR Protocol']

  return (
    <article className="dl-rec" aria-label="Answer record">
      <div className="dl-rec-head">
        <span className="dl-rec-head-t">The answer</span>
        <span className="dl-rec-head-n">№ {index}</span>
      </div>

      <div className="dl-rec-qlab">Your question</div>
      <p className="dl-rec-q" dir="auto">{question}</p>

      <div className="dl-rec-band" style={{ color: b.color }}>
        <span className="dl-rec-band-tag" style={{ background: meta.color }}><span>{meta.label}</span></span>
        <span className="dl-rec-band-msg">{b.text}</span>
        <span className="dl-rec-band-status">{b.status}</span>
      </div>

      <p className={`dl-rec-answer ${hasCap ? 'has-cap' : ''}`} dir="auto">{answer}</p>

      <div className="dl-instruments">
        <div className="dl-dialwrap">
          <Dial pct={pct} color={b.color} />
          <div className="dl-dial-v" style={{ color: b.color }}>{pct}<small> /100</small></div>
          <div className="dl-dial-s" style={{ color: b.color }}>{b.status}</div>
          <div className="dl-dial-k">Evidence sufficiency: how well the rulebook covers this question, not whether the call was right.</div>
        </div>
        <div className="dl-stampwrap"><DecisionEmblem label={meta.label} color={meta.color} /></div>
      </div>

      {showSpatial && scene && (
        <Suspense fallback={<div className="dl-inset-stage"><span className="dl-inset-loading">Drawing the rule geometry…</span></div>}>
          <SpatialInset scene={scene} citations={citations} />
        </Suspense>
      )}

      {result.tactical_context && (decisionType === 'red_card' || decisionType === 'penalty') && (
        <>
          <div className="dl-rec-sec">Match impact</div>
          <div className="dl-marg">
            <b>Interpretation, not rule text</b>
            <span dir="auto">{result.tactical_context}</span>
          </div>
        </>
      )}

      {steps.length > 0 && (
        <>
          <div className="dl-rec-sec">Step by step</div>
          <ol className="dl-ladder">
            {steps.map((s, i) => (
              <li key={i}><span className="dl-rung-no">{i + 1}.</span><span dir="auto">{s}</span></li>
            ))}
          </ol>
        </>
      )}

      {citations.length > 0 && (
        <>
          <div className="dl-rec-sec">The rules it quoted</div>
          {citations.map((c, i) => {
            const law = c.law_or_section || c.law || 'Rule reference'
            const src = c.source || 'IFAB official rules'
            return (
              <figure className="dl-cite" key={i}>
                {c.quoted_span ? (
                  <blockquote className="dl-cite-q" dir="auto">{c.quoted_span}</blockquote>
                ) : (
                  <blockquote className="dl-cite-q">Section consulted in full.</blockquote>
                )}
                <figcaption className="dl-cite-src">
                  <b>{law}</b> · {src}
                </figcaption>
              </figure>
            )
          })}
        </>
      )}

      {showMissing && (
        <>
          <div className="dl-rec-sec" style={{ color: 'var(--red)' }}>What it could not determine</div>
          <div className="dl-missing">
            <div className="dl-missing-t">Facts the system does not have</div>
            <ul>{missing.map((m, i) => <li key={i} dir="auto">{m}</li>)}</ul>
          </div>
        </>
      )}

      <div className="dl-rec-foot">
        <span>Sources consulted: {sources.join(' · ')}</span>
        <span className="sep">·</span>
        <span>rendered in {result.language || 'English'}</span>
        {typeof result.api_latency_seconds === 'number' && (
          <>
            <span className="sep">·</span>
            <span>{result.api_latency_seconds.toFixed(1)}s</span>
          </>
        )}
      </div>
    </article>
  )
}
