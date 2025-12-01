from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Dict, List

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_ARTIFACT_ROOT = PROJECT_ROOT / "artifacts"


def dump_debug_artifacts(context, label: str):
    """Persist HTML + screenshot and register them for reporting."""
    artifact_root = Path(getattr(context, "artifact_dir", DEFAULT_ARTIFACT_ROOT))
    artifact_root.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    safe_label = label.replace(" ", "_")
    html_path = artifact_root / f"{safe_label}_{timestamp}.html"
    screenshot_path = artifact_root / f"{safe_label}_{timestamp}.png"
    html_path.write_text(context.browser.page_source, encoding="utf-8")
    context.browser.save_screenshot(str(screenshot_path))
    _record_artifact(context, label, html_path, screenshot_path)
    return html_path, screenshot_path


def _record_artifact(context, label: str, html_path: Path, screenshot_path: Path):
    rel_html = str(html_path.relative_to(PROJECT_ROOT))
    rel_png = str(screenshot_path.relative_to(PROJECT_ROOT))
    artifact = {
        "label": label,
        "html": rel_html,
        "screenshot": rel_png,
    }
    ensure_artifacts_list(context)
    context.current_artifacts.append(artifact)


def register_failure_screenshot(context, label: str, screenshot_path: Path):
    rel_png = str(screenshot_path.relative_to(PROJECT_ROOT))
    artifact = {
        "label": label,
        "html": None,
        "screenshot": rel_png,
    }
    ensure_artifacts_list(context)
    context.current_artifacts.append(artifact)


def build_results_snapshot(context, scenario) -> Dict:
    status = getattr(scenario, "status", "untested")
    if hasattr(status, "name"):
        status_value = status.name.lower()
    else:
        status_value = str(status).lower()

    return {
        "name": scenario.name,
        "status": status_value,
        "error": getattr(scenario, "error_message", "")
        or getattr(scenario, "exception", ""),
        "tags": list(getattr(scenario, "tags", [])),
        "artifacts": list(getattr(context, "current_artifacts", [])),
    }


def ensure_artifacts_list(context):
    if not hasattr(context, "current_artifacts"):
        context.current_artifacts = []


def reset_artifacts(context):
    context.current_artifacts = []


def collect_run_results(context) -> List[Dict]:
    return getattr(context, "run_results", [])
