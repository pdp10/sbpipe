Model from https://github.com/pdp10/simqueue
Author: Piero Dalle Pezze
License: MIT
Year: 2005

This is a queue simulator based on stochastic time events. The aim is to simulate a real queue,
like a queue at the post office, where users arrive in a random order. When a client arrives,
s/he is the last one who will be served. Therefore, this is a FIFO (First In First Out) queue.

For each client there are two stochastic events: arrival and service times. In this simulation,
the arrival time is sampled from an exponential distribution, whereas the service time from a
triangular distribution.

This simulation shows when a person arrives, is ready to be served, and finally leaves.



To generate the jar file, run the python script:
python get_jar_model.py

NOTE: `maven` and `git` packages are required.

