# TODO:

Agora temos que automatizar o processamento do input.
- No process_input.py é necessário ler os ficheiros da pasta graph e da scen e gerar uma pasta dzn com ficheiros semelhantes ao example_input.dzn, que foi criado à mão a partir dos dados do example_graph.txt e do example_scenario.txt

Depois é preciso pôr o python a comunicar com o minizinc, para testar com diferentes quantidades de timesteps. 
- O proj.py é chamado da seguinte forma: 
    python proj.py <graph-file-name> <scenario-file-name> > solution.txt
- Precisamos dentro do proj.py usar as funções do process_input.py e depois chamar o minzinc da seguinte forma:
    minizinc --solver Gecode solver.mzn example_input.dzn 

É ainda necessário transformar o output do solver.mzn, para que esteja como no enunciado (example_solution.txt)

Por fim testar com grafos grandes e desconfio que vamos perceber que temos que otimizar a nossa solução.
- Para isto é preciso ver as orientações em chkcpf/README-chkcpf.txt

Uma otimização que deve ser simples é substituir a representação do grafo, agora é uma matriz de adjacencias, mas pode ser um vetor de listas (ou pelos vistos o melhor é um vetor de sets).
Outra otimização é definir um lower bound para os timesteps e ir incrementando até um upperbound.

(esquecer isto, já tive a comentar com malta e não é necessário) Outra otimização é implementar o algoritmo do paper, mas não fiz esse porque ou é preciso fazer uma binary tree e o minizinc só tem arrays, dá para fazer uma binary tree a partir de arrays, mas é complicado.