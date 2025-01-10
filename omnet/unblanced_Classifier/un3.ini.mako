[General]
ned-path = .;../queueinglib
network = un3
#cpu-time-limit = 60s
cmdenv-config-name =   un3Base
#tkenv-default-config = un3Base
qtenv-default-config = un3Base
repeat = 5
sim-time-limit = 10000s
#debug-on-errors = true
**.vector-recording = false

[Config un3Base]
description = "Global scenario"
**.Sink1.lifeTime.result-recording-modes = +histogram
**.Sink2.lifeTime.result-recording-modes = +histogram
**.LowLoadSrv.queueLength.result-recording-modes = +histogram
**.HiLoadSrv.queueLength.result-recording-modes = +histogram

% for s in [0, 1, 2, 3]:
[Config un3_x${"%02d" % int(s*10)}]
extends = un3Base
**.sigma = ${s}

%endfor


