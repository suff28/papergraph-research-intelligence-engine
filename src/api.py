from fastapi import FastAPI, Query
from sqlalchemy import text

from src.db import db_session
from src.indexer import ingest_sample_corpus
from src.search import paper_details, search_papers


app = FastAPI(title="PaperGraph Research Intelligence API")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ingest/sample")
def ingest_sample():
    return ingest_sample_corpus()


@app.get("/papers")
def papers(limit: int = Query(default=50, ge=1, le=200)):
    with db_session() as connection:
        rows = connection.execute(
            text(
                """
                SELECT p.paper_id, p.title, p.year, p.venue, p.domain, p.task,
                       COUNT(DISTINCT e.entity_id) AS extracted_entities,
                       COUNT(DISTINCT m.metric_id) AS metrics
                FROM papers p
                LEFT JOIN extracted_entities e ON p.paper_id = e.paper_id
                LEFT JOIN paper_metrics m ON p.paper_id = m.paper_id
                GROUP BY p.paper_id
                ORDER BY p.year DESC, p.title
                LIMIT :limit
                """
            ),
            {"limit": limit},
        ).mappings().all()
    return [dict(row) for row in rows]


@app.get("/papers/{paper_id}")
def get_paper(paper_id: str):
    return paper_details(paper_id)


@app.get("/search")
def search(q: str, limit: int = Query(default=20, ge=1, le=100)):
    return search_papers(q, limit=limit)


@app.get("/graph")
def graph(limit: int = Query(default=100, ge=1, le=500)):
    with db_session() as connection:
        nodes = connection.execute(
            text("SELECT paper_id AS id, title AS label, domain, task, year FROM papers ORDER BY year DESC LIMIT :limit"),
            {"limit": limit},
        ).mappings().all()
        edges = connection.execute(
            text(
                """
                SELECT source_paper_id AS source, target_paper_id AS target, relation_type, weight
                FROM paper_edges
                ORDER BY weight DESC
                LIMIT :limit
                """
            ),
            {"limit": limit},
        ).mappings().all()
    return {"nodes": [dict(row) for row in nodes], "edges": [dict(row) for row in edges]}


@app.get("/metrics")
def metrics():
    with db_session() as connection:
        paper_count = connection.execute(text("SELECT COUNT(*) FROM papers")).scalar_one()
        entity_count = connection.execute(text("SELECT COUNT(*) FROM extracted_entities")).scalar_one()
        edge_count = connection.execute(text("SELECT COUNT(*) FROM paper_edges")).scalar_one()
        method_count = connection.execute(
            text("SELECT COUNT(DISTINCT entity_value) FROM extracted_entities WHERE entity_type = 'method'")
        ).scalar_one()
    return {
        "papers": paper_count,
        "entities": entity_count,
        "edges": edge_count,
        "methods": method_count,
    }


@app.get("/leaderboard")
def leaderboard():
    with db_session() as connection:
        rows = connection.execute(
            text(
                """
                SELECT p.title, p.task, m.dataset, m.metric_name, m.metric_value, p.url
                FROM paper_metrics m
                JOIN papers p ON m.paper_id = p.paper_id
                ORDER BY m.metric_value DESC
                """
            )
        ).mappings().all()
    return [dict(row) for row in rows]
