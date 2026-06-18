# Example: a real `/pre-loop` run (Getting Automated content library)

This is a worked example of what the **`/pre-loop`** skill produces. It was run on a
genuine Getting Automated task and grounded in a real **[context repo](https://github.com/Getting-Automated/context-repo)**
— the business-context repo that tells agents who Getting Automated is, what's
authoritative, and how work gets reviewed. That's why the brief it wrote reads like
the actual business and not a generic template.

**The prompt that kicked it off:**
> "Keep my public content library valid — I keep finding guides with missing frontmatter and dead related-links."

**The output:** [`loop-brief.md`](loop-brief.md) — the full contract the loop runs on.
Everything below is the run that produced it.

> ### 🧪 …and then we actually ran it → [`run-result.md`](run-result.md)
> On Hunter's real library, the loop took the validator it built
> ([`validate_content.py`](validate_content.py)) from **20 errors to 0** — fixing 14
> structural issues (frontmatter only, bodies untouched) and **refusing to invent**
> the 67 facts it was missing (flagged for review instead). Real before/after, on a branch.

---

## 1. What `/pre-loop` read first  (Step 1 — infer before asking)

Before asking a single question, the skill read the repos.

**From the context repo (the business):**
- `AGENTS.md` / `00-start-here.md` — Getting Automated is a production-automation business **and** a free public library; the position is *"reliability, not template theater."*
- `content-and-assets.md` — the public content is the trust surface; the pillars and the lead magnet.
- `systems/source-of-truth.md` — *"content already published"* is authoritative in `content-and-assets.md` + the `s3-content/` folder; owner = Hunter Sneed.
- `company/claims-and-cautions.md` — avoid legacy membership/community copy; use confidence labels.
- `workflows/agent-workflow.md` — cite sources, review before output, don't invent facts.

**From the website repo (the system being looped on):**
- `frontend/src/api/contentService.ts`, `frontend/src/types/blog.ts` — the frontmatter schema the site expects.
- `s3-content/guides/*.md`, `s3-content/videos/*.md` — the real, current frontmatter shape.
- `frontend/package.json` — the build command (the downstream check).

**What it inferred:** stack = Python scripts + markdown content + a TS frontend; convention = YAML frontmatter per the frontend types; owner = Hunter; nothing publishes without his review; the production-first voice must not drift.

## 2. What it asked  (the wizard — only the gaps)

It didn't re-ask anything it could infer from the repos. It surfaced five quick choices:

| Question | Answer |
|---|---|
| **Good fit to loop?** | Loop it — a real verifier exists once we scaffold a validator |
| **Scope?** | Frontmatter validity + `relatedContent` links + index sync. *Not* prose, claims, or positioning |
| **Run on a branch or in place?** | A branch (`loop/content-integrity`); nothing deploys |
| **What needs human approval?** | Hunter reviews the PR before any merge/deploy; pause on anything touching a claim or price |
| **Verifier — existing or scaffold one?** | Scaffold one — no content validator exists today |

## 3. Fitness check  (Step 5 — when *not* to loop)

✅ **Good loop.** It cleared every gate:

- **Real verifier** — a content validator we can build and run, so "done" is checkable independent of the agent.
- **Clear source of truth** — the frontend schema + the files; ownership is Hunter.
- **Reversible** — all git, on a branch, no auto-publish.
- **Reviewed** — Hunter approves before anything ships.

> If there had been *no* checkable "done" — say, *"make the guides more engaging"* — the skill would have **stopped here** and told you to define a checkable proxy first, instead of writing a brief.

## 4. What it wrote

- **[`loop-brief.md`](loop-brief.md)** — the full contract: architecture foundations, scope/non-goals, the verifier stack, the anti-gaming guards, safe execution, and the health signals.
- **A schema doc** (`CONTENT_SCHEMA.md`, in the website repo) — the inferred frontmatter schema, so the validator and the loop share one source of truth.

## 5. The kickoff it handed back

Not just an end-state — the full seed, pointed at the verifier stack and guarded against gaming:

```
/goal "scripts/validate_content.py exits 0 (all s3-content frontmatter valid, every
relatedContent id resolves, index.json matches the files on disk) and the frontend
build passes — fixes touch only frontmatter and relatedContent, never the validator,
the schema, or any post-frontmatter prose"
```

Plus: read the context repo's `content-and-assets.md` + `source-of-truth.md` and the
frontend content types first; mirror the frontmatter of a known-good guide
(`your-ai-agent-needs-a-context-repo.md`); work only under `s3-content/`, `scripts/`,
and CI.

**Recurring version:** once it's green, the same brief runs as a **Routine** (Claude
Code) or an **Automation** (Codex) on every content change — so new guides are
validated *before* they can publish, not after the fact.

---

*Want to see the blank version it fills in? → [`../../loop-brief-template.md`](../../loop-brief-template.md). A second filled example (adding rate limiting to an API) → [`../../loop-brief-example.md`](../../loop-brief-example.md).*
