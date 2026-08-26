import inspect
from types import SimpleNamespace

import networkx as nx
import numpy as np

import ahsl.experiments.a1_5_runner as runner
from ahsl.experiments.a1_runner import Job
from ahsl.posterior_marginals import posterior_node_marginals


def test_posterior_api_has_no_clean_data_input():
    parameters = inspect.signature(posterior_node_marginals).parameters
    assert "clean" not in parameters
    assert set(parameters) == {
        "tree",
        "observed",
        "p_false_negative",
        "p_false_positive",
        "branch_probability",
        "root",
    }


def test_fixed_tree_estimated_q_receives_train_rows_only(monkeypatch):
    train = np.zeros((11, 4), dtype=np.int8)
    captured = {}

    def fake_estimate(tree, observed, p_false_negative, p_false_positive, bounds):
        captured["observed"] = observed
        return SimpleNamespace(q=0.37, evaluations=5)

    monkeypatch.setattr(runner, "estimate_q_mle", fake_estimate)
    method = {
        "estimator": "BinaryMWST",
        "tree": nx.path_graph(4),
    }
    job = Job(0, 30, 4, "path", 0.4, 0.2, 0.2, 0)
    tracks = runner._q_tracks(method, train, job, (0.02, 0.98))
    assert captured["observed"] is train
    assert tracks[1]["q_fit_split"] == "train_only"
    assert tracks[1]["q"] == 0.37
