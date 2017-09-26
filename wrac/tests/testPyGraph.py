

from pygraph.algorithms.generators import generate
from pygraph.algorithms.minmax import shortest_path
from pygraph.algorithms.minmax import shortest_path_bellman_ford
from pygraph.classes.digraph import digraph


# l_activities.insert(0, Activity('__s__', TimeInterval(0 , 0) , 0))
# l_activities.append(Activity('__t__', TimeInterval(sys.maxint , sys.maxint) , 0))    
nodes = [0, 1, 2, 3] 


my_graph = digraph()
my_graph.add_nodes(nodes)

my_graph.add_edge((0, 1),wt = 0)
my_graph.add_edge((0, 2),wt = 0)
my_graph.add_edge((0, 3),wt = 0)
my_graph.add_edge((1, 3),wt = 6.8)
my_graph.add_edge((2, 3),wt = 7.1)
 
print my_graph
spanning_tree, dist = shortest_path(my_graph, 0)
print spanning_tree , dist


spanning_tree, dist = shortest_path_bellman_ford(my_graph, 0)
print spanning_tree , dist