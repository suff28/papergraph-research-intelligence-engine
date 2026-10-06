from src.extractor import extract_entities


def test_extracts_methods_datasets_and_metrics():
    entities = extract_entities(
        "Pix2Pix GAN for Lung Segmentation",
        "A U-Net generator is trained on Montgomery and tested on Shenzhen using Dice and accuracy.",
    )
    values = {entity["entity_value"] for entity in entities}

    assert "Pix2Pix GAN" in values
    assert "U-Net" in values
    assert "Montgomery" in values
    assert "Shenzhen" in values
    assert "Dice" in values
