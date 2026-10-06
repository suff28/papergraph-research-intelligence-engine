from sqlalchemy import text

from src.db import db_session
from src.extractor import extract_entities
from src.graph_builder import build_edges
from src.sample_corpus import sample_papers


def ingest_sample_corpus() -> dict:
    papers = sample_papers()
    with db_session() as connection:
        connection.execute(text("DELETE FROM paper_edges"))
        connection.execute(text("DELETE FROM paper_metrics"))
        connection.execute(text("DELETE FROM extracted_entities"))
        connection.execute(text("DELETE FROM paper_authors"))
        connection.execute(text("DELETE FROM papers"))

        for paper in papers:
            connection.execute(
                text(
                    """
                    INSERT INTO papers (paper_id, title, abstract, year, venue, doi, url, domain, task)
                    VALUES (:paper_id, :title, :abstract, :year, :venue, :doi, :url, :domain, :task)
                    """
                ),
                {k: paper[k] for k in ["paper_id", "title", "abstract", "year", "venue", "doi", "url", "domain", "task"]},
            )
            connection.execute(
                text(
                    """
                    INSERT INTO paper_authors (paper_id, author_name, author_order)
                    VALUES (:paper_id, :author_name, :author_order)
                    """
                ),
                [
                    {"paper_id": paper["paper_id"], "author_name": author, "author_order": idx + 1}
                    for idx, author in enumerate(paper["authors"])
                ],
            )
            entities = extract_entities(paper["title"], paper["abstract"])
            connection.execute(
                text(
                    """
                    INSERT INTO extracted_entities (paper_id, entity_type, entity_value, confidence)
                    VALUES (:paper_id, :entity_type, :entity_value, :confidence)
                    """
                ),
                [{**entity, "paper_id": paper["paper_id"]} for entity in entities],
            )
            if paper["metrics"]:
                connection.execute(
                    text(
                        """
                        INSERT INTO paper_metrics (paper_id, metric_name, metric_value, dataset)
                        VALUES (:paper_id, :metric_name, :metric_value, :dataset)
                        """
                    ),
                    [{**metric, "paper_id": paper["paper_id"]} for metric in paper["metrics"]],
                )

        edges = build_edges(papers)
        if edges:
            connection.execute(
                text(
                    """
                    INSERT INTO paper_edges (source_paper_id, target_paper_id, relation_type, weight)
                    VALUES (:source_paper_id, :target_paper_id, :relation_type, :weight)
                    """
                ),
                edges,
            )
    return {"papers": len(papers), "edges": len(edges)}

