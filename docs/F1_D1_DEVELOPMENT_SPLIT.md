# F1-D1 Development split

The split uses only the 113 Lite IDs and safe metadata at the frozen benchmark commit. Projects are shuffled with seed `20260828` and assigned whole to Development until the 20–26 target band is reached. This produces 25 Development instances from eight projects: `c-blosc2`, `librawspeed`, `libredwg`, `libxml2`, `open62541`, `ots`, `php-src`, and `yara`.

The remaining 87 instances are UNTOUCHED. Instance 10445 is ANALYSIS-EXPOSED and belongs to neither unbiased pool. Development and untouched project sets are disjoint. No repair outcome, human patch, or evaluator label informed the split.

Because infrastructure sanity failed globally, the 25 Development instances are currently INFRA-BLOCKED. Their membership remains frozen for the next bounded infrastructure clarification.

## 2026-10-04 runtime re-entry note

Membership remains unchanged. The global storage and agent-authentication gates
failed before instance selection, so all 25 Development rows are recorded as
excluded for this run and no instance was selected. No outcome informed that
decision. The 87 UNTOUCHED instances were not accessed, and 10445 remains
ANALYSIS-EXPOSED.
