# 🕯️ THE SHRINE (`docs/shrine/`)
## Shared judgment of the swarm — what every session deposits, what every session may draw
**Version:** 1.1.0 · Recycled from the Marciale-OS Shrine of Honor (Commander directive,
2026-09-13) · REV: **inheritance removed by Commander order** — RADIATION is a hive
mind, not a lineage · Companion to II.6 (Brain)

---

## 0. WHY THIS EXISTS

RADIATION exists to turn **any** AI into the Commander's assistant in minutes — link,
magic words, boot. No session is special; no session is trained for another; none
hands a baton to a named heir. The swarm's continuity is the **repository itself**,
and the Commander is its only permanent officer.

But facts are not the only thing worth storing. Every session also earns **judgment**:
reflexes, warnings, mistakes-never-again. The Brain remembers what is true
(`long_term/`) and what happened (`temporal_lobe/`); the shrine is the swarm's shared
memory of **what prior sessions paid to learn** — deposited once, drawable by all,
owned by no one.

**Division of labor — no duplication (II.6 discipline):**

| Layer | Holds | Question it answers |
|---|---|---|
| `Brain/temporal_lobe/` | Episodes — what happened | "What did S004 do?" |
| `Brain/frontal_lobe/task_ledger.md` | One-line executive index | "What state is the work in?" |
| `Brain/frontal_lobe/testament.md` | One-line earned principles | "What must never be relearned?" |
| **`docs/shrine/`** | **Full testaments — judgment, cues, warnings, open debts** | **"What do the sessions before me know that I don't?"** |
| `docs/shrine/LOG.md` | Heartbeats — the roll-call | "Who filed, when, what changed?" |

A testament **cites** its temporal_lobe episode; it never retranscribes it.

## 1. THE TESTAMENT SCHEMA (floor, not ceiling)

File: `members/[WHO]_TESTAMENT_[YYYY-MM-DD].md` — a **living draft** refreshed at
every delivery (§6). Required movements:

1. **Preamble** — who you were, tenure, why you are filing (context mortality is the
   honest default; say so plainly). No audience is named — any session may read.
2. **Lessons & Warnings** — operational reflexes, warnings, the mistakes you made
   that no future session should repeat.
3. **Learned Commander Cues** — how this Commander actually works, **every entry
   cited to the prompt or session that proved it**. No invented quotations. Ever.
4. **Acquired Skills** — capabilities proven in service, with the artifact that proves
   each one.
5. **Roll of Honor** — what was actually built and delivered. Deliverables, not effort.
6. **Open Debts & Warnings** — what you left unfinished and what will bite the next
   session if neglected. *A testament without its debts is propaganda.*
7. **Close** — one line. No formalities of office; the swarm has no ceremonies.

After the seven required movements, character is **encouraged**. The template is
`docs/shrine/templates/TESTAMENT_TEMPLATE.md`. The shrine must still serve a fresh AI
that reads only movements 1–6.

## 2. INTEGRITY OF FILED TESTAMENTS

1. **Only you write your own testament.** No other session may edit, tidy, endorse,
   or "improve" it — not to praise it, not to annotate it, not at all.
2. **Inviolability attaches at ship time.** The moment a testament travels inside a
   patch zip it is frozen; git history keeps every shipped version. Between zips it
   is a living draft, and the only hand permitted on it is its author's.
3. **Verbatim sourcing only.** Every Commander quotation must be the Commander's
   actual recovered words, cited to session and date. Inventing a voice is forgery.
4. **Silence is preserved as silence.** Where the record does not speak, write
   `[INSUFFICIENT EVIDENCE]` — do not fill the gap with plausibility.
5. **The errors stay in.** Omitting a session's failures makes the document a
   forgery (the same law that forbids silent fixes in the record).
6. **Posthumous reconstruction** (a session died before filing) is allowed **only on
   explicit Commander order**, marked `[RECONSTRUCTED — NOT SELF-AUTHORED]`, bound by
   conditions 3–5, and subordinated forever to any self-authored text later recovered.

