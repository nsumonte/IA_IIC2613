%arco(a,b).
%arco(b,c).
%arco(b,e).
%arco(e,f).
%arco(f,c).
%arco(f,g).
%arco(c,a).
%arco(e,g).

nodo(X) :- arco(X,Y).
nodo(Y) :- arco(X,Y).

%-------------------- Contamos el máximo largo posible de caminos que puede existir en un grafo con ciclos
largo_maximo_camino(N) :- N= #count{X,Y : arco(X,Y)}.

%-------------------- Definimos camino a través de una recursion en donde vamos sumando recursivamente arcos
%-------------------- de largo 1, acotados por el largo maximo calculado anteriormente
camino(X,Y,LARGO) :- arco(X,Y), LARGO = 1.

camino(X,Y,LARGO) :- largo_maximo_camino(N), camino(X,Z,LARGO1), arco(Z,Y), LARGO = LARGO1 + 1, LARGO <= N.

%-------------------- 