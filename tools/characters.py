#!/usr/bin/env python3
"""The Boost2Business team: six original flat 2D characters in one sticker style.

All six share one anatomy (head, ears, eyes, cheeks, smile, neck, shoulders) and
one outline colour, so they read as one family. Each gets its own skin tone,
hair, accent colour and one identifying prop. Nothing here imitates a known
character: they are simple geometric cartoons drawn for this site.

symbols() returns an SVG <defs> block with <symbol id="ch-<slug>">.
Animation hooks (CSS in the page): .eyes (blink), .wave (prop wiggle).
"""

INK = "#1b1446"
SW = 4  # outline width

CHARS = {
    # slug: skin, skin-shadow, hair, shirt, accent
    "chani": dict(skin="#e9b48f", shade="#d39a74", hair="#3b2416", shirt="#0f766e", acc="#2dd4bf", bg="#134e4a"),
    "dana":  dict(skin="#8d5a3b", shade="#764a30", hair="#17110f", shirt="#1d4ed8", acc="#60a5fa", bg="#1e3a8a"),
    "shira": dict(skin="#f2c9a5", shade="#dfb08b", hair="#5b3a22", shirt="#7e22ce", acc="#d8b4fe", bg="#4c1d95"),
    "noga":  dict(skin="#f6d2b8", shade="#e6b897", hair="#b4532a", shirt="#b45309", acc="#fbbf24", bg="#78350f"),
    "gal":   dict(skin="#c58c62", shade="#a9744f", hair="#231a14", shirt="#4338ca", acc="#a5b4fc", bg="#312e81"),
    "karin": dict(skin="#f3cfb4", shade="#e2b597", hair="#e8c77e", shirt="#7c3aed", acc="#67e8f9", bg="#3b0764"),
}


def _o(fill, extra=""):
    return f'fill="{fill}" stroke="{INK}" stroke-width="{SW}" stroke-linejoin="round" stroke-linecap="round"{extra}'


def base_back(c):
    return (f'<circle cx="100" cy="104" r="94" fill="{c["bg"]}"/>'
            f'<circle cx="100" cy="104" r="94" fill="none" stroke="{c["acc"]}" stroke-opacity=".55" stroke-width="3"/>')


def body(c, collar=True):
    s = (f'<path d="M34 204 C34 162 60 148 100 148 C140 148 166 162 166 204 Z" {_o(c["shirt"])}/>'
         f'<path d="M87 124 h26 v24 q-13 12 -26 0 Z" {_o(c["skin"])}/>'
         f'<path d="M89 140 q11 8 22 0" fill="none" stroke="{c["shade"]}" stroke-width="4" stroke-linecap="round"/>')
    if collar:
        s += f'<path d="M82 150 L100 168 L118 150" fill="none" stroke="{c["acc"]}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>'
    return s


def head(c, smile="open", brows=True):
    s = (f'<circle cx="62" cy="98" r="9" {_o(c["skin"])}/><circle cx="138" cy="98" r="9" {_o(c["skin"])}/>'
         f'<ellipse cx="100" cy="92" rx="38" ry="41" {_o(c["skin"])}/>')
    s += ('<g class="eyes">'
          f'<ellipse cx="86" cy="95" rx="4.6" ry="6" fill="{INK}"/><ellipse cx="114" cy="95" rx="4.6" ry="6" fill="{INK}"/>'
          '<circle cx="87.6" cy="92.6" r="1.6" fill="#fff"/><circle cx="115.6" cy="92.6" r="1.6" fill="#fff"/></g>')
    if brows:
        s += f'<path d="M79 83 q7 -5 14 0 M107 83 q7 -5 14 0" fill="none" stroke="{INK}" stroke-width="3.2" stroke-linecap="round"/>'
    s += '<circle cx="77" cy="108" r="6" fill="#ff7a9a" fill-opacity=".4"/><circle cx="123" cy="108" r="6" fill="#ff7a9a" fill-opacity=".4"/>'
    s += f'<path d="M98 100 q2 4 -1 6" fill="none" stroke="{c["shade"]}" stroke-width="3" stroke-linecap="round"/>'
    if smile == "open":
        s += (f'<path d="M87 113 q13 15 26 0 Z" fill="{INK}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
              '<path d="M90 114.5 h20 q-2 4 -10 4 q-8 0 -10 -4Z" fill="#fff"/>')
    else:
        s += f'<path d="M88 113 q12 11 24 0" fill="none" stroke="{INK}" stroke-width="3.6" stroke-linecap="round"/>'
    return s


