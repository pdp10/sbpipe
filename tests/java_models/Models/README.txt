Model from https://github.com/pdp10/simqueue
Author: Piero Dalle Pezze
License: MIT
Year: 2005

This is a queue simulator based on stochastic time events.
It aims to simulate a real queue, like a queue at the post office,
where clients arrive in a random order. When a client arrives, s/he is
the last one who will be served. (FIFO = First In First Out). In particular
there are two stochastic factors:
    1) the time of arrive,
    2) the time of service.
Meanwhile, clients arrive and others leave.
This simulation shows when a person arrives, is ready to be served, and finally leaves.



To generate the jar file, run the python script:
python get_jar_model.py

NOTE: `maven` and `git` packages are required.

