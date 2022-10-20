from tqdm import tqdm
import os

graphs = os.listdir('graph')
scens = os.listdir('scen')
graphs.sort()
scens.sort()

for i in tqdm(range(len(graphs))):
    print(graphs[i],scens[i])
    os.system(f'python3 proj.py graph/{graphs[i]} scen/{scens[i]} > sol/ex0{i+1}-sol.txt')
