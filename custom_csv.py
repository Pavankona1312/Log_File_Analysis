#!/usr/bin/env python
import sys

log = sys.argv[1]
event = sys.argv[2]
if log == "All":
    log = ['notice','error']
else:
    log = [log]
if event == "All":
    event = ['E1','E2','E3','E4','E5','E6']
else:
    event = []
    for i in range(2,len(sys.argv)):
        event.append(sys.argv[i])

with open('custom.csv','r') as def_data:
    lines = def_data.read().split('\n')
    lines.pop()
    lines = [li.split(',') for li in lines if (li.split(',')[1] in log) and (li.split(',')[3] in event)]

with open("custom.csv", "w") as file:
    for row_list in lines:
        line = ",".join(str(item) for item in row_list)
        file.write(line + "\n")