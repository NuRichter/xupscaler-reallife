import tempfile
from pathlib import Path

from PIL import Image

from .models import get_upscaler, REGISTRY, PIPELINE_ORDER


def run_pipeline(
    input_path: Path,
    scale: int,
    skip_ids: set[str] | None = None,
) -> Image.Image:
    skip_ids = skip_ids or set()
    img = Image.open(input_path).convert("RGB")

    with tempfile.TemporaryDirectory(prefix="xup_") as tmpdir:
        tmp = Path(tmpdir)
        current = img
        checkpoint_path = tmp / "stage.png"

        for model_id in PIPELINE_ORDER:
            entry = REGISTRY[model_id]

            if model_id in skip_ids or not entry.ready:
                status = "skipped (manual)" if entry.manual else "skipped (weights missing)"
                print(f"  [{entry.display_name}] {status}")
                continue

            print(f"  [{entry.display_name}] running ...")
            upscaler = get_upscaler(model_id)
            try:
                upscaler.load()
                current = upscaler.run(current, scale)
                current.save(checkpoint_path)
            except Exception as e:
                print(f"  [{entry.display_name}] FAILED: {e} - skipping stage")
            finally:
                upscaler.unload()

    return current
