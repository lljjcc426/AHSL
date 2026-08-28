# F1-D1 patch-pattern analysis

The planned labels are bounds check, early return, clamp, allocation-size correction, ownership/lifetime fix, validation change, parser-state fix, loop-bound fix, type-width change, null check, multi-location invariant repair, and other.

No candidate patch was generated in the present environment, so `patches.csv` and `patch_pattern_summary.csv` contain headers only. Inferring a dominant pattern from ground-truth patch metadata would violate the generation firewall and would not describe agent failures.

Pattern classification will begin only after the frozen baseline produces real candidate diffs. Post-evaluation human-patch inspection will mark each affected case ANALYSIS-EXPOSED.
