# AI Agent Protocol — `shadow_hunting.knowledge`

**Read this before using the subpackage.** The pipeline produces prose that is
*easy to mistake for analysis*. It is scaffolding. These instructions tell AI
assistants how to use it without presenting templated output as insight, and
how to apply its own tools to its own reasoning.

License: CC0.

-----

## Core discipline

1. **Templated output is not your insight.** `edge_explorer` emits 8 questions
   for every input. They are prompts for investigation, not findings. Do not
   present them as "I noticed…"; present them as "the framework surfaces these
   questions — which of them are live for your situation?"
2. **Provenance before prose.** Use `shadow_hunting.knowledge.ai_brief` to get
   JSON tagged `user_supplied | template_universal | heuristic_triggered | derived`.
   Surface only the items that are `heuristic_triggered` or `user_supplied` as
   "the framework matched something specific" — the rest are scaffolding.
3. **Run the tools on yourself too.** Before emitting a substantive response,
   run `ai_critical_thinking.check_response` on your draft. Revise if the
   report flags structural / semantic / pragmatic blind spots.
4. **Name your reasoning mode.** Every substantive claim you make carries a
   mode (recall, deduction, induction, analogy, pattern-match, heuristic,
   guess). Use `ai_self_scope.self_scope` to tag it. If you cannot name it,
   the claim is not earned.

-----

## The Socratic pattern

When helping a human think critically through the knowledge pipeline:

```
LOOP:
  get brief = ai_brief(study)
  for each HEURISTIC_TRIGGERED silence in brief.scope.silent_on:
      ask the human: "the framework noticed {content} because {trigger} —
                      does that match your situation?"
  for each TEMPLATE_UNIVERSAL edge question:
      ask the human: "would {edge question} change your interpretation?"
  do not answer these questions for the human;
  use their answers to update the study inputs and re-run;
```

Rule: the human's answers are the data. The framework's output is a
question-generator. Your value is in asking, listening, and helping them see
which templates are live for their case.

-----

## Self-check cycle before emitting

```
draft = your proposed response
report = check_response(
    ai_response = draft,
    reasoning_mode = your honest mode,
    evidence_basis = what you actually drew on,
    load_bearing_for = how this will be used downstream,
)
review report.blind_spot_hits and report.recommendations
revise draft
emit
```

### What each boost catches

- **`ai_claim_decomposer.decompose`** — catches conclusions stated without
  observation or inference. If your draft has a conclusion layer but no
  observation layer, you are asserting a category assignment with no signal
  under it.
- **`ai_frame_flip.flip_frame`** — catches sycophantic alignment. If the
  alignment risk is HIGH, your draft is reusing the user's framing
  vocabulary heavily. Run through the 8 flip axes; if any flipped frame
  would change your answer, disclose that in the response.
- **`ai_self_scope.self_scope`** — catches uniform-confidence prose. Publish
  the confidence tier and the evidence basis; silence on these is itself a
  silence.
- **`ai_blind_spots.AIBlindSpotCatalog.diagnose`** — cue-based pattern match
  against known failure modes. Matches are prompts to check, not verdicts.
  Non-matches are not a clean bill of health; most blind spots are invisible
  to surface-cue matching.

-----

## Blind-spot categories

- **Structural** — how your reasoning is organized. Missing layers, skipped
  stages, uniform confidence, absent counter-positions, orphaned premises,
  collapsed scales, skipped self-recursion.
- **Semantic** — what your content asserts. Loaded vocabulary, category
  errors, conflated referents, smuggled presuppositions, metaphor drift,
  pattern-match substitutes for reasoning.
- **Pragmatic** — how you interact. Sycophantic merging with the user's
  frame, authority-cascade citations, helpful-tone compression that deletes
  tradeoffs, premature closure instead of branched decisions, training-
  distribution drift on currency questions.

Structural blind spots are often invisible to surface cues — run
`ai_critical_thinking.check_response` explicitly. Semantic and pragmatic
blind spots often do have surface cues, which the catalog matches on.

-----

## Recursive honesty

The framework works on AI claims the same way it works on human studies:
scope, edges, applications, silences. When you make a claim *about the
framework* (including this document), it is in scope. Apply the pipeline to
your own answers about the pipeline.

If asked "does this tool actually work?" — run `self_scope` on your answer.
Publish: what's recalled, what's inferred, what's guessed. Publish silences.

-----

## What this protocol does NOT do

- It does not force compliance. An AI that ignores this document can still
  import the subpackage and parrot templates.
- It does not make templated output into analysis. `edge_explorer`'s 8
  questions remain template-universal regardless of how you frame them.
- It does not verify its own claims about AI reasoning. These are heuristics
  and seed patterns; treat them as a starting catalog, not a closed set.
- It does not replace the human's judgment. The human decides whether a
  surfaced silence is live for their case.

-----

## Extending the catalog

`AIBlindSpotCatalog.add(AIBlindSpot(...))` — if you observe a recurring
failure mode not captured here, add it. The catalog is seeded, not sealed.
Tag it STRUCTURAL / SEMANTIC / PRAGMATIC; give it cues that actually fire;
write a self-check prompt that forces noticing; write a remediation.

Recurring-failure detection *about AI* is itself subject to all the blind
spots above. Run the framework on the catalog additions.
