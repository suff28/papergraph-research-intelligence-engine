import re


METHOD_PATTERNS = {
    "Pix2Pix GAN": r"\bpix2pix\b",
    "GAN": r"\bgan\b|adversarial",
    "U-Net": r"\bu-net\b|u shaped|u-shaped",
    "Attention U-Net": r"attention u-net|attention gates",
    "DenseNet": r"densenet",
    "Transformer": r"transformer|vision transformer",
    "nnU-Net": r"\bnnu-net\b|nnU-net|self-configuring",
}

DATASET_PATTERNS = {
    "Montgomery": r"montgomery",
    "Shenzhen": r"shenzhen",
    "ChestX-ray14": r"chestx-ray14",
    "ISBI": r"isbi",
    "Medical Segmentation Decathlon": r"medical segmentation decathlon",
    "Synapse": r"synapse",
    "External CXR": r"external",
}

METRIC_PATTERNS = {
    "Accuracy": r"accuracy",
    "Precision": r"precision",
    "Recall": r"recall",
    "F1-score": r"f1",
    "Dice": r"dice",
    "IoU": r"\biou\b|intersection over union",
    "AUC": r"\bauc\b",
}


def extract_entities(title: str, abstract: str) -> list[dict]:
    text = f"{title} {abstract}".lower()
    entities = []
    entities.extend(_extract_by_patterns(text, METHOD_PATTERNS, "method"))
    entities.extend(_extract_by_patterns(text, DATASET_PATTERNS, "dataset"))
    entities.extend(_extract_by_patterns(text, METRIC_PATTERNS, "metric"))
    return entities


def _extract_by_patterns(text: str, patterns: dict[str, str], entity_type: str) -> list[dict]:
    found = []
    for value, pattern in patterns.items():
        if re.search(pattern, text, re.IGNORECASE):
            found.append({"entity_type": entity_type, "entity_value": value, "confidence": 0.95})
    return found
