from hashlib import new
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
graph = []
for i in range(V):
    graph.append([])
for l in example_graph[ix+2:]:
    i,j = l.split(' ')
    i = int(i)-1
    j = int(j)-1
    graph[i].append(j+1)
    graph[j].append(i+1)
#for i in range(V):
#    graph[i].append(i+1)


def print_graph(graph):
    str_out="graph=["
    for i in range(V):
        str_out += "{"
        for j in range(len(graph[i])):
            str_out += str(graph[i][j])
            if j < len(graph[i])-1:
                str_out += ","
        
        str_out += "}"

        if i < V-1:
            str_out += ","
        
    str_out += "];\n"
    return str_out

ix = 0
while example_scenario[ix][0] == "#":
    ix += 1
A = int(example_scenario[ix])
    
start = np.zeros((A),dtype=int)
end = np.zeros((A),dtype=int)

for l in example_scenario[ix+2:ix+2+A]:
    i,j = l.split(' ')
    i = int(i)
    j = int(j)
    start[i-1] = j
    
for l in example_scenario[ix+2+A+1:]:
    i,j = l.split(' ')
    i = int(i)
    j = int(j)
    end[i-1] = j


def print_start_end(start,end):
    str_out = f"A={A};\nstart=["
    for i in range(A):
       
        str_out += f"{start[i]}"
        if i < A-1:
            str_out += ","
    str_out += "];\n"
    str_out += "end=["
    for i in range(A):
     
        str_out += f"{end[i]}"
        if i < A-1:
            str_out += ","

    str_out += "];\n"
    return str_out

distances = np.zeros((V,V))

def bfs(visited, graph, node, queue, dist): #function for BFS
    visited.append(node)
    queue.append([node, 0])
    while queue:          # Creating loop to visit each node
        m, distance = queue.pop(0)
        dist[node][m] = distance 
        for neighbour in graph[m]:
            if (neighbour-1) not in visited:
                queue.append([neighbour-1, distance+1])
                visited.append(neighbour-1)
    return dist

for v in range(V):
    visited = []    # List for visited nodes.
    queue = []      #Initialize a queue
    distances = bfs(visited, graph, v, queue, distances)


def print_distances(dist):
    str_out = "distances=[|"
    for i in tqdm(range(V)):
        for j in range(V):
            str_out += f"{int(dist[i][j])}"
        
            if j < V-1:
                str_out += ","
        if i < V-1:
            str_out += "\n|"
        else:
            str_out += "|];\n"
    return str_out

t_lower = 0
for i in range(len(start)):
    dist = distances[start[i]-1][end[i]-1]
    if dist > t_lower:
        t_lower = dist

for t in tqdm(range(int(t_lower+1),30)):
    v_to_delete = []
    for v in range(V):
        best_time = t
        entered = False
        for a in range(A):
            if start[a]-1 != v and end[a]-1 != v:
                entered = True
                time_for_a = distances[start[a]-1][v] + distances[v][end[a]-1]
                if time_for_a < best_time:
                    best_time = time_for_a
        if best_time >= t and entered:
            v_to_delete.append(v)
    #print(v_to_delete)
    new_distances = distances
    new_distances = np.delete(new_distances, v_to_delete, axis=0)
    new_distances = np.delete(new_distances, v_to_delete, axis=1)
    #print(new_distances)
    new_graph = []
    mapping = np.zeros((V))

    V = len(new_distances)
    #print(V)
    
    for i in range(V):
        new_connections = []
        for j in range(V):
            if new_distances[i][j] == 1:
                new_connections.append(j+1)
        new_graph.append(new_connections)

    new_distances = np.zeros((V,V))
    for v in range(V):
        visited = []    # List for visited nodes.
        queue = []      #Initialize a queue
        new_distances = bfs(visited, new_graph, v, queue, new_distances)
    
    #print(distances)
    #print("\n")
    #print(new_graph)
    #print("\n")
    #print(V,len(new_graph), len(distances))
    #print(v_to_delete)
    if v_to_delete != []:
        for i in range(len(mapping)):
            for c,v in enumerate(v_to_delete):
                if v > i:
                    mapping[i] = i+1-c
                    break
            if v_to_delete[-1] < i:
                mapping[i] = i+1-len(v_to_delete)

        for i in range(A):
            start[i] = mapping[start[i]-1]
            end[i] = mapping[end[i]-1]
    
    print(mapping)

    """
        for i in range(A):
            for c,v in enumerate(v_to_delete):
                if v > start[i]-1:
                    start[i] -= c
                    break
            if v_to_delete[-1] < start[i]-1:
                start[i] -= len(v_to_delete)

            for c,v in enumerate(v_to_delete):
                if v > end[i]-1:
                    end[i] -= c
                    break
            if v_to_delete[-1] < end[i]-1:
                end[i] -= len(v_to_delete)
    """

    str_out_w_t = f"T={t};\nV={V};\n"+print_graph(new_graph)+print_start_end(start,end)+print_distances(new_distances)
    #print(str_out_w_t)
    file = open(f"dzn/{prefix}-input.dzn", "w")
    file.write(str_out_w_t)
    file.close()
    os.system(f"minizinc --solver chuffed solver3.mzn dzn/{prefix}-input.dzn > mzn/{prefix}-solution.txt")
    
    lines = open(f"mzn/{prefix}-solution.txt","r").readlines()
    if len(lines) > 1:
        output = ""
        for i,l in enumerate(lines[:-1]):
            nodes = l.split()

            nodes_after = [4,2,3]
            v_to_delete = [2,3,4,6]
            nodes_before = [8,5,7]
            for j in range(len(nodes)):
                nodes[j] = np.where(mapping==int(nodes[j])+1)  
            print(nodes)
            exit(0)
            output += f"i={i}\t"
            for j,node in enumerate(nodes):
                output += f"{j+1}:{node}"
                if j < len(nodes)-1: output+=" "
            output += "\n"
        print(output,end="")
        break

