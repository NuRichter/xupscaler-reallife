import zipfile
from pathlib import Path

from PIL import Image


def build_output_stem(input_path: Path, scale: int) -> str:
    return f"{input_path.stem}_reallife_{scale}x"


def save_outputs(img: Image.Image, input_path: Path, scale: int) -> tuple[Path, Path]:
    stem = build_output_stem(input_path, scale)
    out_dir = input_path.parent

    img_path = out_dir / f"{stem}.png"
    img.save(img_path, format="PNG", optimize=False)

    zip_path = out_dir / f"{stem}.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(img_path, arcname=img_path.name)

    return img_path, zip_path
