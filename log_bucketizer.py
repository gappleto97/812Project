# This script re-orders the events in a log into probable-concurrent "buckets"
# To run, call like "python log_bucketizer.py <log name>"
# It will produce a file called <log name>.bucketized
from json import dumps, loads
from sys import argv

filepath = argv[-1]
events = []
NUM_NODES = 4
with open(filepath, 'r') as f:
    for idx, line in enumerate(f.readlines()):
        if idx:
            line = line[line.index(":")+1:-1]
            line = line[line.index(":")+1:]
            events.append(loads(line))

buckets = [[]]
curr_group = "send"
for event in events:
    if event[curr_group]:
        buckets[-1].append(event)
    else:
        if curr_group == "send":
            curr_group = "recv"
        elif curr_group == "recv":
            curr_group = "send"
        buckets.append([event])
with open(filepath + '.bucketized', 'w') as f:
    f.write(dumps(buckets))