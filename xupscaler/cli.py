import sys
import click

from .utils import parse_path, parse_scale


@click.group()
def main():
    pass


@main.command()
@click.argument("image_path", required=False)
@click.option("--scale", "-s", default=None, help="Upscale factor: 2, 4, or 8 (e.g. 4x)")
@click.option("--skip", multiple=True, help="Model IDs to skip (repeatable)")
@click.option("--no-download", is_flag=True, help="Skip auto-download of missing weights")
def run(image_path, scale, skip, no_download):
    """Upscale a real-life image through the full model pipeline."""
    from .downloader import ensure_models
    from .pipeline import run_pipeline
    from .output import save_outputs

    if not image_path:
        image_path = click.prompt("Image path")
    if not scale:
        scale = click.prompt("Scale (2, 4, or 8)")

    try:
        path = parse_path(image_path)
        scale_int = parse_scale(scale)
    except (FileNotFoundError, ValueError) as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

    click.echo(f"\nXUpscaler RealLife - {scale_int}x")
    click.echo(f"Input: {path}\n")

    skipped: set[str] = set(skip)

    if not no_download:
        click.echo("Checking model weights ...")
        auto_skipped = ensure_models()
        skipped |= set(auto_skipped)
        click.echo()

    click.echo("Running pipeline ...")
    result = run_pipeline(path, scale_int, skip_ids=skipped)

    click.echo("\nSaving output ...")
    img_path, zip_path = save_outputs(result, path, scale_int)

    click.echo(f"\nDone.")
    click.echo(f"  Image : {img_path}")
    click.echo(f"  ZIP   : {zip_path}")


@main.command()
def status():
    """Show download status of all model weights."""
    from .models.registry import REGISTRY, PIPELINE_ORDER

    click.echo("\nModel weight status:\n")
    for mid in PIPELINE_ORDER:
        entry = REGISTRY[mid]
        label = "ready" if entry.ready else ("manual" if entry.manual else "missing")
        color = "green" if entry.ready else ("yellow" if entry.manual else "red")
        click.echo(f"  {entry.display_name:<12} [{click.style(label, fg=color)}]")
    click.echo()
