#!/usr/bin/env python3
"""Content-integrity validator for the Getting Automated public library.

Checks every markdown file under s3-content/<type>/ against the de-facto schema
for that content type, and verifies that internal relatedContent links resolve.

Exit 0 only if there are zero ERRORS. WARNINGS are recommended-but-missing fields
that need a human or a fact (a publish date, a thumbnail, a category) — they're
surfaced for review but do not fail the check, because the loop must not invent them.

Usage:  python3 scripts/validate_content.py [--root s3-content]

See CONTENT_SCHEMA.md for the field contract this enforces.
"""
import sys
import re
import argparse
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML is required:  pip install pyyaml")

# The identity field must equal the filename slug. Required for every type — it's
# the link target other content points at.
ID_FIELD = {}  # id-bearing types key off "id"; tools are keyed by their filename slug (name is a display label)

# Required fields = the de-facto contract (present across the whole corpus today),
# plus the identity field. Missing one of these is an ERROR.
REQUIRED = {
    "guides":    ["id", "title", "author", "publishDate", "lastUpdated", "category",
                  "difficulty", "readingTime", "description", "topics", "featured",
                  "relatedContent", "tracks"],
    "videos":    ["id", "title", "description", "lastUpdated", "tags",
                  "conceptsCovered", "tracks"],
    "use-cases": ["id", "title", "description", "summary", "tags", "category",
                  "lastUpdated", "primaryPlatform", "supportingPlatforms", "trigger",
                  "difficulty", "timeSaved", "teamImpact", "operationalOwner"],
    "workflows": ["id", "title", "description", "platform", "version", "author",
                  "lastUpdated", "difficulty", "estimatedTime", "workflowImage",
                  "blueprint", "requirements", "steps", "instructions", "tracks"],
    "tools":     ["name", "website", "category", "description", "logo", "hunterEndorsed",
                  "pricing", "features", "pros", "cons", "bestFor", "notIdealFor",
                  "alternatives", "gettingStarted", "resources", "rating",
                  "reviewCount", "lastUpdated"],
}

# Recommended-but-optional fields. Missing one is a WARNING (needs a human/fact).
RECOMMENDED = {
    "guides": ["thumbnail"],
    "videos": ["publishDate", "category", "videoUrl", "thumbnail", "relatedContent"],
}

LINK_FIELDS = ["relatedContent", "relatedPosts", "related"]
DATE_FIELDS = ["publishDate", "lastUpdated", "date"]
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}")


def load_frontmatter(path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---", text, re.S)
    if not m:
        return None, "no YAML frontmatter block"
    try:
        return (yaml.safe_load(m.group(1)) or {}), None
    except yaml.YAMLError as e:
        return None, f"unparseable frontmatter ({str(e).splitlines()[0]})"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="s3-content")
    args = ap.parse_args()
    root = Path(args.root)

    files, all_ids = [], set()
    errors, warns = [], []

    # Pass 1 — load every file, collect every known id.
    for ctype in REQUIRED:
        for p in sorted(root.glob(f"{ctype}/*.md")):
            fm, err = load_frontmatter(p)
            if err:
                errors.append((p, err))
                continue
            files.append((ctype, p, fm))
            all_ids.add(p.stem)  # every file is a valid link target by its filename slug
            idf = ID_FIELD.get(ctype, "id")
            if fm.get(idf):
                all_ids.add(str(fm[idf]))

    # Pass 2 — validate each file against its contract.
    for ctype, p, fm in files:
        idf = ID_FIELD.get(ctype, "id")
        slug = p.stem

        for field in REQUIRED[ctype]:
            if field not in fm or fm[field] in (None, "", []):
                bucket = errors if field == idf else warns
                bucket.append((p, f"missing required field '{field}'"))

        for field in RECOMMENDED.get(ctype, []):
            if field not in fm or fm[field] in (None, "", []):
                warns.append((p, f"missing recommended field '{field}'"))

        if fm.get(idf) and str(fm[idf]) != slug:
            errors.append((p, f"{idf} '{fm[idf]}' does not match filename slug '{slug}'"))

        for df in DATE_FIELDS:
            if df in fm and fm[df] not in (None, "") and not DATE_RE.match(str(fm[df])):
                errors.append((p, f"{df} '{fm[df]}' is not an ISO date (YYYY-MM-DD)"))

        for lf in LINK_FIELDS:
            if lf not in fm or fm[lf] in (None, ""):
                continue
            v = fm[lf]
            if isinstance(v, str):
                errors.append((p, f"{lf} is a string — must be a list (got '{v[:40]}')"))
                continue
            if not isinstance(v, list):
                errors.append((p, f"{lf} must be a list of ids"))
                continue
            for rid in v:
                if str(rid) not in all_ids:
                    errors.append((p, f"{lf} -> '{rid}' does not resolve to any content id"))

    def show(label, items):
        print(f"\n{label}: {len(items)}")
        for p, msg in sorted(items, key=lambda x: str(x[0])):
            print(f"  {p}: {msg}")

    show("ERRORS", errors)
    show("WARNINGS (review — not blocking)", warns)
    print("\n" + "=" * 56)
    print(f"{len(files)} files · {len(all_ids)} ids · {len(errors)} errors · {len(warns)} warnings")
    if errors:
        print("RESULT: FAIL")
        return 1
    print("RESULT: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
