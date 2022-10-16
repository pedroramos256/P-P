include "alldifferent.mzn";


int : T;
set of int: TIMESTEPS = 1..T;
int : V;
set of int: VERTICES = 1..V;

array [VERTICES] of set of int: graph;

int : A;
set of int: AGENTS = 1..A;

array [AGENTS] of var VERTICES: start;
array [AGENTS] of var VERTICES: end;

array [TIMESTEPS,AGENTS] of var VERTICES: makespan;


constraint forall(i in AGENTS)(makespan[1,i] = start[i]);
constraint forall(i in AGENTS)(makespan[T,i] = end[i]);

constraint forall(i in TIMESTEPS)(all_different([makespan[i,j] | j in AGENTS]));

constraint forall(i in 2..T,j in AGENTS,k in AGENTS)(if j != k then makespan[i-1,j]!=makespan[i,k] endif);

%constraint forall(i in 2..T,j in AGENTS)(forall(k in AGENTS)(makespan[i,k]!=makespan[i-1,j]));

constraint forall(i in 2..T,j in AGENTS)(not forall(v in graph[makespan[i-1,j]])(makespan[i,j]!=v));

solve satisfy;

output [ show_int(V, makespan[i,j]) ++ 
         if j == A then "\n" endif |
         i in TIMESTEPS, j in AGENTS
       ];


