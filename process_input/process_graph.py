import numpy as np

lines = open('../example_graph.txt').readlines()

def process_graph(lines):
    ix = 0
    while lines[ix][0] == "#":
        ix += 1
    V = int(lines[ix])
    E = int(lines[ix+1])
    matrix = np.zeros((V,V))
    for l in lines[ix+2:]:
        i = int(l[0])-1
        j = int(l[2])-1
        matrix[i][j] = 1
        matrix[j][i] = 1
    for i in range(V):
        matrix[i][i] = 1
    
    str_out = f"V={V};\ngraph=[|"

    for i in range(V):
        for j in range(V):
            if matrix[i][j] == 0:
                str_out += "false"
            else:
                str_out += "true"
            if j < V-1:
                str_out += ","

        if i < V-1:
            str_out += "\n|"
        else:
            str_out += "|];\n"

    print(str_out)

process_graph(lines)