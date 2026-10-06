# PaperGraph: Research Paper Intelligence Engine

PaperGraph is a research intelligence platform that ingests paper metadata, extracts methods/datasets/metrics from abstracts, builds relationships between papers, and exposes search, graph, and leaderboard views through an API and dashboard.

This project is built around AI and medical imaging research, including a sample entry for Mohammed Sufiyan's IEEE-published Pix2Pix-GAN lung segmentation paper.

## Why This Project Matters

Research papers contain useful structured knowledge, but it is usually trapped inside titles, abstracts, and PDFs.

PaperGraph turns research text into queryable intelligence:

- Which methods are used?
- Which datasets are evaluated?
- Which metrics are reported?
- Which papers are related by task, domain, or method?
- Which paper performs best on which dataset?

That makes it useful for literature reviews, research comparison, and AI/ML knowledge discovery.

## Architecture

```text
Research Paper Metadata
        |
        v
Entity Extraction
methods / datasets / metrics
        |
        v
PostgreSQL Metadata Store
papers / authors / entities / metrics
        |
        v
Graph Builder
paper-to-paper relationships
        |
        +--> FastAPI Search + Graph API
        |
        +--> Streamlit Dashboard
```

## Tech Stack

- Python
- PostgreSQL
- FastAPI
- Streamlit
- Pandas
- NetworkX-style graph modeling
- Scikit-learn-ready search layer
- Docker Compose
- Pytest

## Key Features

- Ingests a research corpus
- Extracts methods such as Pix2Pix GAN, GAN, U-Net, DenseNet, Transformer, nnU-Net
- Extracts datasets such as Montgomery, Shenzhen, ChestX-ray14, ISBI, Synapse
- Extracts metrics such as accuracy, Dice, IoU, AUC, precision, recall, F1-score
- Stores structured paper metadata in PostgreSQL
- Builds paper relationship graph edges
- Provides search API across titles, abstracts, tasks, domains, and extracted entities
- Provides metric leaderboard for comparing papers
- Provides Streamlit dashboard for exploration

## Quick Start: Local Demo

```bash
python3 demo_local.py
```

Outputs:

```text
sample_output/extracted_entities.csv
sample_output/paper_graph_edges.csv
sample_output/papergraph_report.html
```

## Full Docker Run

```bash
cp .env.example .env
docker compose up --build
```

Open:

```text
API docs:  http://localhost:8030/docs
Dashboard: http://localhost:8530
```

Ingest sample corpus:

```bash
curl -X POST http://localhost:8030/ingest/sample
```

Search:

```bash
curl "http://localhost:8030/search?q=lung%20segmentation"
```

## API Endpoints

- `GET /health`
- `POST /ingest/sample`
- `GET /papers`
- `GET /papers/{paper_id}`
- `GET /search`
- `GET /graph`
- `GET /metrics`
- `GET /leaderboard`

## Interview Explanation

> I built PaperGraph, a research intelligence engine that ingests paper metadata, extracts methods, datasets, and metrics from abstracts, stores structured knowledge in PostgreSQL, builds paper-to-paper relationships, and exposes search and graph exploration through FastAPI and Streamlit. I built it around AI and medical imaging research, including my IEEE paper on Pix2Pix-GAN-based lung segmentation.

## Resume Bullets

- Built PaperGraph, a research intelligence engine using Python, PostgreSQL, FastAPI, Streamlit, and Docker to extract methods, datasets, metrics, and relationships from AI research papers.
- Designed a structured metadata store for papers, authors, extracted entities, reported metrics, and paper-to-paper graph edges.
- Implemented NLP-style rule extraction for methods, datasets, and evaluation metrics across medical imaging and computer vision abstracts.
- Built search, graph, and leaderboard APIs to compare research papers by task, method, dataset, and reported performance.

## Project Structure

```text
papergraph-research-intelligence/
  dashboard/
  docs/
  sample_output/
  sql/
  src/
  tests/
  docker-compose.yml
  Dockerfile
  README.md
```
