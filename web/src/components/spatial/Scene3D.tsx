import { useMemo, useRef } from 'react'
import { Canvas, useFrame, useThree } from '@react-three/fiber'
import * as THREE from 'three'

/* Genuinely volumetric pitch schematics under stadium floodlights. These are
   labelled illustrations of the rule geometry, never a reconstruction of a real
   incident and never video: a raised turf fragment with thickness, standing
   figures that cast long shadows, a stitched ball, goal nets, and the broadcast
   offside wall. Procedural assets only (no external files).

   Reduced-motion / no-WebGL users never reach this component; SpatialInset shows
   the static 2D twin instead, so continuous animation is safe here. */

const PI = Math.PI
type SceneName = 'offside' | 'penalty' | 'corner'

const LINE = '#eef5ef'
const SOIL = '#3a2a1b'
const POST = '#eef4ef'
const NET = '#d8e4da'
const ATTACK = '#e0b357'   /* gilt jersey */
const DEFEND = '#5b7fb8'   /* ledger-blue jersey */
const NEUTRAL = '#cdd7cd'
const OFFSIDE = '#e8553a'
const SKIN = '#e4cfae'

/* ── procedural turf with mowing stripes ─────────────────────────────── */
function useTurf() {
  return useMemo(() => {
    const c = document.createElement('canvas')
    c.width = 640
    c.height = 448
    const g = c.getContext('2d')!
    const stripes = 9
    for (let i = 0; i < stripes; i++) {
      g.fillStyle = i % 2 === 0 ? '#2f7d4e' : '#296f44'
      g.fillRect((i * c.width) / stripes, 0, c.width / stripes + 1, c.height)
    }
    const img = g.getImageData(0, 0, c.width, c.height)
    for (let p = 0; p < img.data.length; p += 4) {
      const n = (Math.random() - 0.5) * 14
      img.data[p] += n
      img.data[p + 1] += n
      img.data[p + 2] += n
    }
    g.putImageData(img, 0, 0)
    const vg = g.createRadialGradient(c.width / 2, c.height / 2, 90, c.width / 2, c.height / 2, 430)
    vg.addColorStop(0, 'rgba(0,0,0,0)')
    vg.addColorStop(1, 'rgba(0,0,0,0.28)')
    g.fillStyle = vg
    g.fillRect(0, 0, c.width, c.height)
    const tex = new THREE.CanvasTexture(c)
    tex.anisotropy = 8
    tex.colorSpace = THREE.SRGBColorSpace
    return tex
  }, [])
}

/* the raised turf fragment: a soil block topped by a grass face */
function TurfSlab() {
  const tex = useTurf()
  return (
    <group>
      <mesh position={[0, -0.32, 0]}>
        <boxGeometry args={[18, 0.64, 12]} />
        <meshStandardMaterial color={SOIL} roughness={1} metalness={0} />
      </mesh>
      <mesh rotation-x={-PI / 2} position={[0, 0.002, 0]} receiveShadow>
        <planeGeometry args={[18, 12]} />
        <meshStandardMaterial map={tex} roughness={0.92} metalness={0} />
      </mesh>
    </group>
  )
}

/* a flat painted marking lying on the grass (kept unlit so it stays crisp) */
function Paint({ x = 0, z = 0, w, d, color = LINE, y = 0.02, opacity = 0.92 }:
  { x?: number; z?: number; w: number; d: number; color?: string; y?: number; opacity?: number }) {
  return (
    <mesh position={[x, y, z]} rotation-x={-PI / 2}>
      <planeGeometry args={[w, d]} />
      <meshBasicMaterial color={color} transparent opacity={opacity} />
    </mesh>
  )
}

function Arc({ x, z, inner, outer, start, length, color = LINE }:
  { x: number; z: number; inner: number; outer: number; start: number; length: number; color?: string }) {
  return (
    <mesh position={[x, 0.02, z]} rotation-x={-PI / 2}>
      <ringGeometry args={[inner, outer, 48, 1, start, length]} />
      <meshBasicMaterial color={color} transparent opacity={0.92} side={THREE.DoubleSide} />
    </mesh>
  )
}

