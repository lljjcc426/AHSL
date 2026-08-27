"""Reader for the discrete UAI competition factor format."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np


@dataclass(frozen=True)
class UAIFactor:
    scope: tuple[int, ...]
    table_size: int
    nonzero_count: int
    values: np.ndarray | None = None


@dataclass(frozen=True)
class UAIModel:
    model_type: str
    domain_sizes: tuple[int, ...]
    factors: tuple[UAIFactor, ...]

    @property
    def scopes(self) -> tuple[tuple[int, ...], ...]:
        return tuple(factor.scope for factor in self.factors)


def read_uai(path: str | Path, *, load_values: bool = False) -> UAIModel:
    """Read one MARKOV/BAYES UAI model and profile table sparsity."""

    source = Path(path)
    tokens = source.read_text(encoding="utf-8").split()
    position = 0

    def take() -> str:
        nonlocal position
        token = tokens[position]
        position += 1
        return token

    model_type = take().upper()
    n_variables = int(take())
    domain_sizes = tuple(int(take()) for _ in range(n_variables))
    n_factors = int(take())
    scopes = []
    for _ in range(n_factors):
        arity = int(take())
        scopes.append(tuple(int(take()) for _ in range(arity)))

    factors = []
    for scope in scopes:
        table_size = int(take())
        expected_size = int(np.prod([domain_sizes[v] for v in scope], dtype=np.int64))
        if table_size != expected_size:
            raise ValueError(
                f"{source.name}: table size {table_size} != scope cardinality {expected_size}"
            )
        values = np.asarray(tokens[position : position + table_size], dtype=np.float64)
        position += table_size
        factors.append(
            UAIFactor(
                scope=scope,
                table_size=table_size,
                nonzero_count=int(np.count_nonzero(values)),
                values=values.reshape(tuple(domain_sizes[v] for v in scope))
                if load_values
                else None,
            )
        )
    return UAIModel(model_type, domain_sizes, tuple(factors))
