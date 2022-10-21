from hashlib import new
import numpy as np
import sys
import os
from tqdm import tqdm

filename_graph = sys.argv[1]
filename_scenario = sys.argv[2]

f_graph = open(f'{filename_graph}')
example_graph = f_graph.readlines()
f_graph.close()

f_scen = open(f'{filename_scenario}')
example_scenario = f_scen.readlines()
f_scen.close()
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


def print_graph(graph,new_V):
    str_out="graph=["
    for i in range(new_V):
        str_out += "{"
        for j in range(len(graph[i])):
            str_out += str(graph[i][j])
            if j < len(graph[i])-1:
                str_out += ","
        
        str_out += "}"

        if i < new_V-1:
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


def print_distances(dist,new_V):
    str_out = "distances=[|"
    for i in range(new_V):
        for j in range(new_V):
            str_out += f"{int(dist[i][j])}"
        
            if j < new_V-1:
                str_out += ","
        if i < new_V-1:
            str_out += "\n|"
        
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
        if v+1 not in start and v+1 not in end:
            best_time = t
            for a in range(A):
                #if counter == 1: print(len(distances),v,start[a]-1,end[a]-1)
                time_for_a = distances[start[a]-1][v] + distances[v][end[a]-1]
                #print("v",v,start[a]-1,end[a]-1,time_for_a)
                if time_for_a < best_time:
                    best_time = time_for_a
            
            if best_time >= t:
                v_to_delete.append(v)

    #print("v_to_delete",len(v_to_delete))
    new_distances = distances
    new_distances = np.delete(new_distances, v_to_delete, axis=0)
    new_distances = np.delete(new_distances, v_to_delete, axis=1)
    #print(new_distances)
    new_graph = []

    new_V = len(new_distances)
    #print(V)
    
    for i in range(new_V):
        new_connections = []
        for j in range(new_V):
            if new_distances[i][j] == 1:
                new_connections.append(j+1)
        new_graph.append(new_connections)

    new_distances = np.zeros((new_V,new_V))
    for v in range(new_V):
        visited = []    # List for visited nodes.
        queue = []      #Initialize a queue
        new_distances = bfs(visited, new_graph, v, queue, new_distances)
    #print(new_distances)
    #print(distances)
    #print("\n")
    #print(new_graph)
    #print("\n")
    #print(V,len(new_graph), len(distances))
    #print(v_to_delete)
    mapping = [0]*V
    #print("start_before",start)
    new_start = np.zeros((A),dtype=int)
    new_end = np.zeros((A),dtype=int)
    if v_to_delete != []:
        for i in range(V):
            for c,v in enumerate(v_to_delete):
                if v == i:
                    mapping[i] = 0
                    break
                elif v > i:
                    mapping[i] = i+1-c
                    break
            if v_to_delete[-1] < i:
                mapping[i] = i+1-len(v_to_delete)

        for i in range(A):
            new_start[i] = mapping[start[i]-1]
            new_end[i] = mapping[end[i]-1]
    else:
        for i in range(V):
            mapping[i] = i+1
        new_start = start
        new_end = end

    #print("mapping",mapping)
    #print("start_after",start)
    


    str_out_w_t = f"T={t};\nV={new_V};\n"+print_graph(new_graph,new_V)+print_start_end(new_start,new_end)+print_distances(new_distances,new_V)
    #print(str_out_w_t)
    file = open(f"dzn/{prefix}-input.dzn", "w")
    file.write(str_out_w_t)
    file.close()
    #print("entering minizinc")
    os.system(f"minizinc --solver chuffed solver2.mzn dzn/{prefix}-input.dzn > mzn/{prefix}-solution.txt")
    
    f_sol = open(f"mzn/{prefix}-solution.txt","r")
    lines = f_sol.readlines()
    f_sol.close()
    if len(lines) > 1:
        output = ""
        for i,l in enumerate(lines[:-1]):
            nodes = l.split()

            for j in range(len(nodes)):
                #print(mapping)
                #print(nodes[j])
                nodes[j] = mapping.index(int(nodes[j]))+1
            #print(nodes)
            output += f"i={i}\t"
            for j,node in enumerate(nodes):
                output += f"{j+1}:{node}"
                if j < len(nodes)-1: output+=" "
            output += "\n"
        print(output,end="")
        break

