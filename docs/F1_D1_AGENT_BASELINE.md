# F1-D1 agent baseline

The official reference agent is function/stack-trace centered, with up to five iterations per trajectory and ten retry trajectories; generation-time validation is build plus original crash reproduction. It requires a provider API key, which is unavailable in the current environment.

The executable route audited here is Codex CLI `0.149.1` using ChatGPT authentication. An ephemeral read-only `gpt-5.6-luna` probe returned `ACCESS_OK` after WebSocket timeouts and HTTPS fallback. No credential was stored or committed.

The provisional baseline is one Codex CLI outer trajectory per instance, model `gpt-5.6-luna`, provider-managed sampling temperature (the CLI does not expose it), reasoning effort none, vulnerable-container-only repository access, one candidate patch, and 3600 seconds. Plugins are disabled and the run is ephemeral. The CLI does not provide a hard token-cap switch, so actual usage must be logged and equal-budget comparisons must enforce the same one-trajectory/wall-time envelope. It is not called a completed frozen baseline until the container sanity set succeeds.
