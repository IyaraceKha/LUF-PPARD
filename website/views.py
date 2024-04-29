from flask import Blueprint, render_template, request, redirect
from .ppard import scan, empty_remove, new_file, combine_fastq, scan_pic, mkdir, run_analysis, scan_sample
from .sort_string import natural_keys
import math
import schedule
import os
import threading
import re
from datetime import datetime

views = Blueprint('views', __name__)
f = open('schedule.txt', "w")
f.close()
f = open('tmp.txt', "w")
f.close()
f = open('seq_list.txt', "w")
f.close()
f = open("display_list.txt", "w")
f.close()
f = open('sample_list.txt', "w")
f.close()
f = open('current_dashboard.txt', "w")
f.close()

@views.route('/', methods=['GET','POST'])
def home():
    if os.stat('schedule.txt').st_size == 0 :
        return render_template("newsample.html")
    else:
        return render_template("samplewipe.html")

@views.route('/newsample_wipe', methods=['GET','POST'])
def home_wipe():
    f = open('schedule.txt', "w")
    f.close()
    f = open('tmp.txt', "w")
    f.close()
    f = open('seq_list.txt', "w")
    f.close()
    f = open("display_list.txt", "w")
    f.close()
    f = open('sample_list.txt', "w")
    f.close()

    return render_template("newsample.html")

@views.route('/submit', methods=['GET','POST'])
def submit():
    sample_id = request.form.get('sample_id')
    fastqdir = request.form.get('fastqdir')
    outputdir = request.form.get('outputdir')
    min = request.form.get('time')
    time = int(min) * 60
    dbdir = request.form.get('dbdir')

    if fastqdir[len(fastqdir)-1] != "/":
        fastqdir = fastqdir + "/"
    if outputdir[len(outputdir)-1] != "/":
        outputdir = outputdir + "/"
    if dbdir[len(dbdir)-1] != "/":
        dbdir = dbdir + "/"


    f = open("tmp.txt", "w")
    a = sample_id + "\n" + fastqdir + "\n" + outputdir + "\n" + str(time) + "\n" + dbdir
    f.write(a)
    f.close()
    return render_template("submit.html", sample_id = sample_id, fastqdir = fastqdir, outputdir = outputdir, time=time, dbdir=dbdir)

@views.route('/scanfile', methods=['GET','POST'])
def scan_auto():
    schedule.run_pending()
    new_list = []
    f = open("display_list.txt", "r")
    for line in f:
        new_list.append(line.rstrip('\n'))
    f.close()
    return render_template("scanfile.html", new_list = new_list, time_left = 5)

@views.route('/timer', methods=['GET','POST'])
def timer():
    f = open('tmp.txt', "r")
    lines = f.read().splitlines()
    time = int(lines[3])
    if os.stat('schedule.txt').st_size == 0 :
        schedule.every(time).seconds.do(job)
        f = open('schedule.txt', "w")
        f.write(str(time))
        f.close()

    time_max = time
    time_left = math.ceil(schedule.idle_seconds())

    return render_template("timer.html", time_left = time_left, time_max = time_max)

@views.route('/dashboard', methods=['GET','POST'])
def dashboard():
    f = open('current_dashboard.txt', "r")
    sample = f.read()
    f.close()
    if sample == '':
        return redirect('/samplelist')
    else:
        f = open("website/static/" + sample + "/status.txt", "r")
        status = f.read()
        f.close()
        a = scan_pic("website/static/" + sample, "plasmid", ".png")
        plasmid_list = a.split('\n')
        plasmid_list.sort(key=natural_keys)
        plasmid_list.reverse()
        b = scan_pic("website/static/" + sample, "amr", ".png")
        amr_list = b.split('\n')
        amr_list.sort(key=natural_keys)
        amr_list.reverse()
        k2_report_all = []

        k2_report_s = []
        k2_report_g = []
        k2_report_f = []
        k2_report_o = []
        k2_report_c = []
        k2_report_p = []
        k2_report_k = []
        k2_report_d = []
        k2_report_r = []
        k2_report_u = []

        try:
            f = open("website/static/" + sample + "/kraken2_report.txt", "r")
            k2_file = f.read().splitlines()
            f.close()
            k2_file.sort(reverse = True)

            for line in k2_file:
                elem = line.split('\t')
                if float(elem[0]) >= 1:
                    k2_report_all.append(elem)
                    if elem[3].startswith('S'):
                        k2_report_s.append(elem)
                    elif elem[3].startswith('G'):
                        k2_report_g.append(elem)
                    elif elem[3].startswith('F'):
                        k2_report_f.append(elem)
                    elif elem[3].startswith('O'):
                        k2_report_o.append(elem)
                    elif elem[3].startswith('C'):
                        k2_report_c.append(elem)
                    elif elem[3].startswith('P'):
                        k2_report_p.append(elem)
                    elif elem[3].startswith('K'):
                        k2_report_k.append(elem)
                    elif elem[3].startswith('D'):
                        k2_report_d.append(elem)
                    elif elem[3].startswith('R'):
                        k2_report_r.append(elem)
                    elif elem[3].startswith('U'):
                        k2_report_u.append(elem)

        except:
            print("no kraken2 report detected")
        return render_template("dashboard.html", k2_report_all = k2_report_all,
                                                k2_report_s = k2_report_s,
                                                k2_report_g = k2_report_g,
                                                k2_report_f = k2_report_f,
                                                k2_report_o = k2_report_o,
                                                k2_report_c = k2_report_c,
                                                k2_report_p = k2_report_p,
                                                k2_report_k = k2_report_k,
                                                k2_report_d = k2_report_d,
                                                k2_report_r = k2_report_r,
                                                k2_report_u = k2_report_u,
                                                plasmid_list = plasmid_list,
                                                amr_list=amr_list,
                                                sample=sample,
                                                status=status)

@views.route('/samplelist', methods=['GET','POST'])
def samplelist():
    if request.method == 'POST':
        sample = request.form.get('button')
        f = open('current_dashboard.txt', "w")
        f.write(sample)
        f.close()
        return redirect('/dashboard')
    elif request.method == 'GET':
        a = scan_sample("website/static/")
        sample_list = a.splitlines()
        return render_template('samplelist.html', sample_list=sample_list)

def job():
    f = open('tmp.txt', "r")
    lines = f.read().splitlines()
    sample_id = lines[0]
    fastqdir = lines[1]
    output_dir = lines[2]
    db_dir = lines[4]
    new_list = new_file(fastqdir)
    f = open("display_list.txt", "w")
    f.write('\n'.join(new_list))
    f.close()
    if len(new_list) != 0:
        now = datetime.now()
        dt_string = now.strftime("%d-%m-%Y_%H-%M-%S")
        name = sample_id + "_" + dt_string
        dir_name = output_dir + name + "/"
        static_name = "website/static/" + name + "/"
        f = open("sample_list.txt", "a")
        f.write(dir_name + "\n")
        f.close()
        mkdir(dir_name)
        mkdir(static_name)
        combine_fastq(new_list, fastqdir, dir_name)
        f = open("sample_list.txt", "r")
        sample_list = f.read().splitlines()
        f.close()
        f = open(static_name + 'status.txt', "w")
        f.close()
        threading.Thread(target=run_analysis, args=[dir_name, static_name, sample_list, db_dir], daemon=True).start()
        print("start analysis")
