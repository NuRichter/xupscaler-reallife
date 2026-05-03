import sys
from pathlib import Path

from .models.registry import REGISTRY, PIPELINE_ORDER, ModelEntry, WeightFile, MODELS_DIR


def _download_weight(entry: ModelEntry, wf: WeightFile) -> None:
    dest = entry.weight_dir / wf.filename
    if dest.exists():
        return

    dest.parent.mkdir(parents=True, exist_ok=True)

    if wf.hf_repo and wf.hf_path:
        from huggingface_hub import hf_hub_download
        print(f"  Downloading {wf.filename} from {wf.hf_repo} ...")
        hf_hub_download(
            repo_id=wf.hf_repo,
            filename=wf.hf_path,
            local_dir=str(entry.weight_dir),
            local_dir_use_symlinks=False,
        )
    elif wf.url:
        import requests
        from tqdm import tqdm
        print(f"  Downloading {wf.filename} from URL ...")
        r = requests.get(wf.url, stream=True, timeout=60)
        r.raise_for_status()
        total = int(r.headers.get("content-length", 0))
        with open(dest, "wb") as f, tqdm(total=total, unit="B", unit_scale=True) as bar:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
                bar.update(len(chunk))
    else:
        print(f"  [SKIP] {wf.filename}: no download source configured.", file=sys.stderr)


def ensure_models(model_ids: list[str] | None = None) -> list[str]:
    ids = model_ids or PIPELINE_ORDER
    skipped: list[str] = []

    for mid in ids:
        entry = REGISTRY[mid]
        if entry.manual:
            if not entry.ready:
                print(
                    f"  [MANUAL] {entry.display_name}: {entry.notes}\n"
                    f"           Place weights in: {entry.weight_dir}"
                )
                skipped.append(mid)
            continue

        try:
            for wf in entry.weights:
                _download_weight(entry, wf)
        except Exception as e:
            print(f"  [WARN] Failed to download {entry.display_name}: {e}", file=sys.stderr)
            skipped.append(mid)

    return skipped
