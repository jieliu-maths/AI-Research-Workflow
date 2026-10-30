# Mathematical post-review template

Use this for the human-facing part of every completed review. Keep it short
enough to scan, but include the decisive mathematics.

## Current theorem target

State the theorem or current implication in ordinary mathematical language.

## Established in this review

State one exact result with hypotheses and scope. This may be a proved identity,
a conditional lemma, or a counterexample showing that a specified method class
cannot work.

## Decisive formula or obstruction

Display the equation, inequality, test family, spectral fact, scaling mismatch,
or dependency cycle that decides the review.

## Consequences for the proof

Write the proof chain schematically, marking completed and missing arrows. For
example, using project-specific statements written in words,

\[
\text{proved input A}
+\boxed{\text{missing bridge lemma}}
+\text{proved input B}
\Longrightarrow
\text{target theorem}.
\]

Say explicitly whether the result closes a lemma, eliminates a route, changes
the theorem's plausible quantifiers, or leaves the proof map unchanged.

## Still missing

List only the mathematically blocking inputs. Separate unproved statements from
method classes already rejected.

## Next mathematical question

State one falsifiable question. Give both outcomes:

- if true, what estimate or proof arrow becomes available;
- if false, what route or theorem formulation must be abandoned or changed.

## Internal audit record

Record Run/Task/Proof IDs, the Critic verdict and scope, approval references,
and artifact/hash information here for internal use. Do not reproduce this
section in the normal response to the owner.

<!-- research-workflow:block review-output-boundary start -->
## Human-response boundary

Return only the mathematical sections above. Routine chronology, hashes,
protected-file checks, validator output, task/thread status, file lists,
schemas, sidecars, and code execution stay in the internal audit record.
Mention technical information only when an integrity/runtime problem affects
the mathematical conclusion or blocks progress, or when the owner explicitly
requests audit details.

If the report needs a symbol not already defined in the approved notation,
explain before first use what it denotes, its dependence and scaling when
relevant, why it is needed, its relation to existing symbols, and whether it is
local or proposed globally. Global notation remains a proposal until the owner
approves it.

For a negative candidate result, the mathematical response must distinguish
the formula as written, any repaired version, the precise class actually
excluded, and alternatives not tested. Name the decisive failure as topology,
operator calculus, scale, dependence on existing identities, quantifiers, or
localization. Do not describe a candidate failure as a route rejection unless
the evidence covers the route's defining mechanism.
<!-- research-workflow:block review-output-boundary end -->
