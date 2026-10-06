from sqlalchemy import text

from src.db import db_session


def search_papers(query: str, limit: int = 20) -> list[dict]:
    pattern = f"%{query.lower()}%"
    with db_session() as connection:
        rows = connection.execute(
            text(
                """
                SELECT p.paper_id, p.title, p.year, p.venue, p.domain, p.task, p.url,
                       STRING_AGG(DISTINCT e.entity_value, ', ') AS entities
                FROM papers p
                LEFT JOIN extracted_entities e ON p.paper_id = e.paper_id
                WHERE LOWER(p.title) LIKE :pattern
                   OR LOWER(p.abstract) LIKE :pattern
                   OR LOWER(p.task) LIKE :pattern
                   OR LOWER(p.domain) LIKE :pattern
                   OR LOWER(COALESCE(e.entity_value, '')) LIKE :pattern
                GROUP BY p.paper_id
                ORDER BY p.year DESC
                LIMIT :limit
                """
            ),
            {"pattern": pattern, "limit": limit},
        ).mappings().all()
    return [dict(row) for row in rows]


def paper_details(paper_id: str) -> dict:
    with db_session() as connection:
        paper = connection.execute(
            text("SELECT * FROM papers WHERE paper_id = :paper_id"),
            {"paper_id": paper_id},
        ).mappings().one()
        authors = connection.execute(
            text("SELECT author_name FROM paper_authors WHERE paper_id = :paper_id ORDER BY author_order"),
            {"paper_id": paper_id},
        ).scalars().all()
        entities = connection.execute(
            text("SELECT entity_type, entity_value FROM extracted_entities WHERE paper_id = :paper_id ORDER BY entity_type"),
            {"paper_id": paper_id},
        ).mappings().all()
        metrics = connection.execute(
            text("SELECT metric_name, metric_value, dataset FROM paper_metrics WHERE paper_id = :paper_id"),
            {"paper_id": paper_id},
        ).mappings().all()
    result = dict(paper)
    result["authors"] = list(authors)
    result["entities"] = [dict(row) for row in entities]
    result["metrics"] = [dict(row) for row in metrics]
    return result
