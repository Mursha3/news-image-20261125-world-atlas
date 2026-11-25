"""Deterministic 1024x1024 world news infographic for Wednesday, 25 November 2026."""

import math
import os
import struct
import zlib
from pathlib import Path

WIDTH = 1024
HEIGHT = 1024

STROKE_FONT: dict[str, list[tuple[float, float, float, float]]] = {
    "A": [(0, 6, 2, 0), (2, 0, 4, 6), (0.8, 3.8, 3.2, 3.8)],
    "B": [(0, 0, 0, 6), (0, 0, 2.8, 0), (2.8, 0, 3.6, 0.8), (3.6, 0.8, 3.6, 2.1), (3.6, 2.1, 2.8, 2.9), (0, 2.9, 2.8, 2.9), (2.8, 2.9, 3.8, 3.7), (3.8, 3.7, 3.8, 5.2), (3.8, 5.2, 2.8, 6), (0, 6, 2.8, 6)],
    "C": [(3.8, 1.0, 2.8, 0), (2.8, 0, 1.0, 0), (1.0, 0, 0, 1.0), (0, 1.0, 0, 5.0), (0, 5.0, 1.0, 6), (1.0, 6, 2.8, 6), (2.8, 6, 3.8, 5.0)],
    "D": [(0, 0, 0, 6), (0, 0, 2.4, 0), (2.4, 0, 3.8, 1.4), (3.8, 1.4, 3.8, 4.6), (3.8, 4.6, 2.4, 6), (0, 6, 2.4, 6)],
    "E": [(0, 0, 0, 6), (0, 0, 3.6, 0), (0, 3.0, 2.8, 3.0), (0, 6, 3.6, 6)],
    "F": [(0, 0, 0, 6), (0, 0, 3.6, 0), (0, 3.0, 2.8, 3.0)],
    "G": [(3.8, 1.0, 2.8, 0), (2.8, 0, 1.0, 0), (1.0, 0, 0, 1.0), (0, 1.0, 0, 5.0), (0, 5.0, 1.0, 6), (1.0, 6, 3.0, 6), (3.0, 6, 3.8, 5.0), (3.8, 5.0, 3.8, 3.2), (2.0, 3.2, 3.8, 3.2)],
    "H": [(0, 0, 0, 6), (3.8, 0, 3.8, 6), (0, 3.0, 3.8, 3.0)],
    "I": [(0.8, 0, 3.0, 0), (1.9, 0, 1.9, 6), (0.8, 6, 3.0, 6)],
    "J": [(1.2, 0, 3.6, 0), (3.0, 0, 3.0, 4.8), (3.0, 4.8, 2.0, 6), (2.0, 6, 0.8, 6), (0.8, 6, 0, 4.8)],
    "K": [(0, 0, 0, 6), (3.8, 0, 0, 3.2), (1.2, 2.2, 3.8, 6)],
    "L": [(0, 0, 0, 6), (0, 6, 3.6, 6)],
    "M": [(0, 6, 0, 0), (0, 0, 2.0, 3.2), (2.0, 3.2, 4.0, 0), (4.0, 0, 4.0, 6)],
    "N": [(0, 6, 0, 0), (0, 0, 3.8, 6), (3.8, 6, 3.8, 0)],
    "O": [(1.0, 0, 2.8, 0), (2.8, 0, 3.8, 1.0), (3.8, 1.0, 3.8, 5.0), (3.8, 5.0, 2.8, 6), (2.8, 6, 1.0, 6), (1.0, 6, 0, 5.0), (0, 5.0, 0, 1.0), (0, 1.0, 1.0, 0)],
    "P": [(0, 0, 0, 6), (0, 0, 2.8, 0), (2.8, 0, 3.8, 0.9), (3.8, 0.9, 3.8, 2.3), (3.8, 2.3, 2.8, 3.2), (0, 3.2, 2.8, 3.2)],
    "Q": [(1.0, 0, 2.8, 0), (2.8, 0, 3.8, 1.0), (3.8, 1.0, 3.8, 5.0), (3.8, 5.0, 2.8, 6), (2.8, 6, 1.0, 6), (1.0, 6, 0, 5.0), (0, 5.0, 0, 1.0), (0, 1.0, 1.0, 0), (2.2, 4.4, 4.0, 6.2)],
    "R": [(0, 0, 0, 6), (0, 0, 2.8, 0), (2.8, 0, 3.8, 0.9), (3.8, 0.9, 3.8, 2.2), (3.8, 2.2, 2.8, 3.1), (0, 3.1, 2.8, 3.1), (1.8, 3.1, 3.8, 6)],
    "S": [(3.6, 0.8, 2.8, 0), (2.8, 0, 1.0, 0), (1.0, 0, 0.2, 0.8), (0.2, 0.8, 0.2, 2.1), (0.2, 2.1, 1.2, 2.9), (1.2, 2.9, 2.8, 3.1), (2.8, 3.1, 3.8, 3.9), (3.8, 3.9, 3.8, 5.2), (3.8, 5.2, 2.8, 6), (2.8, 6, 1.0, 6), (1.0, 6, 0.1, 5.1)],
    "T": [(0, 0, 4.0, 0), (2.0, 0, 2.0, 6)],
    "U": [(0, 0, 0, 5.0), (0, 5.0, 1.0, 6), (1.0, 6, 2.8, 6), (2.8, 6, 3.8, 5.0), (3.8, 5.0, 3.8, 0)],
    "V": [(0, 0, 2.0, 6), (2.0, 6, 4.0, 0)],
    "W": [(0, 0, 0.9, 6), (0.9, 6, 2.0, 2.5), (2.0, 2.5, 3.1, 6), (3.1, 6, 4.0, 0)],
    "X": [(0, 0, 3.8, 6), (3.8, 0, 0, 6)],
    "Y": [(0, 0, 2.0, 3.0), (4.0, 0, 2.0, 3.0), (2.0, 3.0, 2.0, 6)],
    "Z": [(0, 0, 3.8, 0), (3.8, 0, 0, 6), (0, 6, 3.8, 6)],
    "0": [(1.0, 0, 2.8, 0), (2.8, 0, 3.8, 1.0), (3.8, 1.0, 3.8, 5.0), (3.8, 5.0, 2.8, 6), (2.8, 6, 1.0, 6), (1.0, 6, 0, 5.0), (0, 5.0, 0, 1.0), (0, 1.0, 1.0, 0), (0.6, 5.0, 3.2, 1.0)],
    "1": [(0.8, 1.2, 2.0, 0), (2.0, 0, 2.0, 6), (0.8, 6, 3.2, 6)],
    "2": [(0.2, 1.2, 1.0, 0), (1.0, 0, 2.8, 0), (2.8, 0, 3.8, 1.0), (3.8, 1.0, 3.8, 2.3), (3.8, 2.3, 0, 6), (0, 6, 3.8, 6)],
    "3": [(0.2, 0.8, 1.0, 0), (1.0, 0, 2.8, 0), (2.8, 0, 3.8, 1.0), (3.8, 1.0, 3.8, 2.1), (3.8, 2.1, 2.6, 2.9), (1.4, 2.9, 2.6, 2.9), (2.6, 2.9, 3.8, 3.8), (3.8, 3.8, 3.8, 5.0), (3.8, 5.0, 2.8, 6), (2.8, 6, 1.0, 6), (1.0, 6, 0.2, 5.1)],
    "4": [(2.8, 6, 2.8, 0), (2.8, 0, 0, 4.0), (0, 4.0, 3.8, 4.0)],
    "5": [(3.6, 0, 0.4, 0), (0.4, 0, 0.2, 2.7), (0.2, 2.7, 2.8, 2.7), (2.8, 2.7, 3.8, 3.6), (3.8, 3.6, 3.8, 5.0), (3.8, 5.0, 2.8, 6), (2.8, 6, 0.8, 6), (0.8, 6, 0.2, 5.1)],
    "6": [(3.4, 0.7, 2.6, 0), (2.6, 0, 1.0, 0), (1.0, 0, 0, 1.2), (0, 1.2, 0, 5.0), (0, 5.0, 1.0, 6), (1.0, 6, 2.8, 6), (2.8, 6, 3.8, 5.0), (3.8, 5.0, 3.8, 3.6), (3.8, 3.6, 2.8, 2.8), (2.8, 2.8, 0, 2.8)],
    "7": [(0, 0, 3.8, 0), (3.8, 0, 1.4, 6)],
    "8": [(1.0, 0, 2.8, 0), (2.8, 0, 3.6, 0.9), (3.6, 0.9, 3.6, 2.1), (3.6, 2.1, 2.8, 2.9), (2.8, 2.9, 1.0, 2.9), (1.0, 2.9, 0.2, 2.1), (0.2, 2.1, 0.2, 0.9), (0.2, 0.9, 1.0, 0), (1.0, 2.9, 0, 3.8), (0, 3.8, 0, 5.1), (0, 5.1, 1.0, 6), (1.0, 6, 2.8, 6), (2.8, 6, 3.8, 5.1), (3.8, 5.1, 3.8, 3.8), (3.8, 3.8, 2.8, 2.9)],
    "9": [(3.8, 3.0, 1.0, 3.0), (1.0, 3.0, 0, 2.2), (0, 2.2, 0, 1.0), (0, 1.0, 1.0, 0), (1.0, 0, 2.8, 0), (2.8, 0, 3.8, 1.0), (3.8, 1.0, 3.8, 5.0), (3.8, 5.0, 2.8, 6), (2.8, 6, 0.6, 6)],
    ".": [(1.6, 5.4, 2.0, 5.4), (2.0, 5.4, 2.0, 6.0), (1.6, 6.0, 2.0, 6.0)],
    ",": [(1.8, 5.3, 1.3, 6.5)],
    ":": [(1.7, 1.8, 1.9, 2.0), (1.7, 5.3, 1.9, 5.5)],
    ";": [(1.7, 1.8, 1.9, 2.0), (1.8, 5.3, 1.3, 6.5)],
    "-": [(0.6, 3.0, 3.2, 3.0)],
    "+": [(0.4, 3.0, 3.4, 3.0), (1.9, 1.5, 1.9, 4.5)],
    "/": [(0.2, 5.8, 3.6, 0.2)],
    "$": [(3.4, 0.9, 2.6, 0.4), (2.6, 0.4, 1.0, 0.4), (1.0, 0.4, 0.3, 1.1), (0.3, 1.1, 0.3, 2.2), (0.3, 2.2, 1.2, 2.9), (1.2, 2.9, 2.7, 3.1), (2.7, 3.1, 3.6, 3.8), (3.6, 3.8, 3.6, 4.9), (3.6, 4.9, 2.7, 5.6), (2.7, 5.6, 1.0, 5.6), (1.0, 5.6, 0.2, 5.0), (1.9, -0.3, 1.9, 6.3)],
    "%": [(0.3, 5.6, 3.5, 0.4), (0.5, 0.6, 1.2, 0.6), (1.2, 0.6, 1.2, 1.3), (0.5, 1.3, 1.2, 1.3), (0.5, 0.6, 0.5, 1.3), (2.6, 4.7, 3.3, 4.7), (3.3, 4.7, 3.3, 5.4), (2.6, 5.4, 3.3, 5.4), (2.6, 4.7, 2.6, 5.4)],
    "&": [(3.2, 5.6, 0.6, 1.8), (0.6, 1.8, 0.8, 0.6), (0.8, 0.6, 1.8, 0.1), (1.8, 0.1, 2.8, 0.6), (2.8, 0.6, 2.6, 1.7), (2.6, 1.7, 0.4, 3.6), (0.4, 3.6, 0.4, 5.1), (0.4, 5.1, 1.4, 6.0), (1.4, 6.0, 2.7, 5.6), (2.7, 5.6, 3.6, 4.2)],
    "|": [(1.9, 0.0, 1.9, 6.0)],
    "'": [(1.9, 0.0, 1.7, 1.5)],
    "!": [(1.9, 0.2, 1.9, 4.1), (1.9, 5.4, 1.9, 5.9)],
    "(": [(2.8, 0, 1.4, 1.4), (1.4, 1.4, 1.4, 4.6), (1.4, 4.6, 2.8, 6)],
    ")": [(1.0, 0, 2.4, 1.4), (2.4, 1.4, 2.4, 4.6), (2.4, 4.6, 1.0, 6)],
}


