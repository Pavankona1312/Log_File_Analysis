import sys
from date_functions import timestamp_comparison,get_date_andr

from_time = [sys.argv[1],sys.argv[2]]
to_time = [sys.argv[3],sys.argv[4]]
level = sys.argv[5]
event = sys.argv[6]

with open('default.csv','r') as def_data:
    tmp_lines = def_data.read().split('\n')
    tmp_lines.pop()
    lines=[]
    for li in tmp_lines:
        #t1=['2025-03-17T16:13:38',811]
        t1 = ['2025-'+li.split(',')[0]+'T'+li.split(',')[1].split('.')[0],int(li.split(',')[1].split('.')[1])] 
        eve = li.split(',')[-1]
        lev = li.split(',')[4]
        if timestamp_comparison(t1,from_time) and timestamp_comparison(to_time,t1):
            if (lev == level or level=='ALL') and (eve == event or event=='ALL'):
                lines.append(li.split(','))

with open("custom.csv", "w") as file:
    for row_list in lines:
        line = ",".join(str(item) for item in row_list)
        file.write(line + "\n")
