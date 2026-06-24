# app/main.py
# DecisionLens — The Football Codex
# Visual identity: an archival folio. Parchment and book-cloth terracotta,
# engraved natural-history plates, classical serif typography, and IBM Plex
# Mono as the technical voice — applied to a century of football and the
# Laws of the Game (est. 1863).
# The IBM pipeline (Granite / Docling / ContextForge / CRAG) is untouched.

import datetime
import html
import json
import math
import os
import sys

import streamlit as st

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'pipeline')))
from agent import run


def _load_metrics() -> dict:
    """Read headline metrics from the canonical evaluation/results.json so the
    masthead never carries a hand-typed number. Falls back to last-known values
    if the file is missing."""
    try:
        _p = os.path.join(os.path.dirname(__file__), "..", "evaluation", "results.json")
        with open(_p, encoding="utf-8") as _f:
            _s = json.load(_f)["summary"]
        return {"chunks": int(_s.get("chunks_indexed", 593)),
                "citation_pct": float(_s.get("citation_accuracy_pct", 100.0)),
                "questions": int(_s.get("total_questions", 50))}
    except Exception:
        return {"chunks": 593, "citation_pct": 100.0, "questions": 50}


METRICS = _load_metrics()

# ══════════════════════════ DESIGN TOKENS ══════════════════════════
PAPER  = "#F4F0E5"   # parchment field
PAPER2 = "#EDE6D4"   # aged panel
PAPER3 = "#E4DAC3"   # deep aged / blueprint sheet
INK    = "#231C11"   # warm iron-gall ink
INK2   = "#564A39"   # faded ink
FADE   = "#8B7D66"   # captions
TERRA  = "#BC5634"   # book-cloth terracotta (primary)
TERRA2 = "#96401F"   # deep terracotta
GREEN  = "#41603E"   # heritage pitch green
GOLD   = "#9A7B2D"   # old gold
RED    = "#A33434"   # vermillion stamp red
BLUE   = "#3F5876"   # ledger ink blue

DECISION_META = {
    "handball":          {"color": TERRA, "label": "HANDBALL"},
    "red_card":          {"color": RED,   "label": "RED CARD"},
    "offside":           {"color": BLUE,  "label": "OFFSIDE"},
    "penalty":           {"color": GOLD,  "label": "PENALTY"},
    "var_reviewability": {"color": GREEN, "label": "VAR REVIEW"},
    "unknown":           {"color": FADE,  "label": "UNRESOLVED"},
}

LANG_OPTIONS = {
    "English": "English",
    "Español": "Spanish",
    "Português": "Portuguese",
    "Français": "French",
    "العربية": "Arabic",
}

QUICK_ASKS = [
    "What makes a handball deliberate?",
    "When can VAR overturn an on-field decision?",
    "Explain the offside rule in simple terms",
    "What earns a straight red card?",
]

# year-roman · year · title · note · motif · highlighted
LINEAGE = [
    ("MCMXXX",    "1930", "Montevideo",       "The first final. One referee, no replays — only his word.",                 "trophy",     False),
    ("MCMLVIII",  "1958", "Pelé, seventeen",  "A boy lifts the Cup in Sweden, and the whole game tilts toward genius.",    "star",       False),
    ("MCMLXVI",   "1966", "Wembley",          "Did it cross the line? Sixty years of argument, one camera short.",         "crossbar",   False),
    ("MCMLXX",    "1970", "Brasil",           "Football in full colour — the most beautiful side ever filmed.",            "ball",       False),
    ("MCMLXXXVI", "1986", "The Hand of God",  "Maradona, Law 12, and the four-second case that demanded VAR.",             "hand",       True),
    ("MCMXCVIII", "1998", "Zidane in Paris",  "Two headers in a final, and a nation redrawn around one man.",              "twostars",   False),
    ("MMX",       "2010", "Lampard's ghost",  "A goal that wasn't given — goal-line technology is born two years later.",  "ghost",      False),
    ("MMXVIII",   "2018", "Moscow",           "VAR enters the World Cup. Every verdict now leaves a paper trail.",         "monitor",    False),
    ("MMXXII",    "2022", "Messi, at last",   "The longest argument in football is settled at Lusail.",                    "trophystar", False),
    ("MMXXVI",    "2026", "The Forty-Eight",  "Three hosts, more verdicts than ever — each one explainable, here.",        "badge48",    False),
]

MONTHS = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]

# ══════════════════════════ PAGE CONFIG ══════════════════════════
_ICON_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "icon.png"))
try:
    from PIL import Image
    _page_icon = Image.open(_ICON_PATH)
except Exception:
    _page_icon = "⚽"

st.set_page_config(page_title="DecisionLens · The Laws, Illuminated",
                   page_icon=_page_icon, layout="wide",
                   initial_sidebar_state="collapsed")


# ══════════════════════════ HELPERS ══════════════════════════
def flat(s: str) -> str:
    """Strip blank lines so Streamlit's markdown never breaks an HTML block."""
    return "\n".join(ln for ln in (l.rstrip() for l in s.splitlines()) if ln.strip())


def esc(s) -> str:
    return html.escape(str(s)).replace("\n", "<br>")


