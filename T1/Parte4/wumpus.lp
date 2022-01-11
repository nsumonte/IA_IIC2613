%-------------------- Se Define neigh tal como en el enunciado
neigh(X,Y,Xp,Yp) :- cell(X,Y), cell(Xp,Yp), |Xp-X|+|Yp-Y|=1.

%-------------------- Si se siente brisa en una casilla donde estoy vivo, entonces en al menos 1 de mis vecinos
%-------------------- hay un pit

1 {pit(X,Y): neigh(X,Y,Xp,Yp)} :- alive(Xp,Yp), sense_breeze(Xp,Yp).

%-------------------- Si se siente hedor en una casilla donde estoy vivo, entonces en al menos 1 de mis vecinos
%-------------------- hay un wumpus

1 {wumpus(X,Y): neigh(X,Y,Xp,Yp)} :- alive(Xp,Yp), sense_stench(Xp,Yp).

%-------------------- No puedo estar vivo en una casilla con un pit

:- pit(X,Y), alive(X,Y).

%-------------------- No puedo estar vivo en una casilla con un wumpus

:- wumpus(X,Y), alive(X,Y).

%-------------------- No hay casillas con wumpus y pits a la misma vez

:- wumpus(X,Y), pit(X,Y).

%-------------------- elimino los modelos donde no se siente brisa ni hedor en los vecinos a un wumpus o pits, donde
%-------------------- ya he estado vivo.

:- wumpus(X,Y), not sense_stench(Xp,Yp), neigh(X,Y,Xp,Yp), alive(Xp,Yp).

:- pit(X,Y), not sense_breeze(Xp,Yp), neigh(X,Y,Xp,Yp), alive(Xp,Yp).

%-------------------- Una casilla es segura si no hay wumpus, no hay pits, y hay una casilla donde se esta vivo alrededor

safe(X,Y) :- not wumpus(X,Y), alive(Xp,Yp), not pit(X,Y), cell(X,Y), neigh(X,Y,Xp,Yp), not alive(X,Y).

#show pit/2.
#show wumpus/2.
#show safe/2.
