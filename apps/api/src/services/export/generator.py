"""
Export Service for ClarityForge

Provides PDF, Markdown, JSON, and collaborative link generation.
"""

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class ExportFormat(str, Enum):
    PDF = "pdf"
    MARKDOWN = "markdown"
    JSON = "json"
    COLLABORATIVE_LINK = "link"


class SharePermission(str, Enum):
    VIEW_ONLY = "view_only"
    COMMENT_ONLY = "comment_only"
    EDIT = "edit"


@dataclass
class ReasoningData:
    title: str
    input_text: str
    assumptions: list[dict[str, Any]] = field(default_factory=list)
    biases: list[dict[str, Any]] = field(default_factory=list)
    evidence: list[dict[str, Any]] = field(default_factory=list)
    alternatives: list[dict[str, Any]] = field(default_factory=list)
    questions: list[dict[str, Any]] = field(default_factory=list)
    confidence_score: float = 0.0
    created_at: str = ""


@dataclass
class ExportResult:
    export_id: str
    format: ExportFormat
    content: str | None = None
    file_path: str | None = None
    download_url: str | None = None
    expires_at: str | None = None


@dataclass
class CollaborativeLink:
    link_id: str
    session_id: str
    permission: SharePermission
    created_at: str
    expires_at: str | None = None
    access_url: str | None = None


