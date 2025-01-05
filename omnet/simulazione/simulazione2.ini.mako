[General]
ned-path = . ;../queueinglib
network = simulazione2
#cpu-time-limit = 10000s
cmdenv-config-name = simulazione2Base
#tkenv-default-config = simulazione2Base
qtenv-default-config = simulazione2Base
repeat = 5
sim-time-limit = 10000s
#debug-on-errors = true
**.vector-recording = false

[Config simulazione2Base]
description = "Global scenario"
**.sink.lifeTime.result-recording-modes = +histogram
**.LocalProcessing.queueLength.result-recording-modes = +histogram

% for ft in [ 0.500, 0.501, 0.502, 0.503, 0.504, 0.505, 0.506, 0.507, 0.508, 0.509, 0.510]:
[Config simulazione2_ft${"%04d" % int(ft*1000)}]
extends=simulazione2Base
**.ft = ${ft}
% endfor