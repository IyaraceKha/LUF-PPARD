import plotly.graph_objects as go
import sys

def plot_bga(type, file_name, output_dir, area_cover):
    f_list = open(output_dir + type + '_list.txt', "w")
    fig = go.Figure()
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

        if prevLine == "" or elem[0] == prevLine:
            if int(elem[3]) > max:
                max = int(elem[3])
            for i in range(int(elem[1]), int(elem[2])):
                position.append(i)
                depth.append(int(elem[3]))
                a = a + 1
                if int(elem[3]) != 0:
                    b = b + 1
        else:
            if max == 0:
                break
            if b/a >= area_cover and sum(depth)/len(depth) >= 1 and max > 0:
                fig.add_trace(go.Bar(x=position, y=depth))
                fig.update_layout(yaxis=dict(range=[0, max+1]),autosize=False,width=900,height=450,plot_bgcolor="white",margin=dict(l=0,r=0,b=0,t=0))
                fig.update_traces(marker_line_width = 0,selector=dict(type="bar"))
                fig.update_layout(bargap=0,bargroupgap = 0)
                fig.update_xaxes(showgrid=False, zeroline=False)
                fig.update_yaxes(showgrid=False, zeroline=False)
                f_list.write(name + "\t" + str(round(sum(depth)/len(depth),2)) + "\t" + str(max) + "\t" + str(round(b/a*100,2)) + "\n")
                fig.write_image(output_dir + type + "_-_" + str(round(sum(depth)/len(depth),2)) + "_-_" + str(max) + "_-_" + str(round(b/a*100,2)) + "_-_"  + name + ".png")
                fig.data = []
                position.clear()
                depth.clear()
                a = 0
                b = 0
                name = elem[0]
                max = int(elem[3])
                for i in range(int(elem[1]), int(elem[2])):
                    position.append(i)
                    depth.append(int(elem[3]))
                    a = a + 1
                    if int(elem[3]) != 0:
                        b = b + 1
            else:
                fig.data = []
                position.clear()
                depth.clear()
                a = 0
                b = 0
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

    if b/a >= area_cover and sum(depth)/len(depth) >= 1 and max > 0:
        fig.add_trace(go.Bar(x=position, y=depth))
        fig.update_layout(yaxis=dict(range=[0, max+1]),autosize=False,width=900,height=450,plot_bgcolor="white",margin=dict(l=0,r=0,b=0,t=0))
        fig.update_traces(marker_line_width = 0,selector=dict(type="bar"))
        fig.update_layout(bargap=0,bargroupgap = 0)
        fig.update_xaxes(showgrid=False, zeroline=False)
        fig.update_yaxes(showgrid=False, zeroline=False)
        f_list.write(name + "\t" + str(round(sum(depth)/len(depth),2)) + "\t" + str(max) + "\t" + str(round(b/a*100,2)) + "\n")
        fig.write_image(output_dir + type + "_-_" + str(round(sum(depth)/len(depth),2)) + "_-_" + str(max) + "_-_" + str(round(b/a*100,2)) + "_-_"  + name + ".png")
    f_list.close()