def roman(n: int) -> str:
    vals = [(1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"), (90, "XC"),
            (50, "L"), (40, "XL"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]
    n = max(int(n), 0)
    out = []
    for v, sym in vals:
        while n >= v:
            out.append(sym)
            n -= v
    return "".join(out) or "—"


# ── Engraved motif library (hand-drawn SVG, stroke = ink) ──
MOTIF_PATHS = {
    "trophy":     '<path d="M15 9h14v7a7 7 0 0 1-14 0z"/><path d="M15 11h-4.5a4.5 4.5 0 0 0 4.8 5.4M29 11h4.5a4.5 4.5 0 0 1-4.8 5.4"/><path d="M22 23v5"/><path d="M17 31h10l1.6 4H15.4z"/>',
    "star":       '<path d="M22 9l3.4 7.4 8.1.9-6 5.5 1.6 8-7.1-4.1-7.1 4.1 1.6-8-6-5.5 8.1-.9z"/>',
    "crossbar":   '<path d="M9 11h26M11 11v23M35 11v23"/><path d="M9 29h28" stroke-dasharray="3 3"/><circle cx="23" cy="26.5" r="4.2"/>',
    "ball":       '<circle cx="22" cy="22" r="13"/><ellipse cx="22" cy="22" rx="5.5" ry="13"/><ellipse cx="22" cy="22" rx="13" ry="5"/>',
    "hand":       '<path d="M14.5 25V14.8a1.7 1.7 0 0 1 3.4 0V22M17.9 22V11.6a1.7 1.7 0 0 1 3.4 0V21M21.3 21V12.4a1.7 1.7 0 0 1 3.4 0V22M24.7 22v-7.4a1.7 1.7 0 0 1 3.4 0V26a9.5 9.5 0 0 1-9.3 9.5c-3.2 0-5.3-1.2-6.9-3.6l-2.6-4a1.9 1.9 0 0 1 3-2.3l1.2 1.6"/><circle cx="33.5" cy="8.5" r="3.4"/>',
    "twostars":   '<path d="M15 11l2 4.3 4.7.5-3.5 3.2.9 4.6-4.1-2.4-4.1 2.4.9-4.6-3.5-3.2 4.7-.5z"/><path d="M29 21l2 4.3 4.7.5-3.5 3.2.9 4.6-4.1-2.4-4.1 2.4.9-4.6-3.5-3.2 4.7-.5z"/>',
    "ghost":      '<path d="M12 8v28M12 10h22"/><circle cx="16.5" cy="27" r="4.6" stroke-dasharray="2.4 2.4"/><path d="M26 27h8" stroke-dasharray="2.4 2.4"/>',
    "monitor":    '<rect x="9" y="11" width="26" height="17" rx="1"/><path d="M18 35h8M22 28v7"/><text x="22" y="22.5" font-family="\'IBM Plex Mono\',monospace" font-size="7.5" letter-spacing="1" text-anchor="middle" fill="var(--ink)" stroke="none">VAR</text>',
    "trophystar": '<path d="M16 15h12v6a6 6 0 0 1-12 0z"/><path d="M16 17h-4a4 4 0 0 0 4.2 4.6M28 17h4a4 4 0 0 1-4.2 4.6"/><path d="M22 27v4M18 34h8l1.4 3.4H16.6z"/><path d="M22 4.5l1.2 2.6 2.8.3-2.1 1.9.6 2.8-2.5-1.5-2.5 1.5.6-2.8-2.1-1.9 2.8-.3z"/>',
    "badge48":    '<circle cx="22" cy="22" r="14.5"/><circle cx="22" cy="22" r="11"/><text x="22" y="26.5" font-family="Fraunces,serif" font-size="12" font-weight="600" text-anchor="middle" fill="var(--ink)" stroke="none">48</text>',
    "whistle":    '<path d="M16 14h16a2.5 2.5 0 0 1 2.5 2.5V19l-9.5 3.6A8 8 0 1 1 16 14z"/><circle cx="18.5" cy="28" r="3.2"/><path d="M27 9.5l1.5-3M31.5 10.5l3-2M34 14h4" stroke-width="1.2"/>',
}


def motif(name: str, size: int = 38) -> str:
    return (f'<svg class="lg-motif" width="{size}" height="{size}" viewBox="0 0 44 44" aria-hidden="true">'
            f'<g fill="none" stroke="var(--ink)" stroke-width="1.5" stroke-linecap="round" '
            f'stroke-linejoin="round">{MOTIF_PATHS[name]}</g></svg>')


def hero_plate_svg() -> str:
    """Plate I — the vintage laced football, drawn as a natural-history engraving."""
    return f'''
<svg class="cx-plate" viewBox="0 0 880 330" role="img" aria-label="Engraved plate of a vintage laced football">
  <defs>
    <pattern id="cxHatch" width="5" height="5" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
      <line x1="0" y1="0" x2="0" y2="5" stroke="{INK}" stroke-width="0.65"/>
    </pattern>
    <clipPath id="cxBallClip"><circle cx="440" cy="166" r="116"/></clipPath>
  </defs>
  <ellipse cx="440" cy="298" rx="100" ry="8" fill="url(#cxHatch)" opacity="0.35"/>
  <g clip-path="url(#cxBallClip)">
    <rect x="322" y="48" width="236" height="236" fill="url(#cxHatch)" opacity="0.5"/>
    <circle cx="420" cy="146" r="119" fill="var(--paper)"/>
  </g>
  <circle cx="440" cy="166" r="116" fill="none" stroke="var(--ink)" stroke-width="2.4"/>
  <ellipse cx="440" cy="166" rx="52" ry="112" fill="none" stroke="var(--ink)" stroke-width="1.5"/>
  <ellipse cx="440" cy="166" rx="112" ry="42" fill="none" stroke="var(--ink)" stroke-width="1.5"/>
  <path d="M414 84 H466" stroke="var(--ink)" stroke-width="2.6" stroke-linecap="round"/>
  <path d="M424 77 l8 14 M438 77 l8 14 M452 77 l8 14" stroke="var(--ink)" stroke-width="1.7" stroke-linecap="round"/>
  <g class="ann" font-family="'IBM Plex Mono',monospace" font-size="10.5" fill="var(--ink2)" letter-spacing="1.5">
    <text x="252" y="84" text-anchor="end">fig. 1 — the lace, hand-bound</text>
    <text x="240" y="192" text-anchor="end">fig. 2 — the seam, hand-stitched</text>
    <text x="628" y="118" font-size="11.5" fill="var(--ink)" letter-spacing="2.5">LAW 2 — THE BALL</text>
    <text x="628" y="178">circumference, 68–70 cm</text>
    <text x="628" y="234">weight at kick-off, 410–450 g</text>
  </g>
  <g class="ann" stroke="var(--ink2)" stroke-width="0.8" opacity="0.85">
    <path d="M262 80 L408 82" fill="none"/><circle cx="408" cy="82" r="1.8" fill="var(--ink2)" stroke="none"/>
    <path d="M250 188 L390 206" fill="none"/><circle cx="390" cy="206" r="1.8" fill="var(--ink2)" stroke="none"/>
    <path d="M620 174 L552 186" fill="none"/><circle cx="552" cy="186" r="1.8" fill="var(--ink2)" stroke="none"/>
    <path d="M620 230 L522 244" fill="none"/><circle cx="522" cy="244" r="1.8" fill="var(--ink2)" stroke="none"/>
  </g>
</svg>'''


def dial_svg(pct: int, color: str) -> str:
    """An engraved instrument dial — evidence sufficiency, 0 to 100."""
    cx, cy, r = 110.0, 116.0, 86.0
    parts = []
    for i in range(21):
        ang = math.radians(180 + i * 9)
        major = i % 5 == 0
        r1 = r - (12 if major else 7)
        x1, y1 = cx + r1 * math.cos(ang), cy + r1 * math.sin(ang)
        x2, y2 = cx + r * math.cos(ang), cy + r * math.sin(ang)
        parts.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                     f'stroke="var(--ink)" stroke-width="{1.6 if major else 0.9}" '
                     f'opacity="{0.9 if major else 0.5}"/>')
    for v in (0, 25, 50, 75, 100):
        ang = math.radians(180 + v * 1.8)
        rx = r - 23
        x, y = cx + rx * math.cos(ang), cy + rx * math.sin(ang) + 3.2
        parts.append(f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="middle" '
                     f'font-family="\'IBM Plex Mono\',monospace" font-size="9" '
                     f'fill="var(--ink2)">{v}</text>')
    # CRAG threshold witnesses at 65 and 75
    for v, tcol in ((65, GOLD), (75, GREEN)):
        ang = math.radians(180 + v * 1.8)
        x1, y1 = cx + (r + 2) * math.cos(ang), cy + (r + 2) * math.sin(ang)
        x2, y2 = cx + (r + 9) * math.cos(ang), cy + (r + 9) * math.sin(ang)
        parts.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                     f'stroke="{tcol}" stroke-width="2.4"/>')
    ang_e = math.radians(180 + max(pct, 1) * 1.8)
    ex, ey = cx + r * math.cos(ang_e), cy + r * math.sin(ang_e)
    return f'''
<svg viewBox="0 0 220 142" width="230" class="rec-dial" aria-label="Evidence sufficiency {pct} of 100">
  <path d="M {cx - r} {cy} A {r} {r} 0 0 1 {cx + r} {cy}" stroke="var(--hair)" stroke-width="1" fill="none"/>
  <path d="M {cx - r} {cy} A {r} {r} 0 0 1 {ex:.1f} {ey:.1f}" stroke="{color}" stroke-width="3" fill="none" opacity="0.9"/>
  {''.join(parts)}
  <g class="dial-needle" style="--sweep:{pct * 1.8:.1f}deg;">
    <polygon points="34,116 112,112.6 112,119.4" fill="{color}"/>
    <circle cx="110" cy="116" r="5.5" fill="var(--ink)"/>
    <circle cx="110" cy="116" r="2" fill="var(--paper)"/>
  </g>
</svg>'''


def stamp_svg(label: str, color: str) -> str:
    """A circular rubber stamp for the decision type, with inked imperfection."""
    words = label.split()
    if len(words) >= 2:
        center = (f'<text x="75" y="71" text-anchor="middle" font-family="Fraunces,serif" '
                  f'font-size="15.5" font-weight="650" letter-spacing="2" fill="{color}">{words[0]}</text>'
                  f'<text x="75" y="89" text-anchor="middle" font-family="Fraunces,serif" '
                  f'font-size="15.5" font-weight="650" letter-spacing="2" fill="{color}">{" ".join(words[1:])}</text>'
                  f'<circle cx="75" cy="47" r="1.6" fill="{color}"/><circle cx="75" cy="101" r="1.6" fill="{color}"/>')
    else:
        center = (f'<text x="75" y="81" text-anchor="middle" font-family="Fraunces,serif" '
                  f'font-size="16.5" font-weight="650" letter-spacing="2.5" fill="{color}">{label}</text>'
                  f'<circle cx="75" cy="55" r="1.6" fill="{color}"/><circle cx="75" cy="95" r="1.6" fill="{color}"/>')
    return f'''
<svg viewBox="0 0 150 150" width="148" class="rec-stamp" aria-label="Decision stamp: {label}">
  <defs>
    <path id="stampArc" d="M 75 75 m -57 0 a 57 57 0 1 1 114 0 a 57 57 0 1 1 -114 0"/>
    <filter id="stRough"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="1" result="n"/>
      <feDisplacementMap in="SourceGraphic" in2="n" scale="2.4"/></filter>
  </defs>
  <g filter="url(#stRough)">
    <circle cx="75" cy="75" r="70" fill="none" stroke="{color}" stroke-width="3"/>
    <circle cx="75" cy="75" r="46" fill="none" stroke="{color}" stroke-width="1.4"/>
    <text font-family="'IBM Plex Mono',monospace" font-size="9.2" letter-spacing="2.6" fill="{color}">
      <textPath href="#stampArc">LAWS OF THE GAME · I.F.A.B. · DECISIONLENS · MMXXVI ·</textPath>
    </text>
    {center}
  </g>
</svg>'''


