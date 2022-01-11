from multi_binary_heap import MultiBinaryHeap
from multi_node import MultiNode
import time
import sys


class PrefAstar:
    def __init__(self, initial_state, heuristic, num_pref, out_of, suboptimality):
        self.expansions = 0
        self.generated = 0
        self.initial_state = initial_state
        self.heuristic = heuristic
        self.num_pref = num_pref
        self.out_of = out_of
        self.suboptimality = suboptimality


    def estimate_suboptimality(self):
        minimun_cost = 100000000
        if self.solution:
            for node in self.open:
                function_value = int(node.h[0]) + int(node.g)
                if minimun_cost > function_value:
                    minimun_cost = function_value
            for node in self.preferred:
                function_value = int(node.h[0]) + int(node.g)
                if minimun_cost > function_value:
                    minimun_cost = function_value
            return self.solution.g/minimun_cost


    def fvalue(self, g, h):
        return 100000000*(g + h) - g


    def evaluate_suboptimality(self,n,suboptimality):
        function_value_node = n.key[0]
        ele_open = self.open.top()
        ele_pref = self.preferred.top()
        min_value = 100000000000
        if ele_open is not None:
            function_value_open = ele_open.key[0]
        if ele_pref is not None:
            function_value_preferred = ele_pref.hey[0]
        if ele_open and ele_pref:
            min_value = min(function_value_open,function_value_preferred)
        if ele_open and not ele_pref:
            min_value = function_value_open
        if ele_pref and not ele_open:
            min_value = function_value_preferred
        if function_value_node > suboptimality*min_value:
            self.open.insert(n)
            return True
        else:
            return False

    def search(self):
        self.start_time = time.process_time()
        self.preferred = MultiBinaryHeap(0)
        self.open = MultiBinaryHeap(1)
        self.expansions = 0
        self.open_extractions = 0
        self.preferred_extractions = 0
        incumbent_cost = 10000000
        initial_node = MultiNode(self.initial_state)
        initial_node.g = 0
        initial_node.h[0] = self.heuristic(self.initial_state)
        initial_node.h[1] = initial_node.h[0]
        initial_node.key[0] = self.fvalue(initial_node.g,initial_node.h[0])  # asignamos el valor f
        initial_node.key[1] = self.fvalue(initial_node.g,initial_node.h[1])
        self.open.insert(initial_node)
        # para cada estado alguna vez generado, generated almacena
        # el Node que le corresponde
        self.generated = {}
        self.generated[self.initial_state] = initial_node
        self.incumbent = None
        counter = 0
        while not self.open.is_empty() or not self.preferred.is_empty():
            if self.preferred.is_empty():
                queue = self.open
                self.open_extractions += 1
            elif self.open.is_empty():
                queue = self.preferred
                self.preferred_extractions += 1
            elif counter % self.out_of < self.num_pref:
                queue = self.preferred
                self.preferred_extractions += 1
            else:
                queue = self.open
                self.open_extractions += 1

            counter += 1
            
            n = queue.extract()
            
            if n.h[0] == 0:
                self.end_time = time.process_time()
                self.solution = n
                return self.solution
            
            calculate_subopt = self.evaluate_suboptimality(n,self.suboptimality)

            if calculate_subopt is False:
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
                            child_node = MultiNode(child_state, n)
                            child_node.h[0] = self.heuristic(child_state)
                            child_node.h[1] = child_node.h[0]
                            self.generated[child_state] = child_node
                        child_node.action = action
                        child_node.parent = n
                        child_node.g = path_cost
                        child_node.key[0] =  self.fvalue(child_node.g, child_node.h[0])
                        child_node.key[1] =  self.fvalue(child_node.g, child_node.h[0]) # actualizamos el f de child_node
                        if child_node.state.preferred:
                            self.preferred.insert(child_node) # inserta child_node a la open si no esta en la open
                        else:
                            self.open.insert(child_node)
            else:
                continue
            self.end_time = time.process_time()      # en caso contrario, modifica la posicion de child_node en open 
        return None
