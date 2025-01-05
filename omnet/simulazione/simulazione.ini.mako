[General]
ned-path = . ;../queueinglib
network = simulazione
#cpu-time-limit = 10000s
cmdenv-config-name = simulazioneBase
#tkenv-default-config = simulazioneBase
qtenv-default-config = simulazioneBase
repeat = 5
sim-time-limit = 10000s
#debug-on-errors = true
**.vector-recording = false

[Config simulazioneBase]
description = "Global scenario"
**.sink.lifeTime.result-recording-modes = +histogram
**.LocalProcessing.queueLength.result-recording-modes = +histogram

% for ft in [0.7]:
[Config simulazione_ft${"%03d" % int(ft*100)}]
extends=simulazioneBase
**.ft = ${ft}

% endfor