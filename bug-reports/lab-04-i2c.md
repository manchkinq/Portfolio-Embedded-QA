# Lab 4 — I2C Fault Injection Bug Reports

[Original test report](https://docs.google.com/document/d/1mMwtw9YUV-qiAuHMGlWaU8QaRK1wLnRnp5C-2thL3_s/edit) · [All test reports](../test-reports/README.md) · [Bug report index](README.md)

Extracted from the source report on 2026-11-02. Original bug IDs, stated expectations, severity, reproducibility, and evidence text are retained; no fix retest is implied. Embedded screenshots and video placeholders are not copied by this text extraction; see the original document for available images. Blank fields are marked explicitly.

## BUG-01 — System freezes after connection to I2C periphery is lost

### Preconditions

System is working

### Steps

1. Trigger FAULT switch to simulate connection loss
   2. Observe UART logs
   3. Restore connection by triggering FAULT switch
   4. Observe system behaviour

### Expected Result

System correctly handles an error and work controllable. Error does not block the work of a main loop.

### Actual Result

System freezes after connection to I2C periphery is lost. After restoring connection to the periphery, the system is still not alive.

### Severity

Critical

### Reproducibility

5/5

### Evidence

```text
UART LOGS:
=== WEBINAR 4: I2C PRACTICE / BUGGY ===
Find the defect using trace + firmware behavior.
FAULT OFF = normal sensor; FAULT ON = simulated peripheral loss.
[DATA] Temperature: 24.00 C
                           [SYSTEM] Main loop alive
[DATA] Temperature: 24.00 C
                           [SYSTEM] Main loop alive
[DATA] Temperature: 24.00 C
                           [SYSTEM] Main loop alive
[DATA] Temperature: 24.00 C
                           [SYSTEM] Main loop alive
[DATA] Temperature: 24.00 C
                           [SYSTEM] Main loop alive
[DATA] Temperature: 24.00 C
                           [SYSTEM] Main loop alive
[DATA] Temperature: 24.00 C
                           [SYSTEM] Main loop alive
[DATA] Temperature: 24.00 C
                           [SYSTEM] Main loop alive
[  8522][E][Wire.cpp:499] requestFrom(): i2cWriteReadNonStop returned Error -1
















I2C signals:
Moment of failure:
```

