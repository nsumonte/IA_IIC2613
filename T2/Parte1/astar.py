from binary_heap import BinaryHeap
from node import Node
import time


class Astar:
    def __init__(self, initial_state, heuristic, weight):
        self.expansions = 0
        self.generated = 0
        self.initial_state = initial_state
        self.heuristic = heuristic
        self.weight = weight
        self.solution_node = None

    def estimate_suboptimality(self):
        solution_cost = 10000*self.solution_node.g - self.solution_node.g
        minimun_cost = None
        for nodo in self.open:
            f_value = 10000*(nodo.g + nodo.h) - nodo.g
            if minimun_cost != None:
                if f_value < minimun_cost:
                    minimun_cost = f_value
            else:
                minimun_cost = f_value
        suboptimality = solution_cost / minimun_cost
        return suboptimality

    def fvalue(self, g, h):
        return 100000*(g + self.weight*h) - g

    def search(self):
        self.start_time = time.process_time()
        self.open = BinaryHeap()
        self.expansions = 0
        initial_node = Node(self.initial_state)
        initial_node.g = 0
        initial_node.h = self.heuristic(self.initial_state)
        initial_node.key = self.fvalue(0, initial_node.h) # asignamos el valor f
        self.open.insert(initial_node)
        # para cada estado alguna vez generado, generated almacena
        # el Node que le corresponde
        self.generated = {}
        self.generated[self.initial_state] = initial_node
        while not self.open.is_empty():
            n = self.open.extract()
    
            if n.state.is_goal():
                self.end_time = time.process_time()
                self.solution_node = n
                return n
                
            succ = n.state.successors()
            self.expansions += 1
            for child_state, action, cost in succ:
                child_node = self.generated.get(child_state)
                is_new = child_node is None  # es la primera vez que veo a child_state
                path_cost = n.g + cost  # costo del camino encontrado hasta child_state
                if is_new or path_cost < child_node.g:
                    # si vemos el estado child_state por primera vez o lo vemos por
                    # un mejor camino, entonces lo agregamos a open
                    if is_new:  # creamos el nodo de child_state
                        child_node = Node(child_state, n)
                        child_node.h = self.heuristic(child_state)
                        self.generated[child_state] = child_node
                    child_node.action = action
                    child_node.parent = n
                    child_node.g = path_cost
                    child_node.key = self.fvalue(child_node.g, child_node.h) # actualizamos el valor f de child_node
                    self.open.insert(child_node) # inserta child_node a la open si no esta en la open
        self.end_time = time.process_time()      # en caso contrario, modifica la posicion de child_node en open
        return None
