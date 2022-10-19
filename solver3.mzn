include "alldifferent.mzn";


int : T;
set of int: TIMESTEPS = 1..T;
int : V;
set of int: VERTICES = 1..V;

int : A;
set of int: AGENTS = 1..A;

array [VERTICES] of set of int: graph;

array [AGENTS] of VERTICES: start;
array [AGENTS] of VERTICES: end;

array [VERTICES,VERTICES] of int : distances;

array [TIMESTEPS,AGENTS,VERTICES] of var 0..1: makespan;

%initialization
constraint forall(i in AGENTS)(makespan[1,i,start[i]] = 1);
constraint forall(i in AGENTS)(makespan[T,i,end[i]] = 1); 

%verifying no agent is getting out of route
constraint forall(i in TIMESTEPS,j in AGENTS,k in VERTICES)(if makespan[i,j,k] == 1 then distances[k,end[j]] <= T-i endif);   

%if an agent goes to a vertex, than no agent can be there before and the agent has a connection to that vertex, or the agent stays in the same place
constraint forall(i in 2..T,j in AGENTS,k in VERTICES)(if makespan[i,j,k] == 1 then ((not forall(l in graph[k])(makespan[i-1,j,l] == 0)) /\
                                                                                    sum(makespan[i-1,..,k])==0)  %verifying no agent was there before)%verifying the agent came from an adjacent vertice 
                                                                                 \/ (makespan[i-1,j,k] == 1) endif);                                              
                                                                            

%each agent is only in one vertex
constraint forall(i in TIMESTEPS,j in AGENTS)(sum(makespan[i,j,..]) == 1); 
%each vertex has 1 or 0 agents  
constraint forall(i in TIMESTEPS,j in VERTICES)(sum(makespan[i,..,j]) <= 1);                                                                                                                                                                                                        



%starting with all values at zero (indomain_min) and changing values starting at timestep 1 (input_order).
solve:: int_search(makespan,input_order,indomain_min) satisfy;


output [ if fix(makespan[i,j,k]) == 1 then "\(k) " endif ++ 
         if k == V /\ j == A then "\n" endif |
         i in TIMESTEPS, j in AGENTS, k in VERTICES
       ];


