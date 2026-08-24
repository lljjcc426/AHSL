import numpy as np

from ahsl.metrics import recovery_metrics
from ahsl.trees import generate_tree


def test_perfect_recovery_metrics() -> None:
    clean = np.array([[1, 1, 0], [0, 1, 0]], dtype=np.int8)
    metrics = recovery_metrics(clean, clean, generate_tree(3, "path", 0), clean)
    assert metrics["clean_precision"] == 1.0
    assert metrics["clean_recall"] == 1.0
    assert metrics["clean_f1"] == 1.0
    assert metrics["hamming_error"] == 0.0
    assert metrics["exact_row_recovery"] == 1.0
    assert metrics["average_hyperedge_jaccard"] == 1.0
    assert metrics["exact_hyperedge_recovery"] == 1.0


def test_mean_symmetric_difference_is_row_hamming_count() -> None:
    clean = np.array([[1, 1, 0], [0, 1, 0]], dtype=np.int8)
    predicted = np.array([[1, 0, 0], [1, 1, 0]], dtype=np.int8)
    metrics = recovery_metrics(clean, predicted, generate_tree(3, "path", 0), clean)
    assert metrics["mean_symmetric_difference"] == 1.0
    assert metrics["hamming_error"] == 2 / 6

