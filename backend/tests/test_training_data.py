import pytest
from app.data.training_samples import TRAINING_SAMPLES


class TestTrainingData:
    def test_all_have_text_and_label(self):
        for i, sample in enumerate(TRAINING_SAMPLES):
            assert "text" in sample, f"Sample {i} missing 'text'"
            assert "label" in sample, f"Sample {i} missing 'label'"
            assert isinstance(sample["text"], str)
            assert len(sample["text"]) > 20

    def test_cv_label_count(self):
        cv_count = sum(1 for s in TRAINING_SAMPLES if s["label"] == "cv")
        non_cv_count = sum(1 for s in TRAINING_SAMPLES if s["label"] == "non-cv")
        assert cv_count > non_cv_count, f"Expected more CV than non-CV samples ({cv_count} vs {non_cv_count})"

    def test_non_cv_label_count(self):
        non_cv_count = sum(1 for s in TRAINING_SAMPLES if s["label"] == "non-cv")
        assert non_cv_count >= 10, f"Expected at least 10 Non-CV samples, got {non_cv_count}"

    def test_all_labels_valid(self):
        valid = {"cv", "non-cv"}
        for i, sample in enumerate(TRAINING_SAMPLES):
            assert sample["label"] in valid, f"Sample {i} has invalid label '{sample['label']}'"
