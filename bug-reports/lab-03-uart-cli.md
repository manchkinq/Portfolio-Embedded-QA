# Lab 3 — UART CLI Bug Reports

[Original test report](https://docs.google.com/document/d/1jcBNWhEgigxrRnEYKmBW-NpaF4PijaBy93Jh6VNS-i4/edit) · [All test reports](../test-reports/README.md) · [Bug report index](README.md)

Extracted from the source report on 2026-11-02. Original bug IDs, stated expectations, severity, reproducibility, and evidence text are retained; no fix retest is implied. Embedded screenshots and video placeholders are not copied by this text extraction; see the original document for available images. Blank fields are marked explicitly.

## BUG-01 — Status command is not case sensitive

### Steps

1. Type ‘STATUS’ in Terminal
2. Observe output

### Expected

Status command is case sensitive. Output is ‘ERROR: unknown command’ (REQ-06)

### Actual

Status command is not case sensitive. Status command works, system status is displayed in output

### Severity

Minor(2/5)

### Reproducibility

5/5

### Evidence

Not specified in the source text. See the original report for any embedded evidence.


## BUG-02 — Speed becomes 255 value when setting speed 256

### Steps

1. In Terminal input ‘set speed 256’
2. Observe output
3. Input ‘status’
4. Observe SPEED value

### Expected

Speed is not set with value 256, it remains unchanged. Output is: ERROR: speed out of range(REQ-03)

### Actual

Speed is set with value 255. Output is: ‘OK: speed=255’

### Severity

Major(3/5)

### Reproducibility

5/5

### Evidence

Not specified in the source text. See the original report for any embedded evidence.


## BUG-03 — Timeout can be set with value 0

### Steps

1. In Terminal input ‘set timeout 0’
2. Observe output
3. Input ‘status’
4. Observe TIMEOUT value

### Expected

Timeout is not set with value 0, it remains unchanged. Output is: ERROR: timeout out of range (REQ-07)

### Actual

Timeout is set with value 0. Output is: ‘OK: timeout=0’

### Severity

Major(3/5)

### Reproducibility

5/5

### Evidence

Not specified in the source text. See the original report for any embedded evidence.


## BUG-04 — Command ‘led on’ is ignored by the system to change CONFIG status for DIRTY

### Precondition

system CONFIG status is SAVED

### Steps

1. In Terminal input ‘led on’
2. Observe output
3. Input status
4. Observe CONFIG value

### Expected

CONFIG status is changed for DIRTY.

### Actual

CONFIG status remained as SAVED.

### Severity

Major(3/5)

### Reproducibility

5/5

### Evidence

Not specified in the source text. See the original report for any embedded evidence.


## BUG-05 — After input of command that consists of UTF-8 symbols output is OK

### Steps

1. In Terminal input some UTF-8 symbols, e.g ‘@#$’
2. Observe output

### Expected

Output indicates an error that the command is wrong: ERROR: unknown command

### Actual

Output says: OK

### Severity

Minor(2/5)

### Reproducibility

5/5

### Evidence

Not specified in the source text. See the original report for any embedded evidence.


## BUG-06 — System crashes and reboots when inputting any 41 symbol in terminal

### Steps

In Terminal input any 41 symbol
Observe system behavior

### Expected

There is an Error handler, which will display that the command is too long. This does not influence the system in any way.

### Actual

System is crushing and rebooting

### Severity

Critical(4/5)

### Reproducibility

5/5

### Evidence

Not specified in the source text. See the original report for any embedded evidence.


## BUG-07 — Reset command resets all saved changes to the initial system configuration

### Preconditions

Some changes were done to the system, configuration has DIRTY value

### Steps

1. In terminal input ‘save’
2. Input ‘status’ and observe configuration status
3. Remember all system values
4. Input ‘reset’
5. Input ‘status’ and and observe system values

### Expected

All values are reset to the latest saved configuration

### Actual

All values are reset to the initial system configuration

### Severity

Critical (4/5)

### Reproducibility

5/5

### Evidence

Not specified in the source text. See the original report for any embedded evidence.