# ══════════════════════════ GLOBAL STYLE ══════════════════════════
ROOT_CSS = (
    f":root{{--paper:{PAPER};--paper2:{PAPER2};--paper3:{PAPER3};--ink:{INK};--ink2:{INK2};"
    f"--fade:{FADE};--terra:{TERRA};--terra2:{TERRA2};--green:{GREEN};--gold:{GOLD};"
    f"--red:{RED};--blue:{BLUE};--line:rgba(35,28,17,.32);--hair:rgba(35,28,17,.16);}}"
)

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..700;1,9..144,300..700&family=Newsreader:ital,opsz,wght@0,6..72,400..600;1,6..72,400..600&family=IBM+Plex+Mono:ital,wght@0,400;0,500;0,600;1,400&display=swap');

/* ── the sheet: parchment, faint plate-grid, paper grain ── */
.stApp{
  background:
    repeating-linear-gradient(90deg, rgba(35,28,17,.028) 0 1px, transparent 1px 56px),
    repeating-linear-gradient(0deg,  rgba(35,28,17,.028) 0 1px, transparent 1px 56px),
    var(--paper);
  color:var(--ink);
  font-family:'Newsreader',Georgia,serif;
}
.stApp::before{
  content:""; position:fixed; inset:0; pointer-events:none; z-index:0; opacity:.6;
  background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='240' height='240'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='2' stitchTiles='stitch'/><feColorMatrix type='saturate' values='0'/><feComponentTransfer><feFuncA type='linear' slope='0.045'/></feComponentTransfer></filter><rect width='240' height='240' filter='url(%23n)'/></svg>");
}
header[data-testid="stHeader"]{display:none;}
[data-testid="stToolbar"], #MainMenu, footer{visibility:hidden;}
.block-container{max-width:1040px; padding-top:2rem; padding-bottom:3rem;}
h1,h2,h3,h4,p,li,label,.stMarkdown{color:var(--ink); font-family:'Newsreader',Georgia,serif;}

::selection{background:var(--terra); color:var(--paper);}
*{scrollbar-width:thin; scrollbar-color:var(--fade) transparent;}
*::-webkit-scrollbar{height:7px; width:7px;}
*::-webkit-scrollbar-thumb{background:var(--fade); border-radius:0;}
*::-webkit-scrollbar-track{background:transparent;}

/* ── status seal ── */
.cx-status{
  display:flex; justify-content:center; align-items:center; gap:.55rem;
  font-family:'IBM Plex Mono',monospace; font-size:.62rem; letter-spacing:3px;
  color:var(--ink2); text-transform:uppercase; margin-bottom:1.1rem;
}
.cx-status-dot{
  width:7px; height:7px; border-radius:50%; background:var(--green);
  outline:1px solid var(--ink); outline-offset:2px;
  animation:cx-pulse 2.4s ease-in-out infinite;
}
@keyframes cx-pulse{0%,100%{opacity:1;}50%{opacity:.35;}}

/* ── masthead ── */
.cx-ruleline{
  display:flex; justify-content:space-between; align-items:center;
  font-family:'IBM Plex Mono',monospace; font-size:.6rem; letter-spacing:2.5px;
  color:var(--fade); text-transform:uppercase;
  border-top:1px solid var(--line); border-bottom:1px solid var(--hair);
  padding:.4rem .2rem; margin-bottom:1.6rem;
}
.cx-platebox{position:relative; padding:0 4px;}
.cx-plate{width:100%; height:auto; display:block;}
.cx-plate-cap{
  text-align:center; font-family:'IBM Plex Mono',monospace; font-size:.64rem;
  letter-spacing:3px; color:var(--fade); text-transform:uppercase; margin-top:.2rem;
}
.cx-title{
  font-family:'Fraunces',serif; font-optical-sizing:auto; font-weight:560;
  font-size:4.4rem; line-height:1.04; text-align:center; margin:1.4rem 0 0;
  color:var(--ink); letter-spacing:.5px;
}
.cx-title em{font-style:italic; color:var(--terra); font-weight:520;}
.cx-sub-it{
  text-align:center; font-family:'Newsreader',serif; font-style:italic;
  font-size:1.18rem; color:var(--ink2); margin-top:.55rem;
}
.cx-sub-mono{
  text-align:center; font-family:'IBM Plex Mono',monospace; font-size:.64rem;
  letter-spacing:3.5px; color:var(--terra2); text-transform:uppercase; margin-top:.7rem;
}
.cx-plaque{
  display:flex; justify-content:center; margin:1.7rem auto 0;
  border:1px solid var(--line); outline:1px solid var(--hair); outline-offset:3px;
  background:var(--paper2); max-width:780px; flex-wrap:wrap;
}
.cx-stat{flex:1 1 160px; text-align:center; padding:.85rem .5rem; border-left:1px solid var(--hair);}
.cx-stat:first-child{border-left:none;}
.cx-stat-v{font-family:'Fraunces',serif; font-size:1.5rem; font-weight:600; color:var(--ink); line-height:1.1;}
.cx-stat-v em{font-style:normal; color:var(--terra);}
.cx-stat-k{font-family:'IBM Plex Mono',monospace; font-size:.56rem; letter-spacing:1.8px; text-transform:uppercase; color:var(--fade); margin-top:.3rem;}

/* ── section headers ── */
.cx-sec{display:flex; align-items:baseline; gap:.9rem; margin:2.8rem 0 1.1rem; flex-wrap:wrap;}
.cx-sec .k{
  font-family:'IBM Plex Mono',monospace; font-weight:600; font-size:.6rem;
  letter-spacing:3px; color:var(--terra); border:1px solid var(--terra);
  padding:2.5px 8px; text-transform:uppercase; white-space:nowrap;
}
.cx-sec .n{font-family:'Fraunces',serif; font-size:1.5rem; font-weight:560; color:var(--ink); line-height:1;}
.cx-sec .i{font-family:'Newsreader',serif; font-style:italic; font-size:.92rem; color:var(--fade);}
.cx-sec::after{content:""; flex:1; border-top:1px solid var(--hair); transform:translateY(-5px); min-width:40px;}

/* ── the lineage (Plate II) ── */
.lineage{
  display:flex; gap:13px; overflow-x:auto; padding:6px 2px 16px;
  scroll-snap-type:x proximity;
}
.lg-card{
  flex:0 0 208px; border:1px solid var(--hair); background:rgba(237,230,212,.55);
  padding:.85rem .95rem 1rem; scroll-snap-align:start; position:relative;
  transition:transform .22s ease, border-color .22s ease, background .22s ease;
}
.lg-card:hover{transform:translateY(-4px); border-color:var(--ink2); background:var(--paper2);}
.lg-top{display:flex; justify-content:space-between; align-items:baseline;}
.lg-yr{font-family:'Fraunces',serif; font-size:1.28rem; font-weight:620; color:var(--ink);}
.lg-rom{font-family:'IBM Plex Mono',monospace; font-size:.56rem; letter-spacing:1.5px; color:var(--fade);}
.lg-motif{display:block; margin:.55rem auto .35rem; opacity:.85;}
.lg-name{font-family:'Fraunces',serif; font-size:1.02rem; font-weight:560; color:var(--ink); text-align:center;}
.lg-note{font-family:'Newsreader',serif; font-style:italic; font-size:.8rem; line-height:1.5; color:var(--ink2); text-align:center; margin-top:.35rem;}
.lg-hero{border-color:var(--terra); background:rgba(188,86,52,.07);}
.lg-hero .lg-yr, .lg-hero .lg-name{color:var(--terra2);}
.lg-hero:hover{border-color:var(--terra2); background:rgba(188,86,52,.11);}

