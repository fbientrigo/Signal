"""Cheap factorized image reward for Signal Reverse.

This is intentionally not a scientific-correctness metric. It only helps rank
rendered candidates during chart reproduction.

Dependencies: numpy, Pillow.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image


def _rgb(path: Path, size: tuple[int, int]) -> np.ndarray:
    with Image.open(path) as src:
        image = src.convert("RGB").resize(size, Image.Resampling.LANCZOS)
    return np.asarray(image, dtype=np.float32) / 255.0


def _cosine(a: np.ndarray, b: np.ndarray, eps: float = 1e-8) -> float:
    av = a.ravel()
    bv = b.ravel()
    denom = float(np.linalg.norm(av) * np.linalg.norm(bv))
    if denom < eps:
        return 1.0 if np.allclose(av, bv) else 0.0
    return float(np.dot(av, bv) / denom)


def _edge_map(rgb: np.ndarray) -> np.ndarray:
    gray = 0.2126 * rgb[..., 0] + 0.7152 * rgb[..., 1] + 0.0722 * rgb[..., 2]
    gy, gx = np.gradient(gray)
    mag = np.hypot(gx, gy)
    scale = float(np.percentile(mag, 99))
    if scale > 0:
        mag = np.clip(mag / scale, 0, 1)
    return mag


def _hist(rgb: np.ndarray, bins: int = 24) -> np.ndarray:
    pieces = []
    for channel in range(3):
        h, _ = np.histogram(rgb[..., channel], bins=bins, range=(0, 1), density=True)
        pieces.append(h.astype(np.float32))
    h = np.concatenate(pieces)
    total = float(h.sum())
    return h / total if total else h


def score(reference: Path, candidate: Path, *, width: int = 512) -> dict[str, float]:
    with Image.open(reference) as ref_img:
        aspect = ref_img.height / ref_img.width
    size = (width, max(64, round(width * aspect)))

    ref = _rgb(reference, size)
    cand = _rgb(candidate, size)

    mae = float(np.mean(np.abs(ref - cand)))
    luminance_layout = max(0.0, 1.0 - mae)
    edge = max(0.0, _cosine(_edge_map(ref), _edge_map(cand)))
    color = max(0.0, _cosine(_hist(ref), _hist(cand)))
    total = 0.50 * edge + 0.30 * luminance_layout + 0.20 * color

    return {
        "total": round(total, 6),
        "edge_structure": round(edge, 6),
        "luminance_layout": round(luminance_layout, 6),
        "color_distribution": round(color, 6),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("reference", type=Path)
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--width", type=int, default=512)
    args = parser.parse_args()
    print(json.dumps(score(args.reference, args.candidate, width=args.width), indent=2))


if __name__ == "__main__":
    main()
