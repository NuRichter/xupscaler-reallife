from pathlib import Path


def parse_path(raw: str) -> Path:
    cleaned = raw.strip().strip('"').strip("'")
    p = Path(cleaned)
    if not p.exists():
        raise FileNotFoundError(f"File not found: {p}")
    if not p.is_file():
        raise ValueError(f"Path is not a file: {p}")
    return p.resolve()


def parse_scale(raw: str) -> int:
    value = raw.strip().lower().removesuffix("x")
    try:
        scale = int(value)
    except ValueError:
        raise ValueError(f"Invalid scale: '{raw}'. Use 2, 4, or 8.")
    if scale not in (2, 4, 8):
        raise ValueError(f"Scale must be 2, 4, or 8. Got: {scale}")
    return scale
