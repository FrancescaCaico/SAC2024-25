[General]
ned-path = . ;../queueinglib
network = server2
#cpu-time-limit = 10000s
cmdenv-config-name = server2Base
#tkenv-default-config = server2Base
qtenv-default-config = server2Base
repeat = 5
sim-time-limit = 10000s
#debug-on-errors = true
**.vector-recording = false

[Config server2Base]
description = "Global scenario"
**.sink.lifeTime.result-recording-modes = +histogram
**.net.queueLength.result-recording-modes = +histogram
**.cpu1.queueLength.result-recording-modes = +histogram
**.cpu2.queueLength.result-recording-modes = +histogram
**.disk.queueLength.result-recording-modes = +histogram

%for l in [10, 10.2, 10.4, 10.6, 10.8, 11, 11.2, 11.4, 11.5, 11.6, 11.7, 11.8, 11.9, 11.91, 11.92, 11.93, 11.94,  11.95, 11.96, 11.97, 11.98, 11.99, 12, 12.1, 12.15, 12.20, 12.25, 12.30]: 
[Config server2_lambda${"%03d" % int(l*1000)}]
extends=server2Base
**.lambda = ${l}
**.mu_net=20
**.mu_cpu=10
**.mu_disk=15
% endfor

