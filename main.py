#!/usr/bin/env python3
"""news-image-20261121: one-day newspaper front page for Saturday 21 November 2026.

Draws the whole image with Python 3.13 standard library only: an own PNG
encoder (zlib + struct) and an own 5x7 bitmap font. No network, no files read
besides this program itself. Deterministic: two runs write identical bytes.

Output: $MAKEFUN_OUTPUT_DIR/entry.png (default /output/entry.png),
1024x1024, PNG, under 1 MiB.
"""

import os
import struct
import zlib

W = 1024
H = 1024

PAPER = (247, 241, 222)   # cream #F7F1DE
INK = (26, 26, 26)        # near-black
RED = (166, 58, 42)       # brick red #A63A2A
SAGE = (203, 214, 188)    # map land
SAGE_LINE = (140, 160, 128)
BLUE = (38, 84, 124)
GOLD = (198, 154, 52)
TAN = (232, 220, 190)     # illustration panel


# ---------------------------------------------------------------- PNG encoder
def _chunk(kind, data):
    out = struct.pack(">I", len(data)) + kind + data
    out += struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
    return out


def encode_png(rgb, width, height):
    """rgb: bytes-like of width*height*3. Filter 0 (None) on every row."""
    raw = bytearray()
    stride = width * 3
    for y in range(height):
        raw.append(0)
        raw += rgb[y * stride:(y + 1) * stride]
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + _chunk(b"IHDR", ihdr)
            + _chunk(b"IDAT", zlib.compress(bytes(raw), 9))
            + _chunk(b"IEND", b""))


# ------------------------------------------------------------------ 5x7 font
# Each glyph: 7 rows, each a 5-bit number, bit 4 = leftmost column.
FONT = {
    'A': (0x0E, 0x11, 0x11, 0x1F, 0x11, 0x11, 0x11),
    'B': (0x1E, 0x11, 0x11, 0x1E, 0x11, 0x11, 0x1E),
    'C': (0x0E, 0x11, 0x10, 0x10, 0x10, 0x11, 0x0E),
    'D': (0x1E, 0x11, 0x11, 0x11, 0x11, 0x11, 0x1E),
    'E': (0x1F, 0x10, 0x10, 0x1E, 0x10, 0x10, 0x1F),
    'F': (0x1F, 0x10, 0x10, 0x1E, 0x10, 0x10, 0x10),
    'G': (0x0E, 0x11, 0x10, 0x17, 0x11, 0x11, 0x0F),
    'H': (0x11, 0x11, 0x11, 0x1F, 0x11, 0x11, 0x11),
    'I': (0x0E, 0x04, 0x04, 0x04, 0x04, 0x04, 0x0E),
    'J': (0x07, 0x02, 0x02, 0x02, 0x02, 0x12, 0x0C),
    'K': (0x11, 0x12, 0x14, 0x18, 0x14, 0x12, 0x11),
    'L': (0x10, 0x10, 0x10, 0x10, 0x10, 0x10, 0x1F),
    'M': (0x11, 0x1B, 0x15, 0x15, 0x11, 0x11, 0x11),
    'N': (0x11, 0x19, 0x15, 0x13, 0x11, 0x11, 0x11),
    'O': (0x0E, 0x11, 0x11, 0x11, 0x11, 0x11, 0x0E),
    'P': (0x1E, 0x11, 0x11, 0x1E, 0x10, 0x10, 0x10),
    'Q': (0x0E, 0x11, 0x11, 0x11, 0x15, 0x12, 0x0D),
    'R': (0x1E, 0x11, 0x11, 0x1E, 0x14, 0x12, 0x11),
    'S': (0x0F, 0x10, 0x10, 0x0E, 0x01, 0x01, 0x1E),
    'T': (0x1F, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04),
    'U': (0x11, 0x11, 0x11, 0x11, 0x11, 0x11, 0x0E),
    'V': (0x11, 0x11, 0x11, 0x11, 0x11, 0x0A, 0x04),
    'W': (0x11, 0x11, 0x11, 0x15, 0x15, 0x15, 0x0A),
    'X': (0x11, 0x11, 0x0A, 0x04, 0x0A, 0x11, 0x11),
    'Y': (0x11, 0x11, 0x0A, 0x04, 0x04, 0x04, 0x04),
    'Z': (0x1F, 0x01, 0x02, 0x04, 0x08, 0x10, 0x1F),
    '0': (0x0E, 0x11, 0x13, 0x15, 0x19, 0x11, 0x0E),
    '1': (0x04, 0x0C, 0x04, 0x04, 0x04, 0x04, 0x0E),
    '2': (0x0E, 0x11, 0x01, 0x06, 0x08, 0x10, 0x1F),
    '3': (0x1E, 0x01, 0x01, 0x0E, 0x01, 0x01, 0x1E),
    '4': (0x02, 0x06, 0x0A, 0x12, 0x1F, 0x02, 0x02),
    '5': (0x1F, 0x10, 0x1E, 0x01, 0x01, 0x11, 0x0E),
    '6': (0x06, 0x08, 0x10, 0x1E, 0x11, 0x11, 0x0E),
    '7': (0x1F, 0x01, 0x02, 0x04, 0x08, 0x08, 0x08),
    '8': (0x0E, 0x11, 0x11, 0x0E, 0x11, 0x11, 0x0E),
    '9': (0x0E, 0x11, 0x11, 0x0F, 0x01, 0x02, 0x0C),
}