function Spot({ x, z }: { x: number; z: number }) {
  return (
    <mesh position={[x, 0.025, z]} rotation-x={-PI / 2}>
      <circleGeometry args={[0.13, 24]} />
      <meshBasicMaterial color={LINE} />
    </mesh>
  )
}

/* a standing figure: it has height, so it throws a long shadow under the lights */
function Player({ x, z, color }: { x: number; z: number; color: string }) {
  return (
    <group position={[x, 0, z]}>
      <mesh position={[0, 0.03, 0]} rotation-x={-PI / 2}>
        <circleGeometry args={[0.34, 24]} />
        <meshBasicMaterial color={color} transparent opacity={0.22} />
      </mesh>
      <mesh position={[0, 0.52, 0]} castShadow>
        <cylinderGeometry args={[0.17, 0.24, 0.98, 14]} />
        <meshStandardMaterial color={color} roughness={0.62} metalness={0.04} />
      </mesh>
      <mesh position={[0, 1.16, 0]} castShadow>
        <sphereGeometry args={[0.17, 20, 20]} />
        <meshStandardMaterial color={SKIN} roughness={0.74} />
      </mesh>
    </group>
  )
}

/* a stitched ball: white panels with black pentagons, painted to a canvas */
function useBallTexture() {
  return useMemo(() => {
    const c = document.createElement('canvas')
    c.width = 256
    c.height = 256
    const g = c.getContext('2d')!
    g.fillStyle = '#f6f7f3'
    g.fillRect(0, 0, 256, 256)
    const pent = (cx: number, cy: number, r: number, rot: number) => {
      g.beginPath()
      for (let i = 0; i < 5; i++) {
        const a = rot + (i * 2 * Math.PI) / 5
        const px = cx + r * Math.cos(a)
        const py = cy + r * Math.sin(a)
        i === 0 ? g.moveTo(px, py) : g.lineTo(px, py)
      }
      g.closePath()
      g.fillStyle = '#1b1b1b'
      g.fill()
    }
    // a mid-latitude band of pentagons (poles left plain to hide UV pinching)
    const centers: [number, number, number][] = [
      [40, 96, 0.3], [104, 70, -0.4], [168, 96, 0.2], [232, 74, 0.5],
      [16, 160, -0.2], [80, 150, 0.4], [144, 168, -0.3], [208, 152, 0.25], [248, 168, -0.5],
      [56, 210, 0.1], [128, 220, -0.4], [196, 212, 0.3],
    ]
    for (const [cx, cy, rot] of centers) pent(cx, cy, 16, rot)
    g.strokeStyle = 'rgba(40,40,40,0.35)'
    g.lineWidth = 1.4
    for (const [cx, cy] of centers) {
      g.beginPath()
      g.arc(cx, cy, 23, 0, 2 * Math.PI)
      g.stroke()
    }
    const tex = new THREE.CanvasTexture(c)
    tex.colorSpace = THREE.SRGBColorSpace
    tex.anisotropy = 8
    return tex
  }, [])
}

function Ball({ x, z, r = 0.22 }: { x: number; z: number; r?: number }) {
  const tex = useBallTexture()
  const ref = useRef<THREE.Mesh>(null)
  useFrame((_, dt) => {
    if (ref.current) ref.current.rotation.y += dt * 0.35
  })
  return (
    <mesh ref={ref} position={[x, r, z]} castShadow>
      <sphereGeometry args={[r, 32, 32]} />
      <meshStandardMaterial map={tex} roughness={0.5} metalness={0.02} />
    </mesh>
  )
}

