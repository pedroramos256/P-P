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

array [TIMESTEPS,VERTICES] of var 0..A: agent_pos;

constraint forall(i in AGENTS)(agent_pos[1,start[i]] = i);
constraint forall(i in AGENTS)(agent_pos[T,end[i]] = i);


constraint sum(j in VERTICES)(agent_pos[1,j]) == A*(A-1)/2;                                                                                                          
constraint sum(j in VERTICES)(agent_pos[T,j]) == A*(A-1)/2;                                                                                                       



constraint forall(i in 2..T,j in VERTICES)(if agent_pos[i,j] != 0 then j in graph[makespan[i-1,j]] 
                                      /\ (makespan[i,j] == makespan[i-1,j] \/ occupied[i-1,makespan[i,j]] == 0)
                                      /\ occupied[i,makespan[i,j]] = 1);
                                                                            
constraint forall(i in 2..T-1)(sum(j in VERTICES)(occupied[i,j]) == A);                                                                                                          
                                                                            
constraint forall(i in TIMESTEPS)(all_different([makespan[i,j] | j in AGENTS]));

%constraint forall(i in 2..T,j in AGENTS,v in graph[makespan[i-1,j]])(if j != k then makespan[i-1,j]!=makespan[i,k] endif);


solve satisfy;

output [ show_int(V, makespan[i,j]) ++ 
         if j == A then "\n" endif |
         i in TIMESTEPS, j in AGENTS
       ];

