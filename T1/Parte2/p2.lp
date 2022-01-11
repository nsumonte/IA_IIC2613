%-------------------- Generamos arcos no dirigidos y definimos iluminada/2 que se activa si alguno de los nodos
%-------------------- adyacentes a una calle está encendido.
arco(X,Y) :- arco(Y,X).
iluminada(X,Y) :- iluminado(X), iluminado(Y), arco(X,Y).
iluminada(X,Y) :- iluminado(X), nodo(Y), arco(X,Y).
iluminada(X,Y) :- iluminado(Y), nodo(X), arco(X,Y).

%-------------------- Conectado_K aparece como modelo si y solo sí, hay K arcos no iluminados, para esto se generó
%-------------------- una funcion recursiva que cuenta los arcos no iluminados y se van sumando segun su largo
conectado_K(X,Y,K) :- arco(X,Y), K = #count{X,Y: not iluminada(X,Y)}.
conectado_K(X,Y,K) :- conectado_K(X,Z,N1), arco(Z,Y), camino(X,Y,N2), K2 = #count{Z: not iluminada(Z,Y), arco(Z,Y)}, K = N1 + K2, K <= N2, X!=Y.
