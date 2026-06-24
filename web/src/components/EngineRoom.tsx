import type { ReactNode } from 'react'
import type { ExplainResult, TopChunk } from '../api/client'
import { isIncidentGuardAbstention } from '../api/client'
import { CragRuler } from './instruments'

interface Station {
  numeral: string
  name: string
  role: string
  desc: string
  ibm: string | null
}

const STATIONS: Station[] = [
  { numeral: '1', name: 'Question check', role: 'the gate',
    desc: 'A guard reads the question first. Player names, minutes, and specific matches are facts no rulebook holds, so they are sent straight to an honest "cannot say".', ibm: null },
  { numeral: '2', name: 'Match context', role: 'optional side input',
    desc: 'Match details can be attached to the prompt for context only. They never enter the rule search and are never treated as evidence.', ibm: 'Context Forge' },
  { numeral: '3', name: 'Rule search', role: 'two searches at once',
    desc: 'Two searches run over the IBM Docling rulebook together: keyword matching for the exact wording, and meaning-based search for the intent, then the results are merged.', ibm: 'IBM Docling' },
  { numeral: '4', name: 'Evidence check', role: 'good enough?',
    desc: 'The evidence is scored before any answer is written. 0.75 and above is sufficient; below 0.65 the engine declines to answer; in between, the answer is marked as possibly incomplete.', ibm: null },
  { numeral: '5', name: 'Granite 3.1 · 8B', role: 'the writer',
    desc: 'IBM Granite writes the answer from the found passages only, with no randomness, in strict JSON — private inference via Ollama, not a third-party chat API.', ibm: 'IBM Granite' },
  { numeral: '6', name: 'Final answer', role: 'the result',
    desc: 'The answer, citations with the exact quoted text, step-by-step reasoning, an evidence score, and a clear note on anything it could not determine.', ibm: null },
]

function ChunkBars({ chunks }: { chunks: TopChunk[] }) {
  if (!chunks.length) return null
  const maxBm = Math.max(...chunks.map((c) => Number(c.bm25_score) || 0), 1)
  return (
    <div className="dl-chunks">
      {chunks.map((c, i) => {
        const bm = ((Number(c.bm25_score) || 0) / maxBm) * 100
        const vec = Math.max(0, Math.min(1, Number(c.vector_score) || 0)) * 100
        return (
          <div className="dl-chunk" key={i}>
            <span className="dl-chunk-id">passage {String(c.chunk_id ?? 'n/a')}</span>
            <span className="dl-bars">
              <i className="b-bm" style={{ width: `${bm.toFixed(0)}%` }} />
              <i className="b-vec" style={{ width: `${vec.toFixed(0)}%` }} />
            </span>
            <span className="dl-chunk-v">bm25 {(Number(c.bm25_score) || 0).toFixed(2)} · cos {(Number(c.vector_score) || 0).toFixed(2)}</span>
          </div>
        )
      })}
      <div className="dl-legend"><i className="b-bm" /> BM25 lexical &nbsp; <i className="b-vec" /> embedding cosine</div>
    </div>
  )
}

