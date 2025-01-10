[General]
ned-path = .;../queueinglib
network = un
#cpu-time-limit = 60s
cmdenv-config-name =   unBase
#tkenv-default-config = unBase
qtenv-default-config = unBase
repeat = 5
sim-time-limit = 10000s
#debug-on-errors = true
**.vector-recording = false

[Config unBase]
description = "Global scenario"
**.Sink.lifeTime.result-recording-modes = +histogram
**.LowLoadSrv.queueLength.result-recording-modes = +histogram
**.HiLoadSrv.queueLength.result-recording-modes = +histogram

% for s in [0, 1, 2, 3]:
[Config un_x${"%02d" % int(s*10)}]
extends = unBase
**.sigma = ${s}

%endfor


