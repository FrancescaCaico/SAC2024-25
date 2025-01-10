[General]
ned-path = .;../queueinglib
network = un2
#cpu-time-limit = 60s
cmdenv-config-name =   un2Base
#tkenv-default-config = un2Base
qtenv-default-config = un2Base
repeat = 5
sim-time-limit = 10000s
#debug-on-errors = true
**.vector-recording = false

[Config un2Base]
description = "Global scenario"
**.Sink.lifeTime.result-recording-modes = +histogram
**.LowLoadSrv.queueLength.result-recording-modes = +histogram
**.HiLoadSrv.queueLength.result-recording-modes = +histogram

% for s in [0, 1, 2, 3]:
[Config un2_x${"%02d" % int(s*10)}]
extends = un2Base
**.sigma = ${s}

%endfor