export function EngineRoom({ result, running }: { result?: ExplainResult; running: boolean }) {
  const debug = result?.retrieval_debug
  const gateTripped = result ? isIncidentGuardAbstention(result) : false
  const cragDecision = debug?.crag_decision
  const poorAbstain = cragDecision === 'POOR'
  const graniteEngaged = !!debug && !poorAbstain && typeof debug.timings_ms?.generation === 'number'
  const timings = debug?.timings_ms ?? {}

  const telem: ReactNode[] = STATIONS.map(() => null)
  if (result) {
    telem[0] = gateTripped
      ? <><b>Tripped.</b> Your question named a player, minute, or match. Those facts are in no rulebook, so the engine abstained at the gate.</>
      : <><b>Passed.</b> No player, minute, or match named, so this is a question about the Laws themselves.</>
    telem[1] = 'Off this run. Match context is a stub, standing by.'
    telem[2] = debug ? <ChunkBars chunks={debug.top_chunks ?? []} /> : (gateTripped ? 'Never consulted. The gate closed first.' : null)
    telem[3] = debug ? (
      <span>
        sufficiency reading <b>{(debug.crag_score ?? 0).toFixed(3)}</b> · verdict <b>{cragDecision ?? 'n/a'}</b>
        <CragRuler score={debug.crag_score ?? 0} />
      </span>
    ) : (gateTripped ? 'Never convened. The gate closed first.' : null)
    telem[4] = graniteEngaged ? (
      <span className="tg">Ran. granite3.1-dense:8b · no randomness · JSON enforced{typeof timings.generation === 'number' ? ` · written in ${(timings.generation / 1000).toFixed(1)}s` : ''}</span>
    ) : (
      <span className="tr">Did not run. The engine declined to answer first; nothing was made up.</span>
    )
    const nCit = result.rule_citations?.length ?? 0
    const nSteps = result.decision_steps?.length ?? 0
    const pct = Math.round((result.confidence || 0) * 100)
    const tbits = [
      typeof timings.retrieval === 'number' ? `retrieval ${timings.retrieval} ms` : null,
      typeof timings.total === 'number' ? `total ${(timings.total / 1000).toFixed(1)}s` : null,
    ].filter(Boolean).join(' · ')
    telem[5] = `Done. ${pct}% evidence · ${nCit} citation(s) · ${nSteps} reasoning step(s)${tbits ? ` · ${tbits}` : ''}`
  }

  const skip = (idx: number): boolean => {
    if (idx === 2 || idx === 3) return gateTripped
    if (idx === 4) return gateTripped || poorAbstain
    return false
  }

  const intro = running && !result
    ? 'Six steps turn a question into a cited answer. They are running now; real readings replace the preview as each step reports.'
    : result
      ? 'Six steps turn a question into a cited answer. The readings below are live, taken from this question exactly as the engine produced them.'
      : 'Six steps turn a question into a cited answer. Ask a question above and watch each step report real readings.'

  return (
    <details className="dl-engine" open={running || !!result}>
      <summary>
        How the answer was reached
        <span className="dl-engine-sum-tag">live readings</span>
      </summary>
      <div className="dl-engine-wrap">
        <p className="dl-engine-intro">{intro}</p>
        <div className={`dl-rail ${running && !result ? 'is-running' : ''}`}>
          <span className="dl-rail-ball" aria-hidden="true" />
          {STATIONS.map((s, i) => (
            <div key={s.numeral}>
              <div className={`dl-st ${skip(i) ? 'is-skip' : ''} ${running && !result ? 'is-wait' : ''}`} style={{ animationDelay: `${i * 0.28}s` }}>
                <div className="dl-node">{s.numeral}</div>
                <div className="dl-st-body">
                  <div className="dl-st-head">
                    <span className="dl-st-name">{s.name}</span>
                    <span className="dl-st-latin">{s.role}</span>
                    {s.ibm && <span className="dl-st-ibm">{s.ibm}</span>}
                  </div>
                  <div className="dl-st-desc">{s.desc}</div>
                  {telem[i] != null && <div className="dl-st-telem">{telem[i]}</div>}
                </div>
              </div>
              {poorAbstain && i === 3 && (
                <div className="dl-siding">
                  Stopped here. Evidence fell below 0.65, so Granite was never asked to write.
                  An honest "cannot say" beats a made-up answer.
                </div>
              )}
            </div>
          ))}
        </div>
        {result && (
          <div className="dl-engine-note">
            {gateTripped || poorAbstain
              ? 'IBM Granite was never asked to write an answer. An honest "not enough evidence" beats a confident guess.'
              : 'Every reading above is real, taken from this question. Nothing here is decorative.'}
          </div>
        )}
      </div>
    </details>
  )
}
