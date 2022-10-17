include "alldifferent.mzn";


int : T;
set of int: TIMESTEPS = 1..T;
int : V;
set of int: VERTICES = 1..V;

array [VERTICES] of set of int: graph;

int : A;
set of int: AGENTS = 1..A;

array [AGENTS] of VERTICES: start;
array [AGENTS] of VERTICES: end;

array [TIMESTEPS,AGENTS] of var VERTICES: makespan;


constraint forall(i in AGENTS)(makespan[1,i] = start[i]);
constraint forall(i in AGENTS)(makespan[T,i] = end[i]);
                                         
%constraint forall(i in TIMESTEPS,j in AGENTS)(distance[makespan[i,j],end[j]] < T-i);                                                             

constraint forall(i in 2..T,j in AGENTS)(makespan[i,j] == makespan[i-1,j] \/ ((makespan[i,j] in graph[makespan[i-1,j]]) /\ not(makespan[i,j] in makespan[i-1,..])));
                                                                            
%constraint forall(i in 2..T-1)(sum(j in VERTICES)(occupied[i,j]) == A);                                                                                                          
                                                                            
constraint forall(i in TIMESTEPS)(all_different([makespan[i,j] | j in AGENTS]));

%constraint forall(i in 2..T,j in AGENTS,v in graph[makespan[i-1,j]])(if j != k then makespan[i-1,j]!=makespan[i,k] endif);


solve satisfy;

output [ show_int(V, makespan[i,j]) ++ 
         if j == A then "\n" endif |
         i in TIMESTEPS, j in AGENTS
       ];


