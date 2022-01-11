
%-------------------- Camino minimo, cuenta solo los caminos, cuyo largo es el menor a todos los otros caminos iguales
%-------------------- Dentro del modelo.
camino_minimo(X,Y,K1) :- conectado_K(X,Y,K1), #count{K3: conectado_K(X,Y,K3), K3<K1} = 0.
%-------------------- 