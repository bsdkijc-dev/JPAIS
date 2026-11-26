<div align="center">

<img src="assets/logo.png" alt="JPAIS: Judicial Policy and Artificial Intelligence System Logo" width="140">

# JPAIS: Judicial Policy and Artificial Intelligence System

### Neuro-symbolic AI and structured RAG for judicial knowledge and evidence-based legal policy analysis.

[![License](https://img.shields.io/badge/License-CC_BY_4.0_/_MIT-blue?style=flat)](LICENSE) ![Stack](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white) [![Kaggle](https://img.shields.io/badge/Kaggle-Dataset-20BEFF?style=flat&logo=kaggle&logoColor=white)](https://www.kaggle.com/datasets/judicialcollege/jpais-judicial-corpus)

[Documentation](National%20Court%20Census%202026.md) · [Kaggle](https://www.kaggle.com/datasets/judicialcollege/jpais-judicial-corpus) · [Repository](https://github.com/bsdkijc-dev/JPAIS)

</div>

---

**Reliable Neuro-Symbolic AI & Structured Retrieval-Augmented Generation for Judicial Knowledge, Caseflow Velocity, and Evidence-Based Legal Policy Analysis**

- **Principal Researcher:** Cecep Mustafa, Ph.D.
- **Host Institution:** Indonesian Judicial College (IJC)
- **Primary Workstation:** Dell Precision 7540 (Intel Xeon/Core, 64 GB RAM, NVIDIA Quadro T2000 4GB VRAM, Ubuntu Linux)
- **Deployment Model:** Sovereign Air-Gapped Setup · Local Bare-Metal Compute · Docker Native

---

## 1. Executive Overview

Generic probabilistic language models frequently suffer from generative hallucinations, misgrounded citations, and jurisdictional opacity. **JPAIS** implements a dual-layer neuro-symbolic architecture that couples:
1. **Symbolic Deterministic Verification:** A Neo4j Knowledge Graph enforcing statutory hierarchy, procedural rules, and legal definitions.
2. **Dense Semantic Retrieval:** A Qdrant Vector Engine indexing precedent rulings, case dockets, and ratio decidendi.
3. **Constrained Local Synthesis:** A quantized Ollama LLM (`qwen2.5:3b-instruct`) running locally on NVIDIA Quadro T2000 to produce auditable judicial bench memos without cloud leakage.
4. **Decision-Before-Assistance Protocol:** An ethical safeguard mandating that judges and legal clerks enter a provisional analysis prior to reviewing algorithmic recommendations.
5. **Cryptographic Provenance:** SHA-256 Write-Once-Read-Many (WORM) audit leaves for every decision cycle.

---

## 2. System Architecture

```text
               +---------------------------------------------+
               |        FASTAPI JUDICIAL SANDBOX API         |
               |      (Decision-Before-Assistance Gate)      |
               +----------------------+----------------------+
                                      |
                 +--------------------+--------------------+
                 |                                         |
                 v                                         v
   +---------------------------+             +---------------------------+
   |   NEO4J KNOWLEDGE GRAPH   |             |   QDRANT VECTOR ENGINE    |
   | (Symbolic Statutory Gate) |             |  (Empirical Case Search)  |
   |  - UU No. 37/2004         |             |  - Ratio Decidendi Index  |
   |  - UU No. 5/2004          |             |  - Commercial Court Dockets|
   |  - Legal Concept Ontology |             |  - Supreme Court PK Cases |
   +-------------+-------------+             +-------------+-------------+
                 |                                         |
                 +--------------------+--------------------+
                                      |
                                      v
               +---------------------------------------------+
               |        LOCAL OLLAMA INFERENCE ENGINE        |
               |   (Strictly Constrained Legal Synthesis)    |
               +----------------------+----------------------+
                                      |
                                      v
               +---------------------------------------------+
               |       SHA-256 PROVENANCE AUDIT LEAF         |
               +---------------------------------------------+

## Author and citation

**Author:** Cecep Mustafa, Indonesian Judicial College (IJC). ORCID: [0000-0003-0037-497X](https://orcid.org/0000-0003-0037-497X)

**Cite as:** Mustafa, C. (2026). *JPAIS: Judicial Policy and Artificial Intelligence System* [Computer software]. GitHub. https://github.com/bsdkijc-dev/JPAIS

Pilot corpus on Kaggle: https://www.kaggle.com/datasets/judicialcollege/jpais-judicial-corpus

GitHub also shows a "Cite this repository" button, built from `CITATION.cff`.

## Licence
Data: [CC BY 4.0](LICENSE). Code (scripts, notebooks, pipelines): [MIT](LICENSE-CODE). © 2026 Cecep Mustafa / Indonesian Judicial College (IJC) — ORCID 0000-0003-0037-497X.

---

<div align="center">

**JPAIS: Judicial Policy and Artificial Intelligence System**

[github.com/bsdkijc-dev/JPAIS](https://github.com/bsdkijc-dev/JPAIS)

</div>