/* goal frame + a stylised net behind the line (line geometry reads as netting) */
function Goal({ x, zCenter = 0, span = 2.6, depth = 1.15, height = 1.55 }:
  { x: number; zCenter?: number; span?: number; depth?: number; height?: number }) {
  const zL = zCenter - span / 2
  const zR = zCenter + span / 2
  const xb = x - depth
  const netGeom = useMemo(() => {
    const pts: number[] = []
    const nz = 6
    const ny = 4
    for (let i = 0; i <= nz; i++) {
      const z = zL + ((zR - zL) * i) / nz
      pts.push(xb, 0, z, xb, height, z)
    }
    for (let j = 0; j <= ny; j++) {
      const y = (height * j) / ny
      pts.push(xb, y, zL, xb, y, zR)
    }
    for (let i = 0; i <= nz; i++) {
      const z = zL + ((zR - zL) * i) / nz
      pts.push(x, height, z, xb, height, z)
    }
    pts.push(x, 0, zL, xb, 0, zL, x, 0, zR, xb, 0, zR)
    const g = new THREE.BufferGeometry()
    g.setAttribute('position', new THREE.Float32BufferAttribute(pts, 3))
    return g
  }, [x, xb, zL, zR, height])

  return (
    <group>
      {[zL, zR].map((z, i) => (
        <mesh key={i} position={[x, height / 2, z]} castShadow>
          <cylinderGeometry args={[0.055, 0.055, height, 12]} />
          <meshStandardMaterial color={POST} roughness={0.5} />
        </mesh>
      ))}
      <mesh position={[x, height, zCenter]} rotation-x={PI / 2} castShadow>
        <cylinderGeometry args={[0.055, 0.055, span, 12]} />
        <meshStandardMaterial color={POST} roughness={0.5} />
      </mesh>
      <lineSegments geometry={netGeom}>
        <lineBasicMaterial color={NET} transparent opacity={0.4} />
      </lineSegments>
    </group>
  )
}

/* the broadcast offside wall: a translucent vertical plane rising from the line */
function OffsideWall({ x }: { x: number }) {
  return (
    <group>
      <Paint x={x} z={0} w={0.16} d={12} color={OFFSIDE} y={0.03} opacity={0.95} />
      <mesh position={[x, 1.15, 0]} rotation-y={PI / 2}>
        <planeGeometry args={[12, 2.3]} />
        <meshBasicMaterial color={OFFSIDE} transparent opacity={0.16} side={THREE.DoubleSide} depthWrite={false} />
      </mesh>
      <mesh position={[x, 2.3, 0]} rotation-y={PI / 2}>
        <planeGeometry args={[12, 0.04]} />
        <meshBasicMaterial color={OFFSIDE} transparent opacity={0.7} side={THREE.DoubleSide} />
      </mesh>
    </group>
  )
}

/* a corner flag with a slowly waving pennant */
function CornerFlag({ x, z }: { x: number; z: number }) {
  const flag = useRef<THREE.Group>(null)
  useFrame((s) => {
    if (flag.current) flag.current.rotation.y = Math.sin(s.clock.elapsedTime * 2.2) * 0.32
  })
  return (
    <group position={[x, 0, z]}>
      <mesh position={[0, 0.62, 0]} castShadow>
        <cylinderGeometry args={[0.035, 0.035, 1.24, 10]} />
        <meshStandardMaterial color="#e9eee9" roughness={0.5} />
      </mesh>
      <group ref={flag} position={[0.02, 1.05, 0]}>
        <mesh position={[0.22, 0, 0]} castShadow>
          <boxGeometry args={[0.44, 0.27, 0.02]} />
          <meshStandardMaterial color={OFFSIDE} roughness={0.6} side={THREE.DoubleSide} />
        </mesh>
      </group>
    </group>
  )
}

