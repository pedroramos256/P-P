include "alldifferent.mzn";


int : T;
set of int: TIMESTEPS = 1..T;
int : V;
set of int: VERTICES = 1..V;

int : A;
set of int: AGENTS = 1..A;

array [AGENTS] of VERTICES: start;
array [AGENTS] of VERTICES: end;

array [VERTICES,VERTICES] of int : distances;


array [TIMESTEPS,AGENTS] of var VERTICES: agent_state;
array [TIMESTEPS,VERTICES] of var 0..A: vertice_state;



constraint forall(i in AGENTS)(agent_state[1,i] = start[i]);
constraint forall(i in AGENTS)(agent_state[T,i] = end[i]);

constraint forall(i in AGENTS)(vertice_state[1,start[i]] = i);
constraint forall(i in AGENTS)(vertice_state[T,end[i]] = i);

constraint forall(i in 2..T-1,j in VERTICES)(vertice_state[i,j] == 0 \/ j == agent_state[i,vertice_state[i,j]]);

constraint forall(i in TIMESTEPS)(all_different([agent_state[i,j] | j in AGENTS]));
constraint forall(i in TIMESTEPS)(sum(vertice_state[i,..]) == A*(A+1)/2);

constraint forall(i in TIMESTEPS,j in AGENTS)(distances[agent_state[i,j],end[j]] <= T-i);   

constraint forall(i in 2..T,j in AGENTS)((distances[agent_state[i,j],agent_state[i-1,j]] == 1 /\ vertice_state[i-1,agent_state[i,j]] == 0) 
                                      \/ (agent_state[i,j] = agent_state[i-1,j]));                                              
                                                                            

solve satisfy;

output [ show_int(V, agent_state[i,j]) ++ 
         if j == A then "\n" endif |
         i in TIMESTEPS, j in AGENTS
       ];


