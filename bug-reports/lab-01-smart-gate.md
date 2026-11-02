# Lab 1 — Smart Gate Controller Bug Reports

[Original test report](https://docs.google.com/document/d/1RnQ53j7FTkc4PFf75_F1NkKhJpfTR6eCDeyq4Qgv_og/edit) · [All test reports](../test-reports/README.md) · [Bug report index](README.md)

Original bug IDs, stated expectations, severity, reproducibility, and evidence text are retained; no fix retest is implied. Embedded screenshots and video placeholders are not copied by this text extraction; see the original document for available images. Blank fields are marked explicitly.

## BUG-01 — Can't reach OPEN state after pressing LIMIT_OPEN in OPENING status

### Requirement

R3

### Severity

Critical

### Precondition

OPENING status is active less than 10sec

### Steps to Reproduce

1. Click LIMIT_OPEN

### Expected Result

OPEN status

### Actual Result

OPENING status; spam in logs

### Reproducibility

5/5

### Evidence

```text
LOGS:
=== SMART GATE CONTROLLER ===
Commands: O=open, C=close, S=stop, R=reset error
Initial state: CLOSED
COMMAND: O
STATE: CLOSED -> OPENING
OPEN LIMIT DETECTED
OPEN LIMIT DETECTED
OPEN LIMIT DETECTED
OPEN LIMIT DETECTED
```


## BUG-02 — Immediate transitions from OPENING to CLOSING and reverse

### Requirement

R8

### Severity

High

### Precondition

OPENING status is active less than 10sec

### Steps to Reproduce

1. Click CLOSING
2. Observe the relays and transition between states

### Expected Result

Transition between states is safe. Switch is not immediate.

### Actual Result

Switch between OPENING and CLOSING is immediate

### Reproducibility

5/5


## BUG-03 — ERROR status is not activated when OPENING > 10 sec

### Requirement

R10

### Severity

Critical

### Precondition

Any status from which OPENING can be activated

### Steps to Reproduce

1. Click OPEN
2. Wait more than 10 sec

### Expected Result

ERROR status is active. Both relays are OFF

### Actual Result

OPENING status

### Reproducibility

5/5



## BUG-04 — ERROR status is not activated when both LIMITS are active

### Requirement

R11

### Severity

High

### Precondition

Any valid state

### Steps to Reproduce

1. Actavate both limits simultaneously

### Expected Result

ERROR; relays OFF; error indication

### Actual Result

Relay OFF, warning in logs, BUT not ERROR status

### Reproducibility

5/5

### Evidence

LOGS:
WARNING: both limit switches active


## BUG-05 — STOP button changes status from ERROR|OPEN|CLOSED

### Requirement

Not specified in the source report.

### Severity

Medium

### Precondition

ERROR|OPEN|CLOSED status

### Steps to Reproduce

1. Click STOP button

### Expected Result

Nothing changes

### Actual Result

System in STOPPED status

### Reproducibility

5/5


## BUG-06 — Reset and Stop commands should appear in logs when does not influence system

### Requirement

Not specified in the source report.

### Severity

Low

### Precondition

Any state when Reset/Stop does not change something, e.g. STOPPED status

### Steps to Reproduce

1. Activate STOP/RESET command

### Expected Result

Message in logs that the command is ignored/invalid in current state

### Actual Result

Nothing in logs

### Reproducibility

5/5

### Evidence

```text
LOGS:
STATE: CLOSED -> STOPPED
COMMAND: S
COMMAND: R
```


## BUG-07 — OPEN LED is ON in STOPPED status

### Requirement

Not specified in the source report.

### Severity

Medium

### Precondition

Any valid status

### Steps to Reproduce

1. Activate STOP command

### Expected Result

System in STOPPED. All LEDs are OFF

### Actual Result

System in STOPPED. OPEN LED is ON

### Reproducibility

5/5


