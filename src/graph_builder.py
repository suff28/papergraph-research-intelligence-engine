import itertools

from src.extractor import extract_entities


def build_edges(papers: list[dict]) -> list[dict]:
    entity_map = {}
    for paper in papers:
        entities = extract_entities(paper["title"], paper["abstract"])
        values = {entity["entity_value"] for entity in entities}
        values.add(paper["task"])
        values.add(paper["domain"])
        entity_map[paper["paper_id"]] = values

    edges = []
    for left, right in itertools.combinations(papers, 2):
        left_values = entity_map[left["paper_id"]]
        right_values = entity_map[right["paper_id"]]
        shared = left_values.intersection(right_values)
        union = left_values.union(right_values)
        if not shared:
            continue
        weight = round(len(shared) / len(union), 4)
        edges.append(
            {
                "source_paper_id": left["paper_id"],
                "target_paper_id": right["paper_id"],
                "relation_type": _relation_type(shared),
                "weight": weight,
            }
        )
    return edges


def _relation_type(shared: set[str]) -> str:
    if "Lung Segmentation" in shared:
        return "same_task"
    if "Medical Imaging" in shared:
        return "same_domain"
    if any(value in shared for value in ["U-Net", "GAN", "Pix2Pix GAN", "Transformer"]):
        return "shared_method"
    return "shared_concept"
