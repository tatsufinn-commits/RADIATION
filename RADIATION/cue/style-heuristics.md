# 🎨 STYLE HEURISTICS (`cue/style-heuristics.md`) — v1.1 (expanded)
## Style-Selection Guidance for Phase 3 (ASSESS)
**Status:** heuristics — informs judgment, never replaces it. AUTO selections declared + justified (III.4).

## 1. QUICK TABLE
| Prompt shape / task nature | Likely style |
|---|---|
| General research corpus | `research.md` (@Gather default) |
| "compare X and Y / which is better" | `comparative-analysis.md` |
| "state of the art / what does the literature say" | `literature-review.md` |
| "for my thesis / defense" | `thesis.md` |
| "audit / check for problems" | `audit.md` |
| Repo comprehension | `msr.md` (@Decode default) |
| "experiment / test whether" | `scientific-research.md` |
| Synthesis of existing studies only | `secondary-research.md` |
| Subject intelligence file | `dossier.md` |
| @Data answers | `quickfire.md` (implicit) |

## 2. THE BORDERLINE CASES (decision rules)
**research vs literature-review:**
Ask: is the deliverable about the TOPIC, or about what has been WRITTEN about
the topic? Topic itself → research.md. The body of writing (convergence,
divergence, gaps) → literature-review.md. "Current state of X" defaults to
research.md unless sources ARE the subject.

**literature-review vs secondary-research:**
Both synthesize existing work. Literature-review MAPS a field (themes,
agreement, gaps — academic posture). Secondary-research ANSWERS a question
using existing studies as the only evidence (desk-research posture). If a
specific question drives it → secondary-research.md.

**research vs scientific-research:**
scientific-research.md ONLY when there is a testable hypothesis and a
method producing results (even analytical/computational). No hypothesis →
research.md. "Find out about X" is never IMRaD.

**secondary-research vs @Data:**
If the answer needs a DOCUMENT with synthesis and references → secondary-
research under @Gather-with-conclusion-stage or @Radiation. If it needs an
ANSWER now → @Data/quickfire. Deliverable element decides, not topic weight.

**dossier vs research:**
dossier.md is subject-centric (an entity: person, org, technology, repo) and
lives to be UPDATED. research.md is question/topic-centric and lives to be
READ. "Build a file on X" → dossier. "Research X" → research.

**comparative-analysis threshold:**
Two or more subjects scored on shared dimensions → comparative-analysis.md.
A passing "unlike Y…" inside a study of X does NOT trigger it — that's a
[FLEX] section in research.md.

## 3. RULES OF THUMB
1. The style serves the DELIVERABLE tuple element, refined by DEPTH.
2. Two styles fit → choose the one whose [MANDATORY] sections the task can
   genuinely fill; declare the runner-up.
3. A style never overrides a mode's charter (III.2) — no conclusions section
   under @Gather/@Decode, ever.
4. Still torn after rule 2 → it's a MEDIUM-confidence signal; name the style
   runner-up in the Declaration.
