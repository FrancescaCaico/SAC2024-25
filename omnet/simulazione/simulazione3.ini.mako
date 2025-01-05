[General]
ned-path = . ;../queueinglib
network = simulazione3
#cpu-time-limit = 10000s
cmdenv-config-name = simulazione3Base
#tkenv-default-config = simulazione3Base
qtenv-default-config = simulazione3Base
repeat = 5
sim-time-limit = 10000s
#debug-on-errors = true
**.vector-recording = false

[Config simulazione3Base]
description = "Global scenario"
**.sink.lifeTime.result-recording-modes = +histogram
**.LocalProcessing.queueLength.result-recording-modes = +histogram

% for ft in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]:
[Config simulazione3_ft${"%04d" % int(ft*1000)}]
extends=simulazione3Base
**.ft = ${ft}
% endfor