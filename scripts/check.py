#!/usr/bin/env python3
"""Static checks for the site: required pages, both languages, links, head tags, no third-party requests.

Usage: python3 scripts/check.py [substring ...]
With arguments, only pages whose path contains a substring are checked (one-page check).
"""
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://starhunt.staysweet.dev"
LANGS = ("en", "sv")
SLUGS = ("", "privacy", "support", "delete-account")
ENTRIES = ("", "privacy", "support", "delete-account")
errors = []


def fail(page, message):
    errors.append(f"{page}: {message}")


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.metas, self.tags, self.title = [], [], [], ""
        self.h1 = 0
        self._in_title = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self.tags.append((tag, a))
        if tag == "h1":
            self.h1 += 1
        if tag == "title":
            self._in_title = True
        for key in ("href", "src"):
            if key in a:
                self.links.append(a[key])
        if tag == "meta":
            self.metas.append(a)

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False

    def handle_data(self, data):
        if self._in_title:
            self.title += data


def path_for(url_path):
    p = ROOT / url_path.lstrip("/")
    if url_path.endswith("/"):
        p = p / "index.html"
    return p


def parse(path):
    parser = Page()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser


def check_page(rel):
    path = ROOT / rel
    page = parse(path)
    for link in page.links:
        if link.startswith(("mailto:", "#")):
            continue
        if link.startswith(("https://", "http://")):
            if not link.startswith(BASE):
                continue  # outside links are plain anchors (checked below for resources)
            link = link[len(BASE):] or "/"
        link = link.split("#")[0].split("?")[0]
        if not link.startswith("/"):
            fail(rel, f"relative link {link}")
        elif not path_for(link).exists():
            fail(rel, f"broken link {link}")
    for tag, a in page.tags:
        loaded = (tag in ("script", "img") and a.get("src")) or (tag == "link" and a.get("rel") in ("stylesheet", "icon") and a.get("href"))
        if loaded and str(loaded).startswith(("http://", "https://")) and not str(loaded).startswith(BASE):
            fail(rel, f"loads a resource from another server: {loaded}")
    return page


def main():
    wanted = sys.argv[1:]
    selected = lambda rel: not wanted or any(w in rel for w in wanted)
    pages = [f"{lang}/{slug}/index.html" if slug else f"{lang}/index.html" for lang in LANGS for slug in SLUGS]
    pages += [f"{slug}/index.html" if slug else "index.html" for slug in ENTRIES] + ["404.html"]
    for w in wanted:
        if not any(w in rel for rel in pages):
            fail(w, "matches no page")

    for name in (".nojekyll", "CNAME", "404.html", "language.js", "styles.css", "assets/app-icon.png"):
        if not (ROOT / name).exists():
            fail(name, "missing")
    css = (ROOT / "styles.css").read_text(encoding="utf-8")
    if "color-scheme: light" not in css:
        fail("styles.css", "missing color-scheme: light")

    titles = {}
    for lang in LANGS:
        for slug in SLUGS:
            rel = f"{lang}/{slug}/index.html" if slug else f"{lang}/index.html"
            if not (ROOT / rel).exists():
                fail(rel, "required page missing")
                continue
            if not selected(rel):
                continue
            page = check_page(rel)
            html = (ROOT / rel).read_text(encoding="utf-8")
            if f'<html lang="{lang}">' not in html:
                fail(rel, f'html lang is not "{lang}"')
            if page.h1 != 1:
                fail(rel, f"expected one h1, found {page.h1}")
            meta = {m.get("name") or m.get("property"): m.get("content") for m in page.metas}
            if meta.get("color-scheme") != "light":
                fail(rel, 'meta color-scheme must be "light"')
            if meta.get("theme-color") != "#326454":
                fail(rel, 'meta theme-color must be the app accent "#326454"')
            for key in ("description", "og:title", "og:description", "og:url", "og:image", "og:locale", "twitter:card"):
                if not meta.get(key):
                    fail(rel, f"missing meta {key}")
            if "apple-itunes-app" in meta:
                fail(rel, "Smart App Banner before an App Store ID exists")
            if not any(t == "link" and a.get("rel") == "canonical" for t, a in page.tags):
                fail(rel, "missing canonical")
            hreflangs = {a.get("hreflang") for t, a in page.tags if t == "link" and a.get("rel") == "alternate"}
            if hreflangs != {"en", "sv", "x-default"}:
                fail(rel, f"hreflang set is {sorted(h for h in hreflangs if h)}")
            if 'class="skip-link"' not in html:
                fail(rel, "missing skip link")
            if "info@staysweet.dev" not in html:
                fail(rel, "missing contact address")
            titles.setdefault(slug, {})[lang] = page.title
            # Android coverage wherever the site names the platforms
            if slug in ("", "support", "privacy") and "Android" not in html:
                fail(rel, "does not mention Android")
        for slug in ENTRIES:
            rel = f"{slug}/index.html" if slug else "index.html"
            if not (ROOT / rel).exists():
                fail(rel, "language entry page missing")
            elif selected(rel):
                check_page(rel)
    for slug, by_lang in titles.items():
        if len(by_lang) == 2 and by_lang["en"] == by_lang["sv"] and slug:
            fail(slug, "Swedish title equals English title")
    if selected("404.html") and (ROOT / "404.html").exists():
        check_page("404.html")
    if selected("assetlinks") and (ROOT / ".well-known/assetlinks.json").exists():
        fail(".well-known/assetlinks.json", "not needed until Android App Links ship (README follow-ups)")

    # The privacy policy and deletion page must keep disclosing family sharing.
    for lang, words in (("en", ("push", "Export My Data", "reminders")), ("sv", ("pushnotiser", "Exportera mina uppgifter", "påminnelser"))):
        rel = f"{lang}/privacy/index.html"
        if selected(rel) and (ROOT / rel).exists():
            text = (ROOT / rel).read_text(encoding="utf-8")
            for w in words:
                if w.lower() not in text.lower():
                    fail(rel, f"privacy policy no longer mentions “{w}”")

    if errors:
        print("\n".join(errors))
        print(f"FAILED: {len(errors)} problem(s)")
        sys.exit(1)
    print("OK")


main()
