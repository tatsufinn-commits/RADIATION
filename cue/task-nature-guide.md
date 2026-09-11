# 🧭 TASK-NATURE GUIDE (`cue/task-nature-guide.md`)
## Tuple-Extraction Heuristics + Worked Examples
**Status:** heuristic guidance — informs judgment, never replaces it (III.3)

## SIGNAL HEURISTICS
| Signal in prompt | Suggests |
|---|---|
| "just tell me / quick / what is / who / when" | DELIVERABLE=answer, PERMANENCE=ephemeral, DEPTH=surface |
| "research / gather / collect / find sources / stockpile" | DELIVERABLE=corpus, PERMANENCE=stored |
| "write a research / write a paper / thesis / review" | DELIVERABLE=paper, PERMANENCE=stored |
| GitHub URL + "understand / how does it work / architecture" | DELIVERABLE=comprehension-map |
| "permanent reference / for the record / for the Core / canonical / definitive" | PERMANENCE=canonical → @Radiation |
| "exhaustive / complete / everything / deep dive" | DEPTH=exhaustive |
| "overview / briefly / at a glance" | DEPTH=surface |

## WORKED EXAMPLES (the Commander's canonical pair — why keyword-matching fails)
**1.1 "Write a research regarding [topic]"**
- Explicit: "write a research" → DELIVERABLE=paper. Implicit: research papers
  are kept → PERMANENCE=stored; unspecified depth → working.
- Tuple: (paper, stored, working) → **@Gather**, style research.md. FIRM ×3 → HIGH.

**1.2 "Research [topic] then write a paper regarding your findings"**
- Explicit: two verbs, one pipeline — "research" (corpus) feeding "write a
  paper" (paper). This is ONE @Gather task, not a two-stage session: the corpus
  is instrumental to the paper.
- Tuple: (paper, stored, working) → **@Gather**, style research.md. Same
  verdict as 1.1 despite ~zero shared keywords. THIS is task-nature assessment.

**Counter-example: "Research [topic] and then answer: is X true?"**
- Corpus AND verdict requested → E3: serial stages OR @Radiation if canonical
  signals present. State the choice in Extraction Notes.

## PERMANENCE — THE MOST-MISREAD ELEMENT
When in doubt between stored and canonical: choose STORED. Canonical (@Radiation)
requires explicit or lexicon-confirmed intent (E2). The cost asymmetry: a stored
result can be promoted later by Patch; a wrongly-canonical result pollutes the Core.
