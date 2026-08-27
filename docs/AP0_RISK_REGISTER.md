# AP0 risk register

| Risk | Level | Evidence/trigger | Mitigation or stop |
|---|---|---|---|
| F1 prior-art saturation | high | FlowLog, DBSP/Feldera, Materialize and Kuzu are strong | AP1 must map any residual to an exact unoccupied mechanism; stop on exact collision |
| F2 benchmark mismatch | medium | LDBC is synthetic though standardized | require independent program-analysis/real-graph route |
| F3 residual disappears | medium | recent systems may already handle small workloads | compare modern unmodified systems first; stop if no meaningful state/tail gap |
| F4 engineering burden | medium | Rust/dataflow internals are nontrivial | begin with external measurements and one engine; no new DBMS |
| F5 compute burden | low | CPU-only, scalable data | start SF1/SF10; cap first serious study below 1,000 CPUh |
| F6 wrapper/integration | medium | adapters alone are not novelty | require algorithm/execution novelty and causal ablation |
| F7 fragmented community | low | DB, graph and Datalog share SIGMOD/PVLDB/ICDE | primary framing stays data systems |
| F8 contribution ceiling | low | current related work appears in PVLDB/SIGMOD | calibrate against FlowLog/Kuzu-class breadth |
| F9 hype dependence | low | incremental queries predate LLM hype | AI remains optional |
| F10 theory-only drift | medium | dynamic-query theory can dominate | Paper 1 must improve a running system on accepted workloads |
| F11 application-only/no novelty | medium | tuning engine flags could improve results | require a new reusable execution/state principle |
| F12 proprietary dependence | low | both routes and engines are public | reject any gate that needs private traces |

## Strongest reason to reject Rank 1

The mature generality of DBSP/Feldera and the breadth of FlowLog may leave only narrow engineering corners. If AP1 cannot demonstrate a cross-workload residual that survives their latest versions, AP0 should be reopened rather than forcing a method.
