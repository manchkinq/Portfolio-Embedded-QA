# Lab 2 — Button Debounce Bug Reports

[Original test report](https://docs.google.com/document/d/1PiFFS-wlG33fqmrNn2XvBdExLiEm5MU6Nybptxeibgs/edit) · [All test reports](../test-reports/README.md) · [Bug report index](README.md)

Extracted from the source report on 2026-11-02. Original bug IDs, stated expectations, severity, reproducibility, and evidence text are retained; no fix retest is implied. Embedded screenshots and video placeholders are not copied by this text extraction; see the original document for available images. Blank fields are marked explicitly.

The source report has no bug ID for its single defect; BUG-01 is assigned here for navigation. The source actual-result sentence ends with “LED” and is retained as written.

## BUG-01 — Extra logical event when there is noise during critical operation

### Environment

Debounce_Homework_LogicAnalyzer_Logger

### Preconditions

Critical operation is running.

### Steps to Reproduce

During critical operation, simulate noise on NOISE button

### Expected Result

Noise does not lead to extra logical event during critical operation

### Actual Result

Noise creates an extra logical event during critical operation. LED

### Evidence

```text
Logs:
================================
LOGICAL EVENT #1
Button press ACCEPTED
RAW interrupts total: 84 | RAW interrupts since previous logical event: 84 | LOGICAL events total: 1 | ACTIONS total: 1 | ACTION executed ONCE
LOGGER: physical press -> RAW -> LOGICAL -> ACTION
================================
[SYSTEM] Critical operation is running...
Button RELEASE accepted
<<<Here the noise was simulated>>
================================
LOGICAL EVENT #2
Button press ACCEPTED
RAW interrupts total: 94 | RAW interrupts since previous logical event: 10 | LOGICAL events total: 2 | ACTIONS total: 2| ACTION executed ONCE
LOGGER: physical press -> RAW -> LOGICAL -> ACTION
================================
Button RELEASE accepted
[SERIAL] Wokwi UART alive
[LOGGER] RAW interrupts: 95 | Logical events: 2 | Actions: 2 | [SYSTEM] Critical operation finished.
```

### Reproducibility

5/5

### Severity

Major(3/5)

### Priority

High(4/5)

