# Lab 7 — Network Resilience Model Bug Reports

[Original test report](https://docs.google.com/document/d/1f36czSSsQ44c1iMlR18BEHP7hC2O73t1qC8wXBUiYtE/edit) · [All test reports](../test-reports/README.md) · [Bug report index](README.md)

Extracted from the source report on 2026-11-02. Original bug IDs, stated expectations, severity, reproducibility, and evidence text are retained; no fix retest is implied. Embedded screenshots and video placeholders are not copied by this text extraction; see the original document for available images. Blank fields are marked explicitly.

These observations concern the supplied network model; Serial publish logs do not establish delivery to a real MQTT broker.

## BUG-01 — Reconnect attempts repeat about every 50 ms while the network is down

### Environment

Wokwi in VS Code, firmware homework_buggy, macOS.

### Preconditions

The node is CONNECTED. The buffer is empty.

### Steps

1. Enter RESET STATS.
2. Enter NET DOWN.
3. Watch the reconnect logs for 10–20 seconds.
4. Compare the timestamps.
5. Enter NET UP.

### Expected result

According to R2, retries use backoff and do not create a reconnect storm.

### Actual result

The first reported delay is 500 ms. The next delays are 50 ms and do not increase. The timestamps show about 20 attempts per second.

### Recovery behavior

After NET UP, the node returns to CONNECTED.

### Evidence

```text
21:47:03.620 > [NET] retry=1 backoff_ms=500
21:47:04.093 > [NET] state=CONNECTING
21:47:04.093 > [NET] reconnect=FAILED
21:47:04.093 > [NET] state=BACKOFF
21:47:04.093 > [NET] retry=2 backoff_ms=50


21:47:04.241 > [NET] state=CONNECTING
21:47:04.290 > [NET] state=CONNECTING
21:47:04.341 > [NET] state=CONNECTING
```

### Reproducibility

Observed in multiple NET DOWN tests.

### Severity

Major. Many devices with this retry behavior could create a reconnect storm and overload the broker.


## BUG-02 — Buffer count exceeds 8 and drops are not counted after overflow

### Environment

Wokwi in VS Code, firmware homework_buggy, macOS.

### Preconditions

The node is CONNECTED. The buffer is empty.

### Steps

1. Enter RESET STATS.
2. Enter NET DOWN.
3. Enter SEND 12 times.
4. Enter BUFFER and STATUS.
5. Enter NET UP.
6. Check the flush log.

### Expected result

According to R4, the buffer count stays at 8. The four oldest messages are dropped. The dropped counter becomes 4, and the drops appear in the log.

### Actual result

The buffer reports count=12/8. The dropped counter stays at 0. After recovery, IDs 1–4 are absent from the publish log.

### Recovery behavior

The buffer becomes empty after NET UP. The dropped counter remains 0.

### Evidence

```text
21:37:40.843 > [BUFFER] queued id=8 count=8/8
21:37:41.983 > [BUFFER] overflow policy=DROP_OLDEST dropped_total=0
21:37:41.984 > [BUFFER] queued id=9 count=9/8
21:37:43.275 > [BUFFER] queued id=10 count=10/8
21:37:44.608 > [BUFFER] queued id=11 count=11/8
21:37:46.190 > [BUFFER] queued id=12 count=12/8
21:37:50.303 > [BUFFER] flush_start count=12
21:37:50.338 > [BUFFER] flush_end count=0
Final STATUS: buffer=0, capacity=8, dropped=0.
```

### Reproducibility

2/2 overflow tests, with 9 and 12 messages.

### Severity

Major. The buffer count is incorrect, and lost messages are not counted.


## BUG-03 — Buffered messages are published more than once after NET UP

### Environment

Wokwi in VS Code, firmware homework_buggy, macOS.

### Preconditions

The node is CONNECTED. The buffer is empty.

### Steps

1. Enter RESET STATS.
2. Enter NET DOWN.
3. Enter SEND five times.
4. Enter NET UP.
5. Enter STATUS.
6. Count the publish lines for each message ID.

### Expected result

According to R6, each message ID is successfully published only once. Five messages produce sent=5and duplicates=0.

### Actual result

Each of the five IDs is published twice. STATUS reports sent=10 and duplicates=5.

### Recovery behavior

The node returns to CONNECTED and the buffer becomes empty. The repeated publishes have already happened.

### Evidence

```text
20:04:43.020 > [BUFFER] flush_start count=5
20:04:43.020 > [MQTT] publish id=1 temp=24.5
20:04:43.021 > [MQTT] publish id=1 temp=24.5
20:04:43.021 > [MQTT] publish id=2 temp=24.5
20:04:43.021 > [MQTT] publish id=2 temp=24.5
20:04:43.024 > [BUFFER] flush_end count=0
IDs 3–5 are also published twice. In the 12-message test, IDs 5–8 are published twice, and IDs 9–12 are published four times.
```

### Reproducibility

4/4 tests, with 5, 8, 9, and 12 messages.

### Severity

Major. Repeated telemetry can cause incorrect counts and repeated processing on the server.


## BUG-04 — The duplicates counter reports fewer duplicates than the publish log shows after buffer overflow

### Environment

Wokwi in VS Code, firmware homework_buggy, macOS.

### Preconditions

The node is CONNECTED. The buffer is empty.

### Steps

1. Enter RESET STATS.
2. Enter NET DOWN.
3. Enter SEND 12 times.
4. Enter NET UP.
5. Enter STATUS.
6. Compare the duplicates counter with the publish log.

### Expected result

The duplicates counter in STATUS matches the number of repeated publishes. R8 requires this counter as evidence.

### Actual result

The log contains 24 publishes for eight unique IDs. This means 16 publishes are repeats. STATUS reports only duplicates=12.

### Recovery behavior

The next STATUS still reports 12. No counter correction was observed.

### Evidence

```text
Message IDs
	Publishes per ID
	Repeated publishes
	5–8
	2
	4
	9–12
	4
	12
	Total
	24 publishes
	16 repeats
	21:39:07.334 > {"net":"CONNECTED","broker":true,"buffer":0,"capacity":8,"sent":24,"dropped":0,"duplicates":12,"reconnect_attempts":167,"heap":349644}
The nine-message test also shows a difference: 10 repeated publishes in the log, but duplicates=9 in STATUS.
```

### Reproducibility

2/2 overflow tests, with 9 and 12 messages.

### Severity

Minor. The counter gives incorrect diagnostic information. The repeated publishing itself is covered by BUG-03.


## BUG-05 — Free heap keeps decreasing after repeated STRESS commands

### Environment

Wokwi in VS Code, firmware homework_buggy, macOS.

### Preconditions

The node is CONNECTED. The buffer is empty.

### Steps

1. Enter RESET STATS.
2. Enter STATUS and record free heap.
3. Enter STRESS 100.
4. Enter STATUS and record free heap again.
5. Repeat steps 3–4 at least five times.

### Expected result

According to R7, free heap does not show a systematic decrease without recovery during repeated SEND or STRESS commands.

### Actual result

Free heap decreases by about 8,000 bytes per 100 messages. In the full test, it decreases from 349,964 to 189,956 bytes after 2,000 messages. This is a decrease of 160,008 bytes, or about 80 bytes per message.

### Recovery behavior

No heap recovery was observed between the recorded iterations. The node remained CONNECTED and continued to publish messages.

### Evidence

```text
22:00:21.545 > [STRESS] start count=100 heap=349964
22:00:21.764 > [STRESS] end heap=341964


22:01:11.546 > [STRESS] start count=100 heap=341964
22:01:11.777 > [STRESS] end heap=333964


22:01:25.972 > [STRESS] start count=100 heap=333964
22:01:26.196 > [STRESS] end heap=325972
Final STATUS: sent=2000, buffer=0, duplicates=0, heap=189956.
```

### Reproducibility

Observed in all 14 stress iterations within one session. A second test session is still needed.

### Severity

Major. Continued memory loss could lead to memory exhaustion and device failure. No crash was observed in this test.

