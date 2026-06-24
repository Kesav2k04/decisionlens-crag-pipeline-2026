import { useRef, useState } from 'react'
import { useMutation, useQuery } from '@tanstack/react-query'
import { explain, getConfig, getHealth, getMetrics } from './api/client'
import type { ExplainRequest, ExplainResult, Metrics } from './api/client'
import { Masthead } from './components/Masthead'
import { Lineage, Motif } from './components/Lineage'
import { InquiryDesk } from './components/InquiryDesk'
import { VerdictRecord } from './components/VerdictRecord'
import { EngineRoom } from './components/EngineRoom'
import './components/components.css'

interface Entry {
  id: number
  question: string
  result: ExplainResult
}

export default function App() {
  const config = useQuery({ queryKey: ['config'], queryFn: getConfig })
  const metrics = useQuery({ queryKey: ['metrics'], queryFn: getMetrics })
  const health = useQuery({ queryKey: ['health'], queryFn: getHealth, refetchInterval: 60_000 })

  const [mode, setMode] = useState<'fan' | 'analyst'>('fan')
  const [language, setLanguage] = useState('English')
  const [history, setHistory] = useState<Entry[]>([])
  const [pendingQ, setPendingQ] = useState<string | null>(null)
  const idRef = useRef(0)

  const mutation = useMutation({
    mutationFn: (req: ExplainRequest) => explain(req),
    onSuccess: (result, req) => {
      idRef.current += 1
      setHistory((h) => [...h, { id: idRef.current, question: req.question, result }].slice(-8))
      setPendingQ(null)
    },
  })

  const loading = mutation.isPending
  const latest = history[history.length - 1]
  const maxChars = config.data?.max_question_chars ?? 2000
  const languageCount = config.data?.languages?.length ?? 5

  const onAsk = (q: string) => {
    setPendingQ(q)
    mutation.reset()
    mutation.mutate({ question: q, mode, language })
  }

  return (
    <>
      <Masthead metrics={metrics.data} health={health.data} languageCount={languageCount} />

      <main className="shell">
        <Lineage />

        <InquiryDesk
          config={config.data}
          mode={mode}
          language={language}
          loading={loading}
          maxChars={maxChars}
          onAsk={onAsk}
          onModeChange={setMode}
          onLanguageChange={setLanguage}
        />

        <div className="section-rule">
          <span className="k">The Answer</span>
          <span className="n">
            {loading ? 'Reading the rulebook' : latest ? 'Latest answer' : 'Your answer appears here'}
          </span>
        </div>

        {loading && (
          <div className="dl-deliberating" role="status" aria-live="polite">
            <span className="dl-spinner" aria-hidden="true" />
            <div>
              <div className="dl-delib-t">Reading the rulebook</div>
              <div className="dl-delib-s">Granite is finding the passages that answer “{pendingQ}”</div>
            </div>
          </div>
        )}

        {mutation.isError && !loading && (
          <div className="dl-rec dl-rec-error" role="alert">
            <div className="dl-rec-head"><span className="dl-rec-head-t" style={{ color: 'var(--red)' }}>Engine notice</span></div>
            <p className="dl-rec-answer" style={{ marginTop: '0.8rem' }}>
              {(mutation.error as Error).message || 'The rule engine could not be reached.'}
            </p>
            <p className="dl-rec-foot" style={{ borderTop: 'none', marginTop: '0.4rem' }}>
              Check that the API is running (uvicorn api.main:app) and that Ollama is serving granite3.1-dense:8b.
            </p>
          </div>
        )}

        {!loading && !mutation.isError && latest && (
          <VerdictRecord question={latest.question} result={latest.result} index={latest.id} />
        )}

        {!loading && !latest && !mutation.isError && <AwaitingState />}

        <EngineRoom result={!loading ? latest?.result : undefined} running={loading} />

        {history.length > 1 && (
          <section aria-label="Earlier questions this session">
            <div className="section-rule">
              <span className="k">History</span>
              <span className="n">Earlier questions, this session</span>
            </div>
            <div className="dl-history">
              {history.slice(0, -1).reverse().map((e) => {
                const pct = Math.round((e.result.confidence || 0) * 100)
                return (
                  <details key={e.id}>
                    <summary>
                      <span className="dl-lgr-no">№ {e.id}</span>
                      <span className="dl-lgr-q" dir="auto">{e.question}</span>
                      <span className="dl-lgr-pct">{pct}% evidence</span>
                    </summary>
                    <div className="dl-lgr-a" dir="auto">{e.result.answer || 'No answer recorded.'}</div>
                  </details>
                )
              })}
            </div>
          </section>
        )}

        <Colophon metrics={metrics.data} />
      </main>
    </>
  )
}

function AwaitFeature({ title, body }: { title: string; body: string }) {
  return (
    <div className="dl-await-card">
      <div className="dl-await-card-t">{title}</div>
      <div className="dl-await-card-d">{body}</div>
    </div>
  )
}

function AwaitingState() {
  return (
    <div className="dl-await">
      <Motif name="whistle" size={48} className="dl-await-motif" />
      <div className="dl-await-t">Ask your first question</div>
      <p className="dl-await-s">
        Ask anything about VAR or referee decisions. The engine answers only from the official IFAB
        rulebook, quotes the exact passage, and says clearly when it cannot know.
      </p>
      <div className="dl-await-row">
        <AwaitFeature title="Backed by the rules" body="Every claim cites its Law, with the exact passage quoted." />
        <AwaitFeature title="Honest when unsure" body="It says 'not enough evidence' instead of guessing." />
        <AwaitFeature title="Fully transparent" body="You can see every step the engine took, just below." />
      </div>
    </div>
  )
}

function Colophon({ metrics }: { metrics?: Metrics }) {
  const run = metrics?.run_date_utc?.split('T')[0]
  return (
    <footer className="dl-footer">
      <div className="dl-fleuron">❦</div>
      <div className="dl-colo-t">Built with</div>
      <div className="dl-foot-badges">
        <span className="dl-fbadge"><b>IBM Granite</b> 3.1 · 8B</span>
        <span className="dl-fbadge"><b>IBM Docling</b> 2.97.0</span>
        <span className="dl-fbadge">Context Forge · MCP</span>
        <span className="dl-fbadge">BM25 + embeddings · RRF</span>
        <span className="dl-fbadge">CRAG self-correction</span>
      </div>
      {metrics && (
        <p className="dl-foot-note">
          {metrics.citation_accuracy_pct.toFixed(0)}% citation accuracy across {metrics.total_questions} test
          questions · {metrics.avg_latency_seconds.toFixed(1)}s per answer · {metrics.chunks_indexed} rule
          passages indexed{run ? ` · measured ${run}` : ''}.
        </p>
      )}
      <p className="dl-foot-note">
        Private inference via IBM Granite and Ollama on the demo server — questions are not sent to
        third-party chat APIs. The confidence score measures how well the rulebook covers the question,
        not whether the referee's call was right.
      </p>
    </footer>
  )
}
