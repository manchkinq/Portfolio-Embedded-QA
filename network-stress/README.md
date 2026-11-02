# Network Stress and Resilience

Lab 7 examines network loss and recovery, retry/backoff, offline telemetry buffering, buffer overflow, duplicate publishing, and memory stability.

## Reports and evidence

- [Lab 7 test report and recorded evidence](https://docs.google.com/document/d/1f36czSSsQ44c1iMlR18BEHP7hC2O73t1qC8wXBUiYtE/edit?tab=t.0)
- [Lab 7 bug reports](../bug-reports/lab-07-network.md)
- [All test reports](../test-reports/README.md)

The test report contains the execution results, log excerpts, message-ID comparisons, heap measurements, and conclusions. Use it as the evidence reference; the full report is not duplicated here. Separate raw capture and CSV files have not been added to this folder.

## Scenarios

| Scenario | Focus | Evidence in the test report |
|---|---|---|
| A — Connection loss and recovery | Network states, retry/backoff, command responsiveness, recovery after NET UP | Timestamped reconnect logs and STATUS output |
| B — Offline buffering | Queue telemetry while offline and flush after recovery | Queued message IDs and publish logs |
| C — Buffer capacity boundary | Capacity of eight messages, DROP_OLDEST, overflow counters, repeated publishes | Buffer and flush logs, per-ID publish-count comparison |
| D — Network stress and memory stability | Repeated STRESS commands and free-heap trend | Iteration table, workload counts, heap measurements and logs |

## Scope

The supplied firmware models network availability and MQTT publishing. Serial publish logs are evidence of model behavior, not delivery to a real MQTT broker. Real Wi-Fi/MQTT outages and long-duration hardware testing remain follow-up validation.
