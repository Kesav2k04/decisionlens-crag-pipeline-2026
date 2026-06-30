import { z } from 'zod'

/* ── Response schemas (tolerant; the model output can be sparse) ──────────────
   Mirrors pipeline/agent.py run(): 8 documented keys + optional retrieval_debug.
   retrieval_debug is ABSENT when the incident guard fires; its timings_ms omits
   `generation` on the POOR/abstain route. We never crash on a missing field. */

const CitationSchema = z
  .object({
    source: z.string().optional().default(''),
    law_or_section: z.string().optional(),
    law: z.string().optional(),
    quoted_span: z.string().optional().default(''),
  })
  .passthrough()

const TopChunkSchema = z
  .object({
    chunk_id: z.union([z.number(), z.string()]).optional(),
    bm25_score: z.number().optional().default(0),
    vector_score: z.number().optional().default(0),
  })
  .passthrough()

const RetrievalDebugSchema = z
  .object({
    crag_decision: z.string().optional(),
    crag_score: z.number().optional(),
    top_chunks: z.array(TopChunkSchema).optional().default([]),
    timings_ms: z
      .object({
        retrieval: z.number().optional(),
        generation: z.number().optional(),
        total: z.number().optional(),
      })
      .partial()
      .optional(),
  })
  .passthrough()

export const ExplainResultSchema = z
  .object({
    answer: z.string().optional().default(''),
    decision_type: z.string().optional().default('unknown'),
    rule_citations: z.array(CitationSchema).optional().default([]),
    // decision_steps should be flat strings; coerce defensively just in case.
    decision_steps: z
      .array(z.any())
      .optional()
      .default([])
      .transform((arr) => arr.map((s) => (typeof s === 'string' ? s : JSON.stringify(s)))),
    confidence: z.number().optional().default(0),
    missing_evidence: z.array(z.string()).optional().default([]),
    sources: z.array(z.string()).optional().default([]),
    tactical_context: z.string().optional().default(''),
    language: z.string().optional().default('English'),
    retrieval_debug: RetrievalDebugSchema.optional(),
    api_latency_seconds: z.number().optional(),
  })
  .passthrough()

export type Citation = z.infer<typeof CitationSchema>
export type TopChunk = z.infer<typeof TopChunkSchema>
export type RetrievalDebug = z.infer<typeof RetrievalDebugSchema>
export type ExplainResult = z.infer<typeof ExplainResultSchema>

export interface ApiConfig {
  modes: string[]
  languages: string[]
  quick_asks: string[]
  crag: { good_threshold: number; poor_threshold: number }
  decision_types: string[]
  max_question_chars: number
}

export interface Metrics {
  total_questions: number
  citation_accuracy_pct: number
  keyword_accuracy_pct: number
  abstention_accuracy_pct: number
  decision_type_accuracy_pct: number
  avg_latency_seconds: number
  avg_latency_generative_seconds?: number
  generative_questions?: number
  run_date_utc?: string
  machine: string
  model: string
  parser: string
  chunks_indexed: number
  source_counts: Record<string, number>
}

export interface Health {
  status: string
  ollama_reachable: boolean
  granite_model: string
  granite_loaded: boolean
  models: string[]
}

export interface ExplainRequest {
  question: string
  mode: 'fan' | 'analyst'
  language: string
  use_match_context?: boolean
}

/* ── fetch helpers ──────────────────────────────────────────────────────────────
   Dev: relative /api (Vite proxy). Production: set VITE_API_BASE to the FastAPI host. */

const API_BASE = (import.meta.env.VITE_API_BASE ?? '').replace(/\/$/, '')

function apiUrl(path: string): string {
  return `${API_BASE}${path}`
}

class ApiError extends Error {
  status: number
  constructor(status: number, message: string) {
    super(message)
    this.status = status
    this.name = 'ApiError'
  }
}

async function getJson<T>(path: string): Promise<T> {
  const res = await fetch(apiUrl(path), { headers: { Accept: 'application/json' } })
  if (!res.ok) throw new ApiError(res.status, await safeDetail(res))
  return (await res.json()) as T
}

async function safeDetail(res: Response): Promise<string> {
  try {
    const body = await res.json()
    return body?.detail ?? `HTTP ${res.status}`
  } catch {
    return `HTTP ${res.status}`
  }
}

