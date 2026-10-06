from src.graph_builder import build_edges
from src.sample_corpus import sample_papers


def test_build_edges_finds_related_papers():
    edges = build_edges(sample_papers())

    assert len(edges) > 0
    assert all(edge["weight"] > 0 for edge in edges)
    assert any(edge["relation_type"] == "same_task" for edge in edges)
