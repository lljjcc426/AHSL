# A1 Identifiability Notes

## Population result in the matched interior regime

Assume labeled columns, `m>=2`, `0<q<1`, and known independent bit-flip noise
with `p_+ + p_- != 1`.

For one bit, the observation channel matrix has determinant
`1-p_+-p_-`. The `m`-bit channel is its Kronecker power and is invertible.
Consequently the population distribution of the clean support `S` is identified
by the population distribution of the noisy row.

Under the anchor-growth prior, a two-element set `{u,v}` has positive
probability if and only if `{u,v}` is an edge of `T`. Thus the positive
two-element supports identify the complete labeled edge set. Finally,

```text
P(S=V) = q^(m-1),
```

so `q` is identified once `m>=2`. This gives a simple injectivity argument for
the matched population model.

## Obvious nonidentifiable cases

- `q=0`: every support is a uniformly chosen singleton, independent of `T`.
- `q=1`: every support is all of `V`, independent of `T`.
- `p_+ + p_-=1`: the two columns of the binary noise channel coincide, so `Y`
  contains no information about `X`.
- `m=1`: there is no tree parameter and `q` has no effect.
- Unlabeled observation coordinates: tree automorphisms can only be identified
  up to relabeling. A1 uses labeled columns, so this does not apply.

## Weakly identified finite-sample regimes

Population identifiability does not imply practical recovery. At small `q`,
most supports are singletons and pair events carrying direct edge information
are rare. Near `q=1`, the full support dominates and cut events are rare. High
noise attenuates both signals through an increasingly ill-conditioned channel.

Stars can be especially difficult under finite samples because many leaf roles
are exchangeable and a large fraction of rows either contain only the center or
several interchangeable leaves. This is statistical symmetry, not population
nonidentifiability of labeled edges in the interior regime.

## Unknown-noise caveat

A1 treats `p_+` and `p_-` as known. If both noise rates and `q` are unknown, the
invertible-channel argument no longer establishes joint identifiability; channel
noise and support dispersion may trade off. This phase will not claim a theorem
for that model.

## Empirical checks required

1. Estimate `q` with the generating tree fixed at `n=100,300,1000`.
2. Compare local and global tree optima for small labeled trees.
3. Report likelihood gaps and edge disagreement by topology.
4. Treat near-ties as weak information rather than forced recovery failures.

Empirical results will be appended after the preregistered runs.