class RasterCanvas:
    """Anti-aliased RGB raster surface backed by a flat bytearray."""

    def __init__(self, w: int, h: int, bg: tuple[int, int, int]):
        self.w = w
        self.h = h
        self.buf = bytearray([bg[0], bg[1], bg[2]] * (w * h))

    def blend(self, x: int, y: int, col: tuple[int, int, int], alpha: float):
        if x < 0 or y < 0 or x >= self.w or y >= self.h or alpha <= 0.0:
            return
        i = (y * self.w + x) * 3
        if alpha >= 0.999:
            self.buf[i], self.buf[i + 1], self.buf[i + 2] = col
            return
        inv = 1.0 - alpha
        self.buf[i] = int(self.buf[i] * inv + col[0] * alpha + 0.5)
        self.buf[i + 1] = int(self.buf[i + 1] * inv + col[1] * alpha + 0.5)
        self.buf[i + 2] = int(self.buf[i + 2] * inv + col[2] * alpha + 0.5)

    def rect(self, x0: int, y0: int, x1: int, y1: int, col: tuple[int, int, int], alpha: float = 1.0):
        x0, y0 = max(0, x0), max(0, y0)
        x1, y1 = min(self.w, x1), min(self.h, y1)
        if x0 >= x1 or y0 >= y1:
            return
        if alpha >= 0.999:
            row = bytes(col) * (x1 - x0)
            for y in range(y0, y1):
                s = (y * self.w + x0) * 3
                self.buf[s:s + len(row)] = row
        else:
            for y in range(y0, y1):
                for x in range(x0, x1):
                    self.blend(x, y, col, alpha)

    def rounded_rect(self, x0: float, y0: float, x1: float, y1: float, r: float, col: tuple[int, int, int], alpha: float = 1.0):
        ix0, iy0 = max(0, int(math.floor(x0 - 1))), max(0, int(math.floor(y0 - 1)))
        ix1, iy1 = min(self.w, int(math.ceil(x1 + 1))), min(self.h, int(math.ceil(y1 + 1)))
        cl, cr = x0 + r, x1 - r
        ct, cb = y0 + r, y1 - r
        for y in range(iy0, iy1):
            py = y + 0.5
            for x in range(ix0, ix1):
                px = x + 0.5
                d = math.hypot(max(cl - px, 0.0, px - cr), max(ct - py, 0.0, py - cb)) - r
                if d <= -0.5:
                    self.blend(x, y, col, alpha)
                elif d < 0.5:
                    self.blend(x, y, col, (0.5 - d) * alpha)

    def circle(self, cx: float, cy: float, r: float, col: tuple[int, int, int], alpha: float = 1.0):
        ix0, iy0 = max(0, int(math.floor(cx - r - 1.5))), max(0, int(math.floor(cy - r - 1.5)))
        ix1, iy1 = min(self.w, int(math.ceil(cx + r + 1.5))), min(self.h, int(math.ceil(cy + r + 1.5)))
        for y in range(iy0, iy1):
            dy = y + 0.5 - cy
            for x in range(ix0, ix1):
                d = math.hypot(x + 0.5 - cx, dy) - r
                if d <= -0.5:
                    self.blend(x, y, col, alpha)
                elif d < 0.5:
                    self.blend(x, y, col, (0.5 - d) * alpha)

    def polygon(self, pts: list[tuple[float, float]], col: tuple[int, int, int], alpha: float = 1.0):
        if len(pts) < 3:
            return
        iy0 = max(0, int(math.floor(min(p[1] for p in pts))))
        iy1 = min(self.h, int(math.ceil(max(p[1] for p in pts))) + 1)
        n = len(pts)
        for y in range(iy0, iy1):
            py = y + 0.5
            xs: list[float] = []
            for i in range(n):
                x1, y1 = pts[i]
                x2, y2 = pts[(i + 1) % n]
                if (y1 <= py < y2) or (y2 <= py < y1):
                    xs.append(x1 + (py - y1) * (x2 - x1) / (y2 - y1))
            xs.sort()
            for i in range(0, len(xs) - 1, 2):
                for x in range(max(0, int(math.floor(xs[i]))), min(self.w, int(math.ceil(xs[i + 1])))):
                    self.blend(x, y, col, alpha)

    def capsule(self, x1: float, y1: float, x2: float, y2: float, r: float, col: tuple[int, int, int], alpha: float = 1.0):
        pad = r + 1.5
        ix0, iy0 = max(0, int(math.floor(min(x1, x2) - pad))), max(0, int(math.floor(min(y1, y2) - pad)))
        ix1, iy1 = min(self.w, int(math.ceil(max(x1, x2) + pad))), min(self.h, int(math.ceil(max(y1, y2) + pad)))
        vx, vy = x2 - x1, y2 - y1
        l2 = vx * vx + vy * vy
        for y in range(iy0, iy1):
            py = y + 0.5
            for x in range(ix0, ix1):
                px = x + 0.5
                t = 0.0 if l2 <= 1e-9 else max(0.0, min(1.0, ((px - x1) * vx + (py - y1) * vy) / l2))
                d = math.hypot(px - (x1 + t * vx), py - (y1 + t * vy)) - r
                if d <= -0.5:
                    self.blend(x, y, col, alpha)
                elif d < 0.5:
                    self.blend(x, y, col, (0.5 - d) * alpha)

    def measure(self, text: str, size: float) -> float:
        if not text:
            return 0.0
        sc = size / 6.0
        total = 0.0
        for ch in text.upper():
            total += (3.3 if ch == " " else 5.0) * sc
        return max(0.0, total - 1.0 * sc)

    def text(self, s: str, x: float, y: float, size: float, col: tuple[int, int, int], thickness: float = 0.115):
        sc = size / 6.0
        sr = max(0.7, size * thickness)
        cx = x
        for ch in s.upper():
            if ch == " ":
                cx += 3.3 * sc
                continue
            segs = STROKE_FONT.get(ch)
            if segs:
                for x1, y1, x2, y2 in segs:
                    self.capsule(cx + x1 * sc, y + y1 * sc, cx + x2 * sc, y + y2 * sc, sr, col)
            cx += 5.0 * sc

    def text_fit(self, s: str, x: float, y: float, max_w: float, size: float, col: tuple[int, int, int], thickness: float = 0.115):
        w = self.measure(s, size)
        sz = size if w <= max_w or w <= 0 else size * (max_w / w)
        self.text(s, x, y + (size - sz) * 0.45, sz, col, thickness)

    def text_center(self, s: str, cx: float, y: float, size: float, col: tuple[int, int, int], thickness: float = 0.115):
        self.text(s, cx - self.measure(s, size) / 2.0, y, size, col, thickness)

    def encode_png(self) -> bytes:
        raw = bytearray()
        stride = self.w * 3
        for y in range(self.h):
            raw.append(0)
            raw.extend(self.buf[y * stride:(y + 1) * stride])

        def chunk(tag: bytes, payload: bytes) -> bytes:
            return struct.pack(">I", len(payload)) + tag + payload + struct.pack(">I", zlib.crc32(tag + payload) & 0xFFFFFFFF)

        ihdr = struct.pack(">IIBBBBB", self.w, self.h, 8, 2, 0, 0, 0)
        return b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) + chunk(b"IDAT", zlib.compress(bytes(raw), 9)) + chunk(b"IEND", b"")


