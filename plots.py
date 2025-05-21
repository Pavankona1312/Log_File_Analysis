import matplotlib.pyplot as plt
import numpy as np
from date_functions import time_list,get_date

with open('custom.csv','r') as data:
    init_time = time_list(get_date(data.read().split(',')[0]))


def ref_time(t1,t2=init_time): #gives the time difference between t1 and t2 in seconds.
    mon_dict = {
        1 : 31,
        2 : 59,
        3 : 89,
        4 : 120,
        5 : 151,
        6 : 181,
        7 : 212,
        8 : 243,
        9 : 273,
        10 : 304,
        11 : 334,
        12 : 365
    }
    t1[1] = mon_dict[t1[1]]
    if t2[1]<=12 and t2[1] >=1:
        t2[1] = mon_dict[t2[1]]
    tmp = [t1[i]-t2[i] for i in range(len(t1))]
    ref = tmp[0]*525600 + (tmp[1]+tmp[2])*1440 + tmp[3]*60 + tmp[4] + tmp[5]/60
    #yr * 525600{removing leap years}
    #mon -> days --> * 1440
    #days* 1440
    #hrs * 60
    #min*1
    #sec/60
    return ref*60

with open('custom.csv','r') as data:
    lines = data.read().split('\n')
    events = np.array([li.split(',')[3] for li in lines if li])
    time1 = np.array([li.split(',')[0] for li in lines if li])
    time = [time_list(get_date(li.split(',')[0])) for li in lines if li]
    log_levels = np.array([li.split(',')[1] for li in lines if li])

# "from each data line, timestamp is taken and is converted into list yr,mon...", time represents list of these lists.
# time1 represents an array of all timestamps from data which is used for labelling.
# time2 represents an array of all reference times (w.r.t to init time,i.e,from first time stamp) 
# time_u represents the array of all unique  elements in time2
# time_counts represents the count of those unique elements
# time_dict represents the mapping between the elements of time_u and their previous form (their initial time stamp) which is used in labelling.

time2 = np.array([ref_time(i) for i in time])

time_dict = {}
for k,v in zip(time2,time1):
    if k not in time_dict:
        time_dict[k] = v

time_u,time_counts = np.unique(time2,return_counts=True)
custom_labels = [time_u[0]]
for i in time_u:
    if i - custom_labels[-1]>=1100: #This should be modified because it only works for apache2k.log. This helps in having only some labels such that they are readable.
        custom_labels.append(i)
# The above for loop is to add equally spaced times to custom_labels and whose gap is decided in consideration of readability,specifically for apache2k.log and image size manually.
plt.figure(figsize=(20,5))
plt.plot(time_u,time_counts,'r-o')
plt.xticks(custom_labels,[time_dict[i] for i in custom_labels],rotation=90)
plt.title('Line Plot')
plt.tight_layout()
plt.savefig('./static/line.png',bbox_inches='tight')
plt.close()

events_u,events_count = np.unique(events,return_counts=True)
plt.figure()
plt.bar(events_u,events_count)
plt.title('Bar Graph')
plt.savefig('./static/bar.png')
plt.close()

log_levels_u,log_levels_counts = np.unique(log_levels,return_counts=True)
plt.figure()
plt.pie(log_levels_counts,labels=log_levels_u)
plt.title('Pie Chart')
plt.savefig('./static/pie.png')
plt.close()


