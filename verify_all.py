import os

graphs = os.listdir('graph')
scens = os.listdir('scen')
graphs.sort()
scens.sort()

for i in range(len(graphs)):
    print(graphs[i],scens[i])
    os.system(f'./chkcpf/chkcpf -v 1 -graph graph/{graphs[i]} -scen scen/{scens[i]} -sol sol/ex0{i+1}-sol.txt > verification/ex0{i+1}-verification.txt')
