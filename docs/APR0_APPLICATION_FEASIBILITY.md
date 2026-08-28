# AP-R0 application and engineering feasibility

| Candidate | Application | Burden | First scientific signal | Compute | Assessment |
|---|---|:---:|---|---|---|
| A1 hybrid execution | search/analytics systems | E4 | after datasets and several engine builds | multi-core, high memory | too much setup before a fair signal |
| B1 verified workflows | business/SaaS automation | E2-E3 | after model/API and simulations | API/GPU dependent | feasible in principle, not current-baseline independent |
| C1 test generation | repository maintenance | E2-E3 | after containers and model inference | API/GPU plus CPU tests | benchmark strong, residual unmeasured |
| D1 dynamic compilation | ML runtime deployment | E2 here | after MSVC/CUDA compiler setup | CPU/GPU | official current evidence weakens payoff |
| E1 constraint synthesis | planning/optimization modeling | E1-E2 | benchmark ground truths run now | low CPU plus model/API | most accessible benchmark; no current semantic baseline |
| F1 fuzz repair | security vulnerability remediation | E4 | after dual containers and current agent | substantial CPU/storage plus model | high value but not bounded locally |

None satisfies both small-team first-paper feasibility and executable G5. The
engineering grades concern time to scientific signal, not eventual project
value.
