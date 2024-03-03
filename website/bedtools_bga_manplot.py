import matplotlib.pyplot as plt
import sys

def plot_bga(type, file_name, output_dir, threshold):
    position = []
    depth = []
    name = ""
    max = 0
    prevLine = ""
    a = 0
    b = 0
    f = open(file_name, "r")
    for line in f:
        elem = line.rstrip('\n').split("\t")
        if name == "":
            name = elem[0]
        if int(elem[3]) > max:
            max = int(elem[3])

        if prevLine == "" or elem[0] == prevLine:
            for i in range(int(elem[1]), int(elem[2])):
                position.append(i)
                depth.append(int(elem[3]))
                a = a + 1
                if int(elem[3]) != 0:
                    b = b + 1
        else:
            if b/a >= threshold:
                plt.plot(position, depth)
                plt.yticks(range(0,max+1))
                plt.xlabel("Position (bp)")
                plt.ylabel("Depth")
                plt.ticklabel_format(useOffset=False)
                plt.savefig(output_dir + type + "_-_" + str(round(b/a*100,2)) + "_-_" + str(max) + "_-_" + name + ".png")
                plt.cla()
                position.clear()
                depth.clear()
                name = elem[0]
                max = int(elem[3])
                for i in range(int(elem[1]), int(elem[2])):
                    position.append(i)
                    depth.append(int(elem[3]))
                    a = a + 1
                    if int(elem[3]) != 0:
                        b = b + 1
            else:
                plt.cla()
                position.clear()
                depth.clear()
                name = elem[0]
                max = int(elem[3])
                for i in range(int(elem[1]), int(elem[2])):
                    position.append(i)
                    depth.append(int(elem[3]))
                    a = a + 1
                    if int(elem[3]) != 0:
                        b = b + 1
        prevLine = elem[0]

    f.close()
    if b/a >= threshold:
        plt.plot(position, depth)
        plt.yticks(range(0,max+1))
        plt.xlabel("Position (bp)")
        plt.ylabel("Depth")
        plt.ticklabel_format(useOffset=False)
        plt.savefig(output_dir + type + "_-_" + str(round(b/a*100,2)) + "_-_" + str(max) + "_-_" + name + ".png")
