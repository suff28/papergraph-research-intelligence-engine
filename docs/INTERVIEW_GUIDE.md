# Interview Guide

## 30-Second Explanation

PaperGraph is a research intelligence engine. It ingests paper metadata, extracts methods, datasets, and metrics from abstracts, stores the structured knowledge in PostgreSQL, builds relationships between related papers, and exposes search, graph, and leaderboard views through FastAPI and Streamlit.

## Why I Built It

I wanted a project that connects my IEEE research experience with data engineering. Research papers have a lot of useful metadata, but it is scattered across text. PaperGraph turns that unstructured research text into structured data that can be searched and compared.

## What The Pipeline Does

1. Loads paper metadata.
2. Extracts methods, datasets, and metrics.
3. Stores entities and metrics in PostgreSQL.
4. Builds graph edges between related papers.
5. Exposes search and graph APIs.
6. Shows paper trends, metric leaderboard, and related paper links in a dashboard.

## Strong Talking Points

- I modeled research papers as structured data.
- I used PostgreSQL for metadata and graph edge storage.
- I separated extraction, indexing, search, and API layers.
- I included my IEEE paper as part of the sample corpus.
- I made the extraction auditable instead of pretending black-box AI is always correct.

## How This Relates To Data Engineering

This project includes ingestion, text processing, schema design, entity extraction, relationship modeling, API serving, and dashboarding. Those are common pieces of real data platforms.
