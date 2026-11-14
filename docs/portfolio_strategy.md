# Portfolio Strategy

## Current Diagnosis

The portfolio has strong material across analytics engineering, layered pipelines, documentation, and governance. What weakens the impression is not lack of substance, but lack of hierarchy and inconsistent messaging between the GitHub profile, the hub repository, and the GitHub Pages site.

Current issues:

- The public narrative can look closer to a collection of repositories than to a coherent portfolio thesis.
- Repository descriptions and README depth are not always aligned with the desired first impression.
- Some strategic documents still reflect an older hierarchy where revenue analytics was treated as the flagship.

## Strategic Direction

The portfolio should present a single professional thesis:

`Samuel Maia builds decision-ready data products with governance, quality controls, and controlled publishing.`

That thesis should be visible at three layers:

1. GitHub profile headline and summary
2. Pinned repository order
3. GitHub Pages project hierarchy and repository descriptions

## Target Portfolio Architecture (Updated)

### Layer 1: Flagship (current)

Use one repository to represent the highest level of maturity and architectural range:

- `Governed-Analytics-Platform`

Rationale: contracts, quality gates, lineage, controlled publishing, and reproducible validation evidence. It is a portfolio project (no corporate production claim).

### Layer 2: Core Proofs

Use two repositories to reinforce the flagship from complementary angles:

- `azure-databricks-governed-lakehouse`
- `central-automacao-operacoes`

### Layer 3: Complementary Proofs

Keep additional repositories visible as supporting evidence, without competing with the flagship:

- `aws-serverless-access-counter`
- `churn-prediction`
- `revenue-intelligence-platform-suite`

### Layer 4: Supporting Depth / Legacy

De-emphasize repositories that dilute the narrative (keep for history/redirects only):

- `samuelmaia-data-analyst`
- generic or older analysis-focused repositories

## Historical Note

Earlier drafts (before the 13/11/2026 validation update) treated revenue analytics repositories as the flagship. The current portfolio direction uses `Governed-Analytics-Platform` as the flagship to anchor the narrative on governed publishing, quality discipline, and defensible evidence.

## README Standard to Use Across Major Repositories

Every major repository should follow roughly this structure:

1. Headline
2. Business context
3. What problem it solves
4. Who it is for
5. Evidence and validation scope
6. Architecture
7. Data pipeline or system flow
8. Quality, governance, and CI/CD
9. Main outputs
10. Demo or usage
11. Repository structure
12. Links

## Naming and Presentation Rules

- Keep repository titles and descriptions in English when possible.
- Use Portuguese as secondary localized documentation.
- Avoid generic words like `portfolio`, `case`, or `analysis` without business context.
- Prefer names and descriptions that signal business domain, operating model, and analytical value.

## Immediate Priority Actions

1. Keep `samuelmaia-analytics` as the canonical entry point.
2. Ensure the GitHub Pages site highlights the flagship first (GAP), then Lakehouse and Central.
3. Update strategic documents to reflect the current hierarchy.
4. Keep complementary projects visible, but clearly secondary.