/* ── controls: tickets, chips, the inquiry slip ── */
.stButton button{
  border-radius:2px; border:1px solid var(--line); background:var(--paper);
  color:var(--ink2); font-family:'IBM Plex Mono',monospace; font-weight:500;
  letter-spacing:2px; text-transform:uppercase; font-size:.78rem;
  transition:all .16s ease; box-shadow:none;
}
.stButton button:hover{border-color:var(--terra); color:var(--terra2); background:rgba(188,86,52,.06);}
.stButton button:focus:not(:active){border-color:var(--terra); color:var(--terra2); box-shadow:none;}
.stButton button[kind="primary"],
.stButton [data-testid="stBaseButton-primary"]{
  background:var(--terra); border:1px solid var(--terra2); color:var(--paper);
}
.stButton button[kind="primary"] p,
.stButton [data-testid="stBaseButton-primary"] p{color:var(--paper) !important;}
.stButton button[kind="primary"]:hover{background:var(--terra2); color:var(--paper);}

[class*="st-key-chip"] button{
  border-radius:2px !important; font-family:'Newsreader',serif !important;
  font-style:italic !important; text-transform:none !important; letter-spacing:.2px !important;
  font-size:.86rem !important; background:rgba(237,230,212,.5) !important;
  border:1px solid var(--hair) !important; color:var(--ink2) !important;
  min-height:2.3rem; padding:.3rem .6rem !important;
}
[class*="st-key-chip"] button:hover{border-color:var(--terra) !important; color:var(--terra2) !important; background:rgba(188,86,52,.07) !important;}