def art_space(c: RasterCanvas, x: int, y: int, w: int, h: int):
    c.rounded_rect(x, y, x + w, y + h, 8, (15, 23, 42))
    for sx, sy in [(26, 22), (74, 18), (118, 34), (168, 20), (212, 76), (48, 78)]:
        c.circle(x + sx, y + sy, 1.8, (226, 232, 240))
    # Orbital arc from rocket to station
    for t in range(6):
        c.circle(x + 76 + t * 8, y + 48 - t * 2, 1.5, (56, 189, 248))
    c.polygon([(x + 42, y + 64), (x + 56, y + 26), (x + 70, y + 64)], (248, 250, 252))
    c.polygon([(x + 49, y + 64), (x + 56, y + 88), (x + 63, y + 64)], (249, 115, 22))
    c.rect(x + 114, y + 44, x + 216, y + 56, (148, 163, 184))
    c.rect(x + 132, y + 26, x + 144, y + 74, (56, 189, 248))
    c.rect(x + 186, y + 26, x + 198, y + 74, (56, 189, 248))
    c.rounded_rect(x + 244, y + 14, x + w - 14, y + h - 14, 8, (2, 132, 199))
    c.text_fit("SHENZHOU-24", x + 258, y + 25, w - 286, 17, (255, 255, 255), 0.115)
    c.text_fit("CN + PK CREW", x + 258, y + 58, w - 286, 13, (224, 242, 254), 0.11)