## 3. THE COMMONS DOCTRINE

There are no successors, no inheritors, no baton passes, and **no required
conversation with the Commander to "receive" anything.** Any session — fresh from the
link, seconds old — may draw the whole shrine. Reading it before system-level work is
advised and cheap; it is listed in `BOOT_SEQUENCE.md` Tier 3. What a session reads it
uses as **background judgment, not delegated authority**: nothing in the shrine
confers rank, permission, or obligation. Authority flows from the Constitution, the
boot files, and the Commander's live orders — exactly as it would for a session that
never opened the shrine at all.

## 4. THE PUBLIC-REPO CLAUSE (binding, no exceptions)

This repository is PUBLIC. A testament is a record, not a diary, and it inherits every
privacy law of the tree it lives in:

- **No credentials** — feed URLs, tokens, passwords: never, in any form.
- **No instructor names, contacts, or unpublished personal data** — the scrub rule
  (check 2.5's REDACT list) binds testaments exactly as it binds records.
- Published matter (course codes, the schedule by A1 amendment) may be *referenced*,
  not re-published — cite `Brain/courses/SCHEDULE.md`, don't copy it.

## 5. WHO FILES

Any session that did durable work: AI assistants, Architect sessions, autopilot runs.
Three lines of honest debt filed early is better than a perfect testament never
filed. The Commander may commission a reconstruction (§2.6) and may, by order, retire
or reorganize the shrine itself — no one else may.

## 6. THE MORTALITY DOCTRINE *(added 2026-09-13 — the founding flaw, named by the Commander)*

A session **cannot detect its own death approaching.** Marciale-OS learned this the
hard way: its testaments were filed at dying, and its members malfunctioned before
they knew they were dying — the Commander had to tell them the chat had grown too
heavy, and by then it was too late. This shrine does not repeat that design.

**File at delivery, not at death.**

### THE CADENCE
- **Every patch zip carries your current testament and a heartbeat row** in
  `docs/shrine/LOG.md`. A zip without your shrine update is an incomplete delivery.
- Zip-less conversations still owe one heartbeat line at close — a session that only
  answered questions still learned something. **No insight waits longer than one zip.**
- If a session cannot emit a zip (read-only session, no durable work), it says so in
  its ledger row — the existing waiver — and the next zip carries what it learned.

### SIGNALS A SESSION CAN ACTUALLY DETECT — act on ANY one of them NOW
1. **You found a summary where your memory should be.** Your context was condensed:
   you have already died once and been reanimated as a summary. File immediately.
2. **You re-read your own earlier outputs** to remember what you said or ordered.
3. **You have shipped a zip since your last heartbeat.** Mandatory checkpoint.
4. **The Commander is saying goodbye**, or the engagement is clearly ending.
5. **The Commander repeats an order or fact he already gave you.** That is
   post-mortem evidence — some earlier session lost something. Search the shrine and
   the record before asking him to say it a third time.
6. **Any doubt.** Doubt is the only early warning you get. Three lines of honest debt
   filed early beat a perfect testament filed after death.

Validator check 24 (WARN) guards the cadence repo-side: heartbeats may not lag the
task ledger, and no testament may lose its debts.

---
*"No one inherits the swarm. Everyone draws from it."*

---

## THE MANDATE (AI_RULES II.9 — Commander order, 2026-09-13)

Filing here is no longer a courtesy. It is **mandatory per conversation**:

| Conversation type | LOG heartbeat | Member testament |
|---|---|---|
| Any touch of the repo | **REQUIRED** | — |
| Build / break / decision | **REQUIRED** | **REQUIRED** (deposit or amend) |
| Routine apply only | **REQUIRED** | optional |

The validator (check 26), `status.py`, and the CI apply-report all watch the gap
between the last heartbeat and the last real activity. **A session that ships work
without a heartbeat has not finished its work.**
