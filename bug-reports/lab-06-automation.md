# Lab 6 — Python and pytest Automation Bug Reports

[Original test report](https://docs.google.com/document/d/188b_UX_jMUF5VH1Q4yGQT1vFHNa87Oas8NXphapZJuY/edit) · [All test reports](../test-reports/README.md) · [Bug report index](README.md)

Extracted from the source report on 2026-11-02. Original bug IDs, stated expectations, severity, reproducibility, and evidence text are retained; no fix retest is implied. Embedded screenshots and video placeholders are not copied by this text extraction; see the original document for available images. Blank fields are marked explicitly.

Environment from the source: BUGGY firmware, Python 3.15.1, pytest 9.1.1, pyserial 3.5, Serial 115200, DEVICE_PORT `rfc2217://localhost:4000`. The source leaves STATUS PWM units unspecified and does not rule out communication truncation for GET TEMP.

## BUG-01 — PWM upper boundary is rejected

### Requirement

SET PWM accepts every integer from 0 through 100 inclusive.(REQ-5)

### Environment

Environment above

### Preconditions

Device connected and responsive; normal fixture setup.

### Test/Steps

1. Send SET PWM 100
   2. Parse the response
   3. Check status is OK.

### Expected

status OK and pwm 100.

### Actual

status ERROR; test stops at the status assertion.

### Raw Serial Evidence

```text
{"status":"OK","reset":true}
{"status":"ERROR","code":"INVALID_VALUE"}
{"status":"OK","reset":true}
```

### Pytest Evidence

```text
______________test_pwm_valid_boundaries[100] _________


device = <device.Device object at 0x10b73fce0>, value = 100


    @pytest.mark.parametrize("value", [0, 1, 50, 99, 100])
    def test_pwm_valid_boundaries(device, value):
        r = device.command(f"SET PWM {value}")
>       assert r["status"] == "OK"
E       AssertionError: assert 'ERROR' == 'OK'
E
E         - OK
E         + ERROR


tests/test_boundaries.py:6: AssertionError
```

### Severity

Major

### Reproducibility

Always


## BUG-02 — STATUS reports inconsistent PWM units

### Requirement

STATUS returns the current PWM state. (REQ-02)

### Environment

Environment above

### Preconditions

Device connected and responsive.

### Test/Steps

1. Send SET PWM 50.
   2. Read its response.
   3. Send STATUS and compare pwm.

### Expected

STATUS reports PWM 50

### Actual

The SET PWM boundary case reports 50 and passes, while STATUS after SET PWM 50 reports 127.

### Raw Serial Evidence

```text
{"status":"OK","pwm":50}
                        {"status":"OK","led":true,"pwm":127,"heap":350116}
```

### Pytest Evidence

```text
______test_reset_restores_safe_state ___________


device = <device.Device object at 0x10b8cdd30>


    def test_reset_restores_safe_state(device):
        device.command("SET LED ON")
        device.command("SET PWM 50")
        status = device.command("STATUS")
>       assert status["pwm"] == 50
E       assert 127 == 50


tests/test_relay.py:9: AssertionError
```

### Severity

Major

### Reproducibility

Always


## BUG-03 — RESET leaves reported PWM nonzero

### Requirement

RESET restores safe outputs: LED OFF and PWM 0. (REQ-07)

### Environment

Environment above

### Preconditions

SET LED ON and SET PWM 50 sent. STATUS confirms led True and pwm nonzero.

### Test/Steps

1. Establish the preconditions
   2. Send RESET
   3. Send STATUS
   4. Check pwm == 0 and led is False.

### Expected

STATUS reports pwm 0 and led False.

### Actual

STATUS reports pwm 127 after RESET. The LED assertion is not reached.

### Raw Serial Evidence

```text
{"status":"OK","pwm":50}
                        {"status":"OK","led":true,"pwm":127,"heap":349852}
                          {"status":"OK","reset":true}
{"status":"OK","led":true,"pwm":127,"heap":349852}
```

### Pytest Evidence

```text
____________test_reset_restores_safe_state ____________


device = <device.Device object at 0x1078996d0>


    def test_reset_restores_safe_state(device):
        device.command("SET LED ON")
        device.command("SET PWM 50")
        status = device.command("STATUS")
        assert status["pwm"] != 0
        assert status["led"] is True
        device.command("RESET")
        status = device.command("STATUS")
>       assert status["pwm"] == 0
E       assert 127 == 0


tests/test_relay.py:13: AssertionError
```

### Severity

Critical

### Reproducibility

Always


## BUG-04 — GET TEMP returns incomplete JSON

### Requirement

GET TEMP returns valid JSON containing a temperature or an explicit sensor error.(REQ-03)

### Environment

Environment above. Sensor response contains temperature 24.5.

### Preconditions

Device connected; temperature-response test executing.

### Test/Steps

1. Send GET TEMP
   2. Read its response line
   3. Parse the line with json.loads.

### Expected

Valid JSON, for example {"status":"OK","temperature":24.5}.

### Actual

JSON parsing fails because the received text has no closing brace.

### Raw Serial Evidence

```text
{"status":"OK","temperature":24.5
                                 {"status":"OK","reset":true}
```

### Pytest Evidence

```text
______________ test_temperature_response ___________
………..
……….
………..


self = <device.Device object at 0x105bc1cc0>, command = 'GET TEMP'


    def command(self, command):
        raw = self.command_raw(command)
        try:
            return json.loads(raw)
        except json.JSONDecodeError as e:
>           raise AssertionError(f"Invalid JSON from device: {raw!r}") from e
E           AssertionError: Invalid JSON from device: '{"status":"OK","temperature":24.5'


device.py:31: AssertionError
```

### Severity

Critical

### Reproducibility

Always