FONT.update({
    'a': (0x00, 0x00, 0x0E, 0x01, 0x0F, 0x11, 0x0F),
    'b': (0x10, 0x10, 0x1E, 0x11, 0x11, 0x11, 0x1E),
    'c': (0x00, 0x00, 0x0E, 0x11, 0x10, 0x11, 0x0E),
    'd': (0x01, 0x01, 0x0F, 0x11, 0x11, 0x11, 0x0F),
    'e': (0x00, 0x00, 0x0E, 0x11, 0x1F, 0x10, 0x0E),
    'f': (0x06, 0x09, 0x08, 0x1E, 0x08, 0x08, 0x08),
    'g': (0x0F, 0x11, 0x11, 0x0F, 0x01, 0x01, 0x0E),
    'h': (0x10, 0x10, 0x1E, 0x11, 0x11, 0x11, 0x11),
    'i': (0x04, 0x00, 0x0C, 0x04, 0x04, 0x04, 0x0E),
    'j': (0x02, 0x00, 0x06, 0x02, 0x02, 0x12, 0x0C),
    'k': (0x10, 0x10, 0x12, 0x14, 0x18, 0x14, 0x12),
    'l': (0x0C, 0x04, 0x04, 0x04, 0x04, 0x04, 0x0E),
    'm': (0x00, 0x00, 0x1A, 0x15, 0x15, 0x15, 0x15),
    'n': (0x00, 0x00, 0x1E, 0x11, 0x11, 0x11, 0x11),
    'o': (0x00, 0x00, 0x0E, 0x11, 0x11, 0x11, 0x0E),
    'p': (0x1E, 0x11, 0x11, 0x1E, 0x10, 0x10, 0x10),
    'q': (0x0F, 0x11, 0x11, 0x0F, 0x01, 0x01, 0x01),
    'r': (0x00, 0x00, 0x16, 0x19, 0x10, 0x10, 0x10),
    's': (0x00, 0x00, 0x0F, 0x10, 0x0E, 0x01, 0x1E),
    't': (0x08, 0x08, 0x1E, 0x08, 0x08, 0x08, 0x06),
    'u': (0x00, 0x00, 0x11, 0x11, 0x11, 0x13, 0x0D),
    'v': (0x00, 0x00, 0x11, 0x11, 0x11, 0x0A, 0x04),
    'w': (0x00, 0x00, 0x11, 0x11, 0x15, 0x15, 0x0A),
    'x': (0x00, 0x00, 0x11, 0x0A, 0x04, 0x0A, 0x11),
    'y': (0x00, 0x00, 0x11, 0x11, 0x13, 0x0D, 0x04),
    'z': (0x00, 0x00, 0x1F, 0x02, 0x04, 0x08, 0x1F),
    ' ': (0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00),
    '.': (0x00, 0x00, 0x00, 0x00, 0x00, 0x0C, 0x0C),
    ',': (0x00, 0x00, 0x00, 0x00, 0x0C, 0x04, 0x08),
    ':': (0x00, 0x0C, 0x0C, 0x00, 0x0C, 0x0C, 0x00),
    ';': (0x00, 0x0C, 0x0C, 0x00, 0x0C, 0x04, 0x08),
    '!': (0x04, 0x04, 0x04, 0x04, 0x04, 0x00, 0x04),
    '?': (0x0E, 0x11, 0x01, 0x02, 0x04, 0x00, 0x04),
    "'": (0x04, 0x04, 0x08, 0x00, 0x00, 0x00, 0x00),
    '"': (0x0A, 0x0A, 0x00, 0x00, 0x00, 0x00, 0x00),
    '-': (0x00, 0x00, 0x00, 0x0E, 0x00, 0x00, 0x00),
    '(': (0x02, 0x04, 0x08, 0x08, 0x08, 0x04, 0x02),
    ')': (0x08, 0x04, 0x02, 0x02, 0x02, 0x04, 0x08),
    '/': (0x01, 0x02, 0x02, 0x04, 0x08, 0x08, 0x10),
    '&': (0x0C, 0x12, 0x14, 0x08, 0x15, 0x12, 0x0D),
    '%': (0x19, 0x19, 0x02, 0x04, 0x08, 0x13, 0x13),
    '$': (0x04, 0x0F, 0x14, 0x0E, 0x05, 0x1E, 0x04),
    '+': (0x00, 0x04, 0x04, 0x1F, 0x04, 0x04, 0x00),
    '=': (0x00, 0x00, 0x1F, 0x00, 0x1F, 0x00, 0x00),
    '*': (0x00, 0x04, 0x15, 0x0E, 0x15, 0x04, 0x00),
    '#': (0x0A, 0x0A, 0x1F, 0x0A, 0x1F, 0x0A, 0x0A),
    '@': (0x0E, 0x11, 0x17, 0x15, 0x16, 0x10, 0x0E),
    '_': (0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x1F),
    '>': (0x08, 0x04, 0x02, 0x01, 0x02, 0x04, 0x08),
    '<': (0x02, 0x04, 0x08, 0x10, 0x08, 0x04, 0x02),
    '~': (0x00, 0x00, 0x0A, 0x15, 0x00, 0x00, 0x00),
    # middle dot, bullet, em dash (drawn with the same 5-wide cell)
    '\u00b7': (0x00, 0x00, 0x00, 0x0C, 0x0C, 0x00, 0x00),
    '\u2022': (0x00, 0x0C, 0x1E, 0x1E, 0x1E, 0x0C, 0x00),
    '\u2014': (0x00, 0x00, 0x00, 0x1F, 0x00, 0x00, 0x00),
})

CHAR_W = 6   # advance per character at scale 1 (5 px glyph + 1 px gap)


def text_width(text, scale):
    return len(text) * CHAR_W * scale - scale


