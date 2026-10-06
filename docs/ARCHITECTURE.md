# Architecture

PaperGraph is organized as a research intelligence pipeline.

## Ingestion

The current version ingests a curated sample corpus containing AI, computer vision, and medical imaging papers. The ingestion interface can be extended to arXiv, PubMed, CrossRef, Semantic Scholar, or IEEE metadata sources.

## Extraction

The extractor reads paper titles and abstracts and identifies:

- methods
- datasets
- metrics

The current engine uses deterministic rules so the output is auditable. This is intentional: the system can later add LLM extraction, but the first layer should be reliable.

## Storage

PostgreSQL stores:

- papers
- authors
- extracted entities
- reported metrics
- graph edges

## Graph Builder

PaperGraph creates edges when papers share:

- task
- domain
- method
- dataset
- metric

Edges receive a similarity weight.

## Serving

FastAPI exposes:

- search
- paper detail
- graph data
- metric leaderboard
- system metrics

## Dashboard

Streamlit provides a research exploration interface.
