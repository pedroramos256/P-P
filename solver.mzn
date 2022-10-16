include "alldifferent.mzn";


int : T;
set of int: TIMESTEPS = 1..T;
int : V;
set of int: VERTICES = 1..V;
array [VERTICES,VERTICES] of bool : graph;

int : A;
set of int: AGENTS = 1..A;

array [AGENTS] of var VERTICES: start;
array [AGENTS] of var VERTICES: end;

array [TIMESTEPS,AGENTS] of var VERTICES: makespan;


constraint forall(i in AGENTS)(makespan[1,i] = start[i]);
constraint forall(i in AGENTS)(makespan[T,i] = end[i]);

constraint forall(i in TIMESTEPS)(all_different([makespan[i,j] | j in AGENTS]));

constraint forall(i in 2..T,j in AGENTS)(graph[makespan[i-1,j],makespan[i,j]]==true);

solve satisfy;

output [ show_int(V, makespan[i,j]) ++ 
         if j == A then "\n" endif |
         i in TIMESTEPS, j in AGENTS
       ];


