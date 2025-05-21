import matplotlib.pyplot as plt
import numpy as np

with open('custom.csv','r') as data:
    lines=data.read().splitlines()
    levels=np.array([li.split(',')[-1] for li in lines])
    events=np.array([li.split(',')[4] for li in lines])
    time1=np.array([li.split(',')[1] for li in lines])
    time=np.array([li.split(',')[1].split('.')[0] for li in lines])

#bar
events_u,events_count = np.unique(events,return_counts=True)
plt.figure()
plt.bar(events_u,events_count)
plt.title('Bar Graph')
plt.savefig('./static/bar_android.png')
plt.close()

#pie
levels_u,levels_counts = np.unique(levels,return_counts=True)
plt.figure()
plt.pie(levels_counts,labels=levels_u)
plt.title('Pie Chart')
plt.savefig('./static/pie_android.png')
plt.close()

#line
time_u,time_counts = np.unique(time,return_counts=True)
time_dict={}
for k,v in zip(time,time1):
    if k not in time_dict:
        time_dict[k] = v
custom_labels = [time_u[i] for i in range(len(time_u)) if i%5==0]
plt.figure()
plt.plot(time_u,time_counts,'r-o')
plt.xticks(custom_labels,[time_dict[i] for i in custom_labels],rotation=90)
plt.title('Line Plot')
plt.tight_layout()
plt.savefig('./static/line_android.png')
plt.close()