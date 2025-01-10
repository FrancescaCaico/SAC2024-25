[General]
ned-path = .;../queueinglib
network = lognormal
#cpu-time-limit = 60s
cmdenv-config-name =   lognormalBase
#tkenv-default-config = lognormalBase
qtenv-default-config = lognormalBase
repeat = 3
sim-time-limit = 300s
#debug-on-errors = true
**.vector-recording = false

[Config lognormalBase]
description = "Global scenario"
**.sink.lifeTime.result-recording-modes = +histogram
**.srv.queueLength.result-recording-modes = +histogram

% for rho in [0.7, 0.9]:
% for cv in [0.5, 1.0, 1.5]: 
[Config lognormal_rho${"%02d" % int(rho*10)}_cv${"%02d" % int(cv*10)}]
extends = lognormalBase
**.rho = ${rho}
**.cv = ${cv}

%endfor
%endfor