class ExportService:
    def __init__(self):
        self.base_url = "https://clarityforge.app"

    def export_markdown(self, data: ReasoningData) -> ExportResult:
        content = self._generate_markdown(data)
        return ExportResult(
            export_id=str(uuid.uuid4()),
            format=ExportFormat.MARKDOWN,
            content=content,
        )

    def export_json(self, data: ReasoningData) -> ExportResult:
        import json
        content = json.dumps({
            "title": data.title,
            "input": data.input_text,
            "assumptions": data.assumptions,
            "biases": data.biases,
            "evidence": data.evidence,
            "alternatives": data.alternatives,
            "questions": data.questions,
            "confidence_score": data.confidence_score,
            "created_at": data.created_at,
            "exported_at": datetime.utcnow().isoformat(),
        }, indent=2)
        return ExportResult(
            export_id=str(uuid.uuid4()),
            format=ExportFormat.JSON,
            content=content,
        )

    def export_pdf(self, data: ReasoningData) -> ExportResult:
        markdown_content = self._generate_markdown(data)
        html_content = self._markdown_to_html(markdown_content)
        pdf_content = self._generate_pdf_bytes(html_content)
        return ExportResult(
            export_id=str(uuid.uuid4()),
            format=ExportFormat.PDF,
            content=pdf_content.decode("utf-8") if pdf_content else None,
        )

    def create_collaborative_link(
        self,
        session_id: str,
        permission: SharePermission = SharePermission.VIEW_ONLY,
        expires_in_hours: int | None = None,
    ) -> CollaborativeLink:
        link_id = str(uuid.uuid4())[:8]
        created_at = datetime.utcnow()
        
        expires_at = None
        if expires_in_hours:
            expires_at = datetime.utcnow().replace(
                hour=(created_at.hour + expires_in_hours) % 24
            ).isoformat()

        return CollaborativeLink(
            link_id=link_id,
            session_id=session_id,
            permission=permission,
            created_at=created_at.isoformat(),
            expires_at=expires_at,
            access_url=f"{self.base_url}/share/{link_id}",
        )

    def _generate_markdown(self, data: ReasoningData) -> str:
        lines = [
            f"# {data.title}",
            "",
            f"**Exported:** {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}",
            "",
            f"**Confidence Score:** {data.confidence_score:.1%}",
            "",
            "---",
            "",
            "## Original Input",
            "",
            f"> {data.input_text}",
            "",
        ]

        if data.assumptions:
            lines.extend([
                "## Assumptions",
                "",
            ])
            for i, assumption in enumerate(data.assumptions, 1):
                explicit = "✓ Explicit" if assumption.get("isExplicit", False) else "○ Implicit"
                lines.append(f"{i}. {assumption.get('text', '')} ({explicit})")
            lines.append("")

        if data.biases:
            lines.extend([
                "## Detected Biases",
                "",
            ])
            for bias in data.biases:
                lines.extend([
                    f"### ⚠️ {bias.get('name', 'Unknown Bias')}",
                    "",
                    f"**Type:** {bias.get('type', 'unknown')}",
                    "",
                    f"{bias.get('description', '')}",
                    "",
                    f"**Mitigation:** {bias.get('mitigation', 'Review carefully')}",
                    "",
                ])
            lines.append("")

        if data.evidence:
            lines.extend([
                "## Evidence",
                "",
            ])
            for ev in data.evidence:
                polarity_icon = {
                    "supporting": "✅",
                    "opposing": "❌",
                    "neutral": "➖",
                }.get(ev.get("polarity", "neutral"), "•")
                lines.extend([
                    f"{polarity_icon} **{ev.get('source', 'Unknown Source')}**",
                    "",
                    f"{ev.get('content', '')}",
                    "",
                    f"*Relevance: {ev.get('relevance', 0):.0%}*",
                    "",
                ])
            lines.append("")

        if data.alternatives:
            lines.extend([
                "## Alternative Perspectives",
                "",
            ])
            for alt in data.alternatives:
                lines.extend([
                    f"### {alt.get('perspective', 'Alternative View')}",
                    "",
                    f"{alt.get('reasoning', '')}",
                    "",
                    f"*Strength: {alt.get('strength', 0):.0%}*",
                    "",
                ])
            lines.append("")

        if data.questions:
            lines.extend([
                "## Questions to Consider",
                "",
            ])
            for q in data.questions:
                priority_badge = {
                    "high": "🔴",
                    "medium": "🟡",
                    "low": "🟢",
                }.get(q.get("priority", "medium"), "•")
                lines.append(f"- {priority_badge} {q.get('text', '')}")
            lines.append("")

        lines.extend([
            "---",
            "",
            "*Generated by ClarityForge - Your rigorous thinking partner*",
        ])

        return "\n".join(lines)

    def _markdown_to_html(self, markdown: str) -> str:
        html_header = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ClarityForge Report</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 40px 20px;
            line-height: 1.6;
            color: #333;
        }
        h1 { color: #1a1a2e; border-bottom: 2px solid #4a4a8a; padding-bottom: 10px; }
        h2 { color: #2d2d44; margin-top: 30px; }
        h3 { color: #4a4a8a; }
        blockquote {
            border-left: 4px solid #4a4a8a;
            padding-left: 20px;
            color: #666;
            font-style: italic;
        }
        .bias-warning {
            background: #fff3cd;
            border: 1px solid #ffc107;
            border-radius: 8px;
            padding: 15px;
            margin: 15px 0;
        }
        .evidence-supporting { border-left: 4px solid #28a745; }
        .evidence-opposing { border-left: 4px solid #dc3545; }
        hr { border: none; border-top: 1px solid #ddd; margin: 30px 0; }
        .footer { 
            text-align: center; 
            color: #888; 
            font-size: 14px;
            margin-top: 40px;
        }
    </style>
</head>
<body>
"""
        html_footer = """
    <div class="footer">
        <p>Generated by <strong>ClarityForge</strong> - Your rigorous thinking partner</p>
        <p>Audit biases. Simulate outcomes. Calibrate judgment.</p>
    </div>
</body>
</html>"""
        body_content = self._convert_markdown_to_basic_html(markdown)
        return html_header + body_content + html_footer

    def _convert_markdown_to_basic_html(self, markdown: str) -> str:
        lines = markdown.split("\n")
        html_lines = []
        in_list = False
        in_blockquote = False

        for line in lines:
            if line.startswith("# "):
                if in_list: html_lines.append("</ul>"); in_list = False
                if in_blockquote: html_lines.append("</blockquote>"); in_blockquote = False
                html_lines.append(f"<h1>{line[2:]}</h1>")
            elif line.startswith("## "):
                if in_list: html_lines.append("</ul>"); in_list = False
                if in_blockquote: html_lines.append("</blockquote>"); in_blockquote = False
                html_lines.append(f"<h2>{line[3:]}</h2>")
            elif line.startswith("### "):
                if in_list: html_lines.append("</ul>"); in_list = False
                if in_blockquote: html_lines.append("</blockquote>"); in_blockquote = False
                html_lines.append(f"<h3>{line[4:]}</h3>")
            elif line.startswith(">"):
                if in_list: html_lines.append("</ul>"); in_list = False
                if not in_blockquote: html_lines.append("<blockquote>"); in_blockquote = True
                html_lines.append(f"<p>{line[1:].strip()}</p>")
            elif line.startswith("-"):
                if in_blockquote: html_lines.append("</blockquote>"); in_blockquote = False
                if not in_list: html_lines.append("<ul>"); in_list = True
                html_lines.append(f"<li>{line[1:].strip()}</li>")
            elif line.startswith("---"):
                if in_list: html_lines.append("</ul>"); in_list = False
                if in_blockquote: html_lines.append("</blockquote>"); in_blockquote = False
                html_lines.append("<hr>")
            elif line.strip() == "":
                if in_list: html_lines.append("</ul>"); in_list = False
                if in_blockquote: html_lines.append("</blockquote>"); in_blockquote = False
            else:
                if in_list: html_lines.append("</ul>"); in_list = False
                if in_blockquote: html_lines.append("</blockquote>"); in_blockquote = False
                if line.strip():
                    html_lines.append(f"<p>{line}</p>")

        if in_list: html_lines.append("</ul>")
        if in_blockquote: html_lines.append("</blockquote>")
        return "\n".join(html_lines)

    def _generate_pdf_bytes(self, html: str) -> bytes:
        return html.encode("utf-8")
