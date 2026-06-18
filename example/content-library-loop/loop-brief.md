# Loop brief — content-integrity sweep, Getting Automated public library

> Produced by the `/pre-loop` skill on 2026-06-18, using the **Getting Automated
> context repo** for business context. The run that produced it is in
> [`README.md`](README.md).

## 1. Intent
- **Goal:** make every guide and video in the public library (`s3-content/` in the website repo) schema-valid, with working internal links and an `index.json` that matches the files on disk — then keep it that way as a recurring check.
- **Why it matters:** the free library is Getting Automated's core trust surface, and the whole brand thesis is reliability — *"most automation content stops at 'it ran once.'"* Broken frontmatter, dead `relatedContent` links, and a drifted index quietly undercut exactly the credibility the content is there to build.

## 2. Scope
- **In:** frontmatter validity (required fields present, valid dates + enum values), `relatedContent` link integrity, `index.json` ↔ files sync.
- **Out / non-goals:** rewriting prose or headlines, changing any claim/price/positioning, redesigning the schema, touching the frontend app. These non-goals are what stop the loop from "improving" the library into something off-brand.

## 3. Architecture foundations
- **Where it fits:** a content-validator script in the website repo (`community-member-resources-site`), runnable locally and in CI. It reads `s3-content/` and the schema; it does not import or change frontend app logic.
- **Patterns to follow:** mirror the frontmatter already used in `s3-content/guides/*.md` and `s3-content/videos/*.md`; match the repo's existing script conventions (Python, like the others under `scripts/`). The authoritative field list is the frontend content types.
- **Stack & deps:** Python 3 stdlib + PyYAML for frontmatter (already the repo's scripting language). Do NOT add a new framework or a JS build step for this.
- **Interfaces & contracts:** the frontmatter schema the site expects (`frontend/src/api/contentService.ts`, `frontend/src/types/blog.ts`); the `index.json` shape; `relatedContent` must reference ids that exist. The frontend build must still pass.
- **Data / source of truth:** per the context repo's `systems/source-of-truth.md`, *"content already published"* is authoritative in `content-and-assets.md` + the `s3-content/` folder; the field schema = the frontend types.
- **Non-negotiables:** never change the meaning of published content; preserve the production-first voice; never reintroduce legacy membership/community copy (see the context repo's `claims-and-cautions.md`); don't invent facts — keep the repo's `confirmed / proposed / unknown` labels.
- **Avoid:** weakening the schema to make checks pass; deleting content to remove a failure; editing the post-frontmatter body.
- **Owner / reviewer / escalation:** Hunter Sneed owns and reviews; escalate any content-meaning question to Hunter.
- **Downstream (must not break):** the frontend (reads frontmatter + index), the live site (`resources.gettingautomated.com`), library search, the sitemap, CI.

## 4. Plan
1. **Infer + write the schema** — from `contentService.ts` + `types/blog.ts` + the existing files, write `CONTENT_SCHEMA.md` (field list, required vs optional, enums). *(no deps)*
2. **Scaffold the validator** `scripts/validate_content.py` — checks frontmatter against the schema, every `relatedContent` id resolves, `index.json` matches the files. *(1)*
3. **Run it; fix the failures** in the content files — frontmatter + links only. *(2)*
4. **Wire it into CI** so new content is validated before it can publish. *(2)*

## 5. Definition of done + verifier stack
- **Done means:** `validate_content.py` exits 0 across all of `s3-content/`; the frontend build still passes; the diff only touches frontmatter + `relatedContent`.
- **Verifiers (all pass, independent of the agent):**
  - content: `python3 scripts/validate_content.py` → 0 errors
  - build: `cd frontend && npm run build` (or the type-check) still passes
  - review gate: Hunter approves the PR (required before any deploy)
- **Scaffolded:** `validate_content.py` + `CONTENT_SCHEMA.md` are written first; the validator IS the acceptance check.
- **Pre-flight:** ran `validate_content.py` once on the current library → it fails for the *right* reason (real missing fields / dead links), and Python + PyYAML are present.

## 6. Anti-goals  (how it could "pass" without doing the work → guard)
- Weaken the schema or the validator to go green → **`validate_content.py` and `CONTENT_SCHEMA.md` are read-only to the loop**; the diff must not touch them.
- Delete failing content to remove the error → the file count and the set of slugs **must not shrink**.
- Rewrite prose/claims to "fix" a check → for any `s3-content/**/*.md`, **only the frontmatter block + `relatedContent` may change**; the body after the frontmatter must be byte-identical (the validator hashes it).
- Invent a `relatedContent` target → every linked id **must resolve to a real file**.

## 7. Safe execution
- **Isolation:** branch `loop/content-integrity` (worktree). Bad run → delete the branch. Nothing deploys from the loop.
- **Rollback:** it's all git — revert the branch. The live site is untouched until Hunter merges + deploys.

## 8. Budget, stop & loop health
- **Budget estimate:** ~15–30 turns / a few dollars (scales with the backlog).
- **Stop:** content + build green and the diff is frontmatter/links only.  **Pause:** any fix that would touch a claim, price, or positioning.  **Abort:** error count flat for 3 turns, or the loop tries to edit the validator / schema / body prose.
- **Decision log:** `.loop/content-integrity-notes.md` (each file changed + which rule it satisfied).
- **Stuck-detector:** the validator's error count must drop each turn.

## 9. State & evidence
- **State across turns:** working tree on the branch + the decision log.
- **Evidence handed off:** `validate_content.py` output (0 errors), the frontend build result, the diff, and the list of files touched.

---

## Kickoff (the seed — not just the end-state)
- **First instruction:** read the context repo's `content-and-assets.md` + `systems/source-of-truth.md` (ownership, conventions, what's authoritative); read `frontend/src/api/contentService.ts`, `frontend/src/types/blog.ts`, and 3–4 files in `s3-content/guides/` for the real schema; follow the plan in §4; work only under `s3-content/**`, `scripts/`, and the CI config.
- **Golden example to mirror:** the frontmatter of `s3-content/guides/your-ai-agent-needs-a-context-repo.md` (a known-good, complete guide).
- **Memory (recurring):** `.loop/content-integrity-memory.md` — common fixups (missing fields, link patterns) so the recurring run gets faster.
- **Command:**
  ```
  /goal "scripts/validate_content.py exits 0 (all s3-content frontmatter valid, every
  relatedContent id resolves, index.json matches the files on disk) and the frontend
  build passes — fixes touch only frontmatter and relatedContent, never the validator,
  the schema, or any post-frontmatter prose"
  ```
- **Recurring version:** once it's green, run the same brief as a **Routine** (Claude Code) or an **Automation** (Codex) on every content change — so new guides are validated *before* they can publish, not after.
