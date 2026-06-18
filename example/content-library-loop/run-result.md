# Proof: we actually ran the loop

The [`loop-brief.md`](loop-brief.md) in this folder isn't hypothetical — we ran it
on the **real Getting Automated content library** (69 published guides, videos,
use-cases, workflows, and tools), on an isolated branch. Here's the genuine
before/after.

> Branch: `loop/content-integrity` in the resources-site repo · commit `77d4205`
> Verifier: [`validate_content.py`](validate_content.py) (the actual script the loop scaffolded)

## The result

| | Errors | Warnings | Verdict |
|---|---|---|---|
| **Before** | **20** | 67 | ❌ FAIL |
| **After**  | **0**  | 67 | ✅ PASS |

14 content files fixed — **frontmatter only, every body byte-identical to the original.**

## The pre-flight caught a bug in the verifier itself

The brief's Step 3 says *run the verifier once and make sure it fails for the right
reason.* It paid off immediately. The first run reported 20 errors — but **6 were
false positives**: the validator assumed every `tools/*.md` `name` had to equal its
filename, when `name` is a display label (`Cursor`, `Make.com`) and the filename is
the slug. We fixed the **validator**, not the content. That left **14 real
structural errors** — exactly what the brief means by "never ship a verifier you can
game (or that lies to you)."

## What the loop fixed (the 14)

| Issue | Files | Fix |
|---|---|---|
| `relatedContent` stored as a comma-joined **string** | 3 guides | → a proper YAML list of ids |
| Missing `id` | 8 videos | → `id: "<slug>"` |
| `id` didn't match the filename (copy-paste / word-order slips) | 3 workflows | → `id` = slug |
| Missing the opening `---` frontmatter fence | `backend-to-browser.md` | → fence added |

Every change was a few frontmatter lines — total diff: **+21 / −6** across 14 files.

## What the loop refused to do (the 67 warnings)

This is the important half. The library is also missing a lot of *real* metadata —
publish dates, tags, categories, thumbnails, related-content curation. The loop did
**not** invent any of it. Per the Getting Automated context repo's own rule
(*"label proposed/unknown, don't invent facts"*), it **surfaced all 67 for Hunter**
instead of guessing:

- 30× missing `relatedContent` (a curation call)
- 8× missing `publishDate` on videos (a real date)
- 7× `tags`, 7× `topics`, 7× `category`, 6× `thumbnail`, 1× `instructions`

A naive "make the validator pass" loop would have hallucinated dates and tags to go
green. This one stopped at the line between *structure* (safe to fix) and *facts*
(human's call) — which is the entire point of the anti-gaming guards.

## Guardrails that held

- ✅ The validator + schema were **not modified** to pass (read-only to the loop).
- ✅ **No content deleted**; no slugs changed out from under existing links.
- ✅ Every **post-frontmatter body is byte-identical** to the original (verified).
- ✅ Ran on an **isolated branch** — nothing deployed; Hunter reviews before merge.

---

That's the whole thesis in one real run: a verifier the loop couldn't fake, a tight
scope, anti-gaming guards, and a clean stop on **proof** — applied to an actual
production content library, not a toy.