export const getConfig = () => getJson<ApiConfig>('/api/config')
export const getMetrics = () => getJson<Metrics>('/api/metrics')
export const getHealth = () => getJson<Health>('/api/health')

export async function explain(req: ExplainRequest): Promise<ExplainResult> {
  const res = await fetch(apiUrl('/api/explain'), {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
    body: JSON.stringify(req),
  })
  if (!res.ok) throw new ApiError(res.status, await safeDetail(res))
  const raw = await res.json()
  return ExplainResultSchema.parse(raw)
}

export { ApiError }

/* ── derived helpers shared across views ──────────────────────────────────────── */

/* One vintage tone per decision family, chosen for hue separation and so each
   reads as stamp ink on parchment while carrying paper-coloured tag text at AA.
   Presentation only; the routing in the engine is untouched. */
export const DECISION_META: Record<string, { color: string; label: string }> = {
  handball: { color: '#9c4a2a', label: 'Handball' },        /* deep terracotta */
  red_card: { color: '#993030', label: 'Red card' },        /* vermillion */
  yellow_card: { color: '#b38f1a', label: 'Yellow card' },  /* gold/yellow */
  offside: { color: '#344e6b', label: 'Offside' },          /* ledger blue */
  penalty: { color: '#7a611f', label: 'Penalty' },          /* deep gold */
  var_reviewability: { color: '#3a5638', label: 'VAR review' }, /* heritage green */
  unknown: { color: '#6b5d47', label: 'General' },          /* faded ink */
}

/** Which rule-geometry schematic (if any) fits this question.
 *  Decided on the frontend from the question text + decision type, so the
 *  agent is never altered. Every scene is a labelled illustration of the rule,
 *  not a reconstruction of a real incident. */
export type SceneType = 'offside' | 'penalty' | 'corner' | 'var' | null

const CORNER_RE = /\bcorner[-\s]?kicks?\b/
const CORNER_LOOSE_RE = /\bcorner\b/

export function pickScene(question: string, decisionType: string): SceneType {
  const q = (question || '').toLowerCase()
  // Corner is detected from wording: corner questions classify under other
  // families in the agent, so the text is the reliable signal.
  if (CORNER_RE.test(q) || (CORNER_LOOSE_RE.test(q) && /\b(kick|arc|flag|quadrant|taken|whip|deliver)\b/.test(q))) {
    return 'corner'
  }
  if (decisionType === 'offside') return 'offside'
  if (decisionType === 'penalty') return 'penalty'
  if (decisionType === 'var_reviewability') return 'var'
  return null
}

/** Does this scene render as a 3D pitch schematic (offside/penalty/corner)?
 *  'var' renders as a flat scope diagram only. */
export function isPitchScene(s: SceneType): s is 'offside' | 'penalty' | 'corner' {
  return s === 'offside' || s === 'penalty' || s === 'corner'
}

/** Visual hint for quick-ask chips: what kind of diagram (if any) the answer may include.
 *  Based on question wording only; the engine still decides after retrieval. */
export type QuickAskVisualKind = '3d' | 'scope' | 'text'

export function getQuickAskVisualTag(question: string): { kind: QuickAskVisualKind; label: string } | null {
  const q = (question || '').toLowerCase()
  if (/\boffside\b/.test(q)) return { kind: '3d', label: '3D schematic' }
  if (CORNER_RE.test(q) || (CORNER_LOOSE_RE.test(q) && /\b(kick|arc|flag|quadrant|taken|whip|deliver)\b/.test(q))) {
    return { kind: '3d', label: '3D schematic' }
  }
  if (/\bpenalty\b/.test(q) && /\b(area|kick|box|spot|boundary)\b/.test(q)) {
    return { kind: '3d', label: '3D schematic' }
  }
  if (/\bvar\b|video assistant|four categories|review categories/.test(q)) {
    return { kind: 'scope', label: 'Scope diagram' }
  }
  if (/\bhandball\b/.test(q)) return { kind: 'text', label: 'Text only' }
  if (/\bred card\b|straight red\b/.test(q)) return { kind: 'text', label: 'Text only' }
  if (/\byellow card\b|caution\b/.test(q)) return { kind: 'text', label: 'Text only' }
  return null
}

/** Did the engine abstain at the incident guard? (no retrieval_debug, confidence 0) */
export function isIncidentGuardAbstention(r: ExplainResult): boolean {
  return !r.retrieval_debug && (r.confidence ?? 0) === 0
}
