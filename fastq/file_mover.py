import time
import subprocess
import sys

dir_name = sys.argv[1]

if dir_name[len(dir_name)-1] != "/":
        dir_name = dir_name + "/"

p1 = subprocess.Popen(["ls", dir_name], stdout=subprocess.PIPE)
p1.wait()
p2 = subprocess.Popen(["grep", ".fastq"], stdin=p1.stdout, stdout=subprocess.PIPE)
p2.wait()
a = p2.communicate()[0].decode('ascii').strip()
list = a.split('\n')

for line in list:
	p3 = subprocess.Popen(["cp", dir_name+line, line], stdout=subprocess.PIPE)
	time.sleep(600)