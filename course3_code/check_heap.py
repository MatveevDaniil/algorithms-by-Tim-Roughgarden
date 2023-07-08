from typing import Optional, Tuple, Union


class MinHeapMap:
    def __init__(self):
        self.h = [] 
        self.map = {}
        
    def insert(self, item: Tuple[int]):
        self.check()
        self.h.append(item)
        key, node = item # get node
        self.map[node] = len(self) - 1 # remember node position
        self.bubble_up(len(self) - 1)
        self.check()
        
    def bubble_up(self, idx: int):
        parent = self.parent(idx)
        while parent is not None:
            if self.h[idx] < self.h[parent]:
                idx_node, parent_node = self.h[idx][1], self.h[parent][1] # get nodes
                self.map[idx_node], self.map[parent_node] = parent, idx # swap nodes positions
                self.h[idx], self.h[parent] = self.h[parent], self.h[idx]
                idx, parent = parent, self.parent(parent)
            else:
                break
        # self.check()
    
    def get_min(self) -> Optional[Tuple[int]]:
        if self.h:
            return self.h[0]
        self.check()
    
    def pop_min(self) -> Tuple[int]: 
        self.check()
        min_item = self.h[0]
        _, min_node = min_item # get min_node
        self.map.pop(min_node) # remove min_node from the mapping
        last_item = self.h.pop()
        if len(self) > 0:
            self.h[0] = last_item
            _, last_node = last_item # get last_node
            self.map[last_node] = 0 # set last_node map position as 0
            self.bubble_down(0)
        self.check()
        return min_item

    def bubble_down(self, idx: int): 
        l_child, r_child = self.childs(idx)
        while l_child < len(self):
            if r_child >= len(self) or self.h[l_child] < self.h[r_child]:
                min_child = l_child
            else:
                min_child = r_child
                
            if self.h[idx] > self.h[min_child]:
                idx_node, min_child_node = self.h[idx][1], self.h[min_child][1] # get nodes
                self.map[idx_node], self.map[min_child_node] = min_child, idx # swap map positions
                self.h[idx], self.h[min_child] = self.h[min_child], self.h[idx]
                idx, (l_child, r_child) = min_child, self.childs(min_child)
            else:
                break
        # self.check()
    
    def parent(self, idx: int) -> Optional[int]:
        if idx > 0:
            return (idx - 1) >> 1
        
    def childs(self, idx: int) -> Tuple[int]:
        l_child = idx << 1 
        return l_child + 1, l_child + 2
    
    def __len__(self) -> int:
        return len(self.h)
    
    def pop_node(self, node: int) -> Tuple[int]: # now we can delete any node from heap for O(h) time
        self.check()
        node_idx = self.map.pop(node)
        node_key, _ = self.h[node_idx]
        last_key, last_node = self.h.pop()
        if node_idx != len(self):
            self.h[node_idx] = (last_key, last_node)
            self.map[last_node] = node_idx
            self.bubble_down(node_idx)
            self.bubble_up(node_idx)
        self.check()
        return node_key, node
    
    def __contains__(self, node: int): # and check does we have node in heap
        return node in self.map
    
    def check(self):
        for node, idx in self.map.items():
            assert self.h[idx][1] == node, f'{node} {self.h[idx]}'
        for idx, (key, node) in enumerate(self.h):
            assert idx == self.map[node]
        for i in range(len(self.h)):
            child1, child2 = self.childs(i)
            if child1 < len(self):
                assert self.h[child1][0] >= self.h[i][0]
            if child2 < len(self):
                assert self.h[child2][0] >= self.h[i][0]
            
            
from collections import defaultdict
import heapq

class Graph:
    def __init__(self):
        self.nodes_num = 0
        self.edges_num = 0
        self.E = defaultdict(list)
        self.W = {}
    
    def read_file(self, file_name: str):
        with open(file_name) as f:
            lines = [line.split('\n')[0] for line in f.readlines()]
            self.nodes_num, self.edges_num = list(map(int, lines[0].split(' ')))
            for line in lines[1:]:
                if line != '':
                    node1, node2, weight = list(map(int, line.split(' ')))
                    self.W[(node1, node2)] = self.W[(node2, node1)] = weight
                    self.E[node1].append(node2)
                    self.E[node2].append(node1)
                
    def prims_stupid(self) -> int:
        X = set([1])
        weight_sum = 0
        ordered = []
        while len(X) < self.nodes_num:
            min_weight = float('inf')
            for edge in self.W:
                if (edge[0] in X) != (edge[1] in X):
                    if self.W[edge] < min_weight:
                        min_weight = self.W[edge]
                        min_edge = edge
            if min_edge[0] in X:
                ordered.append(min_edge[1])
                X.add(min_edge[1])
            else:
                ordered.append(min_edge[0])
                X.add(min_edge[0])
            weight_sum += min_weight
        return weight_sum, ordered
    
    def prims_heap(self) -> int:
        self.X = set([1])
        ordered=[]
        V_X = MinHeapMap()
        for node in range(2, self.nodes_num + 1):
            dist = self.W.get((1, node), float('inf'))
            V_X.insert((dist, node))
        weight_sum = 0
        while V_X:
            if V_X.get_min()[1] == 76:
                pass
            min_weight, min_node = V_X.pop_min()
            ordered.append(min_node)
            weight_sum += min_weight
            self.X.add(min_node)
            for node2 in self.E[min_node]:
                if node2 in V_X:
                    old_dist, _node2 = V_X.pop_node(node2)
                    new_dist = min(old_dist, self.W[(min_node, node2)])
                    V_X.insert((new_dist, node2))
        return weight_sum, ordered


import os
path = ''
fname = 'edges.txt'
G = Graph()
G.read_file(path + fname)
stupid_sum, ordered_stupid = G.prims_stupid()
smart_sum, ordered_smart = G.prims_heap()
for i in range(len(ordered_stupid)):
    if ordered_stupid[i] != ordered_smart[i]:
        print(i)
        break
print(stupid_sum, smart_sum)