def art_hormuz(c: RasterCanvas, x: int, y: int, w: int, h: int):
    c.rounded_rect(x, y, x + w, y + h, 8, (254, 242, 242))
    # Drone intercept burst in upper sky
    c.capsule(x + 34, y + 20, x + 84, y + 36, 1.8, (185, 28, 28))
    c.circle(x + 88, y + 28, 5, (234, 88, 12))
    c.rect(x + 14, y + 66, x + 224, y + h - 10, (30, 64, 175))
    c.polygon([(x + 42, y + 66), (x + 172, y + 66), (x + 158, y + 48), (x + 54, y + 48)], (51, 65, 85))
    c.circle(x + 128, y + 52, 15, (220, 38, 38))
    c.circle(x + 128, y + 52, 7, (251, 191, 36))
    # Spiky naval mine
    mx, my = x + 196, y + 56
    for dx, dy in [(12, 0), (-12, 0), (0, 12), (0, -12), (9, 9), (-9, -9), (9, -9), (-9, 9)]:
        c.capsule(mx, my, mx + dx, my + dy, 1.8, (15, 23, 42))
    c.circle(mx, my, 8, (15, 23, 42))
    c.rounded_rect(x + 244, y + 14, x + w - 14, y + h - 14, 8, (185, 28, 28))
    c.text_fit("2 TANKERS", x + 258, y + 25, w - 286, 17, (255, 255, 255), 0.115)
    c.text_fit("4 DRONES DOWN", x + 258, y + 58, w - 286, 13, (254, 202, 202), 0.11)


