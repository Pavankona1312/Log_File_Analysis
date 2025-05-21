def time_list(t1):
    #t1='2025-03-17T16:13:38'
    time1 = t1.split('T')[1]
    return [int(t1[0:4]),int(t1[5:7]),int(t1[8:10]),int(time1[0:2]),int(time1[3:5]),int(time1[6:8])]

def time_list_andr(t1):
    #t1=['2025-03-17T16:13:38',811]
    time1 = t1[0].split('T')[1]
    return [int(t1[0][0:4]),int(t1[0][5:7]),int(t1[0][8:10]),int(time1[0:2]),int(time1[3:5]),int(time1[6:8]),int(t1[1])]

                
def timestamp_comparison(t1,t2):
    #returns true if t1>=t2
    return tuple(time_list_andr(t1))>=tuple(time_list_andr(t2))

def get_date(time):
    #from:Sun Dec 04 04:47:44 2005
    #to:2005-12-04T04:47:44
    dy,mon,dt,tim,yr = time.split(' ')
    mon_dict = {
        'Jan' : '01',
        'Feb' : '02',
        'Mar' : '03',
        'Apr' : '04',
        'May' : '05',
        'Jun' : '06',
        'Jul' : '07',
        'Aug' : '08',
        'Sep' : '09',
        'Oct' : '10',
        'Nov' : '11',
        'Dec' : '12'
    }
    num_date = f'{yr}-{mon_dict[mon]}-{dt}T{tim}'
    return num_date

def change_date(time):
    #from: 2005-12-04T04:47:44
    #to: 'Sun Dec 04 04:47:44 2005'
    time1 = [time[0:4],time[5:7],time[8:10],time.split('T')[1][0:2],time.split('T')[1][3:5],time.split('T')[1][6:8]]
    mon_dict = {
        '01':'Jan',
        '02':'Feb',
        '03':'Mar',
        '04':'Apr',
        '05':'May',
        '06':'Jun',
        '07':'Jul',
        '08':'Aug',
        '09':'Sep',
        '10':'Oct',
        '11':'Nov',
        '12':'Dec' 
    }
    tmp=f'Sun {mon_dict[time1[1]]} {time1[2]} {time1[3]}:{time1[4]}:{time1[5]} {time1[0]}'
    return tmp

def get_date_andr(time):
    #from: 03-17,16:13:38.811
    #to: ['2025-03-17T16:13:38',811]
    tmp=time.replace(',','T')
    tmp='2025-'+tmp
    tmp=tmp.split('.')
    return tmp