# ---------- characters ----------

def chani():
    c = CHARS["chani"]
    s = base_back(c)
    s += f'<path d="M60 96 q-6 -50 40 -52 q46 2 40 52 l5 36 q-14 9 -26 -1 l-4 -32 h-30 l-4 32 q-12 10 -26 1Z" {_o(c["hair"])}/>'
    s += body(c)
    s += head(c)
    s += f'<path d="M64 84 q4 -22 36 -24 q32 2 36 24 q-12 -12 -36 -12 q-24 0 -36 12Z" {_o(c["hair"])}/>'
    # detective hat: crown + wide brim + band
    s += (f'<path d="M66 62 q2 -28 34 -30 q32 2 34 30 Z" {_o("#5b21b6")}/>'
          f'<path d="M50 66 q50 -16 100 0 q-50 8 -100 0Z" {_o("#6d28d9")}/>'
          f'<path d="M68 57 q32 -8 64 0" fill="none" stroke="{c["acc"]}" stroke-width="6" stroke-linecap="round"/>')
    # magnifier in raised hand
    s += ('<g class="wave">'
          f'<path d="M150 186 l12 -30" {_o(c["shirt"])}/>'
          f'<path d="M163 148 l-8 22" stroke="{INK}" stroke-width="9" stroke-linecap="round"/>'
          f'<circle cx="168" cy="132" r="18" fill="#cffafe" fill-opacity=".55" stroke="{INK}" stroke-width="{SW}"/>'
          f'<circle cx="168" cy="132" r="12" fill="none" stroke="{c["acc"]}" stroke-width="3"/>'
          f'<path d="M161 126 q4 -4 9 -3" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round"/>'
          f'<circle cx="156" cy="168" r="9" {_o(c["skin"])}/></g>')
    return s


def dana():
    c = CHARS["dana"]
    s = base_back(c)
    # curly cloud of hair behind the head
    curls = [(64, 70, 18), (80, 52, 19), (100, 46, 20), (120, 52, 19), (136, 70, 18), (142, 92, 15), (58, 92, 15),
             (60, 114, 13), (140, 114, 13)]
    s += "".join(f'<circle cx="{x}" cy="{y}" r="{r}" {_o(c["hair"])}/>' for x, y, r in curls)
    s += body(c)
    s += head(c)
    s += "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c["hair"]}"/>' for x, y, r in [(78, 62, 13), (96, 56, 14), (114, 58, 13), (126, 68, 11), (70, 74, 9)])
    # glasses
    s += (f'<rect x="73" y="85" width="24" height="19" rx="8" fill="#bfdbfe" fill-opacity=".25" stroke="{INK}" stroke-width="3.6"/>'
          f'<rect x="103" y="85" width="24" height="19" rx="8" fill="#bfdbfe" fill-opacity=".25" stroke="{INK}" stroke-width="3.6"/>'
          f'<path d="M97 93 h6" stroke="{INK}" stroke-width="3.6"/>')
    # chart tablet held low
    s += ('<g class="wave">'
          f'<rect x="120" y="140" width="62" height="46" rx="8" transform="rotate(-8 151 163)" {_o("#0b1440")}/>'
          f'<g transform="rotate(-8 151 163)"><rect x="129" y="166" width="8" height="12" rx="2" fill="{c["acc"]}"/>'
          f'<rect x="141" y="158" width="8" height="20" rx="2" fill="{c["acc"]}"/>'
          f'<rect x="153" y="150" width="8" height="28" rx="2" fill="#f87171"/>'
          f'<rect x="165" y="160" width="8" height="18" rx="2" fill="{c["acc"]}"/>'
          f'<path d="M128 156 L142 150 L156 142 L172 148" fill="none" stroke="#fde68a" stroke-width="3" stroke-linecap="round"/></g>'
          f'<circle cx="124" cy="182" r="9" {_o(c["skin"])}/></g>')
    return s


