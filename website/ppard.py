import subprocess
import datetime
import os
from .bedtools_bga_plotly import plot_bga
import threading

lock = threading.Lock()

def empty_remove(a):
    new_list = []
    for x in a:
        if x != '':
            new_list.append(x)
    return new_list

def print_list(list):
    for x in list:
        print(x)

def mkdir(file_path):
    mkdir = subprocess.Popen(["mkdir", file_path])
    mkdir.wait()

def combine_fastq(list, fastq_dir, output_dir):
    cat_list = ["cat"]
    for x in list:
        y = fastq_dir + x
        cat_list.append(y)
    file_name = output_dir + "combined.fastq"
    cat_out = open(file_name, "w")
    cat = subprocess.Popen(cat_list, stdout=cat_out)
    cat.wait()
    cat_out.close()

def run_analysis(output_dir, static_dir, sample_list, db_dir):
        lock.acquire()
        kraken = subprocess.Popen(["kraken2", "--db", db_dir + "kraken","--output", output_dir + "kraken2_output.txt","--report", output_dir + "kraken2_report.txt", output_dir + "combined.fastq"],)
        kraken.wait()
        if(len(sample_list) < 2):
            copy = subprocess.Popen(["cp", output_dir + "kraken2_report.txt", static_dir + "kraken2_report.txt"])
            copy.wait()
        else:
            list = ["python", "website/combine_kreports.py", "--no-headers", "--only-combined", "-r"]
            for line in sample_list:
                list.append(line + "kraken2_report.txt")
            list.append("-o")
            list.append(static_dir + "kraken2_report.txt")
            combine_kreports = subprocess.Popen(list)
            combine_kreports.wait()

        card_out = open(output_dir + "card.sam", "w")
        card = subprocess.Popen(["minimap2", "-ax", "map-ont", db_dir + "card/card.mmi", output_dir + "combined.fastq"], stdout=card_out)
        card.wait()
        card_out.close()
        card_sort_out = open(output_dir + "card_sorted.sam", "w")
        card_sort = subprocess.Popen(["samtools", "sort", output_dir + "card.sam"], stdout=card_sort_out)
        card_sort.wait()
        card_sort_out.close()
        card_sort_bam_out = open(output_dir + "card_sorted.bam", "w")
        card_sort_bam = subprocess.Popen(["samtools", "view", "-bS", output_dir + "card_sorted.sam"], stdout=card_sort_bam_out)
        card_sort_bam.wait()
        card_sort_bam_out.close()
        if(len(sample_list) < 2):
            copy = subprocess.Popen(["cp", output_dir + "card_sorted.bam", static_dir + "card_sorted.bam"])
            copy.wait()
            card_cov_out = open(static_dir + "card_cov.bed", "w")
            card_cov = subprocess.Popen(["bedtools", "genomecov", "-bga", "-ibam", static_dir + "card_sorted.bam"], stdout=card_cov_out)
            card_cov.wait()
            card_cov_out.close()
        else:
            list = ["samtools", "merge", static_dir + "card_sorted.bam"]
            for line in sample_list:
                list.append(line + "card_sorted.bam")
            card_combine = subprocess.Popen(list)
            card_combine.wait()
            card_cov_out = open(static_dir + "card_cov.bed", "w")
            card_cov = subprocess.Popen(["bedtools", "genomecov", "-bga", "-ibam", static_dir + "card_sorted.bam"], stdout=card_cov_out)
            card_cov.wait()
            card_cov_out.close()
        plot_bga("amr", static_dir + "card_cov.bed", static_dir, 1)

        compass_out = open(output_dir + "compass.sam", "w")
        compass = subprocess.Popen(["minimap2", "-ax", "map-ont", db_dir + "compass/compass.mmi", output_dir + "combined.fastq"], stdout=compass_out)
        compass.wait()
        compass_out.close()
        compass_sort_out = open(output_dir + "compass_sorted.sam", "w")
        compass_sort = subprocess.Popen(["samtools", "sort", output_dir + "compass.sam"], stdout=compass_sort_out)
        compass_sort.wait()
        compass_sort_out.close()
        compass_sort_bam_out = open(output_dir + "compass_sorted.bam", "w")
        compass_sort_bam = subprocess.Popen(["samtools", "view", "-bS", output_dir + "compass_sorted.sam"], stdout=compass_sort_bam_out)
        compass_sort_bam.wait()
        compass_sort_bam_out.close()
        if(len(sample_list) < 2):
            copy = subprocess.Popen(["cp", output_dir + "compass_sorted.bam", static_dir + "compass_sorted.bam"])
            copy.wait()
            compass_cov_out = open(static_dir + "compass_cov.bed", "w")
            compass_cov = subprocess.Popen(["bedtools", "genomecov", "-bga", "-ibam", static_dir + "compass_sorted.bam"], stdout=compass_cov_out)
            compass_cov.wait()
            compass_cov_out.close()
        else:
            list = ["samtools", "merge", static_dir + "compass_sorted.bam"]
            for line in sample_list:
                list.append(line + "compass_sorted.bam")
            compass_combine = subprocess.Popen(list)
            compass_combine.wait()
            compass_cov_out = open(static_dir + "compass_cov.bed", "w")
            compass_cov = subprocess.Popen(["bedtools", "genomecov", "-bga", "-ibam", static_dir + "compass_sorted.bam"], stdout=compass_cov_out)
            compass_cov.wait()
            compass_cov_out.close()
        plot_bga("plasmid", static_dir + "compass_cov.bed", static_dir, 1)
        f = open(static_dir + 'status.txt', "w")
        f.write('1')
        f.close()
        lock.release()

def scan(fastq_dir):
    p1 = subprocess.Popen(["ls", fastq_dir], stdout=subprocess.PIPE)
    p1.wait()
    p2 = subprocess.Popen(["grep", ".fastq"], stdin=p1.stdout, stdout=subprocess.PIPE)
    p2.wait()
    a = p2.communicate()[0].decode('ascii').strip()
    return a

def scan_sample(sample_dir):
    p1 = subprocess.Popen(["ls", sample_dir], stdout=subprocess.PIPE)
    p1.wait()
    a = p1.communicate()[0].decode('ascii').strip()
    return a

def scan_pic(output_dir, type, extension):
    p1 = subprocess.Popen(["ls", output_dir], stdout=subprocess.PIPE)
    p1.wait()
    p2 = subprocess.Popen(["grep", type], stdin=p1.stdout, stdout=subprocess.PIPE)
    p2.wait()
    p3 = subprocess.Popen(["grep", extension], stdin=p2.stdout, stdout=subprocess.PIPE)
    p3.wait()
    p4 = subprocess.Popen(["sed", "-e", "s/\.png$//"], stdin=p3.stdout, stdout=subprocess.PIPE)
    p4.wait()
    a = p4.communicate()[0].decode('ascii').strip()
    return a

def new_file(fastq_dir):
    a = scan(fastq_dir)
    b = []
    if os.stat('seq_list.txt').st_size == 0:
        f = open("seq_list.txt", "w")
        f.write(str(a))
        f.close()
        new_list = a.split('\n')
        b = empty_remove(new_list)

    else :
        f = open("seq_list.txt", "r")
        old_list = []
        for line in f:
            old_list.append(line.rstrip('\n'))

        f.close()
        new_list = a.split('\n')
        new_list = empty_remove(new_list)

        f = open("seq_list.txt", "w")
        f.write(str(a))
        f.close()

        for line in new_list :
            if line not in old_list :
                b.append(line)
    return b
