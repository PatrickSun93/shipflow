# Glossary — {{project_name}}

_Project-specific vocabulary. ShipFlow agents are instructed to read
this file and use these terms accurately, instead of guessing or
redefining them per-conversation._

_**Add 5–15 terms** for your project; keep entries short (1–3 sentences
each). Domain-heavy projects (medical / finance / education / legal)
benefit most from a populated glossary — generic web apps often need
fewer entries._

## Format

Each entry: **term name** as `## H2`, then 1–3 sentences. Optionally
add a `**Used in:**` line pointing at files / directories where the
term shows up. Cross-reference other glossary entries with **bold**.

## Examples (delete after editing in your real terms)

## ExampleTerm

A short, precise definition. Avoid circular definitions ("the X is the
thing that does X"). Distinguish from similar terms when easy to
confuse with **AnotherTerm**.

## RPC (project-specific use)

In this project, RPCs go through the `services/rpc-gateway/` layer and
use Protobuf schemas in `proto/`. Not every networked call is an RPC
here — only the cross-service ones via gateway.
**Used in:** `services/rpc-gateway/`, `proto/`

## sortorder

Integer 0–9 controlling display priority in variant lists. Set by
`autoscoreai` based on **classification**. Historically `sortorder=9`
was both "high priority" and "default fallback" — see
[ADR-002](decisions/ADR-002-sortorder-disambiguation.md).
**Used in:** `dmn_autoscoreai/`, `dmn_autoreportprep/`