def shira():
    c = CHARS["shira"]
    s = base_back(c)
    # long hair behind
    s += f'<path d="M60 96 q-6 -54 40 -56 q46 2 40 56 l6 62 q-20 10 -36 0 l-10 -40 h0 l-10 40 q-16 10 -36 0Z" {_o(c["hair"])}/>'
    s += body(c)
    s += head(c)
    # side-swept bangs
    s += f'<path d="M62 90 q2 -44 42 -44 q36 2 34 40 q-26 -2 -40 -20 q-12 18 -36 24Z" {_o(c["hair"])}/>'
    # headset
    s += (f'<path d="M58 96 q-2 -58 42 -60 q44 2 42 60" fill="none" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>'
          f'<path d="M58 96 q-2 -58 42 -60 q44 2 42 60" fill="none" stroke="{c["acc"]}" stroke-width="3" stroke-linecap="round"/>'
          f'<rect x="50" y="88" width="16" height="24" rx="7" {_o(c["acc"])}/>'
          f'<rect x="134" y="88" width="16" height="24" rx="7" {_o(c["acc"])}/>'
          f'<path d="M58 110 q4 18 26 16" fill="none" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>'
          f'<circle cx="86" cy="126" r="5" {_o("#a78bfa")}/>')
    # chat bubble
    s += ('<g class="wave">'
          f'<path d="M140 22 h44 a10 10 0 0 1 10 10 v22 a10 10 0 0 1 -10 10 h-26 l-12 10 l2 -10 h-8 a10 10 0 0 1 -10 -10 v-22 a10 10 0 0 1 10 -10Z" {_o("#ffffff")}/>'
          f'<circle cx="150" cy="43" r="4" fill="{c["shirt"]}"/><circle cx="162" cy="43" r="4" fill="{c["shirt"]}"/><circle cx="174" cy="43" r="4" fill="{c["shirt"]}"/></g>')
    return s


def noga():
    c = CHARS["noga"]
    s = base_back(c)
    # short bob behind
    s += f'<path d="M58 118 q-8 -66 42 -68 q50 2 42 68 q-8 6 -16 0 l-2 -30 h-48 l-2 30 q-8 6 -16 0Z" {_o(c["hair"])}/>'
    s += body(c)
    s += head(c)
    s += f'<path d="M64 84 q10 -26 36 -26 q26 0 36 26 q-18 -6 -36 -6 q-18 0 -36 6Z" {_o(c["hair"])}/>'
    # hard hat
    s += (f'<path d="M62 70 q0 -36 38 -38 q38 2 38 38 Z" {_o(c["acc"])}/>'
          f'<path d="M52 72 h96 q4 0 4 4 q0 4 -4 4 h-96 q-4 0 -4 -4 q0 -4 4 -4Z" {_o("#f59e0b")}/>'
          f'<path d="M100 34 v36" stroke="{INK}" stroke-width="3.2" stroke-linecap="round"/>'
          f'<path d="M92 36 q-2 16 0 34 M108 36 q2 16 0 34" fill="none" stroke="#fde68a" stroke-width="3" stroke-linecap="round"/>')
    # wrench over shoulder + key ring
    s += ('<g class="wave">'
          f'<path d="M136 196 L176 128" stroke="{INK}" stroke-width="14" stroke-linecap="round"/>'
          f'<path d="M136 196 L176 128" stroke="#cbd5e1" stroke-width="7" stroke-linecap="round"/>'
          f'<path d="M168 120 a14 14 0 1 0 22 10 l-9 -3 l-4 -8 l4 -8Z" {_o("#cbd5e1")}/>'
          f'<circle cx="150" cy="172" r="9" {_o(c["skin"])}/></g>')
    s += (f'<circle cx="56" cy="174" r="11" fill="none" stroke="{INK}" stroke-width="5"/>'
          f'<circle cx="56" cy="174" r="11" fill="none" stroke="{c["acc"]}" stroke-width="2"/>'
          f'<path d="M48 184 l-6 12 l5 2 M60 186 l2 13 l5 -1" fill="none" stroke="{INK}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>')
    return s