/* ── stadium floodlight: mast, lamp head, and a volumetric light cone ──── */
function LightCone({ from, to, radius, color }:
  { from: [number, number, number]; to: [number, number, number]; radius: number; color: string }) {
  const { position, quaternion, height } = useMemo(() => {
    const a = new THREE.Vector3(...from)
    const b = new THREE.Vector3(...to)
    const dir = new THREE.Vector3().subVectors(a, b) /* base->apex points to the lamp */
    const len = dir.length()
    const q = new THREE.Quaternion().setFromUnitVectors(new THREE.Vector3(0, 1, 0), dir.clone().normalize())
    const mid = new THREE.Vector3().addVectors(a, b).multiplyScalar(0.5)
    return { position: mid, quaternion: q, height: len }
  }, [from, to])
  return (
    <mesh position={position} quaternion={quaternion}>
      <coneGeometry args={[radius, height, 28, 1, true]} />
      <meshBasicMaterial color={color} transparent opacity={0.06} side={THREE.DoubleSide} blending={THREE.AdditiveBlending} depthWrite={false} />
    </mesh>
  )
}

function Floodlight({ x, z, aim = [0, 0, 0], cone = true }:
  { x: number; z: number; aim?: [number, number, number]; cone?: boolean }) {
  const h = 7.6
  const headTilt = Math.atan2(x, z) /* roughly face the pitch centre */
  return (
    <group position={[x, 0, z]}>
      <mesh position={[0, h / 2, 0]} castShadow>
        <cylinderGeometry args={[0.09, 0.16, h, 10]} />
        <meshStandardMaterial color="#26302c" roughness={0.7} metalness={0.3} />
      </mesh>
      <group position={[0, h, 0]} rotation-y={-headTilt}>
        <mesh position={[0, 0.2, 0.18]} rotation-x={0.5}>
          <boxGeometry args={[1.5, 0.7, 0.18]} />
          <meshStandardMaterial color="#1b231f" roughness={0.6} metalness={0.4} />
        </mesh>
        {[-0.5, -0.17, 0.17, 0.5].map((lx) =>
          [-0.16, 0.16].map((ly) => (
            <mesh key={`${lx}_${ly}`} position={[lx, 0.2 + ly, 0.28]} rotation-x={0.5}>
              <circleGeometry args={[0.11, 16]} />
              <meshStandardMaterial color="#fff3d0" emissive="#ffe9b0" emissiveIntensity={2.4} toneMapped={false} />
            </mesh>
          )),
        )}
      </group>
      {cone && <LightCone from={[0, h, 0]} to={[aim[0] - x, aim[1], aim[2] - z]} radius={3.4} color="#ffeec2" />}
    </group>
  )
}

/* the four corner floodlights, the front pair throwing visible shafts */
function Floodlights() {
  return (
    <group>
      <Floodlight x={-8.6} z={-6.6} aim={[-2, 0, 0]} />
      <Floodlight x={8.6} z={-6.6} aim={[2, 0, 0]} />
      <Floodlight x={-8.6} z={6.6} aim={[-2, 0, 1]} cone={false} />
      <Floodlight x={8.6} z={6.6} aim={[2, 0, 1]} cone={false} />
    </group>
  )
}

/* ── scenes ───────────────────────────────────────────────────────────── */

function OffsideScene() {
  return (
    <group>
      <TurfSlab />
      <Floodlights />
      <Paint x={-5} z={0} w={0.12} d={12} />
      <Goal x={-5} span={2.6} />
      <OffsideWall x={0} />
      <Player x={0} z={1.7} color={DEFEND} />
      <Player x={-1.5} z={-0.9} color={ATTACK} />
      <Player x={0.2} z={-2.6} color={DEFEND} />
      <Ball x={3.4} z={1.2} />
    </group>
  )
}

function PenaltyScene() {
  return (
    <group>
      <TurfSlab />
      <Floodlights />
      <Paint x={-5} z={0} w={0.12} d={12} />
      <Goal x={-5} span={2.6} />
      <Paint x={-1} z={0} w={0.1} d={7.2} />
      <Paint x={-3} z={3.6} w={4} d={0.1} />
      <Paint x={-3} z={-3.6} w={4} d={0.1} />
      <Paint x={-3.4} z={0} w={0.08} d={3.4} />
      <Paint x={-4.2} z={1.7} w={1.6} d={0.08} />
      <Paint x={-4.2} z={-1.7} w={1.6} d={0.08} />
      <Spot x={-2.4} z={0} />
      <Arc x={-2.4} z={0} inner={1.55} outer={1.65} start={PI * 0.62} length={PI * 0.76} />
      <Ball x={-2.4} z={0} />
      <Player x={-2.1} z={1.5} color={ATTACK} />
      <Player x={0.5} z={-1.3} color={DEFEND} />
      <Player x={-4.6} z={0} color={NEUTRAL} />
    </group>
  )
}

