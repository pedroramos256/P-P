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
#for i in range(V):
#    matrix[i].append(i+1)

str_out = f"V={V};\n"
"""graph=["

for i in range(V):
    str_out += "{"
    for j in range(len(matrix[i])):
        str_out += str(matrix[i][j])
        if j < len(matrix[i])-1:
            str_out += ","
       
    str_out += "}"

    if i < V-1:
        str_out += ","
    
str_out += "];\n"
"""
ix = 0
while example_scenario[ix][0] == "#":
    ix += 1
A = int(example_scenario[ix])
    
start = []
end = []
for i in range(A):
    start.append(0)
    end.append(0)
str_out += f"A={A};\nstart=["
for l in example_scenario[ix+2:ix+2+A]:
    i,j = l.split(' ')
    i = int(i)
    j = int(j)
    start[i-1] = j
    str_out += f"{j}"
    if i < A:
        str_out += ","
str_out += "];\n"
str_out += "end=["
for l in example_scenario[ix+2+A+1:]:
    i,j = l.split(' ')
    i = int(i)
    j = int(j)
    end[i-1] = j
    str_out += f"{j}"
    if i < A:
        str_out += ","

str_out += "];\n"

distances = np.zeros((V,V))

def bfs(visited, graph, node, queue): #function for BFS
    visited.append(node)
    queue.append([node, 0])
    while queue:          # Creating loop to visit each node
        m, distance = queue.pop(0)
        distances[node][m] = distance 
        for neighbour in graph[m]:
            if (neighbour-1) not in visited:
                queue.append([neighbour-1, distance+1])
                visited.append(neighbour-1)

for v in range(V):
    visited = []    # List for visited nodes.
    queue = []      #Initialize a queue
    bfs(visited, matrix, v, queue)


str_out += "distances=[|"
for i in range(V):
    for j in range(V):
        str_out += f"{int(distances[i][j])}"
      
        if j < V-1:
            str_out += ","
    if i < V-1:
        str_out += "\n|"
    else:
        str_out += "|];\n"


t_lower = 0
for i in range(len(start)):
    dist = distances[start[i]-1][end[i]-1]
    if dist > t_lower:
        t_lower = dist

for t in tqdm(range(int(t_lower+1),30)):
    str_out_w_t = f"T={t};\n"+str_out
    file = open(f"dzn/{prefix}-input.dzn", "w")
    file.write(str_out_w_t)
    file.close()
    os.system(f"minizinc --solver chuffed solver3.mzn dzn/{prefix}-input.dzn > mzn/{prefix}-solution.txt")
    
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

