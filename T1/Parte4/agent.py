import sys
import os
import queue

class Agent:
    def __init__(self, env):
        self.env = env
        self.x = env.init_x      # tamaño de la grilla
        self.y = env.init_y
        self.visited = set()     # celdas ya visitadas
        self.visited.add((self.x, self.y))
        self.frontier = set()    # al profesor le fue util mantener esta variable
        for n in env.neighbors(self.x, self.y):
            self.frontier.add(n)
        self.path = []           # self.path es el camino que estamos siguiendo        # profe le fue útil


    # get_action(self, perceptions) supone que perceptions es una lista de
    # strings [s1,...,sn] donde si es sense_breeze(x,y) o sense_stench(x,y) para algúun x,y
    # debe retornar:
    #   - una tupla de la forma ('goto',x,y) para hacer que el agente se mueva a (x,y)
    #   - una tupla de la forma ('shoot',x,y) para hacer que el agente dispare a (x,y)
    #   - una tupla de la forma ('unsolvable') cuando el agente ha demostrado que el problema
    #     no tiene una solución segura

    def get_action(self, perceptions):

        def find_path(startx, starty, goalx, goaly, safe_area):

            # encuentra un camino entre (startx,starty) a (goalx,goaly)
            # pasando solo por celdas de safe_area

            if (startx, starty) == (goalx, goaly):
                return True, []
            closed = set()
            fr = queue.Queue()
            fr.put((startx, starty, []))
            while not fr.empty():
                (x, y, path) = fr.get()
                closed.add((x,y))
                for (nx, ny) in self.env.neighbors(x, y):
                    if (nx, ny) in closed:
                        continue
                    newpath = path + [(nx, ny)]
                    if (nx, ny) == (goalx, goaly):
                        return True, newpath
                    else:
                        if (nx, ny) in safe_area:
                            fr.put((nx, ny, newpath))
            return False, []

        def unsat_without(atom):

            def get_models(filename):  # extrae los modelos desde filename
                f = open(filename, 'r')
                lines = f.readlines()
                lines = [l.strip() for l in lines]
                if 'SATISFIABLE' in lines:
                    answers = []
                    i = 0
                    while True:
                        while i < len(lines) - 1 and lines[i].find('Answer:', 0) == -1:
                            i += 1
                        if i == len(lines) - 1:
                            return answers
                        i += 1
                        answers.append(lines[i].split(' '))
                    return answers
                elif 'UNSATISFIABLE' in lines:
                    return []
                print(filename, 'no es un output legal de clingo')
                return []
            # SE ESCRIBE EL ARCHIVO EXTRA, CON EL TAMAÑO DE LA GRILLA (PUSE DOBLE Y PORQUE SELF.X TIRA UN NUMERO PEQUEÑO.)
            # CON LAS CASILLAS VISITADAS (ALIVE), LAS PERCEPCIONES QUE VOY SINTIENDO Y EL ÁTOMO QUE QUIERO VER SI ESTA EN TODOS LOS MODELOS.
            cell = f'cell(0..{self.y},0..{self.y}).'
            visitadas = ''
            for i in self.visited:
                visitadas += f'alive{i}. \n'
            percepciones = ''
            for i in perceptions:
                percepciones += f'{i}. \n'
            atomo = f':- {atom}. \n'
            extra = cell + '\n' + visitadas +'\n' + percepciones + '\n' + atomo
            fextra = open('extra.lp', 'w')
            fextra.write(extra)
            fextra.close()
            os.system('clingo -n 0 wumpus.lp extra.lp > out.txt 2> /dev/null')
            models = get_models('out.txt')
            return models == []
        
        #PARA CADA CELDA EN LA FRONTERA DE DONDE ESTOY POSICIONADO REVISO SI ESQUE HAY UNA CASILLA SAFE QUE ES SEGURA DONDE PUEDA MOVERME
        # SI ES ASÍ, ME MUEVO HACIA ALLA, DE LO CONTRARIO REVISO SI EN LAS CASILLAS ALEDAÑAS EN DONDE YA HE ESTADO EXISTE ALGUNA CASILLA SAFE
        #SI NO ENCUENTRA NINGUN SAFE MÁS COMENZARÁ A ANALIZAR EL NUMERO DE WUMPUS SI ES OBSERVABLE.
        for n in self.frontier:
            agregar_atomo = f'safe{n}'
            modelos = unsat_without(agregar_atomo)
            if modelos != True and n not in self.visited:
                pass
            else:
                if n in self.visited:
                    for k in self.visited:
                        for j in self.env.neighbors(k[0],k[1]):
                            agregar_atomo1 = f'safe{j}'
                            modelos1 = unsat_without(agregar_atomo1)
                            if modelos1 == True and j not in self.visited:
                                existencia, ruta = find_path(self.env.agent_x, self.env.agent_y, j[0], j[1], self.visited)
                                self.path.append(ruta[0])
                                self.visited.add(ruta[0])
                                return('goto',ruta[0][0], ruta[0][1])
                            else:
                                pass
                else:
                    self.path.append(n)
                    self.visited.add(n)
                    self.frontier = set()
                    for i in self.env.neighbors(n[0], n[1]):
                        self.frontier.add(i)
                    print(self.path)
                    return ('goto', n[0], n[1])

        #SI SE PUDEN CONOCER EL NUMERO DE WUMPUS Y DE PITS, SE COMENZARÁ A REVISAR LAS CASILLAS ALEDAÑAS POR DONDE SE HA ESTADO
        # HASTA DESCIFRAR CUALES SON WUMPUS, SI ENCUENTRA ALGUNO Y NO HAY MOVIMIENTOS POSIBLES, VA A MATARLO.
        # CUANDO ENCUENTRA A LOS WUMPUS, SE PROCEDE A ANALIZAR QUE CASILLAS SON PITS PARA NO PASAR POR AHI,
        # CUANDO YA SE HAN ENCONTRADO TODOS LOS PITS, SE DIRIGE A LAS CASILLAS RESTANTES QUE POR DESCARTE SON SAFE.
        if self.env.is_observable():
            numero_wumpus = self.env.get_num_wumpus()
            numero_pits = self.env.get_num_pits()
            pits = set()
            for k in self.path:
                if int(numero_wumpus) > 0:
                    for i in self.env.neighbors(k[0],k[1]): 
                        agregar_wumpus = f'wumpus{i}'
                        wumpus_en_mira = unsat_without(agregar_wumpus)
                        if wumpus_en_mira:
                            existencia, ruta = find_path(self.env.agent_x, self.env.agent_y, i[0], i[1], self.visited)
                            if ruta[0][0] == i[0] and ruta[0][1] == i[1]:
                                numero_wumpus -= 1
                                return ('shoot', ruta[0][0], ruta[0][1])
                            else:
                                return('goto',ruta[0][0], ruta[0][1])

                elif int(numero_pits) > 0:
                    for i in self.env.neighbors(k[0],k[1]):
                        agregar_pits = f'pit{i}'
                        pit_en_mira = unsat_without(agregar_pits)
                        if pit_en_mira and i not in pits:
                            pits.add(i)
                            numero_pits -= 1
                
                elif int(numero_pits) <= 0 and int(numero_wumpus) <= 0 :
                    for i in self.env.neighbors(k[0],k[1]):
                        if i not in pits and i not in self.visited:
                            existencia, ruta = find_path(self.env.agent_x, self.env.agent_y, i[0], i[1], self.visited)
                            self.visited.add(i)
                            return('goto', ruta[0][0], ruta[0][1])
                
                else:
                    return('unsolvable')

        # SI NO SE PUEDE SABER EL NUMERO DE WUMPUS Y PITS, INTENTARA BUSCAR WUMPUS CON LA INFORMACION QUE DISPONE
        # SI ENCUENTRA UNO LO MATARÁ, SI NO, SE PROCEDERÁ A BUSCAR SI ESQUE EXISTE ALGUN PIT CONOCIDO
        # Y REALIZARÁ MOVIMIENTOS SEGUROS LUEGO DE ESO.
        # SI NO PUEDE CONOCER MAS DEL JUEGO Y AUN NO ENCUENTRA EL ORO, SE RETORNARA QUE EL PROBLEMA ES INSATISFACIBLE.
        else:
            pits1 = set()
            for k in self.path:
                for i in self.env.neighbors(k[0],k[1]): 
                        agregar_wumpus = f'wumpus{i}'
                        agregar_pits = f'pit{i}'
                        agregar_atomo2= f'safe{i}'
                        wumpus_en_mira = unsat_without(agregar_wumpus)
                        pit_en_mira = unsat_without(agregar_pits)
                        atomo_en_mira = unsat_without(agregar_atomo2)
                        if pit_en_mira and i not in pits1:
                            pits1.add(i)
                        if wumpus_en_mira:
                            existencia, ruta = find_path(self.env.agent_x, self.env.agent_y, i[0], i[1], self.visited)
                            if ruta[0][0] == i[0] and ruta[0][1] == i[1]:
                                return ('shoot', ruta[0][0], ruta[0][1])
                            else:
                                return('goto',ruta[0][0], ruta[0][1])
                        if i not in pits1 and i not in self.visited and atomo_en_mira:
                            existencia, ruta = find_path(self.env.agent_x, self.env.agent_y, i[0], i[1], self.visited)
                            self.visited.add(i)
                            return('goto', ruta[0][0], ruta[0][1])
            return('unsolvable')
                        
                
                        
                        

    

                

                

                    


        
        
                        



            