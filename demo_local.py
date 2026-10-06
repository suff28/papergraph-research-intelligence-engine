from pathlib import Path

import pandas as pd

from src.extractor import extract_entities
from src.graph_builder import build_edges
from src.sample_corpus import sample_papers


def main():
    papers = sample_papers()
    entity_rows = []
    for paper in papers:
        for entity in extract_entities(paper["title"], paper["abstract"]):
            entity_rows.append({"paper_id": paper["paper_id"], "title": paper["title"], **entity})

    edges = build_edges(papers)
    output = Path("sample_output")
    output.mkdir(exist_ok=True)
    pd.DataFrame(entity_rows).to_csv(output / "extracted_entities.csv", index=False)
    pd.DataFrame(edges).to_csv(output / "paper_graph_edges.csv", index=False)
    report = output / "papergraph_report.html"
    report.write_text(
        f"""
        <html><body style="font-family:Arial;margin:40px">
        <h1>PaperGraph Local Report</h1>
        <p>Papers indexed: {len(papers)}</p>
        <p>Entities extracted: {len(entity_rows)}</p>
        <p>Graph edges created: {len(edges)}</p>
        <h2>Extracted Entities</h2>
        {pd.DataFrame(entity_rows).head(30).to_html(index=False)}
        <h2>Graph Edges</h2>
        {pd.DataFrame(edges).head(30).to_html(index=False)}
        </body></html>
        """
    )
    print(f"Papers indexed: {len(papers)}")
    print(f"Entities extracted: {len(entity_rows)}")
    print(f"Graph edges created: {len(edges)}")
    print(f"Report: {report}")


if __name__ == "__main__":
    main()