def wrap(text, max_chars):
    """Greedy word wrap; returns a list of lines, each <= max_chars."""
    lines = []
    for chunk in text.split("\n"):
        words = chunk.split(" ")
        cur = ""
        for w in words:
            if not cur:
                cur = w
            elif len(cur) + 1 + len(w) <= max_chars:
                cur += " " + w
            else:
                lines.append(cur)
                cur = w
        if cur or not lines:
            lines.append(cur)
    return lines


class Canvas:
    def __init__(self):
        row = bytes(PAPER) * W
        self.buf = bytearray(row * H)

    def px(self, x, y, color):
        if 0 <= x < W and 0 <= y < H:
            i = (y * W + x) * 3
            self.buf[i] = color[0]
            self.buf[i + 1] = color[1]
            self.buf[i + 2] = color[2]

    def rect(self, x, y, w, h, color):
        x0 = max(0, x)
        y0 = max(0, y)
        x1 = min(W, x + w)
        y1 = min(H, y + h)
        if x1 <= x0 or y1 <= y0:
            return
        fill = bytes(color) * (x1 - x0)
        for yy in range(y0, y1):
            i = (yy * W + x0) * 3
            self.buf[i:i + len(fill)] = fill

    def hline(self, x, y, w, color, thick=1):
        self.rect(x, y, w, thick, color)

    def vline(self, x, y, h, color, thick=1):
        self.rect(x, y, thick, h, color)

    def line(self, x0, y0, x1, y1, color, thick=1):
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        x, y = x0, y0
        while True:
            self.rect(x, y, thick, thick, color)
            if x == x1 and y == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x += sx
            if e2 <= dx:
                err += dx
                y += sy

    def circle(self, cx, cy, r, color, fill=True):
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                d2 = (xx - cx) * (xx - cx) + (yy - cy) * (yy - cy)
                if fill:
                    if d2 <= r * r:
                        self.px(xx, yy, color)
                elif r * r - 2 * r <= d2 <= r * r:
                    self.px(xx, yy, color)

    def poly(self, pts, color, outline=None):
        """Scanline fill of a polygon given as [(x, y), ...]."""
        if len(pts) < 3:
            return
        ymin = max(0, min(p[1] for p in pts))
        ymax = min(H - 1, max(p[1] for p in pts))
        n = len(pts)
        for y in range(ymin, ymax + 1):
            xs = []
            for i in range(n):
                x0, y0 = pts[i]
                x1, y1 = pts[(i + 1) % n]
                if (y0 <= y < y1) or (y1 <= y < y0):
                    xs.append(x0 + (y - y0) * (x1 - x0) / (y1 - y0))
            xs.sort()
            for k in range(0, len(xs) - 1, 2):
                a = max(0, int(xs[k]))
                b = min(W - 1, int(xs[k + 1]))
                self.rect(a, y, b - a + 1, 1, color)
        if outline:
            for i in range(n):
                x0, y0 = pts[i]
                x1, y1 = pts[(i + 1) % n]
                self.line(x0, y0, x1, y1, outline)

    def glyph(self, x, y, ch, scale, color):
        rows = FONT.get(ch)
        if rows is None:
            return
        for r in range(7):
            bits = rows[r]
            if not bits:
                continue
            for c in range(5):
                if bits & (1 << (4 - c)):
                    self.rect(x + c * scale, y + r * scale, scale, scale, color)

    def text(self, x, y, s, scale=1, color=INK, bold=False):
        """Draw text; returns x position just past the last character."""
        cx = x
        for ch in s:
            if ch == " ":
                cx += CHAR_W * scale
                continue
            self.glyph(cx, y, ch, scale, color)
            if bold:
                self.glyph(cx + max(1, scale // 2), y, ch, scale, color)
            cx += CHAR_W * scale
        return cx

    def text_center(self, x, y, w, s, scale=1, color=INK, bold=False):
        tw = text_width(s, scale)
        self.text(x + max(0, (w - tw) // 2), y, s, scale, color, bold)

    def para(self, x, y, w, s, scale=1, color=INK, bold=False, leading=None):
        """Wrapped paragraph; returns y just past the last line."""
        if leading is None:
            leading = 7 * scale + 2
        max_chars = max(1, w // (CHAR_W * scale))
        cy = y
        for line in wrap(s, max_chars):
            self.text(x, cy, line, scale, color, bold)
            cy += leading
        return cy


# ---------------------------------------------------------------------- data
# (region, field, headline, summary, tag, source)
LEADS = [
    ("EUROPE", "CONFLICT",
     "RUSSIA STRIKES UKRAINE; MISSILES LAND IN POLAND",
     "Russia fired 400+ drones and 110 missiles at Ukraine; 8 killed "
     "in Kyiv; two hit Poland; NATO scrambled jets.",
     "CONFIRMED", "FRANCE 24, CBS"),
    ("N. AMERICA", "ECONOMY",
     "AI SELL-OFF PUSHES S&P 500 INTO CORRECTION",
     "US stocks fell 3.7% as AI and chip shares sold off; Nasdaq erased "
     "all its 2026 gains; Nikkei fell 5%.",
     "CONFIRMED", "BBC, UPI"),
    ("ASIA", "POLITICS",
     "TRUMP DEFENDS TIES TO PUTIN AND XI",
     "After the Shenzhen summit, Trump gave a 90-minute press conference "
     "and called Putin a friend; Zelensky answered: \"He's a killer.\"",
     "CONFIRMED", "BBC, LE MONDE"),
    ("SPACE", "SCIENCE",
     "BEPICOLOMBO REACHES MERCURY ORBIT",
     "The twin probes entered Mercury's orbit after 8+ years and about "
     "10 billion km; only the second mission to orbit the planet.",
     "CONFIRMED", "GUARDIAN, UPI"),
]

# (region, field, headline, summary, tag, source, icon)
MEDIUM = [
    ("MIDDLE EAST", "CONFLICT",
     "HOUTHI MISSILES AT RIYADH INTERCEPTED",
     "Saudi-led coalition shot down three Houthi missiles headed for Riyadh.",
     "CONFIRMED", "AL JAZEERA", "missile"),
    ("MIDDLE EAST", "CONFLICT",
     "HORMUZ ATTACKS CONTINUE AS TALKS STALL",
     "Iran said it shot down a US MQ-9 drone over Hormuz; US sanctioned oil trustees.",
     "REPORTED", "JAPAN TIMES", "drone"),
    ("EUROPE", "POLITICS",
     "UK AND EU SIGN BIGGEST POST-BREXIT DEALS",
     "UK and EU signed three post-Brexit deals on food, carbon and youth mobility.",
     "CONFIRMED", "BBC, RFI", "flags"),
    ("GLOBAL", "CLIMATE",
     "COP31 TALKS RUN PAST DEADLINE",
     "UN climate summit in Antalya ran into overtime as 200 nations failed to agree.",
     "CONFIRMED", "AL JAZEERA", "globe"),
    ("N. AMERICA", "JUSTICE",
     "PALISADES FIRE ARSONIST CONVICTED",
     "Jury found Rinderknecht guilty of arson that started the Palisades fire.",
     "CONFIRMED", "BBC, GUARDIAN", "flame"),
    ("S. AMERICA", "DISASTER",
     "QUAKE 6.7 SHAKES CENTRAL PERU",
     "A strong quake struck the Andes; residents ran into the streets in Lima.",
     "CONFIRMED", "STRAITS TIMES", "quake"),
    ("N. AMERICA", "TECHNOLOGY",
     "FBI CRIME DATABASE HACKED",
     "CNN reported the FBI's crime database was hacked; Trump fired the cyber chief.",
     "REPORTED", "STRAITS TIMES", "lock"),
    ("N. AMERICA", "ECONOMY",
     "TRUMP WANTS NVIDIA CHIEF REINSTATED",
     "Trump said ousted Nvidia chief Jensen Huang deserves a second chance.",
     "CONFIRMED", "AL JAZEERA", "chip"),
    ("GLOBAL", "SCIENCE",
     "CLAIMED PROOF OF RIEMANN HYPOTHESIS",
     "Mathematician Levent Alpoge released a claimed AI-assisted proof of Riemann.",
     "REPORTED", "BBC, THE HINDU", "math"),
    ("MIDDLE EAST", "POLITICS",
     "IRAQ MOVES INTO MILITIA STRONGHOLD",
     "Iraqi forces entered Jurf al-Sakhar for the first time in 12 years.",
     "CONFIRMED", "AL JAZEERA", "fort"),
    ("MIDDLE EAST", "CONFLICT",
     "ISRAELI STRIKES KILL SIX IN GAZA",
     "Israeli strikes killed six in Gaza, civil defense said; 400+ settler attacks.",
     "REPORTED", "MEE, AL JAZEERA", "burst"),
    ("N. AMERICA", "HEALTH",
     "US LOSES MEASLES-FREE STATUS",
     "The US, Mexico and Bolivia lost measles-free status; US reported 7,700 cases.",
     "CONFIRMED", "GUARDIAN", "virus"),
]

# (number, headline, source) — one line each
ALSO_ON = [
    (17, "GTA VI earns $3.8bn on first day", "BBC, Guardian"),
    (18, "Pancreatic cancer pill breakthrough", "Guardian"),
    (19, "Gen Z protests spread across 25 European countries", "Al Jazeera"),
    (20, "Denmark expels Russian diplomat over alleged plot", "Al Jazeera"),
    (21, "Estonia to close border crossings with Russia", "Al Jazeera"),
    (22, "Myanmar verdict fallout: UK expels envoy", "BBC"),
    (23, "Saudi-Japan oil stockpile deal", "Japan Times"),
    (24, "Oil steady near $90 after 5% weekly fall", "OilPrice"),
    (25, "Argentina risk tops 1,000", "Buenos Aires Times"),
    (26, "Bayer's $7.25bn Roundup settlement approved", "Le Monde"),
    (27, "Tanzania's Lissu convicted of sedition", "BBC"),
    (28, "Uganda restricts gatherings over Ebola threat", "AllAfrica"),
    (29, "Spain heads to Nov 29 election", "France 24"),
    (30, "Bolsonaro hospitalised in Brasilia", "DW"),
    (31, "Nepal PM to visit India Nov 22-23", "BBC"),
    (32, "French police sentenced over racist beating", "Al Jazeera"),
    (33, "France probes Depardieu and Houellebecq", "BBC"),
    (34, "Mamdani to close Rikers Island by 2032", "BBC"),
    (35, "Texas inmate cried out during execution", "BBC"),
    (36, "South Korea moves to impeach chief justice", "Yonhap"),
    (37, "Melbourne teen accused of organising arsons", "Guardian"),
    (38, "YouTube nears US schools settlement", "Straits Times"),
    (39, "Kenya begins onshore crude drilling", "AllAfrica"),
    (40, "CERN finds first evidence of rare particle decay", "ScienceDaily"),
    (41, "Villepin announces French presidential run", "France 24"),
    (42, "Japan-China ties hit record low", "Japan Times"),
    (43, "Isolated Awa approach outpost in Brazil", "Euronews"),
    (44, "US sells deep-sea mining leases off Samoa", "Euronews"),
    (45, "Alcaraz stays unbeaten at ATP Finals", "BBC Sport"),
    (46, "A Lim Kim leads LPGA finale after hole-in-one", "BBC Sport"),
    (47, "Nigeria boat capsizes; 300 missing", "Al Jazeera"),
    (48, "Trump threatens tax on AI data centres abroad", "BBC"),
]

BIG_NUMBERS = [
    ("400+", "drones fired at Ukraine"),
    ("110", "missiles"),
    ("$3.8bn", "GTA VI day one"),
    ("1 in 12", "cancer trial undetectable"),
    ("6.7", "Peru quake"),
    ("$7.25bn", "Bayer settlement"),
]

TIMELINE = [
    ("OVERNIGHT", "Russia fires 400+ drones at Ukraine"),
    ("MORNING", "Peru quake 6.7 shakes the Andes"),
    ("MIDDAY", "COP31 talks run past deadline"),
    ("AFTERNOON", "Trump press conference after Shenzhen summit"),
    ("EVENING", "GTA VI $3.8bn first-day sales reported"),
]

DATE_CHECK = [
    "Anthropic's $83 IPO debut \u2014 Fri 20 Nov",
    "Shenzhen Trump-Xi-Putin summit itself \u2014 Fri 20 Nov (today: the press conference)",
    "Voyager 1's one-light-day milestone \u2014 Wed 18 Nov",
    "St Peter's Square Christmas tree raised \u2014 Fri 20 Nov",
    "ICJ genocide verdict itself \u2014 Fri 20 Nov (today: the fallout)",
]


# ------------------------------------------------------------ illustrations
def draw_missile_map(cv, x, y, w, h):
    """Stylised Ukraine/Poland landmass with missile arcs."""
    cv.rect(x, y, w, h, TAN)
    # landmass (simplified)
    cv.poly([(x + 18, y + h - 12), (x + 30, y + 22), (x + 70, y + 10),
             (x + 120, y + 16), (x + 170, y + 8), (x + 215, y + 20),
             (x + 225, y + 48), (x + 200, y + h - 8), (x + 120, y + h - 16),
             (x + 60, y + h - 6)], SAGE, SAGE_LINE)
    # sea at bottom left
    cv.poly([(x + 4, y + h - 26), (x + 60, y + h - 22), (x + 55, y + h - 2),
             (x + 4, y + h - 2)], (150, 190, 205))
    # missile arcs (dashed red)
    for (ax, ay, bx, by) in [(x + 30, y + 66, x + 150, y + 22),
                             (x + 60, y + 70, x + 190, y + 30),
                             (x + 90, y + 72, x + 210, y + 44)]:
        steps = 24
        for i in range(steps + 1):
            t = i / steps
            px = int(ax + (bx - ax) * t)
            py = int(ay + (by - ay) * t - 26 * 4 * t * (1 - t))
            if i % 2 == 0:
                cv.rect(px, py, 3, 3, RED)
        cv.circle(bx, by, 4, RED)
        cv.circle(bx, by, 2, (255, 220, 120))
    cv.text(x + 8, y + 6, "KYIV", 1, INK, bold=True)
    cv.text(x + 168, y + 6, "POLAND", 1, INK, bold=True)


def draw_chart_down(cv, x, y, w, h):
    """Falling red line chart on axes."""
    cv.rect(x, y, w, h, TAN)
    cv.vline(x + 22, y + 10, h - 26, INK, 2)
    cv.hline(x + 22, y + h - 16, w - 34, INK, 2)
    pts = [(x + 26, y + 18), (x + 60, y + 26), (x + 95, y + 22),
           (x + 130, y + 38), (x + 165, y + 46), (x + 200, y + 58),
           (x + 224, y + 66)]
    for i in range(len(pts) - 1):
        cv.line(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], RED, 3)
    cv.text(x + 150, y + 4, "-3.7%", 1, RED, bold=True)
    cv.text(x + 26, y + h - 13, "S&P 500", 1, INK)


def draw_flags(cv, x, y, w, h):
    """Three flags (US, China, Russia) above a summit hall."""
    cv.rect(x, y, w, h, TAN)
    # hall
    cv.rect(x + 20, y + h - 26, w - 40, 22, (120, 110, 95))
    for i in range(5):
        cv.rect(x + 34 + i * 34, y + h - 22, 10, 18, (210, 198, 170))
    cv.poly([(x + 14, y + h - 26), (x + w // 2, y + h - 44),
             (x + w - 14, y + h - 26)], (150, 135, 110))
    # flag poles + flags
    cols = [(x + 52, "us"), (x + 112, "cn"), (x + 172, "ru")]
    for fx, kind in cols:
        cv.vline(fx, y + 10, 34, INK, 2)
        if kind == "us":
            cv.rect(fx + 2, y + 10, 34, 20, (178, 34, 52))
            cv.rect(fx + 2, y + 10, 34, 3, (255, 255, 255))
            cv.rect(fx + 2, y + 16, 34, 3, (255, 255, 255))
            cv.rect(fx + 2, y + 22, 34, 3, (255, 255, 255))
            cv.rect(fx + 2, y + 10, 14, 11, BLUE)
        elif kind == "cn":
            cv.rect(fx + 2, y + 10, 34, 20, (222, 41, 16))
            cv.circle(fx + 12, y + 18, 3, (255, 215, 0))
        else:
            cv.rect(fx + 2, y + 10, 34, 7, (255, 255, 255))
            cv.rect(fx + 2, y + 17, 34, 6, BLUE)
            cv.rect(fx + 2, y + 23, 34, 7, (200, 30, 30))


def draw_space(cv, x, y, w, h):
    """BepiColombo probe and Mercury against stars."""
    cv.rect(x, y, w, h, (28, 34, 52))
    for (sx, sy) in [(x + 14, y + 12), (x + 60, y + 8), (x + 120, y + 16),
                     (x + 180, y + 10), (x + 210, y + 22), (x + 40, y + 34),
                     (x + 150, y + 40), (x + 90, y + 14)]:
        cv.rect(sx, sy, 2, 2, (255, 255, 255))
    # Mercury
    cv.circle(x + 178, y + 52, 20, (196, 148, 96))
    cv.circle(x + 172, y + 48, 4, (150, 108, 66))
    cv.circle(x + 184, y + 58, 3, (150, 108, 66))
    # probe body + panels
    cv.rect(x + 40, y + 46, 34, 14, (200, 200, 200))
    cv.rect(x + 22, y + 50, 16, 6, BLUE)
    cv.rect(x + 76, y + 50, 16, 6, BLUE)
    cv.circle(x + 57, y + 53, 4, GOLD)
    cv.text(x + 8, y + 66, "MERCURY", 1, (255, 255, 255), bold=True)


def draw_icon(cv, kind, x, y, w, h):
    """Small 24px-high icon band for a medium story."""
    cv.rect(x, y, w, h, TAN)
    cx, cy = x + w // 2, y + h // 2
    if kind == "missile":
        cv.line(x + 14, y + h - 6, x + w - 20, y + 6, RED, 2)
        cv.circle(x + w - 20, y + 6, 4, RED)
        cv.circle(x + w - 20, y + 6, 2, (255, 220, 120))
        cv.circle(x + 30, y + h - 8, 3, INK)
    elif kind == "drone":
        cv.rect(cx - 14, cy - 3, 28, 6, INK)
        cv.rect(cx - 4, cy - 8, 8, 16, INK)
        cv.line(x + 10, y + h - 4, x + w - 10, y + h - 4, BLUE, 2)
    elif kind == "flags":
        cv.rect(x + 12, y + 4, 26, 14, (178, 34, 52))
        cv.rect(x + 12, y + 4, 26, 2, (255, 255, 255))
        cv.rect(x + 12, y + 10, 26, 2, (255, 255, 255))
        cv.circle(x + w - 30, cy, 8, BLUE)
        for a in range(8):
            import math
            ang = a * 3.14159 / 4
            cv.px(int(x + w - 30 + 5 * math.cos(ang)),
                  int(cy + 5 * math.sin(ang)), (255, 215, 0))
    elif kind == "globe":
        cv.circle(cx, cy, 9, BLUE)
        cv.circle(cx - 3, cy - 2, 3, SAGE)
        cv.circle(cx + 4, cy + 3, 2, SAGE)
    elif kind == "flame":
        cv.poly([(cx, y + 2), (cx + 7, cy + 2), (cx + 5, cy + 6),
                 (cx + 8, y + h - 4), (cx - 8, y + h - 4), (cx - 5, cy + 6),
                 (cx - 7, cy + 2)], (230, 90, 30))
        cv.poly([(cx, cy + 2), (cx + 3, cy + 6), (cx, y + h - 5),
                 (cx - 3, cy + 6)], (255, 200, 60))
    elif kind == "quake":
        for i in range(5):
            cv.line(x + 12 + i * 8, cy + (6 if i % 2 else -6),
                    x + 20 + i * 8, cy + (-6 if i % 2 else 6), INK, 2)
        cv.line(x + 8, y + h - 5, x + w - 8, y + h - 5, RED, 2)
    elif kind == "lock":
        cv.rect(cx - 9, cy - 2, 18, 12, INK)
        cv.rect(cx - 5, cy - 9, 10, 8, INK)
        cv.rect(cx - 2, cy + 2, 4, 5, PAPER)
    elif kind == "chip":
        cv.rect(cx - 8, cy - 8, 16, 16, INK)
        cv.rect(cx - 4, cy - 4, 8, 8, GOLD)
        for i in range(3):
            cv.hline(cx - 13, cy - 5 + i * 5, 5, INK, 2)
            cv.hline(cx + 8, cy - 5 + i * 5, 5, INK, 2)
    elif kind == "math":
        cv.line(x + 12, y + 5, x + 12, y + h - 5, INK, 2)
        cv.line(x + 12, y + 5, x + 22, y + 5, INK, 2)
        cv.text(x + 26, y + 6, "x2 + y2 = ?", 1, INK, bold=True)
    elif kind == "fort":
        cv.rect(x + 16, cy - 4, 34, 12, INK)
        cv.rect(x + 22, cy - 10, 6, 6, INK)
        cv.rect(x + 38, cy - 10, 6, 6, INK)
        cv.vline(x + w - 22, y + 4, 14, RED, 2)
        cv.rect(x + w - 20, y + 4, 12, 7, RED)
    elif kind == "burst":
        for i in range(8):
            import math
            ang = i * 3.14159 / 4
            cv.line(cx, cy, int(cx + 10 * math.cos(ang)),
                    int(cy + 10 * math.sin(ang)), RED, 2)
        cv.circle(cx, cy, 4, RED)
    elif kind == "virus":
        cv.circle(cx, cy, 7, (90, 140, 90))
        for i in range(8):
            import math
            ang = i * 3.14159 / 4
            cv.line(int(cx + 7 * math.cos(ang)), int(cy + 7 * math.sin(ang)),
                    int(cx + 11 * math.cos(ang)), int(cy + 11 * math.sin(ang)),
                    (90, 140, 90), 2)


LEAD_DRAW = [draw_missile_map, draw_chart_down, draw_flags, draw_space]


# ------------------------------------------------------------------- map
MAP_X0, MAP_Y0, MAP_W, MAP_H = 16, 628, 992, 116


def ll(lon, lat):
    return (MAP_X0 + int((lon + 170) / 360 * MAP_W),
            MAP_Y0 + int((75 - lat) / 130 * MAP_H))


CONTINENTS = [
    [(-168, 66), (-150, 70), (-135, 69), (-125, 71), (-115, 68), (-100, 69),
     (-90, 68), (-85, 66), (-78, 71), (-70, 62), (-65, 60), (-60, 55),
     (-55, 47), (-60, 45), (-65, 44), (-70, 42), (-75, 35), (-80, 32),
     (-81, 26), (-84, 30), (-90, 21), (-95, 19), (-97, 16), (-102, 18),
     (-105, 22), (-110, 25), (-115, 30), (-120, 34), (-125, 40), (-125, 48),
     (-135, 58), (-150, 60), (-160, 58), (-168, 66)],
    [(-80, 10), (-77, 4), (-75, 0), (-70, -5), (-60, -8), (-50, -5),
     (-40, -8), (-35, -10), (-38, -15), (-40, -22), (-48, -27), (-55, -33),
     (-60, -38), (-65, -42), (-70, -45), (-73, -40), (-73, -30), (-70, -20),
     (-75, -15), (-80, -8), (-80, 2), (-80, 10)],
    [(-10, 36), (-9, 43), (-2, 44), (-1, 46), (0, 50), (2, 51), (5, 53),
     (8, 54), (8, 57), (10, 59), (12, 56), (18, 56), (21, 55), (24, 58),
     (25, 60), (28, 62), (30, 65), (25, 68), (20, 70), (15, 68), (12, 64),
     (8, 60), (5, 58), (0, 54), (-3, 50), (-5, 46), (-9, 43), (-10, 38)],
    [(-6, 35), (0, 36), (10, 37), (15, 34), (20, 32), (25, 31), (30, 31),
     (33, 28), (35, 28), (38, 22), (40, 15), (43, 12), (48, 11), (51, 11),
     (48, 5), (44, 0), (40, -5), (38, -12), (35, -18), (32, -25), (28, -30),
     (20, -35), (16, -30), (14, -22), (12, -15), (10, -8), (8, -2), (5, 4),
     (0, 6), (-5, 5), (-10, 7), (-15, 11), (-17, 15), (-16, 20), (-15, 25),
     (-12, 30), (-8, 33), (-6, 35)],
    [(30, 62), (35, 66), (45, 68), (55, 69), (65, 71), (75, 72), (85, 74),
     (95, 76), (105, 77), (115, 76), (125, 74), (135, 72), (145, 72),
     (155, 70), (162, 68), (170, 66), (165, 62), (160, 58), (158, 52),
     (150, 50), (142, 45), (140, 40), (135, 35), (130, 33), (125, 30),
     (120, 25), (115, 20), (110, 12), (105, 8), (100, 8), (98, 12),
     (95, 16), (90, 22), (85, 20), (80, 15), (78, 8), (75, 10), (72, 20),
     (68, 23), (62, 25), (58, 26), (55, 28), (52, 30), (48, 30), (45, 30),
     (42, 32), (40, 34), (36, 36), (33, 38), (30, 40), (28, 44), (28, 48),
     (30, 55), (30, 62)],
    [(113, -22), (118, -20), (122, -14), (128, -13), (132, -12), (137, -12),
     (142, -11), (146, -14), (150, -20), (153, -26), (153, -30), (150, -37),
     (145, -38), (140, -38), (135, -35), (130, -32), (125, -33), (120, -34),
     (115, -33), (113, -28), (113, -22)],
]

# Hand-tuned dot positions (story number -> (x, y)) to avoid overlaps.
DOTS = {
    1: (567, 645), 2: (281, 653), 3: (798, 671), 4: (955, 635),
    5: (600, 660), 6: (645, 680), 7: (482, 644), 8: (585, 668),
    9: (148, 657), 10: (272, 702), 11: (250, 668), 12: (165, 675),
    13: (470, 660), 14: (625, 690), 15: (560, 685), 16: (300, 695),
}


def draw_lines(cv, x, y, lines, scale=1, color=INK, bold=False, leading=None):
    if leading is None:
        leading = 7 * scale + 2
    cy = y
    for line in lines:
        cv.text(x, cy, line, scale, color, bold)
        cy += leading
    return cy


def capped(text, max_chars, max_lines):
    return wrap(text, max_chars)[:max_lines]


# ------------------------------------------------------------------ layout
def build():
    cv = Canvas()

    # 1. top strip
    cv.text(16, 10, "THE WORLD'S NEWS OF ONE DAY", 1, RED, bold=True)
    right = "48 STORIES \u00b7 8 REGIONS \u00b7 13 FIELDS \u00b7 ALL FROM THIS SATURDAY"
    cv.text(1008 - text_width(right, 1), 10, right, 1, INK, bold=True)
    cv.hline(16, 26, 992, INK, 2)

    # 2. masthead
    mast = "Saturday 21 November 2026"
    cv.text_center(16, 32, 992, mast, 6, INK, bold=True)
    cv.hline(16, 80, 992, INK, 3)
    cv.hline(16, 84, 992, INK, 1)

    # 3. timeline
    cv.text(16, 90, "THE DAY IN UTC", 1, RED, bold=True)
    for i, (label, text) in enumerate(TIMELINE):
        sx = 118 + i * 178
        cv.text(sx, 90, label, 1, INK, bold=True)
        draw_lines(cv, sx, 100, capped(text, 29, 2), 1, INK, leading=9)
    cv.hline(16, 121, 992, INK, 2)

    # 4. four lead stories
    for i, (region, field, head, summ, tag, src) in enumerate(LEADS):
        x = 16 + i * 248
        LEAD_DRAW[i](cv, x, 127, 240, 74)
        # number + label
        cv.circle(x + 8, 213, 8, RED)
        num = str(i + 1)
        cv.text(x + 8 - text_width(num, 1) // 2, 210, num, 1, (255, 255, 255),
                bold=True)
        cv.text(x + 20, 210, region + " \u00b7 " + field, 1, RED, bold=True)
        cy = 222
        cy = draw_lines(cv, x, cy, capped(head, 20, 3), 2, INK, bold=True,
                        leading=16)
        cy = draw_lines(cv, x, cy + 4, capped(summ, 40, 4), 1, INK, leading=9)
        tagline = tag + " \u00b7 " + src
        cv.text(x, cy + 4, tagline, 1, RED, bold=True)
    cv.hline(16, 318, 992, INK, 2)

    # 5. twelve medium stories (4 columns x 3 rows)
    for i, (region, field, head, summ, tag, src, icon) in enumerate(MEDIUM):
        col, row = i % 4, i // 4
        x = 16 + col * 248
        y = 324 + row * 74
        draw_icon(cv, icon, x, y, 240, 24)
        label = str(i + 5) + "  " + region + " \u00b7 " + field
        cy = draw_lines(cv, x, y + 27, capped(label, 40, 1), 1, RED, bold=True,
                        leading=9)
        cy = draw_lines(cv, x, cy + 1, capped(head, 40, 2), 1, INK, bold=True,
                        leading=9)
        cy = draw_lines(cv, x, cy + 1, capped(summ, 40, 2), 1, INK, leading=9)
        cv.text(x, cy + 1, tag + " \u00b7 " + src, 1, RED, bold=True)
    cv.hline(16, 558, 992, INK, 2)

    # 6. big-number strip
    for i, (num, label) in enumerate(BIG_NUMBERS):
        x = 16 + i * 164
        cv.text_center(x, 564, 160, num, 3, RED, bold=True)
        ly = 590
        for line in capped(label, 26, 2):
            cv.text_center(x, ly, 160, line, 1, INK)
            ly += 9
    cv.hline(16, 610, 992, INK, 2)

    # 7. world map
    cv.text(16, 616, "WHERE IT HAPPENED", 1, INK, bold=True)
    for poly in CONTINENTS:
        cv.poly([ll(lon, lat) for lon, lat in poly], SAGE, SAGE_LINE)
    for n, (dx, dy) in DOTS.items():
        cv.circle(dx, dy, 7, RED)
        s = str(n)
        cv.text(dx - text_width(s, 1) // 2, dy - 3, s, 1, (255, 255, 255),
                bold=True)
    cv.text(20, 736, "Numbered dots: stories 1-16", 1, INK)
    cv.hline(16, 748, 992, INK, 2)

    # 8. ALSO ON list, two columns
    cv.text(16, 754, "ALSO ON SATURDAY 21 NOVEMBER", 1, INK, bold=True)
    for j, (num, head, src) in enumerate(ALSO_ON):
        col = 0 if j < 16 else 1
        x = 16 if col == 0 else 520
        y = 770 + (j % 16) * 10
        cv.text(x, y, str(num), 1, RED, bold=True)
        cv.text(x + 24, y, head + " \u2014 " + src, 1, INK)

    # 9. DATE CHECK box
    cv.rect(16, 936, 992, 2, RED)
    cv.rect(16, 992, 992, 2, RED)
    cv.rect(16, 936, 2, 58, RED)
    cv.rect(1006, 936, 2, 58, RED)
    cv.text(28, 941, "DATE CHECK \u2014 LEFT OUT AS OLDER NEWS", 1, RED,
            bold=True)
    for i, item in enumerate(DATE_CHECK):
        cv.text(28, 951 + i * 8, "\u2022  " + item, 1, INK)

    # 10. footer
    cv.text_center(16, 999, 992,
                   "Every story here happened, or was first reported, on "
                   "Saturday 21 November 2026.", 1, INK)
    cv.text_center(16, 1009, 992,
                   "Sources: Reuters, AP, BBC, France 24, Al Jazeera, "
                   "Guardian, and others.", 1, INK)
    return cv


def check_font_coverage():
    """Fail loudly if any character used is missing from the font."""
    texts = [mast for mast in ("Saturday 21 November 2026",)]
    for region, field, head, summ, tag, src in LEADS:
        texts += [region, field, head, summ, tag, src]
    for region, field, head, summ, tag, src, _ in MEDIUM:
        texts += [region, field, head, summ, tag, src]
    for num, head, src in ALSO_ON:
        texts += [str(num), head, src]
    for num, label in BIG_NUMBERS:
        texts += [num, label]
    for label, text in TIMELINE:
        texts += [label, text]
    texts += DATE_CHECK
    missing = sorted({ch for t in texts for ch in t if ch not in FONT})
    if missing:
        raise SystemExit("missing font glyphs: %r" % (missing,))


def main():
    check_font_coverage()
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(outdir, exist_ok=True)  # mkdir only; never delete the dir
    cv = build()
    data = encode_png(bytes(cv.buf), W, H)
    path = os.path.join(outdir, "entry.png")
    with open(path, "wb") as f:
        f.write(data)
    import hashlib
    print("wrote %s (%d bytes) sha256=%s"
          % (path, len(data), hashlib.sha256(data).hexdigest()))


if __name__ == "__main__":
    main()
