import numpy as np

from ahsl.acyclicity import running_intersection_violations
from ahsl.corruption import corrupt_incidence
from ahsl.trees import generate_tree


def test_corruption_masks_match_changed_entries() -> None:
    clean = np.array([[1, 1, 0], [0, 1, 0]], dtype=np.int8)
    result = corrupt_incidence(clean, 1.0, 1.0, seed=3)
    expected = 1 - clean
    assert np.array_equal(result["corrupted_incidence"], expected)
    assert result["num_flipped"] == clean.size
    assert np.array_equal(result["false_negative_mask"], clean == 1)
    assert np.array_equal(result["false_positive_mask"], clean == 0)


def test_corruption_is_not_repaired_to_running_intersection() -> None:
    tree = generate_tree(3, "path", seed=0)
    clean = np.ones((20, 3), dtype=np.int8)
    violation_found = False
    for seed in range(20):
        corrupted = corrupt_incidence(clean, 0.5, 0.0, seed)["corrupted_incidence"]
        if running_intersection_violations(corrupted, tree)["num_violating_vertices"] > 0:
            violation_found = True
            break
    assert violation_found

