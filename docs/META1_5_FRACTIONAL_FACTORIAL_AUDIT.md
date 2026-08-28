# Fractional-factorial and sparse-design audit

## Classical aliasing

Box and Hunter's 1961 fractional-factorial theory makes aliasing, defining relations, resolution, and estimability central design objects. Tang and Wu (1997) and the supersaturated-design literature optimize column correlation summaries such as E(s2)/UE(s2) when orthogonality is impossible. Therefore neither “partial factorial measurement” nor “eliminating exact aliases” is novel.

For regular fractions, exact aliases are deliberately characterized by defining words. For nonregular and supersaturated designs, projection properties, generalized aberration, correlation distributions, and model estimability play the analogous role. META1's observed exact-alias reduction from 0.0168 to 0 is a scientifically useful diagnostic, not a new discovery about DOE.

## Model-robust support uncertainty

Jones et al. (2009) optimize estimation capacity over sparse active-effect models and introduce partially supersaturated designs when a core subset must remain estimable. Smucker and Drew (2015) approximate huge model spaces by sampling models, use coordinate exchange, and evaluate the resulting designs against a much larger model set. These works show that unknown-support robustness via a distribution or finite model space is established.

They do not directly optimize signed Lasso support recovery and do not use the Mobius/AND dictionary, but they remove any claim that averaging design quality over unknown supports is new by itself.

## Support-aware SSD criteria

Weese et al. (2021) use group-orthogonal and constrained Var(s) criteria, especially exploiting prior knowledge that active effects share positive signs. Singh and Stufken (2023) tie SSD selection to Gauss-Dantzig recovery conditions via an active-subset ensemble. Stallrich et al. (2025) then directly optimize Lasso sign-recovery probability.

The sequence is important:

- D/A/E criteria target coefficient estimation under a model;
- UE(s2), Var(s+), and alias criteria target geometry/heuristic screening behavior;
- DCD/HILS target support or sign recovery itself.

META1 belongs to the third category. Calling the intervention D-optimal does not establish novelty once direct recovery-aware criteria exist.

## Sparse polynomial design

Diaz, Doostan, and Hampton (2018) combine compressed sensing with D-optimal sequential design for sparse polynomial chaos expansions under a fixed computational budget. Their polynomial basis and objective differ from Boolean AND support, but the combination “sparse polynomial recovery plus D-opt row acquisition” is occupied.

## What remains structurally different

For `d=6`, the full nonempty AND dictionary contains 63 columns, of which 42 have order>=3. Column supports are nested: if `T` contains `S`, the AND column for `T` can be nonzero only where the column for `S` is nonzero. Partial row sets therefore create many exact zero/alias events that are not present in freely chosen balanced two-level main-effect matrices. Moreover, the target is a subset of coefficients by order, with lower orders acting as nuisance terms.

This structure can change an optimal criterion, but only if the future method explicitly uses it. Merely feeding the 63 columns into a generic criterion would be an application, not a strong methodological contribution.

## Collision judgment

Strongest classical collision: Box-Hunter alias/resolution theory plus modern model-robust SSD construction. Severity **3/5** for the exact META1 object and **5/5** for any claim that alias elimination or limited-run factorial design is new.