def gal():
    c = CHARS["gal"]
    s = base_back(c)
    s += body(c, collar=False)
    # hoodie strings + hood rim
    s += (f'<path d="M66 156 q34 22 68 0" fill="none" stroke="{INK}" stroke-width="{SW}" stroke-linecap="round"/>'
          f'<path d="M92 166 v18 M108 166 v18" stroke="{c["acc"]}" stroke-width="4" stroke-linecap="round"/>')
    s += head(c, smile="closed")
    # short hair with a quiff
    s += f'<path d="M62 92 q-6 -40 26 -48 q8 -10 24 -4 q30 6 26 52 q-6 -20 -16 -26 q-10 8 -30 6 q-16 0 -24 8 q-4 6 -6 12Z" {_o(c["hair"])}/>'
    # short beard line
    s += f'<path d="M66 104 q4 30 34 30 q30 0 34 -30 q-4 18 -34 20 q-30 -2 -34 -20Z" fill="{c["hair"]}" fill-opacity=".85"/>'
    s += f'<path d="M88 114 q12 9 24 0" fill="none" stroke="{INK}" stroke-width="3.6" stroke-linecap="round"/>'
    # two plugs meeting (bridge)
    s += ('<g class="wave">'
          f'<path d="M14 168 q20 -26 50 -10" fill="none" stroke="{INK}" stroke-width="9" stroke-linecap="round"/>'
          f'<path d="M14 168 q20 -26 50 -10" fill="none" stroke="#f472b6" stroke-width="4" stroke-linecap="round"/>'
          f'<rect x="58" y="148" width="20" height="18" rx="5" {_o("#f472b6")}/>'
          f'<path d="M78 152 h7 M78 162 h7" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>'
          f'<path d="M186 168 q-20 -26 -50 -10" fill="none" stroke="{INK}" stroke-width="9" stroke-linecap="round"/>'
          f'<path d="M186 168 q-20 -26 -50 -10" fill="none" stroke="{c["acc"]}" stroke-width="4" stroke-linecap="round"/>'
          f'<rect x="122" y="148" width="20" height="18" rx="5" {_o(c["acc"])}/>'
          f'<path d="M100 150 l-4 8 h8 l-4 8" fill="none" stroke="#fde047" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/></g>')
    return s


def karin():
    c = CHARS["karin"]
    s = base_back(c)
    # long, light-blond hair behind, past the shoulders
    s += f'<path d="M58 96 q-8 -60 42 -62 q50 2 42 62 q4 40 10 70 q-20 8 -34 -4 l-6 -60 h-24 l-6 60 q-14 12 -34 4 q6 -30 10 -70Z" {_o(c["hair"])}/>'
    s += body(c)
    s += head(c)
    # centre-parted long hair framing the face
    s += (f'<path d="M100 52 q-34 2 -40 44 q-2 30 4 50 q6 -30 10 -50 q8 -22 26 -44Z" {_o(c["hair"])}/>'
          f'<path d="M100 52 q34 2 40 44 q2 30 -4 50 q-6 -30 -10 -50 q-8 -22 -26 -44Z" {_o(c["hair"])}/>'
          '<path d="M78 64 q-8 12 -10 28 M124 64 q8 12 10 28" fill="none" stroke="#f5dfa6" stroke-width="3" stroke-linecap="round"/>')
    # small earrings
    s += f'<circle cx="63" cy="110" r="3.4" fill="{c["acc"]}" stroke="{INK}" stroke-width="2"/><circle cx="137" cy="110" r="3.4" fill="{c["acc"]}" stroke="{INK}" stroke-width="2"/>'
    # laptop in front (👩‍💻) with the B-circuit spark
    s += ('<g class="wave">'
          f'<path d="M44 196 l14 -36 h84 l14 36Z" {_o("#c7d2fe")}/>'
          f'<path d="M30 196 h140" stroke="{INK}" stroke-width="{SW + 2}" stroke-linecap="round"/>'
          f'<path d="M95 176 l5 -6 l5 6 l-5 6Z" fill="{c["shirt"]}"/>'
          f'<path d="M150 30 l3 9 l9 3 l-9 3 l-3 9 l-3 -9 l-9 -3 l9 -3Z" fill="{c["acc"]}" stroke="{INK}" stroke-width="2.4" stroke-linejoin="round"/></g>')
    return s


DRAW = {"chani": chani, "dana": dana, "shira": shira, "noga": noga, "gal": gal, "karin": karin}


def symbol(slug):
    return f'<symbol id="ch-{slug}" viewBox="0 0 200 204">{DRAW[slug]()}</symbol>'


def symbols(slugs=None):
    slugs = slugs or list(DRAW)
    return "".join(symbol(s) for s in slugs)


if __name__ == "__main__":
    for s in DRAW:
        print(s, len(symbol(s)), "bytes")