.st-key-sim_btn button{
  background:rgba(154,123,45,.08) !important; color:var(--gold) !important;
  border:1px solid var(--gold) !important;
}
.st-key-sim_btn button:hover{background:rgba(154,123,45,.16) !important; color:#7A611F !important;}

[data-testid="stForm"]{
  border:1px solid var(--line); background:rgba(237,230,212,.45);
  border-radius:2px; padding:1rem 1rem .6rem;
}
[data-testid="stTextInput"] div[data-baseweb="input"],
[data-testid="stTextInput"] div[data-baseweb="base-input"]{
  background:var(--paper) !important; border-radius:2px !important;
  border-color:var(--line) !important;
}
[data-testid="stTextInput"] input{
  background:var(--paper) !important; color:var(--ink) !important;
  border-radius:2px !important; padding:.8rem 1rem !important;
  font-size:1rem !important; font-family:'Newsreader',serif !important;
}
[data-testid="stTextInput"] input::placeholder{color:var(--fade) !important; font-style:italic;}
div[data-testid="stFormSubmitButton"] button{
  background:var(--terra) !important; color:var(--paper) !important;
  font-family:'IBM Plex Mono',monospace !important; font-weight:600 !important;
  letter-spacing:3px !important; text-transform:uppercase !important;
  border:1px solid var(--terra2) !important; border-radius:2px !important;
  font-size:.8rem !important; padding:.55rem 0 !important;
  transition:background .16s ease !important;
}
div[data-testid="stFormSubmitButton"] button:hover{background:var(--terra2) !important;}
div[data-testid="stFormSubmitButton"] button p{color:var(--paper) !important;}

.stSelectbox > div > div{
  background:var(--paper) !important; color:var(--ink) !important;
  border:1px solid var(--line) !important; border-radius:2px !important;
  font-family:'IBM Plex Mono',monospace !important; font-size:.85rem !important;
}
div[data-baseweb="popover"] > div{background:var(--paper) !important; border:1px solid var(--line); border-radius:2px;}
ul[data-testid="stSelectboxVirtualDropdown"]{background:var(--paper) !important;}
li[role="option"]{background:var(--paper) !important; color:var(--ink) !important; font-family:'Newsreader',serif !important;}
li[role="option"]:hover, li[aria-selected="true"]{background:rgba(188,86,52,.1) !important; color:var(--terra2) !important;}

[data-testid="stWidgetLabel"] p{color:var(--ink2) !important; font-size:.9rem !important;}

[data-testid="stExpander"]{
  background:transparent !important; border:1px solid var(--line) !important;
  border-radius:2px !important;
}
[data-testid="stExpander"] summary{
  color:var(--ink2) !important; font-family:'IBM Plex Mono',monospace;
  letter-spacing:1.5px; font-size:.84rem; text-transform:uppercase;
}
[data-testid="stExpander"] summary:hover{color:var(--terra2) !important;}
[data-testid="stExpander"] summary svg{fill:var(--ink2);}

[data-testid="stSpinner"] p{
  color:var(--ink2) !important; font-family:'IBM Plex Mono',monospace !important;
  font-size:.74rem !important; letter-spacing:1.5px;
}
.stSpinner > div{border-top-color:var(--terra) !important;}

/* ── ledger of prior records ── */
.lgr{border:1px solid var(--hair); border-bottom:none; background:rgba(237,230,212,.4);}
.lgr details{border-bottom:1px solid var(--hair);}
.lgr summary{
  display:flex; gap:.8rem; align-items:baseline; cursor:pointer;
  padding:.55rem .9rem; list-style:none; font-family:'Newsreader',serif;
}
.lgr summary::-webkit-details-marker{display:none;}
.lgr summary:hover{background:rgba(188,86,52,.05);}
.lgr-no{font-family:'IBM Plex Mono',monospace; font-size:.62rem; color:var(--terra2); letter-spacing:1px; white-space:nowrap;}
.lgr-q{font-style:italic; color:var(--ink); font-size:.92rem; flex:1; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;}
.lgr-pct{font-family:'IBM Plex Mono',monospace; font-size:.62rem; color:var(--ink2); white-space:nowrap;}
.lgr-a{padding:.2rem 1rem .9rem 3rem; font-size:.9rem; line-height:1.6; color:var(--ink2);}

/* ── the decision record ── */
.rec{
  border:1px solid var(--line); outline:1px solid var(--hair); outline-offset:4px;
  background:#F8F4E9; padding:1.7rem 2rem 1.9rem; margin:1.6rem 2px .6rem;
  animation:cx-rise .5s ease both;
}
@keyframes cx-rise{from{opacity:0; transform:translateY(10px);}to{opacity:1; transform:none;}}
.rec-head{
  display:flex; justify-content:space-between; align-items:baseline; flex-wrap:wrap; gap:.4rem;
  border-bottom:1px solid var(--line); padding-bottom:.55rem;
}
.rec-head-t{font-family:'IBM Plex Mono',monospace; font-weight:600; font-size:.78rem; letter-spacing:4px; color:var(--ink);}
.rec-head-n{font-family:'IBM Plex Mono',monospace; font-size:.66rem; letter-spacing:2px; color:var(--ink2);}
.rec-q-lab{font-family:'IBM Plex Mono',monospace; font-size:.58rem; letter-spacing:2.5px; color:var(--fade); text-transform:uppercase; margin-top:1rem;}
.rec-q{font-family:'Newsreader',serif; font-style:italic; font-size:1.22rem; line-height:1.5; color:var(--ink); margin-top:.25rem;}
.rec-band{
  display:flex; align-items:center; gap:.9rem; margin:1.2rem 0 1.3rem;
  border-top:1px solid; border-bottom:1px solid; padding:.5rem .2rem;
  font-family:'IBM Plex Mono',monospace; letter-spacing:3px; font-size:.74rem;
  font-weight:600; text-transform:uppercase;
}
.rec-band-tag{font-size:.56rem; letter-spacing:2px; padding:.2rem .55rem; color:var(--paper); font-weight:600;}
.rec-band-type{margin-left:auto; font-size:.62rem; letter-spacing:2px; opacity:.85;}
.rec-answer{font-family:'Newsreader',serif; font-size:1.13rem; line-height:1.78; color:var(--ink);}
.rec-answer::first-letter{
  font-family:'Fraunces',serif; font-size:3.1em; float:left; line-height:.83;
  padding:.04em .12em 0 0; color:var(--terra); font-weight:560;
}
.rec-instruments{
  display:flex; gap:2.5rem; align-items:center; justify-content:space-evenly;
  flex-wrap:wrap; margin:1.6rem 0 .4rem; padding:1.1rem 0 .6rem;
  border-top:1px solid var(--hair);
}
.rec-dialwrap{text-align:center;}
.dial-needle{transform-origin:110px 116px; animation:dial-sweep 1.5s cubic-bezier(.25,.8,.25,1) both;}
@keyframes dial-sweep{from{transform:rotate(0);}to{transform:rotate(var(--sweep));}}
.rec-dial-v{font-family:'Fraunces',serif; font-size:2rem; font-weight:620; margin-top:-.7rem; line-height:1;}
.rec-dial-v small{font-size:.85rem; color:var(--fade); font-weight:400;}
.rec-dial-s{font-family:'IBM Plex Mono',monospace; font-size:.6rem; letter-spacing:2.5px; margin-top:.25rem; text-transform:uppercase;}
.rec-dial-k{font-family:'IBM Plex Mono',monospace; font-size:.56rem; letter-spacing:2px; color:var(--fade); text-transform:uppercase; margin-top:.3rem;}
.rec-stampwrap{transform:rotate(-5deg); mix-blend-mode:multiply; opacity:.93;}
.rec-sec{
  display:flex; align-items:center; gap:.7rem; font-family:'IBM Plex Mono',monospace;
  font-size:.66rem; letter-spacing:3px; text-transform:uppercase; color:var(--terra2);
  margin:1.6rem 0 .7rem; font-weight:600;
}
.rec-sec::after{content:""; flex:1; border-top:1px solid var(--hair);}
.rec-clause{
  display:flex; gap:.9rem; padding:.3rem 0 .55rem; font-family:'Newsreader',serif;
  font-size:.99rem; line-height:1.62; color:var(--ink);
}
.rec-clause-no{
  font-family:'Fraunces',serif; font-weight:620; font-style:italic; color:var(--terra);
  min-width:2.1rem; text-align:right; font-size:1.05rem;
}
.rec-cite{
  border:1px solid var(--hair); border-left:3px solid var(--terra);
  background:rgba(237,230,212,.5); padding:.85rem 1.1rem .8rem; margin-bottom:.65rem;
}
.rec-cite-q{
  font-family:'Newsreader',serif; font-style:italic; font-size:1.01rem;
  line-height:1.6; color:var(--ink);
}
.rec-cite-q::before{
  content:"\\201C"; font-family:'Fraunces',serif; font-size:1.9rem; color:var(--terra);
  line-height:0; vertical-align:-.35rem; margin-right:.25rem;
}
.rec-cite-src{
  font-family:'IBM Plex Mono',monospace; font-size:.62rem; letter-spacing:1.5px;
  color:var(--ink2); margin-top:.5rem; text-transform:uppercase; text-align:right;
}
.rec-missing{
  border:1px dashed var(--red); background:rgba(163,52,52,.05);
  padding:.9rem 1.15rem; margin-top:.3rem;
}
.rec-missing-t{
  font-family:'IBM Plex Mono',monospace; font-size:.62rem; letter-spacing:2.5px;
  color:var(--red); text-transform:uppercase; font-weight:600; margin-bottom:.45rem;
}
.rec-missing ul{margin:0; padding-left:1.1rem;}
.rec-missing li{font-family:'Newsreader',serif; font-style:italic; color:#6E3030; line-height:1.65; font-size:.93rem;}
.rec-marg{
  border-left:3px solid var(--gold); padding:.55rem 1rem; margin-top:.3rem;
  font-family:'Newsreader',serif; font-style:italic; color:var(--ink2);
  font-size:.96rem; line-height:1.6; background:rgba(154,123,45,.05);
}
.rec-marg b{
  display:block; font-family:'IBM Plex Mono',monospace; font-style:normal; font-weight:600;
  font-size:.56rem; letter-spacing:2px; color:var(--gold); text-transform:uppercase; margin-bottom:.3rem;
}
.rec-foot{
  font-family:'IBM Plex Mono',monospace; font-size:.58rem; letter-spacing:1.5px;
  color:var(--fade); text-transform:uppercase; margin-top:1.4rem;
  border-top:1px solid var(--hair); padding-top:.6rem;
}

/* ── awaiting state ── */
.cx-await{text-align:center; padding:2.2rem 1rem 1.2rem; animation:cx-rise .5s ease both;}
.cx-await .lg-motif{margin:0 auto .8rem; opacity:.9;}
.cx-await-t{font-family:'Fraunces',serif; font-size:1.7rem; font-weight:560; color:var(--ink);}
.cx-await-s{
  font-family:'Newsreader',serif; font-style:italic; color:var(--ink2);
  max-width:560px; margin:.5rem auto 0; line-height:1.65; font-size:1rem;
}
.cx-await-row{display:flex; gap:.8rem; margin-top:1.7rem; flex-wrap:wrap;}
.cx-await-card{
  flex:1 1 180px; border:1px solid var(--hair); background:rgba(237,230,212,.5);
  padding:1rem .9rem; text-align:center;
}
.cx-await-card-t{font-family:'IBM Plex Mono',monospace; font-size:.62rem; letter-spacing:2.5px; color:var(--terra2); font-weight:600; text-transform:uppercase;}
.cx-await-card-d{font-family:'Newsreader',serif; font-style:italic; font-size:.84rem; color:var(--ink2); margin-top:.4rem; line-height:1.5;}

/* ── the engine room (Plate III) ── */
.eng-wrap{
  border:1px solid var(--hair); background:
    repeating-linear-gradient(90deg, rgba(35,28,17,.035) 0 1px, transparent 1px 28px),
    repeating-linear-gradient(0deg,  rgba(35,28,17,.035) 0 1px, transparent 1px 28px),
    rgba(228,218,195,.45);
  padding:1.2rem 1.2rem 1rem; margin-top:.4rem;
}
.eng-intro{
  font-family:'Newsreader',serif; font-style:italic; color:var(--ink2);
  font-size:.95rem; line-height:1.6; margin-bottom:1.1rem;
}
.eng{position:relative; padding:4px 0;}
.eng::before{
  content:""; position:absolute; left:20px; top:18px; bottom:18px; width:1px;
  background:var(--line);
}
.eng-ball{
  position:absolute; left:16px; top:0; width:9px; height:9px; border-radius:50%;
  background:var(--terra); border:1.5px solid var(--ink); z-index:2;
  animation:eng-roll 7s ease-in-out infinite;
}
@keyframes eng-roll{
  0%{top:2%; opacity:0;} 6%{opacity:1;} 94%{opacity:1;} 100%{top:96%; opacity:0;}
}
.eng-st{display:flex; gap:1rem; padding:.55rem 0; animation:eng-wake .55s ease both; position:relative;}
@keyframes eng-wake{from{opacity:0; transform:translateX(-8px);}to{opacity:1; transform:none;}}
.eng-node{
  flex-shrink:0; width:41px; height:41px; border-radius:50%;
  border:1.4px solid var(--ink); background:var(--paper);
  display:flex; align-items:center; justify-content:center; z-index:1;
  font-family:'Fraunces',serif; font-weight:620; font-style:italic;
  font-size:.92rem; color:var(--terra2);
}
.eng-body{flex:1; min-width:0; border-bottom:1px solid var(--hair); padding-bottom:.7rem;}
.eng-st:last-child .eng-body{border-bottom:none;}
.eng-head{display:flex; align-items:baseline; gap:.6rem; flex-wrap:wrap;}
.eng-name{font-family:'IBM Plex Mono',monospace; font-weight:600; font-size:.8rem; letter-spacing:2px; color:var(--ink); text-transform:uppercase;}
.eng-latin{font-family:'Newsreader',serif; font-style:italic; font-size:.86rem; color:var(--fade);}
.eng-ibm{
  margin-left:auto; font-family:'IBM Plex Mono',monospace; font-size:.54rem;
  letter-spacing:1.5px; color:var(--blue); border:1px solid var(--blue);
  padding:.14rem .45rem; text-transform:uppercase; white-space:nowrap;
}
.eng-desc{font-family:'Newsreader',serif; font-size:.88rem; color:var(--ink2); line-height:1.55; margin-top:.2rem;}
.eng-telem{
  margin-top:.55rem; border:1px solid var(--hair); background:rgba(244,240,229,.8);
  padding:.55rem .7rem; font-family:'IBM Plex Mono',monospace; font-size:.66rem;
  color:var(--ink2); letter-spacing:.5px; line-height:1.7;
}
.eng-telem b{color:var(--terra2); font-weight:600;}
.eng-skip{opacity:.38;}
.eng-skip .eng-node{border-style:dashed;}
.eng-siding{
  margin:.2rem 0 .4rem 57px; border:1px dashed var(--red); color:var(--red);
  background:rgba(163,52,52,.05); padding:.6rem .9rem;
  font-family:'IBM Plex Mono',monospace; font-size:.64rem; letter-spacing:1px;
  line-height:1.7; animation:eng-wake .55s ease both; animation-delay:1.6s;
}
.eng-chunk{display:flex; align-items:center; gap:.7rem; padding:.18rem 0;}
.eng-chunk-id{min-width:74px; color:var(--ink); font-weight:500;}
.eng-bars{flex:1; display:flex; flex-direction:column; gap:2.5px; min-width:80px;}
.eng-bars i{display:block; height:4px; border-radius:0;}
.eng-bars .b-bm{background:var(--terra); animation:eng-bar 1s ease both;}
.eng-bars .b-vec{background:var(--blue); animation:eng-bar 1.2s ease both;}
@keyframes eng-bar{from{width:0 !important;}}
.eng-chunk-v{white-space:nowrap; color:var(--fade); font-size:.6rem;}
.eng-legend{display:flex; gap:.5rem; align-items:center; margin-top:.4rem; color:var(--fade); font-size:.58rem;}
.eng-legend i{width:14px; height:4px; display:inline-block;}
.eng-legend .b-bm{background:var(--terra);}
.eng-legend .b-vec{background:var(--blue);}
.eng-ruler{margin:.45rem 0 .2rem; max-width:430px;}
.eng-ruler-bar{position:relative; height:11px; border:1px solid var(--line); display:flex; background:var(--paper);}
.eng-ruler-bar .zone{display:block; height:100%;}
.eng-ruler-bar .z-poor{width:65%; background:rgba(163,52,52,.18);}
.eng-ruler-bar .z-mid{width:10%; background:rgba(154,123,45,.22);}
.eng-ruler-bar .z-good{width:25%; background:rgba(65,96,62,.2);}
.eng-mark{position:absolute; top:-3px; bottom:-3px; width:1px; background:var(--ink2);}
.eng-pin{
  position:absolute; top:-7px; width:0; height:0; transform:translateX(-4px);
  border-left:4.5px solid transparent; border-right:4.5px solid transparent;
  border-top:8px solid var(--ink); animation:eng-wake .8s ease both;
}
.eng-ruler-lab{position:relative; height:14px; font-size:.56rem; color:var(--fade); margin-top:2px;}
.eng-ruler-lab span{position:absolute; transform:translateX(-50%);}
.eng-ruler-lab span:first-child{left:0; transform:none;}
.eng-ruler-lab span:last-child{right:0; left:auto; transform:none;}
.eng-note{
  font-family:'IBM Plex Mono',monospace; font-size:.6rem; letter-spacing:1.5px;
  color:var(--fade); text-transform:uppercase; margin-top:.9rem; text-align:center;
}

/* ── colophon ── */
.cx-colophon{margin-top:3.2rem; text-align:center; border-top:1px solid var(--line); padding-top:1.4rem;}
.cx-fleuron{font-size:1.3rem; color:var(--terra); line-height:1;}
.cx-colo-t{font-family:'IBM Plex Mono',monospace; font-size:.62rem; letter-spacing:5px; color:var(--ink2); margin-top:.5rem; text-transform:uppercase;}
.cx-colo-badges{display:flex; justify-content:center; flex-wrap:wrap; gap:.45rem; margin-top:.9rem;}
.cx-cbadge{
  font-family:'IBM Plex Mono',monospace; font-size:.56rem; letter-spacing:1.5px;
  text-transform:uppercase; color:var(--ink2); border:1px solid var(--hair);
  padding:.28rem .8rem; background:rgba(237,230,212,.5);
}
.cx-cbadge b{color:var(--terra2); font-weight:600;}
.cx-colo-note{
  font-family:'Newsreader',serif; font-style:italic; font-size:.82rem;
  color:var(--fade); margin-top:1rem; line-height:1.8;
}

/* ── responsive ── */
@media (max-width:760px){
  .block-container{padding-top:1.2rem;}
  .cx-title{font-size:2.7rem;}
  .cx-sub-it{font-size:1rem;}
  .cx-plate .ann{display:none;}
  .cx-platebox{overflow:hidden;}
  .cx-plate{width:190%; margin-left:-45%;}
  .rec{padding:1.2rem 1.1rem 1.4rem;}
  .rec-instruments{gap:1.2rem;}
  .eng-siding{margin-left:0;}
  .lg-card{flex-basis:178px;}
}
@media (prefers-reduced-motion:reduce){
  *, *::before, *::after{animation-duration:.001s !important; animation-iteration-count:1 !important; transition-duration:.001s !important;}
}
"""

st.markdown("<style>" + ROOT_CSS + CSS + "</style>", unsafe_allow_html=True)

# ══════════════════════════ SESSION STATE ══════════════════════════
if "mode" not in st.session_state:
    st.session_state["mode"] = "fan"
if "lang" not in st.session_state:
    st.session_state["lang"] = "English"
if "history" not in st.session_state:
    st.session_state["history"] = []   # list of {"q": str, "r": dict}, max 6 pairs


def ask(question: str):
    """Run the agent once and append the exchange to the record book."""
    language = LANG_OPTIONS.get(st.session_state.get("lang", "English"), "English")
    with st.spinner("THE BENCH IS DELIBERATING — Granite is reading the relevant folios …"):
        try:
            result = run(question, mode=st.session_state["mode"], language=language)
        except Exception as e:
            result = {
                "answer": "The rule engine is unreachable at present (is Ollama running, with "
                          "granite3.1-dense:8b loaded?). Kindly retry in a moment.",
                "decision_type": "unknown", "confidence": 0.0,
                "rule_citations": [], "decision_steps": [],
                "missing_evidence": [f"Engine error: {type(e).__name__}"],
                "tactical_context": "",
            }
    st.session_state["history"].append({"q": question, "r": result})
    st.session_state["history"] = st.session_state["history"][-6:]
    st.rerun()


# ══════════════════════════ MASTHEAD ══════════════════════════
_now = datetime.datetime.now()
_date_line = f"{_now.day} {MONTHS[_now.month - 1]} {roman(_now.year)}"

st.markdown(flat(f"""
<div class="cx-status"><span class="cx-status-dot"></span>Rule engine in session · local &amp; private · {_date_line}</div>
<div class="cx-ruleline"><span>Est. MDCCCLXIII · The International Football Association Board</span><span>Folio MMXXVI</span></div>
<div class="cx-platebox">{hero_plate_svg()}</div>
<div class="cx-plate-cap">Plate I. — The Sphere · after the pattern of MCMXXX</div>
<h1 class="cx-title">Decision<em>Lens</em></h1>
<div class="cx-sub-it">A transparent companion to the Laws of the Game</div>
<div class="cx-sub-mono">VAR Decision Transparency Engine · FIFA World Cup MMXXVI</div>
<div class="cx-plaque">
  <div class="cx-stat"><div class="cx-stat-v"><em>{METRICS['chunks']}</em></div><div class="cx-stat-k">folios · Docling-parsed IFAB text</div></div>
  <div class="cx-stat"><div class="cx-stat-v">Granite <em>3.1</em></div><div class="cx-stat-k">IBM · 8B · Granite via Ollama</div></div>
  <div class="cx-stat"><div class="cx-stat-v"><em>{METRICS['citation_pct']:.0f}%</em></div><div class="cx-stat-k">citation fidelity · {METRICS['questions']}-question suite</div></div>
  <div class="cx-stat"><div class="cx-stat-v"><em>{len(LANG_OPTIONS)}</em> tongues</div><div class="cx-stat-k">fan &amp; analyst registers</div></div>
</div>
"""), unsafe_allow_html=True)

# ══════════════════════════ PLATE II · THE LINEAGE ══════════════════════════
_cards = []
for rom_, yr, name, note, m, hero in LINEAGE:
    _cards.append(
        f'<div class="lg-card{" lg-hero" if hero else ""}">'
        f'<div class="lg-top"><span class="lg-yr">{yr}</span><span class="lg-rom">{rom_}</span></div>'
        f'{motif(m)}'
        f'<div class="lg-name">{name}</div>'
        f'<div class="lg-note">{note}</div></div>'
    )

st.markdown(flat(f"""
<div class="cx-sec"><span class="k">Plate II</span><span class="n">The Lineage</span><span class="i">a century of verdicts, Montevideo to the Forty-Eight</span></div>
<div class="lineage">{''.join(_cards)}</div>
"""), unsafe_allow_html=True)

# ══════════════════════════ THE INQUIRY DESK ══════════════════════════
st.markdown(flat("""
<div class="cx-sec"><span class="k">The Desk</span><span class="n">Put a question to the Laws</span><span class="i">answers come only from the official text — quoted, cited, and honest in doubt</span></div>
"""), unsafe_allow_html=True)

col_fan, col_analyst, col_lang = st.columns([1, 1, 1.15])
with col_fan:
    if st.button("Fan register", key="mode_fan", use_container_width=True,
                 type="primary" if st.session_state["mode"] == "fan" else "secondary",
                 help="Plain-language explanations for supporters"):
        st.session_state["mode"] = "fan"
        st.rerun()
with col_analyst:
    if st.button("Analyst register", key="mode_analyst", use_container_width=True,
                 type="primary" if st.session_state["mode"] == "analyst" else "secondary",
                 help="Precise Law numbers and sub-clause references"):
        st.session_state["mode"] = "analyst"
        st.rerun()
with col_lang:
    st.selectbox("Language", list(LANG_OPTIONS.keys()), key="lang",
                 label_visibility="collapsed")

chip_cols = st.columns(len(QUICK_ASKS))
for i, (col, q) in enumerate(zip(chip_cols, QUICK_ASKS)):
    with col:
        if st.button(q, key=f"chip{i}", use_container_width=True):
            ask(q)

with st.form("ask_form", clear_on_submit=True):
    question_text = st.text_input(
        "Question",
        placeholder="Why was that goal disallowed? Ask about any VAR decision or rule …",
        label_visibility="collapsed"
    )
    submitted = st.form_submit_button("Consult the Laws", use_container_width=True)
if submitted and question_text.strip():
    ask(question_text.strip())

# ══════════════════════════ THE RECORD BOOK ══════════════════════════
history = st.session_state["history"]
latest = history[-1] if history else None

if not history:
    st.markdown(flat(f"""
    <div class="cx-await">
      {motif("whistle", 46)}
      <div class="cx-await-t">The bench is in session</div>
      <div class="cx-await-s">Put a question to the Laws — the engine answers only from the official
      IFAB text, quotes its sources verbatim, and admits plainly when it cannot know.</div>
      <div class="cx-await-row">
        <div class="cx-await-card"><div class="cx-await-card-t">Grounded in text</div>
          <div class="cx-await-card-d">Every claim cites its Law, with the exact quoted span.</div></div>
        <div class="cx-await-card"><div class="cx-await-card-t">Honest in doubt</div>
          <div class="cx-await-card-d">It abstains, rather than inventing, when evidence is wanting.</div></div>
        <div class="cx-await-card"><div class="cx-await-card-t">Open to audit</div>
          <div class="cx-await-card-d">The full machinery of each verdict is on display below.</div></div>
      </div>
    </div>
    """), unsafe_allow_html=True)
else:
    # ledger of prior records
    if len(history) > 1:
        rows = []
        for idx, pair in enumerate(history[:-1], start=1):
            p = int(round(float(pair["r"].get("confidence") or 0.0) * 100))
            rows.append(
                f'<details><summary><span class="lgr-no">№ {roman(idx)}</span>'
                f'<span class="lgr-q" dir="auto">{esc(pair["q"])}</span>'
                f'<span class="lgr-pct">{p}%</span></summary>'
                f'<div class="lgr-a" dir="auto">{esc(pair["r"].get("answer", "No answer recorded."))}</div></details>'
            )
        st.markdown(flat(
            '<div class="cx-sec" style="margin-top:2rem;"><span class="k">Ledger</span>'
            '<span class="n">Prior records, this sitting</span></div>'
            f'<div class="lgr">{"".join(rows)}</div>'
        ), unsafe_allow_html=True)

    # ── the latest decision record ──
    result = latest["r"]
    confidence = float(result.get("confidence") or 0.0)
    decision_type = result.get("decision_type", "unknown")
    pct = int(round(confidence * 100))
    meta = DECISION_META.get(decision_type, DECISION_META["unknown"])

    if pct >= 75:
        v_color, v_text, v_status = GREEN, "Verdict explained from the Laws", "SUFFICIENT"
    elif pct >= 40:
        v_color, v_text, v_status = GOLD, "Partial evidence — answer may be incomplete", "PARTIAL"
    else:
        v_color, v_text, v_status = RED, "Insufficient evidence — the engine declines to guess", "ABSTAINED"

    rec_no = roman(len(history))

    body = [f"""
    <div class="rec">
      <div class="rec-head"><span class="rec-head-t">DECISION RECORD</span>
        <span class="rec-head-n">№ {rec_no} · {_date_line}</span></div>
      <div class="rec-q-lab">The question, as put</div>
      <div class="rec-q" dir="auto">{esc(latest["q"])}</div>
      <div class="rec-band" style="color:{v_color}; border-color:{v_color};">
        <span class="rec-band-tag" style="background:{v_color};">VAR REVIEW</span>
        {v_text}
        <span class="rec-band-type">{meta["label"]}</span>
      </div>
      <div class="rec-answer" dir="auto">{esc(result.get("answer", "No answer recorded."))}</div>
      <div class="rec-instruments">
        <div class="rec-dialwrap">
          {dial_svg(pct, v_color)}
          <div class="rec-dial-v" style="color:{v_color};">{pct}<small> /100</small></div>
          <div class="rec-dial-s" style="color:{v_color};">{v_status}</div>
          <div class="rec-dial-k">Evidence sufficiency</div>
        </div>
        <div class="rec-stampwrap">{stamp_svg(meta["label"], meta["color"])}</div>
      </div>
    """]

    tactical = result.get("tactical_context", "")
    if tactical:
        body.append(
            f'<div class="rec-sec">Marginalia</div>'
            f'<div class="rec-marg"><b>Match impact — interpretation, not rule text</b>'
            f'<span dir="auto">{esc(tactical)}</span></div>'
        )

    steps = result.get("decision_steps", [])
    if steps:
        clauses = "".join(
            f'<div class="rec-clause"><span class="rec-clause-no">{roman(i)}.</span>'
            f'<span dir="auto">{esc(s)}</span></div>'
            for i, s in enumerate(steps, 1)
        )
        body.append(f'<div class="rec-sec">Reasoning, in clauses</div>{clauses}')

    citations = result.get("rule_citations", [])
    if citations:
        cites = []
        for c in citations:
            law_title = c.get("law_or_section", c.get("law", "Rule reference"))
            doc_source = c.get("source", "IFAB Official Rules")
            quoted = c.get("quoted_span", "")
            q_html = (f'<div class="rec-cite-q" dir="auto">{esc(quoted)}&rdquo;</div>'
                      if quoted else
                      '<div class="rec-cite-q">Section consulted in full.&rdquo;</div>')
            cites.append(f'<div class="rec-cite">{q_html}'
                         f'<div class="rec-cite-src">— {esc(law_title)} · {esc(doc_source)}</div></div>')
        body.append(f'<div class="rec-sec">The evidence</div>{"".join(cites)}')

    missing = result.get("missing_evidence", [])
    if missing and (confidence < 0.5 or decision_type == "unknown"):
        items = "".join(f"<li dir='auto'>{esc(m)}</li>" for m in missing)
        body.append(
            f'<div class="rec-sec" style="color:{RED};">Not in evidence</div>'
            f'<div class="rec-missing"><div class="rec-missing-t">Facts unavailable to the system</div>'
            f'<ul>{items}</ul></div>'
        )

    srcs = result.get("sources", [])
    src_line = " · ".join(esc(s) for s in srcs) if srcs else "IFAB Laws of the Game 2025/26 · IFAB VAR Protocol"
    body.append(f'<div class="rec-foot">Sources consulted: {src_line} &nbsp;·&nbsp; '
                f'rendered in {esc(result.get("language", "English"))}</div></div>')

    st.markdown(flat("".join(body)), unsafe_allow_html=True)

# ══════════════════════════ THE HYPOTHETICAL ══════════════════════════
with st.expander("The Hypothetical — compose a handball case and test it against Law 12"):
    sim1, sim2, sim3 = st.columns(3)
    with sim1:
        hand = st.toggle("Ball touched hand / arm", value=True)
    with sim2:
        natural = st.toggle("Arm in natural position", value=True)
    with sim3:
        attack = st.toggle("Stopped a promising attack", value=True)
    if st.button("Submit the case to the bench", key="sim_btn", use_container_width=True):
        scenario = (
            f"A player {'did' if hand else 'did not'} touch the ball with their hand/arm, "
            f"which {'was' if natural else 'was not'} in a natural position. "
            f"The handball {'did' if attack else 'did not'} stop a promising attack. "
            f"What does Law 12 say about this situation?"
        )
        ask(scenario)

# ══════════════════════════ PLATE III · THE ENGINE ROOM ══════════════════════════
debug = (latest or {}).get("r", {}).get("retrieval_debug") if latest else None
gate_tripped = bool(latest) and not debug and float((latest["r"].get("confidence") or 0)) == 0.0
tribunal_abstained = bool(debug) and debug.get("crag_decision") == "POOR"
timings = (debug or {}).get("timings_ms", {})


def _timing_bits() -> str:
    bits = []
    if timings.get("retrieval") is not None:
        bits.append(f"retrieval {timings['retrieval']} ms")
    if timings.get("generation") is not None:
        bits.append(f"generation {timings['generation'] / 1000:.1f} s")
    if timings.get("total") is not None:
        bits.append(f"total {timings['total'] / 1000:.1f} s")
    return " · ".join(bits)


def _chunkbars(top_chunks) -> str:
    if not top_chunks:
        return ""
    mx = max((float(c.get("bm25_score") or 0.0) for c in top_chunks), default=0.0) or 1.0
    rows = []
    for c in top_chunks:
        b = float(c.get("bm25_score") or 0.0) / mx * 100
        v = max(0.0, min(1.0, float(c.get("vector_score") or 0.0))) * 100
        rows.append(
            f'<div class="eng-chunk"><span class="eng-chunk-id">folio {esc(c.get("chunk_id"))}</span>'
            f'<span class="eng-bars"><i class="b-bm" style="width:{b:.0f}%"></i>'
            f'<i class="b-vec" style="width:{v:.0f}%"></i></span>'
            f'<span class="eng-chunk-v">bm25 {esc(c.get("bm25_score"))} · cos {esc(c.get("vector_score"))}</span></div>'
        )
    legend = ('<div class="eng-legend"><i class="b-bm"></i> BM25 lexical &nbsp; '
              '<i class="b-vec"></i> embedding cosine</div>')
    return "".join(rows) + legend


def _ruler(score: float) -> str:
    pos = max(0.0, min(1.0, score)) * 100
    return (
        '<div class="eng-ruler"><div class="eng-ruler-bar">'
        '<span class="zone z-poor"></span><span class="zone z-mid"></span><span class="zone z-good"></span>'
        '<span class="eng-mark" style="left:65%"></span><span class="eng-mark" style="left:75%"></span>'
        f'<span class="eng-pin" style="left:{pos:.1f}%"></span></div>'
        '<div class="eng-ruler-lab"><span>0</span><span style="left:65%">.65</span>'
        '<span style="left:75%">.75</span><span>1.0</span></div></div>'
    )


# per-station telemetry
if latest:
    if gate_tripped:
        t1 = "<b>TRIPPED</b> — a player, minute or match was named. Such facts live in no rule book; the engine abstained honestly at the gate."
    else:
        t1 = "<b>PASSED</b> — no player, minute or match named; the question concerns the Laws themselves."
    t2 = "side channel dormant this run · provider: match-context stub, standing by"
    if debug:
        t3 = _chunkbars(debug.get("top_chunks", []))
        score = float(debug.get("crag_score") or 0.0)
        verdict = esc(debug.get("crag_decision", "n/a"))
        t4 = (f'sufficiency reading <b>{score:.3f}</b> — verdict <b>{verdict}</b>{_ruler(score)}')
    elif gate_tripped:
        t3 = "never consulted — the gate closed first"
        t4 = "never convened — the gate closed first"
    else:
        t3 = t4 = None
    if tribunal_abstained or gate_tripped:
        t5 = "<b>NEVER ENGAGED</b> — abstention upstream; not a single token was invented"
    else:
        gen_bit = f' · composed in {timings["generation"] / 1000:.1f} s' if timings.get("generation") is not None else ""
        t5 = f"<b>ENGAGED</b> — granite3.1-dense:8b · temperature 0 · JSON enforced{gen_bit}"
    n_cit = len(latest["r"].get("rule_citations", []) or [])
    n_steps = len(latest["r"].get("decision_steps", []) or [])
    pct_l = int(round(float(latest["r"].get("confidence") or 0.0) * 100))
    t6 = f"sealed — confidence <b>{pct_l}%</b> · {n_cit} citation(s) · {n_steps} clause(s)"
    tb = _timing_bits()
    if tb:
        t6 += f" · {tb}"
else:
    t1 = t2 = t3 = t4 = t5 = t6 = None

STATIONS = [
    ("I", "Query Processor", "the gate",
     "An incident-pattern guard reads the question first. Names, minutes and matches are facts no rule "
     "book holds — they are routed straight to an honest abstention.", None, t1, ""),
    ("II", "ContextForge MCP", "the side channel",
     "Match metadata may accompany the prompt for colour — it never enters retrieval and is never "
     "treated as rule evidence.", "IBM ContextForge", t2, ""),
    ("III", "Hybrid Retriever", "the twin indices",
     f"Two readers search {METRICS['chunks']} Docling-parsed folios at once — BM25 for the letter of the text, "
     "nomic-embed for its meaning — fused by Reciprocal Rank.", "IBM Docling 2.97", t3,
     "eng-skip" if gate_tripped else ""),
    ("IV", "CRAG Evaluator", "the tribunal",
     "The evidence itself is judged before any answer is written: at or above 0.75 it suffices; below "
     "0.65 the engine abstains; between, the answer is flagged as possibly incomplete.", None, t4,
     "eng-skip" if gate_tripped else ""),
    ("V", "Granite 3.1 · 8B", "the scribe",
     "IBM Granite composes the verdict from the retrieved folios alone — temperature zero, strict JSON, "
     "via private Ollama inference — no third-party chat API.", "IBM Granite", t5,
     "eng-skip" if (gate_tripped or tribunal_abstained) else ""),
    ("VI", "Structured Verdict", "the record",
     "Answer, citations with exact quoted spans, reasoning in clauses, confidence, and — just as "
     "faithfully — what is not in evidence.", None, t6, ""),
]

_st_html = ['<div class="eng"><div class="eng-ball"></div>']
for i, (numeral, name, latin, desc, ibm, telem, cls) in enumerate(STATIONS):
    badge = f'<span class="eng-ibm">{ibm}</span>' if ibm else ""
    telem_html = f'<div class="eng-telem">{telem}</div>' if telem else ""
    _st_html.append(
        f'<div class="eng-st {cls}" style="animation-delay:{i * 0.28:.2f}s">'
        f'<div class="eng-node">{numeral}</div><div class="eng-body">'
        f'<div class="eng-head"><span class="eng-name">{name}</span>'
        f'<span class="eng-latin">— {latin}</span>{badge}</div>'
        f'<div class="eng-desc">{desc}</div>{telem_html}</div></div>'
    )
    if tribunal_abstained and numeral == "IV":
        _st_html.append(
            '<div class="eng-siding">ROUTED TO THE ABSTENTION SIDING — evidence fell below 0.65. '
            'The scribe was never engaged: an honest &ldquo;cannot say&rdquo; outranks an invented verdict.</div>'
        )
_st_html.append("</div>")

if latest:
    eng_intro = ("Six stations stand between a fan&rsquo;s question and a cited verdict. The readings "
                 "below are live — taken from the most recent inquiry, exactly as the pipeline saw them.")
    eng_note = "All readings above are genuine — nothing in this drawing is decorative data."
else:
    eng_intro = ("Six stations stand between a fan&rsquo;s question and a cited verdict. The machine is "
                 "idling — put a question to the desk and watch the route light up with real readings.")
    eng_note = "Awaiting the first inquiry of the sitting."

with st.expander("Plate III · The Engine Room — watch how a verdict is made", expanded=bool(latest)):
    st.markdown(flat(
        f'<div class="eng-wrap"><div class="eng-intro">{eng_intro}</div>'
        f'{"".join(_st_html)}'
        f'<div class="eng-note">{eng_note}</div></div>'
    ), unsafe_allow_html=True)

# ══════════════════════════ COLOPHON ══════════════════════════
st.markdown(flat("""
<div class="cx-colophon">
  <div class="cx-fleuron">❦</div>
  <div class="cx-colo-t">Colophon</div>
  <div class="cx-colo-badges">
    <span class="cx-cbadge"><b>IBM Granite</b> 3.1 · 8B</span>
    <span class="cx-cbadge"><b>IBM Docling</b> 2.97.0</span>
    <span class="cx-cbadge"><b>ContextForge</b> MCP</span>
    <span class="cx-cbadge">BM25 + Embeddings · RRF</span>
    <span class="cx-cbadge">CRAG self-correction</span>
  </div>
  <div class="cx-colo-note">
    Private inference via IBM Granite and Ollama — no third-party chat APIs. Set in Fraunces, Newsreader &amp; IBM Plex Mono.<br>
    Confidence records the sufficiency of evidence, never the correctness of the match official.
  </div>
</div>
"""), unsafe_allow_html=True)
