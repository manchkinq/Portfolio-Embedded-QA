# Embedded QA Portfolio

Practical Embedded QA coursework covering seven Arduino/ESP32 labs: control logic, button debounce, UART/CLI, I2C fault injection, recovery and persistence, Python automation, and network resilience.

## Technologies and approach

**Tools:** Wokwi, PlatformIO, PulseView, Python, pytest, pyserial, Git.

**Interfaces and formats:** GPIO, UART, I2C, JSON, RFC2217, simulated MQTT publishing.

Testing includes state transitions, boundary and negative cases, protocol analysis, fault injection, recovery, and memory stability. Findings are documented with reproduction steps, logs, and available signal captures.

## Portfolio contents

| Section | Contents |
|---|---|
| [Master Test Plan](MASTER_TEST_PLAN.docx) | Portfolio-wide scope, risks, coverage, regression, and readiness criteria |
| [Wokwi projects](wokwi/) | Firmware and simulation projects for Labs 1–7 |
| [Test reports](test-reports/) | Links to detailed lab reports and results |
| [Bug reports](bug-reports/) | Defect reports grouped by lab |
| [PulseView analysis](pulseview/) | Lab 4 I2C screenshots and protocol analysis |
| [Python automation](pytest/) | Lab 6 serial CLI tests, fixtures, and helper |
| [Network resilience](network-stress/) | Lab 7 scenarios and links to supporting evidence |
| [Resume](resume/) | CV section |

## Scope

These are educational projects using intentionally buggy firmware. My work focuses on test design, execution, automation extensions, evidence analysis, and reporting. Results primarily come from Wokwi simulation.