def art_tariffs(c: RasterCanvas, x: int, y: int, w: int, h: int):
    c.rounded_rect(x, y, x + w, y + h, 8, (240, 253, 244))
    # Tariff bars
    c.rounded_rect(x + 28, y + 22, x + 82, y + 84, 4, (5, 150, 105))
    c.text_center("20%", x + 55, y + 44, 16, (255, 255, 255), 0.115)
    c.rounded_rect(x + 100, y + 36, x + 154, y + 84, 4, (16, 185, 129))
    c.text_center("15%", x + 127, y + 52, 16, (255, 255, 255), 0.115)
    c.text_fit("CN vs EU", x + 166, y + 42, 68, 12, (6, 95, 70), 0.11)
    c.rounded_rect(x + 244, y + 14, x + w - 14, y + h - 14, 8, (4, 120, 87))
    c.text_fit("US TARIFFS", x + 258, y + 25, w - 286, 17, (255, 255, 255), 0.115)
    c.text_fit("30 FREED COL", x + 258, y + 58, w - 286, 13, (209, 250, 229), 0.11)


def art_courts(c: RasterCanvas, x: int, y: int, w: int, h: int):
    c.rounded_rect(x, y, x + w, y + h, 8, (245, 243, 255))
    # Courthouse columns + pediment
    c.polygon([(x + 30, y + 34), (x + 92, y + 16), (x + 154, y + 34)], (91, 33, 182))
    for px in (44, 72, 100, 128):
        c.rect(x + px, y + 36, x + px + 10, y + 76, (109, 40, 217))
    c.rect(x + 28, y + 76, x + 156, y + 86, (91, 33, 182))
    c.text_fit("COURTS", x + 168, y + 42, 66, 13, (91, 33, 182), 0.115)
    c.rounded_rect(x + 244, y + 14, x + w - 14, y + h - 14, 8, (91, 33, 182))
    c.text_fit("EU & LEGAL", x + 258, y + 25, w - 286, 17, (255, 255, 255), 0.115)
    c.text_fit("SPAIN + PARIS", x + 258, y + 58, w - 286, 13, (221, 214, 254), 0.11)


