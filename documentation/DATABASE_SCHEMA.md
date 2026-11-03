# JPAIS Knowledge Graph Schema & Entity Specification

## Core Nodes & Unique Identifiers
- `Regulation`: Official normative acts (`id`, `regulation_number`, `year`, `title`, `jurisdiction`, `promulgation_date`, `status`, `verification_status`)
- `RegulationVersion`: Temporal versions reflecting amendment points (`id`, `version_number`, `effective_date`)
- `Article`: Normative provisions (`id`, `article_number`, `content`, `verification_status`)
- `Paragraph`: Granular sub-clauses (`id`, `paragraph_number`, `content`)
- `LegalConcept`: Formal legal terms and definitions (`id`, `canonical_name`, `domain`)
- `Institution`: Legislative, executive, or judicial entities (`id`, `name`, `type`)
- `CourtDecision`: Judicial rulings (`id`, `decision_number`, `court_level`, `decision_date`, `verification_status`)
- `JudicialPrinciple`: Legal ratio decidendi derived from court rulings (`id`, `statement`, `precedent_level`)
- `LegalIssue`: Core disputed questions of law (`id`, `subject`)

## Core Relationships
- `(:Regulation)-[:CONTAINS]->(:Article)`
- `(:Article)-[:CONTAINS]->(:Paragraph)`
- `(:Article)-[:REFERENCES]->(:LegalConcept)`
- `(:Regulation)-[:AMENDS]->(:Regulation)`
- `(:Regulation)-[:REPEALS]->(:Regulation)`
- `(:CourtDecision)-[:INTERPRETS]->(:Article)`
- `(:CourtDecision)-[:APPLIES]->(:JudicialPrinciple)`
- `(:CourtDecision)-[:RESOLVES]->(:LegalIssue)`
