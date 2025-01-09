[General]
ned-path = . ;../queueinglib
network = server
#cpu-time-limit = 10000s
cmdenv-config-name = serverBase
#tkenv-default-config = serverBase
qtenv-default-config = serverBase
repeat = 5
sim-time-limit = 10000s
#debug-on-errors = true
**.vector-recording = false

[Config serverBase]
description = "Global scenario"
**.sink.lifeTime.result-recording-modes = +histogram
**.net.queueLength.result-recording-modes = +histogram
**.cpu.queueLength.result-recording-modes = +histogram
**.disk.queueLength.result-recording-modes = +histogram

%for l in [6.0, 6.5, 6.7, 6.8, 6.9, 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 7.8, 7.900, 7.90126, 7.95, 8, 8.1, 8.2, 8.3]: 
[Config lambda${"%03d" % int(l*1000)}]
extends=serverBase
**.lambda = ${l}
**.mu_net=20
**.mu_cpu=10
**.mu_disk=15
% endfor

