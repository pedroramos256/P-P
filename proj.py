import numpy as np
import sys
import os
from tqdm import tqdm

filename_graph = sys.argv[1]
filename_scenario = sys.argv[2]

example_graph = open(f'{filename_graph}').readlines()
example_scenario = open(f'{filename_scenario}').readlines()
prefix = filename_graph.split('/')[1].split('-')[0]

ix = 0
while example_graph[ix][0] == "#":
    ix += 1
V = int(example_graph[ix])
E = int(example_graph[ix+1])
matrix = []
for i in range(V):
    matrix.append([])
for l in example_graph[ix+2:]:
    i,j = l.split(' ')
    i = int(i)-1
    j = int(j)-1
    matrix[i].append(j+1)
    matrix[j].append(i+1)
for i in range(V):
    matrix[i].append(i+1)

str_out = f"V={V};\ngraph=["

for i in range(V):
    str_out += "{"
    for j in range(len(matrix[i])):
        str_out += str(matrix[i][j])
        if j < len(matrix[i])-1:
            str_out += ","
        else:
            str_out += "}"

    if i < V-1:
        str_out += ","
    else:
        str_out += "];\n"

ix = 0
while example_scenario[ix][0] == "#":
    ix += 1
A = int(example_scenario[ix])
str_out += f"A={A};\nstart=["
for l in example_scenario[ix+2:ix+2+A]:
    i,j = l.split(' ')
    i = int(i)
    j = int(j)
    str_out += f"{j}"
    if i < A:
        str_out += ","
str_out += "];\n"
str_out += "end=["
for l in example_scenario[ix+2+A+1:]:
    i,j = l.split(' ')
    i = int(i)
    j = int(j)
    str_out += f"{j}"
    if i < A:
        str_out += ","

str_out += "];\n"


for t in tqdm(range(2,30)):
    str_out_w_t = f"T={t};\n"+str_out
    file = open(f"dzn/{prefix}-input.dzn", "w")
    file.write(str_out_w_t)
    file.close()
    os.system(f"minizinc --solver Gecode solver2.mzn dzn/{prefix}-input.dzn > mzn/{prefix}-solution.txt")
    
    lines = open(f"mzn/{prefix}-solution.txt","r").readlines()
    if len(lines) > 1:
        output = ""
        for i,l in enumerate(lines[:-1]):
            nodes = l.split()
            output += f"i={i}\t"
            for j,node in enumerate(nodes):
                output += f"{j+1}:{node}"
                if j < len(nodes)-1: output+=" "
            output += "\n"
        print(output,end="")
        break

