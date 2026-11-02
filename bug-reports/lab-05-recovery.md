# Lab 5 — Recovery and Persistence Bug Reports

[Original test report](https://docs.google.com/document/d/18KPHyfEkjMFHiidPlZD5t6V4S-TQKVWjVD0pNDTMhGE/edit) · [All test reports](../test-reports/README.md) · [Bug report index](README.md)

Original bug IDs, stated expectations, severity, reproducibility, and evidence text are retained; no fix retest is implied. Embedded screenshots and video placeholders are not copied by this text extraction; see the original document for available images.

## BUG-01 — Sleep time is 10 times less than input value

### Requirement

R4

### Risk

Timing

### Preconditions

Device is in ACTIVE status

### Steps

1. Input command ‘sleep 50’

### Expected

Sleep for 50sec

### Actual

Sleep for 5s

### Timing / Reset Reason

DEEPSLEEP_RESET

### Evidence

evidence6*

### Severity

Major

### Reproducibility

Always


## BUG-02 — System goes in sleep status when input is ‘sleep’ without a value

### Requirement

R4

### Risk

Wrong command process

### Preconditions

Device is in ACTIVE status

### Steps

1. Input command ‘sleep’

### Expected

Error in logs that command is incorrect. No influence on system.

### Actual

Sleep for 5s

### Timing / Reset Reason

DEEP_SLEEP

### Evidence

evidence5*

### Severity

Major

### Reproducibility

Always


## BUG-03 — Relay state is not set to OFF after Watchdog reset causing unsafe behaviour

### Requirement

R5

### Risk

Safe actuator state

### Preconditions

Device is in ACTIVE status

### Steps

1. Input relay ON
2. Simulate device hang with input command “hang”
3. Wait until device reset and check the relay status

### Expected

Relay state is set to OFF after emergency Watchdog reset

### Actual

Relay state is not set to OFF after Watchdog reset

### Timing / Reset Reason

INT_WDT

### Evidence

evidence1*

### Severity

Critical

### Reproducibility

Always


## BUG-04 — Event counter does not correspond to relay actions number when interrupted save

### Requirement

R6

### Risk

Data integrity

### Preconditions

Device is in ACTIVE status; Event counter value is more than 0.

### Steps

1. Input command ‘status’
2. Remember the number of ‘counter’
3. Simulate interrupt save with input command “powerloss”
4. Wait until device reset
5. Input command ‘status’ and observe counter

### Expected

Event counter corresponds to relay actions number when interrupted save

### Actual

Event counter does not correspond to relay actions number when interrupted save. Counter adds +100 events.

### Timing / Reset Reason

SOFTWARE_RESET

### Evidence

evidence2*

### Severity

Major

### Reproducibility

Always


## BUG-05 — Errors are absent in logs when the device loses connection to the sensor

### Requirement

R2

### Risk

Explicit invalid-data handling

### Preconditions

Device is in ACTIVE status

### Steps

1. Simulate device loss connection to the temperature sensor
2. Input command ‘sensor’
3. Observe the output

### Expected

Clear controlled ERROR in logs that shows device lost connection to the sensor. Fake temperature data is not shown.

### Actual

Errors are absent in logs when the device loses connection to the sensor. Output shows fake temperature data: Temp = 0; humidity = 0.

### Evidence

evidence3*

### Severity

Major

### Reproducibility

Always


## BUG-06 — Sometimes after one physical button press there are two logical events

### Requirement

R3

### Risk

Single logical event

### Preconditions

Device is in ACTIVE status

### Steps

1. Check the relay status
2. Press the button
3. Observe the relay status after press

### Expected

Always one physical press = one logical event

### Actual

Sometimes after one physical button press there are two logical events

### Severity

Major

### Reproducibility

Intermittent


## BUG-07 — System reset with INT_WDT reason after 1sec device goes to sleep status

### Requirement

R5, R4

### Risk

System between state behaviour

### Preconditions

Device is in ACTIVE status

### Steps

1. Input command ‘sleep 50’
2. Check logs in ~1sec
3. Observe logs after system reset

### Expected

No system resets during device sleep status

### Actual

System reset with INT_WDT reason  after 1sec device goes to sleep status

### Evidence

evidence6*

### Timing / Reset Reason

INT_WDT and DEEP_SLEEP

### Severity

Critical

### Reproducibility

Always


## Source evidence appendix

Text attachments referenced as evidence1–evidence6 in the bug reports. Screenshot-only content remains in the original document.

```text
evidence1:


[STORE] saved
[BUTTON] relay=ON
                 [FAULT] firmware hang
E (99544) task_wdt: Task watchdog got triggered. The following tasks did not reset the watchdog in time:
E (99544) task_wdt:  - loopTask (CPU 1)
E (99544) task_wdt: Tasks currently running:
E (99544) task_wdt: CPU 0: IDLE0
E (99544) task_wdt: CPU 1: loopTask
E (99544) task_wdt: Aborting.
abort() was called at PC 0x400dbf11 on core 0
Backtrace: 0x400835b5:0x3ffbea8c |<-CORRUPTED
ELF file SHA256: eb097c4b0755de0a
ets Jul 29 2019 12:21:46
rst:0x8 (TG1WDT_SYS_RESET),boot:0x13 (SPI_FAST_FLASH_BOOT)
configsip: 0, SPIWP:0xee
clk_drv:0x00,q_drv:0x00,d_drv:0x00,cs0_drv:0x00,hd_drv:0x00,wp_drv:0x00
mode:DIO, clock div:2
load:0x3fff0030,len:1156
load:0x40078000,len:11456
ho 0 tail 12 room 4
load:0x40080400,len:2972
entry 0x400805dc
[BOOT] reset_reason=INT_WDT
                           [WDT] enabled timeout=4000 ms
                                                        Commands:
  help
  status
  sensor
  relay on
  relay off
  save
  sleep <seconds>
  hang
  powerloss
  reboot
{"state":"ACTIVE","reset_reason":"INT_WDT","relay":true,"counter":2,"heap":336332,"sensor_ok":false}


evidence2:
{"state":"ACTIVE","reset_reason":"POWER_ON","relay":true,"counter":6,"heap":336332,"sensor_ok":false}
[CLI] ERROR unknown command
[FAULT] power loss DURING save
ets Jul 29 2019 12:21:46


rst:0xc (SW_CPU_RESET),boot:0x13 (SPI_FAST_FLASH_BOOT)
configsip: 0, SPIWP:0xee
clk_drv:0x00,q_drv:0x00,d_drv:0x00,cs0_drv:0x00,hd_drv:0x00,wp_drv:0x00
mode:DIO, clock div:2
load:0x3fff0030,len:1156
load:0x40078000,len:11456
ho 0 tail 12 room 4
load:0x40080400,len:2972
entry 0x400805dc
[BOOT] reset_reason=SOFTWARE_RESET
                                  [WDT] enabled timeout=4000 ms
                                                               Commands:
  help
  status
  sensor
  relay on
  relay off
  save
  sleep <seconds>
  hang
  powerloss
  reboot
{"state":"ACTIVE","reset_reason":"SOFTWARE_RESET","relay":true,"counter":106,"heap":336332,"sensor_ok":false}


evidence3
  
Errors that indicates sensor failure are absent:

ets Jul 29 2019 12:21:46

rst:0x1 (POWERON_RESET),boot:0x13 (SPI_FAST_FLASH_BOOT)
configsip: 0, SPIWP:0xee
clk_drv:0x00,q_drv:0x00,d_drv:0x00,cs0_drv:0x00,hd_drv:0x00,wp_drv:0x00
mode:DIO, clock div:2
load:0x3fff0030,len:1156
load:0x40078000,len:11456
ho 0 tail 12 room 4
load:0x40080400,len:2972
entry 0x400805dc
[BOOT] reset_reason=POWER_ON
                            [WDT] enabled timeout=4000 ms
                                                         Commands:
  help
  status
  sensor
  relay on
  relay off
  save
  sleep <seconds>
  hang
  powerloss
  reboot
[SENSOR] temp=0.0C humidity=0.0%


evidence5*
LOGS:
sleep
[STORE] saved
[STATE] SLEEP timer=5 s
ets Jul 29 2019 12:21:46


rst:0x5 (DEEPSLEEP_RESET),boot:0x13 (SPI_FAST_FLASH_BOOT)
configsip: 0, SPIWP:0xee
clk_drv:0x00,q_drv:0x00,d_drv:0x00,cs0_drv:0x00,hd_drv:0x00,wp_drv:0x00
mode:DIO, clock div:2
load:0x3fff0030,len:1156
load:0x40078000,len:11456
ho 0 tail 12 room 4
load:0x40080400,len:2972
entry 0x400805dc
[BOOT] reset_reason=DEEP_SLEEP
[WAKE] cause=4
[WDT] enabled timeout=4000 ms
Commands:
  help
  status
  sensor
  relay on
  relay off
  save
  sleep <seconds>
  hang
  powerloss
  reboot


evidence6*
sleep 50
[STORE] saved
[STATE] SLEEP timer=50 s
ets Jul 29 2019 12:21:46


rst:0x8 (TG1WDT_SYS_RESET),boot:0x13 (SPI_FAST_FLASH_BOOT)
configsip: 0, SPIWP:0xee
clk_drv:0x00,q_drv:0x00,d_drv:0x00,cs0_drv:0x00,hd_drv:0x00,wp_drv:0x00
mode:DIO, clock div:2
load:0x3fff0030,len:1156
load:0x40078000,len:11456
ho 0 tail 12 room 4
load:0x40080400,len:2972
entry 0x400805dc
[BOOT] reset_reason=INT_WDT
[WDT] enabled timeout=4000 ms
Commands:
  help
  status
  sensor
  relay on
  relay off
  save
  sleep <seconds>
  hang
  powerloss
  reboot
======
in 5 sec
======
ets Jul 29 2019 12:21:46


rst:0x5 (DEEPSLEEP_RESET),boot:0x13 (SPI_FAST_FLASH_BOOT)
configsip: 0, SPIWP:0xee
clk_drv:0x00,q_drv:0x00,d_drv:0x00,cs0_drv:0x00,hd_drv:0x00,wp_drv:0x00
mode:DIO, clock div:2
load:0x3fff0030,len:1156
load:0x40078000,len:11456
ho 0 tail 12 room 4
load:0x40080400,len:2972
entry 0x400805dc
[BOOT] reset_reason=DEEP_SLEEP
[WAKE] cause=4
[WDT] enabled timeout=4000 ms
Commands:
  help
  status
  sensor
  relay on
  relay off
  save
  sleep <seconds>
  hang
  powerloss
  reboot
```
