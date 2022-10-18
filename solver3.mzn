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

array [TIMESTEPS,AGENTS,VERTICES] of var 0..1: makespan;

constraint forall(i in AGENTS)(makespan[1,i,start[i]] = 1);
constraint forall(i in AGENTS)(makespan[T,i,end[i]] = 1);

constraint forall(i in TIMESTESPS,j in AGENTS)(sum(k in VERTICES)(makespan[i,j,k]) == 1);                                                                                                          

constraint forall(i in TIMESTEPS,j in AGENTS,k in VERTICES)(if makespan[i,j,k] != 0 then distances[k,end[j]] <= T-i endif);   

constraint forall(i in 2..T,j in AGENTS,k in VERTICES)(distances[makespan[i,j],makespan[i-1,j]] == 1 /\
                                                        
                                                      else if 
if agent_pos[i-1,j] == k then
                                                          (agent_pos[i,j] = k /\ makespan[i,j,k] = 1) \/ (agent_pos[i,j] = k /\ makespan[i,j,k] = 0
                                                       else if distances[j,k] then
                                                          makespan[i,
                                                          makespan[i-1,j,k] = 1 \/ distances[j,k]
                                                        makespan[i,j,k] == 0 else agent_pos[i,j] in graph[makespan[i-1,j]] 
                                      /\ (makespan[i,j] == makespan[i-1,j] \/ occupied[i-1,makespan[i,j]] == 0)
                                      /\ occupied[i,makespan[i,j]] = 1);
                                                                            
                                                                            
constraint forall(i in 2..T-1)(all_different([agent_pos[i,j] | j in AGENTS]));

%constraint forall(i in 2..T,j in AGENTS,v in graph[makespan[i-1,j]])(if j != k then makespan[i-1,j]!=makespan[i,k] endif);


solve satisfy;

output [ show_int(V, agent_pos[i,j]) ++ 
         if j == A then "\n" endif |
         i in TIMESTEPS, j in AGENTS
       ];


