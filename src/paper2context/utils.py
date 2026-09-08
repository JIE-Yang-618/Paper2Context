from __future__ import annotations
import hashlib, re
from pathlib import Path

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()

def clean_text(text: str) -> str:
    text = text.replace('\u00ad', '')
    text = re.sub(r'(?<=\w)-\n(?=[a-z])', '', text)
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def slug(text: str) -> str:
    s = re.sub(r'[^a-zA-Z0-9]+', '_', text.strip().lower()).strip('_')
    return s[:48] or 'section'

def estimate_tokens(text: str) -> int:
    return max(1, round(len(text) / 4))
