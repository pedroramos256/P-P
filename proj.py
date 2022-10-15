from doctest import Example
import numpy as np
import sys
import os

filename_graph = sys.argv[1]
filename_scenario = sys.argv[2]

example_graph = open(f'{filename_graph}').readlines()
example_scenario = open(f'{filename_scenario}').readlines()

ix = 0
while example_graph[ix][0] == "#":
    ix += 1
V = int(example_graph[ix])
E = int(example_graph[ix+1])
matrix = np.zeros((V,V))
for l in example_graph[ix+2:]:
    i = int(l[0])-1
    j = int(l[2])-1
    matrix[i][j] = 1
    matrix[j][i] = 1
for i in range(V):
    matrix[i][i] = 1

str_out = f"T=4;\nV={V};\ngraph=[|"

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

ix = 0
while example_scenario[ix][0] == "#":
    ix += 1
A = int(example_scenario[ix])
str_out += f"A={A};\nstart=["
for l in example_scenario[ix+2:A+2]:
    i = int(l[0])
    j = int(l[2])
    str_out += f"{j}"
    if i < A:
        str_out += ","
str_out += "];\n"
str_out += "end=["
for l in example_scenario[A+3:]:
    i = int(l[0])
    j = int(l[2])
    str_out += f"{j}"
    if i < A:
        str_out += ","

str_out += "];\n"

file = open("example.dzn", "w")
file.write(str_out)

os.system("minizinc --solver Gecode solver.mzn example_input.dzn")

