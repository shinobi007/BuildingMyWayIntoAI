#!/usr/bin/env python3
"""ProofLoop v0.1 — OpenAI Careers Ingestor

Small first step only:
1. Open a Google Docs "Web Page (.html, zipped)" export.
2. Find the HTML file inside.
3. Extract each role's title, team, displayed location,
   OpenAI careers URL, and Ashby application URL.
4. Validate the records and print a compact report.

Uses only the Python standard library.
"""

from __future__ import annotations

import argparse
import html
import json
import sys
import zipfile
from dataclasses import dataclass, asdict
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse


def unwrap_google_url(url: str | None) -> str | None:
    """Convert Google Docs redirect URLs back to their actual target URLs."""
    if not url:
        return None
    parsed = urlparse(url)
    if parsed.netloc in {"www.google.com", "google.com"} and parsed.path == "/url":
        query = parse_qs(parsed.query)
        if query.get("q"):
            return unquote(query["q"][0])
    return url


@dataclass
class Role:
    role_id: int
    title: str
    team: str
    display_location: str
    career_url: str
    apply_url: str


class CareersParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.roles: list[Role] = []
        self.current: dict | None = None
        self.capture_tag: str | None = None
        self.capture_text: list[str] = []
        self.capture_links: list[str] = []
        self.paragraphs: list[tuple[str, list[str]]] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        attrs = dict(attrs)
        if tag == "h2":
            self._flush_current()
            self.current = {}
            self.paragraphs = []
            self.capture_tag = "h2"
            self.capture_text = []
            self.capture_links = []
        elif tag == "p" and self.current is not None:
            self.capture_tag = "p"
            self.capture_text = []
            self.capture_links = []
        elif tag == "a" and self.capture_tag:
            href = attrs.get("href")
            if href:
                self.capture_links.append(unwrap_google_url(href) or href)

    def handle_data(self, data: str) -> None:
        if self.capture_tag:
            self.capture_text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "h2" and self.capture_tag == "h2" and self.current is not None:
            text = " ".join("".join(self.capture_text).split())
            self.current["title"] = html.unescape(text)
            self.current["career_url"] = self.capture_links[0] if self.capture_links else ""
            self.capture_tag = None
        elif tag == "p" and self.capture_tag == "p" and self.current is not None:
            text = " ".join("".join(self.capture_text).split())
            self.paragraphs.append((html.unescape(text), list(self.capture_links)))
            self.capture_tag = None

    def close(self) -> None:
        super().close()
        self._flush_current()

    def _flush_current(self) -> None:
        if not self.current:
            return

        useful = [(text, links) for text, links in self.paragraphs if text]
        team = useful[0][0] if len(useful) >= 1 else ""
        location = useful[1][0] if len(useful) >= 2 else ""

        apply_url = ""
        for text, links in useful:
            if text.lower() == "apply now" and links:
                apply_url = links[0]
                break

        role = Role(
            role_id=len(self.roles) + 1,
            title=self.current.get("title", ""),
            team=team,
            display_location=location,
            career_url=self.current.get("career_url", ""),
            apply_url=apply_url,
        )
        self.roles.append(role)
        self.current = None
        self.paragraphs = []


def load_html_from_zip(zip_path: Path) -> tuple[str, str]:
    with zipfile.ZipFile(zip_path) as zf:
        html_names = [n for n in zf.namelist() if n.lower().endswith((".html", ".htm"))]
        if not html_names:
            raise ValueError("No .html/.htm file found inside the ZIP.")
        if len(html_names) > 1:
            html_names.sort(key=lambda n: (n.count("/"), len(n)))
        chosen = html_names[0]
        raw = zf.read(chosen)
        return chosen, raw.decode("utf-8", errors="replace")


def validate(roles: list[Role]) -> list[str]:
    warnings: list[str] = []
    required = ("title", "team", "display_location", "career_url", "apply_url")

    for role in roles:
        for field in required:
            if not getattr(role, field):
                warnings.append(f"Role {role.role_id}: missing {field}")

        if role.career_url and "openai.com/careers/" not in role.career_url:
            warnings.append(f"Role {role.role_id}: unexpected career URL: {role.career_url}")
        if role.apply_url and "jobs.ashbyhq.com/openai/" not in role.apply_url:
            warnings.append(f"Role {role.role_id}: unexpected apply URL: {role.apply_url}")

    career_urls = [r.career_url for r in roles if r.career_url]
    apply_urls = [r.apply_url for r in roles if r.apply_url]
    if len(career_urls) != len(set(career_urls)):
        warnings.append("Duplicate OpenAI careers URL(s) detected")
    if len(apply_urls) != len(set(apply_urls)):
        warnings.append("Duplicate Ashby application URL(s) detected")

    return warnings


def main() -> int:
    ap = argparse.ArgumentParser(description="Extract OpenAI careers roles from a Google Docs HTML ZIP export.")
    ap.add_argument("zip_file", type=Path, help="Path to the Google Docs HTML ZIP export")
    ap.add_argument("--expected", type=int, default=None, help="Optional expected role count")
    ap.add_argument("--show", type=int, default=3, help="Show this many roles from the start and end")
    args = ap.parse_args()

    if not args.zip_file.exists():
        print(f"ERROR: file not found: {args.zip_file}", file=sys.stderr)
        return 2

    try:
        html_name, source = load_html_from_zip(args.zip_file)
    except Exception as exc:
        print(f"ERROR reading ZIP: {exc}", file=sys.stderr)
        return 2

    parser = CareersParser()
    parser.feed(source)
    parser.close()

    roles = parser.roles
    warnings = validate(roles)

    print("ProofLoop OpenAI Careers Ingestor v0.1")
    print(f"Source ZIP:       {args.zip_file}")
    print(f"HTML file:        {html_name}")
    print(f"Parsed roles:     {len(roles)}")

    if args.expected is not None:
        status = "PASS" if len(roles) == args.expected else "FAIL"
        print(f"Expected roles:   {args.expected}  [{status}]")

    print(f"Validation issues:{len(warnings):6d}")

    n = max(0, args.show)
    if roles and n:
        sample = roles[:n]
        if len(roles) > n:
            sample += roles[-n:]
        print("\nSample records:")
        for role in sample:
            print(json.dumps(asdict(role), ensure_ascii=False))

    if warnings:
        print("\nWarnings:")
        for warning in warnings[:25]:
            print(f"- {warning}")
        if len(warnings) > 25:
            print(f"- ... {len(warnings) - 25} more")

    return 0 if not warnings and (args.expected is None or len(roles) == args.expected) else 1


if __name__ == "__main__":
    raise SystemExit(main())
