import os
import subprocess
from flask import Flask, render_template, flash, request, redirect,send_from_directory
from werkzeug.utils import secure_filename
from date_functions import get_date,change_date,get_date_andr


UPLOAD_FOLDER = ''
ALLOWED_EXTENSION = 'log'
app = Flask(__name__)
app.secret_key = 'Hello! This is for enabling flash messages and storing the user specific data'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def check_file(filename):
    name,ext = filename.rsplit('.',1) #much better than filename.split('.') because it doesn't work if multiple dot is there or not.
    return ext == ALLOWED_EXTENSION

@app.route('/download/<filename>') #for able to refer/downloaad files in current directory through html.
def download_file(filename):
    return send_from_directory('.', filename, as_attachment=True)

@app.route('/',methods=['GET','POST'])
def file_upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return render_template('home.html')
        file = request.files['file']
        if file.filename == '':
            flash("No file selected")
            return render_template('home.html')
        if file and check_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)) 
            log=request.form.get('log_type')
            if log == "apache":
                bash_file="./check.sh"
            elif log == "android":
                bash_file="./check_android.sh"
            bash = subprocess.run([bash_file,filename],stdout=subprocess.PIPE,text=True)
            if bash.stdout.strip() == "err":
                flash(f'{filename} is not a valid {log} log file')
                return render_template('home.html')
            if log == "apache":
                return redirect('/view')
            return redirect('/view_android')
        if not check_file(file.filename):
            flash("Wrong type of file is uploaded")
            return render_template('home.html')
    return render_template('home.html')

@app.route('/view_android',methods=['GET','POST'])
def parse_csv_android():
    with open('default.csv','r') as data:
        tmp_def_csv_list=data.read().split('\n')
    def_csv_list=[]
    for li in tmp_def_csv_list:
            tmp=li.split(',')[0:6]
            tmp.append(','.join(li.split(',')[6:-1]))
            tmp.append(li.split(',')[-1])
            def_csv_list.append(tmp)

    if request.method == 'POST':
        time_from = request.form.getlist('from-time')[0]
        ms_from = request.form.getlist('from-time')[1]
        time_to = request.form.getlist('to-time')[0]
        ms_to = request.form.getlist('to-time')[1]
        level=request.form.get('level')
        event=request.form.get('event')
        subprocess.run(["python3","custom_android_csv.py",time_from,ms_from,time_to,ms_to,level,event])
        with open('custom.csv','r') as data:
            tmp_csv_list=data.read().split('\n')
            csv_list=[]
        for li in tmp_csv_list:
            tmp=li.split(',')[0:6]
            tmp.append(','.join(li.split(',')[6:-1]))
            tmp.append(li.split(',')[-1])
            csv_list.append(tmp)
        return render_template("view_csv_andr.html",csv=csv_list[0:-1],min_date=get_date_andr(','.join(def_csv_list[0][0:2]))[0],max_date=get_date_andr(','.join(def_csv_list[-2][0:2]))[0],down="custom")    
    return render_template("view_csv_andr.html",csv=def_csv_list[0:-1],min_date=get_date_andr(','.join(def_csv_list[0][0:2]))[0],max_date=get_date_andr(','.join(def_csv_list[-2][0:2]))[0],down="default")



@app.route('/view',methods=['GET','POST'])
def parse_csv():

    with open('default.csv','r') as data:
        def_csv_list=data.read().split('\n')
    def_csv_list = [li.split(',') for li in def_csv_list]

    if request.method == 'POST':
        time_from = request.form.get('from-time')
        time_to = request.form.get('to-time')
        subprocess.run(["bash","custom_csv.sh",change_date(time_from),change_date(time_to)])
        log_level = request.form.get('level')
        events = request.form.getlist('event')
        custom = request.form.get('custom')
        tmp_lis = ["python3","./custom_csv.py",log_level]
        if custom == "All":
            tmp_lis.append(custom)
        elif custom == "Cus":
            for x in events:
                tmp_lis.append(x)
        subprocess.run(tmp_lis)  #Change Here according to python3 or python
        with open('custom.csv','r') as data:
            csv_list=data.read().split('\n')
        csv_list = [li.split(',') for li in csv_list] 
        return render_template("view_csv.html",csv=csv_list[0:-1],min_date=get_date(def_csv_list[0][0]),max_date=get_date(def_csv_list[-2][0]),down="custom")    
    return render_template("view_csv.html",csv=def_csv_list[0:-1],min_date=get_date(def_csv_list[0][0]),max_date=get_date(def_csv_list[-2][0]),down="default") 


@app.route('/plot_android',methods=['GET','POST'])
def get_andr_graphs():
    with open('default.csv','r') as data:
        tmp_def_csv_list=data.read().split('\n')
    def_csv_list=[]
    for li in tmp_def_csv_list:
            tmp=li.split(',')[0:6]
            tmp.append(','.join(li.split(',')[6:-1]))
            tmp.append(li.split(',')[-1])
            def_csv_list.append(tmp)

    if request.method == 'POST':
        time_from = request.form.getlist('from-time')[0]
        ms_from = request.form.getlist('from-time')[1]
        time_to = request.form.getlist('to-time')[0]
        ms_to = request.form.getlist('to-time')[1]
        level=request.form.get('level')
        event=request.form.get('event')
        subprocess.run(["python3","custom_android_csv.py",time_from,ms_from,time_to,ms_to,level,event])
        subprocess.run(['python3','./plots_android.py'])
        return render_template("view_android_graph.html",min_date=get_date_andr(','.join(def_csv_list[0][0:2]))[0],max_date=get_date_andr(','.join(def_csv_list[-2][0:2]))[0],insert=request.form.get('plot')) #add ms_max and ms_min
    return render_template("view_android_graph.html",min_date=get_date_andr(','.join(def_csv_list[0][0:2]))[0],max_date=get_date_andr(','.join(def_csv_list[-2][0:2]))[0],insert='None') #add ms_max and ms_min


@app.route('/plot',methods=['GET','POST'])
def get_graphs():

    with open('default.csv','r') as data:
        def_csv_list=data.read().split('\n')
    def_csv_list = [li.split(',') for li in def_csv_list]

    if request.method == 'POST':
        time_from = request.form.get('from-time')
        time_to = request.form.get('to-time')
        subprocess.run(["bash","custom_csv.sh",change_date(time_from),change_date(time_to)])
        log_level = request.form.get('level')
        events = request.form.getlist('event')
        custom = request.form.get('custom')
        tmp_lis = ["python3","./custom_csv.py",log_level]
        if custom == "All":
            tmp_lis.append(custom)
        elif custom == "Cus":
            for x in events:
                tmp_lis.append(x)
        subprocess.run(tmp_lis)   #Change Here according to python3 or python
        subprocess.run(['python3','./plots.py'])
        return render_template("view_graph.html",min_date=get_date(def_csv_list[0][0]),max_date=get_date(def_csv_list[-2][0]),insert=request.form.get('plot'))
    return render_template("view_graph.html",min_date=get_date(def_csv_list[0][0]),max_date=get_date(def_csv_list[-2][0]),insert='None')