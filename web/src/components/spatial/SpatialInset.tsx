import { Component, Suspense, lazy, useEffect, useState } from 'react'
import type { ReactNode } from 'react'
import type { Citation, SceneType } from '../../api/client'
import { isPitchScene } from '../../api/client'
import { SpatialTwin2D } from './SpatialTwin2D'

const Scene3D = lazy(() => import('./Scene3D').then((m) => ({ default: m.Scene3D })))

const META: Record<Exclude<SceneType, null>, { title: string; note: string; summary: string }> = {
  offside: {
    title: 'Offside geometry',
    note: 'How the offside line is set. An illustration, not the actual incident.',
    summary:
      'The offside line runs across the pitch at the second-last defender. An attacker level with or behind it is onside; one beyond it is in an offside position.',
  },
  penalty: {
    title: 'Penalty-area geometry',
    note: 'The boundary that decides a penalty. An illustration, not the actual incident.',
    summary:
      'An offence inside the penalty area gives a penalty kick from the spot; the same offence just outside gives a direct free kick. The line is what decides.',
  },
  corner: {
    title: 'Corner-kick geometry',
    note: 'Where a corner kick is taken. An illustration, not the actual incident.',
    summary:
      'A corner kick is taken from inside the quarter-circle arc at the corner of the pitch, after the ball has wholly crossed the goal line off a defender.',
  },
  var: {
    title: 'What VAR can review',
    note: 'The four reviewable categories, shown as scope, not the actual incident.',
    summary:
      'VAR may review only four categories: goal / no goal, penalty / no penalty, direct red card (not a second caution), and mistaken identity.',
  },
}

function webglAvailable(): boolean {
  try {
    const c = document.createElement('canvas')
    return !!(window.WebGLRenderingContext && (c.getContext('webgl') || c.getContext('experimental-webgl')))
  } catch {
    return false
  }
}

function prefersReducedMotion(): boolean {
  return typeof window !== 'undefined' && !!window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches
}

class GLErrorBoundary extends Component<{ fallback: ReactNode; children: ReactNode }, { failed: boolean }> {
  state = { failed: false }
  static getDerivedStateFromError() {
    return { failed: true }
  }
  render() {
    return this.state.failed ? this.props.fallback : this.props.children
  }
}

export function SpatialInset({
  scene,
  citations,
}: {
  scene: Exclude<SceneType, null>
  citations: Citation[]
}) {
  const pitchScene = isPitchScene(scene) ? scene : null
  const [use3D, setUse3D] = useState(false)
  useEffect(() => {
    setUse3D(!!pitchScene && webglAvailable() && !prefersReducedMotion())
  }, [scene, pitchScene])

  const meta = META[scene]
  const citedLaw = citations[0]?.law_or_section || citations[0]?.law
  const twin = <SpatialTwin2D type={scene} />

  return (
    <section className="dl-inset" aria-label={`${meta.title}: schematic, not the actual incident`}>
      <div className="dl-rec-sec">Rule geometry</div>
      <div className="dl-inset-stage">
        <span className="dl-inset-flag">Schematic · not the actual incident</span>
        {use3D && pitchScene ? (
          <GLErrorBoundary fallback={twin}>
            <Suspense fallback={<span className="dl-inset-loading">Rendering schematic…</span>}>
              <div className="dl-inset-canvas" aria-hidden="true">
                <Scene3D scene={pitchScene} />
              </div>
            </Suspense>
          </GLErrorBoundary>
        ) : (
          twin
        )}
      </div>
      <p className="visually-hidden">{meta.summary}</p>
      <p className="dl-inset-cap">
        {meta.note}
        {citedLaw ? <> &nbsp;·&nbsp; showing {citedLaw}</> : null}
      </p>
    </section>
  )
}
