
%-------------------- Finalmente, definimos todas las combinaciones posibles de nodos iluminados, contamos los nodos encendidos
%-------------------- para cada modelo, eliminamos los que tengan mas de un camino sin iluminar y minimizamos
%-------------------- sobre la cantidad de nodos encendidos.

{iluminado(X): nodo(X)}.

nodos_encendidos(N) :- N = #count{X: iluminado(X)}.

:- camino_minimo(X,Y,K), K > 1.

#minimize {N : nodos_encendidos(N)}.

%#show iluminada/2.
%#show conectado_K/3.
%#show camino_minimo/3.
%#show camino/3.
#show iluminado/1.