def art_labor(c: RasterCanvas, x: int, y: int, w: int, h: int):
    c.rounded_rect(x, y, x + w, y + h, 8, (255, 247, 237))
    # Factory sawtooth roof
    c.polygon([(x + 24, y + 44), (x + 56, y + 24), (x + 56, y + 44), (x + 88, y + 24), (x + 88, y + 44), (x + 120, y + 24), (x + 120, y + 84), (x + 24, y + 84)], (194, 65, 12))
    c.text_fit("17K TK", x + 136, y + 26, 98, 18, (154, 52, 18), 0.115)
    c.text_fit("REJECTED", x + 136, y + 56, 98, 13, (154, 52, 18), 0.11)
    c.rounded_rect(x + 244, y + 14, x + w - 14, y + h - 14, 8, (180, 83, 9))
    c.text_fit("DHAKA", x + 258, y + 25, w - 286, 18, (255, 255, 255), 0.115)
    c.text_fit("PLANTS SHUT", x + 258, y + 58, w - 286, 13, (254, 215, 170), 0.11)


def art_climate(c: RasterCanvas, x: int, y: int, w: int, h: int):
    c.rounded_rect(x, y, x + w, y + h, 8, (239, 246, 255))
    cx, cy = x + 64, y + h / 2.0
    c.circle(cx, cy, 32, (29, 78, 216))
    c.polygon([(cx - 18, cy - 12), (cx + 10, cy - 20), (cx + 6, cy + 12), (cx - 14, cy + 14)], (34, 197, 94))
    c.text_fit("CLIMATE", x + 110, y + 26, 120, 17, (30, 58, 138), 0.115)
    c.text_fit("IOM WARNING", x + 110, y + 56, 120, 13, (30, 64, 175), 0.11)
    c.rounded_rect(x + 244, y + 14, x + w - 14, y + h - 14, 8, (30, 58, 138))
    c.text_fit("POPE LEO", x + 258, y + 25, w - 286, 18, (255, 255, 255), 0.115)
    c.text_fit("COP31 FALLOUT", x + 258, y + 58, w - 286, 13, (191, 219, 254), 0.11)


