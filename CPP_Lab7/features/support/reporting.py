from __future__ import annotations

from collections import defaultdict
from html import escape
from pathlib import Path
from typing import Dict, List

PROJECT_ROOT = Path(__file__).resolve().parents[2]
REPORTS_DIR = PROJECT_ROOT / "reports"
REPORTS_DIR.mkdir(exist_ok=True)

VARIANT_ORDER = ["variant1", "variant2", "variant3"]
STATUS_COLORS = {
    "passed": "#2ecc71",
    "failed": "#e74c3c",
    "skipped": "#95a5a6",
    "untested": "#f39c12",
}


def generate_variant_report(results: List[Dict]):
    grouped = defaultdict(list)
    for entry in results:
        variants = [tag for tag in entry["tags"] if tag.startswith("variant")]
        if not variants:
            grouped["unclassified"].append(entry)
        else:
            for variant in variants:
                grouped[variant].append(entry)

    html = [
        "<html><head><meta charset='utf-8'>",
        "<title>Lab 7 Variant Summary</title>",
        "<style>body{font-family:Arial,Helvetica,sans-serif;background:#111;color:#eee;padding:24px;}",
        "h1{color:#61dafb;} h2{margin-top:32px;color:#f1c40f;}",
        "table{width:100%;border-collapse:collapse;margin-top:12px;}th,td{padding:8px 10px;border-bottom:1px solid #333;}",
        ".status{font-weight:bold;padding:2px 6px;border-radius:4px;color:#111;}",
        ".artifacts a{color:#61dafb;text-decoration:none;margin-right:12px;} .artifacts a:hover{text-decoration:underline;}",
        ".scenario{background:#1b1b1b;border-radius:8px;padding:12px;margin-top:12px;} ",
        ".artifacts ul{margin:6px 0 0 18px;}",
        "</style></head><body>",
        "<h1>Lab 7 – Google Search Automation Summary</h1>",
        "<p>Generated automatically after Behave run. Attach alongside the default HTML report.</p>",
    ]

    for variant in VARIANT_ORDER + [key for key in grouped.keys() if key not in VARIANT_ORDER]:
        if variant not in grouped:
            continue
        html.append(f"<h2>{variant.title()} Results</h2>")
        for entry in grouped[variant]:
            status = entry["status"] or "untested"
            color = STATUS_COLORS.get(status, "#3498db")
            badge = f"<span class='status' style='background:{color}'>{status.upper()}</span>"
            html.append("<div class='scenario'>")
            html.append(f"<div>{badge} <strong>{escape(entry['name'])}</strong></div>")
            if entry["error"]:
                html.append(f"<div style='color:#ff7675;margin-top:6px;'>⚠ {escape(str(entry['error']))}</div>")
            if entry["artifacts"]:
                html.append("<div class='artifacts'><strong>Artifacts:</strong><ul>")
                for artifact in entry["artifacts"]:
                    html_link = (
                        f"<a href='../{artifact['html']}' target='_blank'>HTML</a>"
                        if artifact.get("html")
                        else ""
                    )
                    screenshot_link = (
                        f"<a href='../{artifact['screenshot']}' target='_blank'>Screenshot</a>"
                        if artifact.get("screenshot")
                        else ""
                    )
                    html.append(
                        f"<li>{escape(artifact['label'])}: {html_link} {screenshot_link}</li>"
                    )
                html.append("</ul></div>")
            html.append("</div>")

    html.append("</body></html>")
    output_path = REPORTS_DIR / "variant-summary.html"
    output_path.write_text("\n".join(html), encoding="utf-8")
    return output_path
