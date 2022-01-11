from binary_heap import BinaryHeap
from node import Node
import time
import sys

class B_discrepancy:
    def __init__(self, initial_state):
        self.expansions = 0
        self.generated = 0
        self.initial_state = initial_state
        self.solution_node = None

    def estimate_suboptimality(self):
        return 1

    def fvalue(self, g, h):
        return 10000*h + h

    def search(self):
        self.start_time = time.process_time()
        self.open = BinaryHeap()
        self.expansions = 0
        initial_node = Node(self.initial_state)
        initial_node.g = 0
        initial_node.h = 0
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
            succ_neuronal = n.state.k_accs_successors()
            maxim_heuristic = max(sublist[3] for sublist in succ_neuronal)
            self.expansions += 1
            for child_state, action, cost, probability in succ_neuronal:
                child_node = self.generated.get(child_state)
                is_new = child_node is None  # es la primera vez que veo a child_state
                path_cost = n.g + cost  # costo del camino encontrado hasta child_state
                if is_new or path_cost < child_node.g:
                    # si vemos el estado child_state por primera vez o lo vemos por
                    # un mejor camino, entonces lo agregamos a open
                    if is_new:  # creamos el nodo de child_state
                        child_node = Node(child_state, n)
                        if probability == maxim_heuristic:
                            child_node.h = 0
                            self.generated[child_state] = child_node
                        else:
                            child_node.h = 0 + 1
                            self.generated[child_state] = child_node
                    child_node.action = action
                    child_node.parent = n
                    child_node.g = path_cost
                    child_node.key = self.fvalue(child_node.g, child_node.h) # actualizamos el valor f de child_node
                    self.open.insert(child_node) # inserta child_node a la open si no esta en la open
        self.end_time = time.process_time()      # en caso contrario, modifica la posicion de child_node en open
        return None