def render_nov25_edition(out_path: Path):
    c = RasterCanvas(WIDTH, HEIGHT, (240, 244, 248))

    # Masthead
    c.rect(0, 0, WIDTH, 118, (11, 19, 43))
    c.rect(0, 118, WIDTH, 124, (2, 132, 199))
    c.circle(66, 59, 34, (2, 132, 199))
    c.polygon([(46, 50), (68, 36), (82, 54), (62, 78)], (52, 211, 153))
    c.text("WORLD IN A DAY", 122, 22, 34, (255, 255, 255), 0.12)
    c.text("WEDNESDAY 25 NOVEMBER 2026", 124, 72, 20, (56, 189, 248), 0.115)
    c.rounded_rect(760, 22, 998, 96, 8, (23, 37, 84))
    c.text_center("25 NOV", 879, 34, 19, (255, 255, 255), 0.115)
    c.text_center("2026", 879, 64, 19, (250, 204, 21), 0.115)

    stories = [
        {
            "x": 24, "y": 144, "w": 480, "h": 262,
            "accent": (2, 132, 199),
            "tag": "SPACE & SCIENCE  |  CHINA & PAKISTAN",
            "art": art_space,
            "head": "SHENZHOU-24 DOCKS AT TIANGONG",
            "l1": "PAKISTANI ASTRONAUT IS 1ST FOREIGN GUEST",
            "l2": "LAUNCHED FROM JIUQUAN ON LONG MARCH 2F",
        },
        {
            "x": 520, "y": 144, "w": 480, "h": 262,
            "accent": (185, 28, 28),
            "tag": "CONFLICT & ENERGY  |  MIDDLE EAST",
            "art": art_hormuz,
            "head": "HORMUZ TANKERS HIT NAVAL MINES",
            "l1": "2 TANKERS BURN; 4 DRONES HIT RAS TANURA",
            "l2": "GAZA STRIKE KILLS HAMAS SECURITY CHIEF",
        },
        {
            "x": 24, "y": 422, "w": 480, "h": 262,
            "accent": (4, 120, 87),
            "tag": "TRADE & SECURITY  |  AMERICAS",
            "art": art_tariffs,
            "head": "US PLANS 20% CHINA, 15% EU TARIFFS",
            "l1": "NEW DUTIES TARGET INDUSTRIAL OVERCAPACITY",
            "l2": "COLOMBIA FORCES FREE 30 IN CARTAGENA",
        },
        {
            "x": 520, "y": 422, "w": 480, "h": 262,
            "accent": (91, 33, 182),
            "tag": "DIPLOMACY & LAW  |  EUROPE & US",
            "art": art_courts,
            "head": "EU KALLAS RIFT & ABREGO TO SPAIN",
            "l1": "ABREGO GARCIA DEPORTS TO MADRID; SARKOZY",
            "l2": "AU COURT CONVICTS LAMARRE-CONDON",
        },
        {
            "x": 24, "y": 700, "w": 480, "h": 262,
            "accent": (180, 83, 9),
            "tag": "LABOR & MIGRATION  |  ASIA",
            "art": art_labor,
            "head": "BANGLADESH WAGE STRIKES PERSIST",
            "l1": "UNIONS REJECT 17K TK FLOOR; PLANTS SHUT",
            "l2": "MALAYSIA PRESSED ON ROHINGYA RETURNS",
        },
        {
            "x": 520, "y": 700, "w": 480, "h": 262,
            "accent": (30, 58, 138),
            "tag": "CLIMATE & CRISES  |  WORLD",
            "art": art_climate,
            "head": "POPE WARNS AFTER COP31 FAILURE",
            "l1": "URGES ACTION AS CLIMATE CRISES ESCALATE",
            "l2": "IOM: AID CUTS LEAVE MIGRANT WOMEN EXPOSED",
        },
    ]

    for s in stories:
        x, y, w, h = s["x"], s["y"], s["w"], s["h"]
        c.rounded_rect(x + 3, y + 4, x + w + 3, y + h + 4, 12, (203, 213, 225))
        c.rounded_rect(x, y, x + w, y + h, 12, (255, 255, 255))
        c.rounded_rect(x + 12, y + 12, x + w - 12, y + 42, 6, s["accent"])
        c.text_fit(s["tag"], x + 22, y + 20, w - 44, 14, (255, 255, 255), 0.11)
        s["art"](c, x + 16, y + 50, w - 32, 100)
        c.text_fit(s["head"], x + 18, y + 166, w - 36, 20, (15, 23, 42), 0.115)
        c.text_fit(s["l1"], x + 18, y + 202, w - 36, 13, (51, 65, 85), 0.105)
        c.text_fit(s["l2"], x + 18, y + 228, w - 36, 13, (51, 65, 85), 0.105)

    c.rect(0, 980, WIDTH, HEIGHT, (11, 19, 43))
    c.text_center(
        "GLOBAL DAILY BRIEFING  |  WEDNESDAY 25 NOVEMBER 2026  |  6 REGIONS COVERED",
        WIDTH / 2.0,
        995,
        14,
        (226, 232, 240),
        0.105,
    )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(c.encode_png())


def main():
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    render_nov25_edition(out_dir / "entry.png")


if __name__ == "__main__":
    main()