function CornerScene() {
  return (
    <group>
      <TurfSlab />
      <Floodlights />
      <Paint x={-5} z={-1} w={0.12} d={9} />
      <Paint x={-1} z={-5} w={8} d={0.12} />
      <Goal x={-5} zCenter={1.4} span={2.6} />
      <Arc x={-5} z={-5} inner={0.92} outer={1.02} start={0} length={PI / 2} />
      <CornerFlag x={-5} z={-5} />
      <Ball x={-4.35} z={-4.35} />
      <Player x={-3.4} z={0.4} color={ATTACK} />
      <Player x={-3.9} z={-0.6} color={DEFEND} />
      <Player x={-2.7} z={-1.6} color={ATTACK} />
    </group>
  )
}

const VIEWS: Record<SceneName, { target: [number, number, number]; radius: number; height: number; baseAngle: number }> = {
  offside: { target: [-1, 0.4, 0], radius: 9.4, height: 6.2, baseAngle: 2.2 },
  penalty: { target: [-2.6, 0.4, 0], radius: 9, height: 6.6, baseAngle: 2.5 },
  corner: { target: [-3.6, 0.4, -2.6], radius: 8.6, height: 6, baseAngle: 1.9 },
}

function AutoCamera({ view }: { view: SceneName }) {
  const { camera } = useThree()
  const t = useRef(0)
  const cfg = VIEWS[view]
  useFrame((_, delta) => {
    t.current += Math.min(delta, 0.05)
    const k = Math.min(1, t.current / 1.6)
    const ease = 1 - Math.pow(1 - k, 3)
    const r = cfg.radius * (1.5 - 0.5 * ease)
    const h = cfg.height * (1.35 - 0.35 * ease)
    const ang = cfg.baseAngle + t.current * 0.11
    camera.position.set(cfg.target[0] + r * Math.cos(ang), h, cfg.target[2] + r * Math.sin(ang))
    camera.lookAt(cfg.target[0], cfg.target[1], cfg.target[2])
  })
  return null
}

export function Scene3D({ scene }: { scene: SceneName }) {
  const cfg = VIEWS[scene]
  return (
    <Canvas
      dpr={[1, 1.75]}
      shadows
      camera={{ position: [cfg.target[0] + cfg.radius, cfg.height * 1.35, cfg.target[2] + cfg.radius], fov: 38, near: 0.1, far: 120 }}
      gl={{ antialias: true, powerPreference: 'high-performance' }}
      style={{ width: '100%', height: '100%' }}
    >
      <color attach="background" args={['#0a2418']} />
      <fog attach="fog" args={['#091f15', 17, 48]} />
      <hemisphereLight args={['#cfe6d2', '#0a1c14', 0.55]} />
      <ambientLight intensity={0.24} />
      <directionalLight
        position={[-7.5, 9, -5.5]}
        intensity={1.7}
        color="#fff1d4"
        castShadow
        shadow-mapSize-width={1024}
        shadow-mapSize-height={1024}
        shadow-camera-near={1}
        shadow-camera-far={42}
        shadow-camera-left={-13}
        shadow-camera-right={13}
        shadow-camera-top={13}
        shadow-camera-bottom={-13}
        shadow-bias={-0.0006}
      />
      <directionalLight position={[8, 7, -5]} intensity={0.55} color="#dbe9ff" />
      <AutoCamera view={scene} />
      {scene === 'offside' && <OffsideScene />}
      {scene === 'penalty' && <PenaltyScene />}
      {scene === 'corner' && <CornerScene />}
    </Canvas>
  )
}
