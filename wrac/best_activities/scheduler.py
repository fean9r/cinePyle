'''
Created on Sep 13, 2016

@author: fean0r
'''
import itertools
import math
import sys
import timeit

import pulp
from pygraph.algorithms.generators import generate
from pygraph.algorithms.minmax import shortest_path
from pygraph.algorithms.minmax import shortest_path_bellman_ford
from pygraph.classes.digraph import digraph

from .model import Activity
from .model import TimeInterval
from .model import overlap
from .model import same_day
from .model import same_week
from .utils import ProgressBar


# Activities List 
#### Name---TimeStart---Duration---Value#####
#      a        10         2         1
#      a        12         2         1
#      b        11         3         5
#      c        13         5         10
#      d        19         1         2
#      e         8         1         20
#      g        22         4         20
#############################################
# a = Activity('a',TimeInterval(10 ,2) ,1)
# a2 = Activity('a',TimeInterval(12 ,2) ,1)
# b = Activity('b',TimeInterval(11 ,3) ,5)
# c = Activity('c',TimeInterval(13 ,5) ,10)
# d = Activity('d',TimeInterval(19 ,1) ,2)
# e = Activity('e',TimeInterval(8 ,1) ,20)
# g = Activity('g',TimeInterval(22 ,4) ,20)
# activity_list = [a, a2, b, c, d, e, g]
# Busy List 
#### BusyTimeStart---Duration #####
#      7                2
#      24               3         
###################################
# busy_list = [TimeInterval(7 ,2), TimeInterval(24 ,3)]     
# Activities List after filtering the busy list
#### Name---TimeStart---Duration---Value#####
#      a        10         2         1
#      b        11         3         5
#      c        13         5         10
#      d        19         1         2
#############################################    
# decisor = GraphActivitiesDecisor(activity_list, busy_list, 1)
# print decisor.decideActivities()
class GraphActivitiesDecisor():
    def __init__(self, activity_list):
        self.activity_list = list(activity_list)
            
    def __makeGraph(self, l_activities):
        
        my_graph = digraph()
        # Nodes
        l_activities.insert(0, Activity('__s__', TimeInterval(0 , 0) , 0))
        l_activities.append(Activity('__t__', TimeInterval(sys.maxint , sys.maxint) , 0))    
        nodes = range(len(l_activities))
        my_graph.add_nodes(nodes)

        # Edges
        for i in nodes:
            for j in nodes:
                a_i = l_activities[i]
                a_j = l_activities[j]
                # 1 they are not the same node 
                # 2 
                if (i != j) and a_i.interval.end < a_j.interval.start:
                    # add one arc from 
                    my_graph.add_edge((i, j), wt=-a_i.value)
        return my_graph
       
    def __hasDuplicates(self, l_activities):
        d_map = self.__duplicates_map(l_activities)
        for l_elem in d_map.values():
            if len(l_elem) > 1:
                return True
        return False
       
    def __duplicates_map(self, l_activities):
        names = {}
        for i in l_activities:
            if names.has_key(i.name):
                names[i.name].append(i)
            else:
                 names[i.name] = [i]
        return names
#         for val in names.items():
#             if val >1 :
#                 return True
#         return False

    def __getBestActivities(self, l_activities):
        my_graph = self.__makeGraph(l_activities)
        # spanning_tree, dist = shortest_path(my_graph, 0)
        spanning_tree, dist = shortest_path_bellman_ford(my_graph, 0)
        final_node_id = len(l_activities) - 1
        v = spanning_tree[final_node_id]
        
        activity_decision = []
        while v != None:
            activity_decision.append(l_activities[v])
            v = spanning_tree[v]
        # pop the __s__ node from decision
        activity_decision.pop()
        activity_decision.reverse()
        return activity_decision , -dist[final_node_id]

    def decideActivities(self):
        
        # 1: separate elements that appears more than one to the single ones from the filtered list
        multiples_acts = []
        singles_acts = []
        
        duplicats_map = self.__duplicates_map(self.activity_list)
        for l_acts_i in duplicats_map.values():
            if len(l_acts_i) == 1:
                singles_acts += l_acts_i
            else:
                multiples_acts += l_acts_i
        
        print 'Tot activities #:', len(self.activity_list)
        print 'Multiples activity #:', len(multiples_acts)
        print 'Single activity #:', len(singles_acts)
        
        # 2: Get the number of activities that appears more than one time
        # Es: multiples_acts = [(a,2,3),(a,4,3),(a,5,3),(b,2,3),(b,4,3),(c,5,3),(c,2,3),(c,4,3)] 
        # num_diff_act == 3
        list_names = []
        for activity in multiples_acts:
            list_names.append(activity.name)
        num_diff_act = len(list(set(list_names)))
        print 'Number of activities that are repeated', num_diff_act

        pool = tuple(multiples_acts)
        n = len(pool)
        r = num_diff_act
        # n!/r!/(n-r)!
        num_item_combinations = math.factorial(n) / math.factorial(r) / math.factorial(n - r)
        print 'Number of combinations', num_item_combinations, 'of length', num_diff_act


        # 3.a: Make all the num_diff_act length combinations of the activities 
        filtered_combinations = []
        if num_diff_act > 0:
            comb_iter = itertools.combinations(multiples_acts, num_diff_act)
            # 3.b: Remove the combinations of same activity and make it a list instead of a tuple
            l_cobinations = list(comb_iter)
            # drop_iter = itertools.dropwhile(lambda x: self.__hasDuplicates([] + list(x)), comb_iter)            
            # filtered_combinations = list(drop_iter)
            filtered_combinations = filter(lambda x: not(self.__hasDuplicates(x)), l_cobinations)
            print 'Number of combinations after filtering' , len(filtered_combinations)
#         print len(filtered_combinations)
#         i=0
#         for alist in filtered_combinations:
#             if self.__hasDuplicates(alist):
#                 i=i+1
#         print 'Duplicates',i
        # 4.a: Make a list of activities for each combination and add to it the single activities
        acts_list = []
        for comb in filtered_combinations:
            acts_list.append(singles_acts + list(comb))
        # 4.b: In case we have no multiple activities use just the single activities
        if len(acts_list) == 0:
            acts_list.append(singles_acts)
       
        # 5: compute __getBestActivities on each activity list and add the results to a list 
        best_activities = []
        best_activities_values = []
        
        print 'Number of time to execute Dijkstra', len(acts_list)
        
        if False :
            # copy to avoid problems
            new_act_list = list(acts_list[0])
            ex_graph = self.__makeGraph(new_act_list)
            print 'Number of nodes in the graph', len(ex_graph.nodes())
            print 'Computing:', len(acts_list), 'times a Dijkstra of O(', len(ex_graph.edges()), '+', len(ex_graph.nodes()) , ')'        
            
            my_pc_op_dur = 5.698616375191018e-06 
            time_estimation = my_pc_op_dur * (len(ex_graph.edges()) + len(ex_graph.nodes())) * len(acts_list)
            print 'Estimate time on my machine [min]:', (time_estimation) / 60.0
        pbar = ProgressBar(len(acts_list))
        for acts in acts_list:
            # sort ?
            acts.sort(key=lambda x: x.interval.start)
            best_acts, value = self.__getBestActivities(acts)
            best_activities.append(best_acts)
            best_activities_values.append(value)
            pbar.progress()
        
        # print  pbar.getTime()
        
        # 6.a: find the max from the distance list 
        maxValue = max(best_activities_values)
        #  indexMaxValue is the index of the max
        indexMaxValue = best_activities_values.index(maxValue)   
        # 6.b: return the activities that correspond to this max value
        return best_activities[indexMaxValue], maxValue


class PLActivitiesDecisor():
    def __init__(self, activity_list, max_film_for_day):
        self.activity_list = list(activity_list)
        self.act_LPname_map = {}
        self.max_num_film_week = 3
        self.max_num_film_day = max_film_for_day
        
    def __activity_overlaps(self, activity):
        i1 = activity.interval
        act_overlaps = map(lambda x: overlap(i1, x.interval) , self.activity_list)
        return act_overlaps

    def __activity_same_day(self, activity):
        i1 = activity.interval
        act_same_days = map(lambda x: same_day(i1, x.interval) , self.activity_list)
        return act_same_days
    
    def __activity_same_week(self, activity):
        i1 = activity.interval
        act_same_week = map(lambda x: same_week(i1, x.interval) , self.activity_list)
        return act_same_week

    def __activity_types(self, activity):
        activity_type = [0] * len(self.type_names)
        index_activity_typeName = self.type_names.index(activity.name)
        activity_type[index_activity_typeName] = 1
        return activity_type

    def __writeProblem(self):
        num_activities = len(self.activity_list)
        # kills order 
        self.type_names = list(set(map(lambda x: x.name, self.activity_list)))
        n = num_activities
        # 1 Make a list of all the activities Rating
        Rat = map(lambda x: x.value, self.activity_list)
        # 2 Make a matrix of the overlapping between activities 
        Overlap = map(self.__activity_overlaps, self.activity_list)
        # 2b Make a vector with the number of overlap for each activity
        OverlapMaxVect = []
        for i in range(n):
            max_ev_in_overlap = sum([Overlap[i][j] for j in range(n)])
            max_ev_in_overlap = max_ev_in_overlap - 1
            if max_ev_in_overlap == 0:
                max_ev_in_overlap = 1
            OverlapMaxVect.append(max_ev_in_overlap)
        # 3 Make a matrix of the type of each         
        Type = map(self.__activity_types, self.activity_list)
        # 4 Make a matrix of same day activities
        SameDay = map(self.__activity_same_day, self.activity_list)
        # 5 Make a matrix of same week activities
        SameWeek = map(self.__activity_same_week, self.activity_list)
        
        # Problem Variables
        # xi  == True if activity xi is decided 0 otherwise
        x = pulp.LpVariable.dicts("x", range(n), cat=pulp.LpBinary)
        
        for i in range(n):
            name = "x_%d" % i
            self.act_LPname_map[name] = self.activity_list[i]       
        
        # Problem Objective Function 
        self.lp_prob = pulp.LpProblem("Minmax Problem", pulp.LpMaximize)
        self.lp_prob += pulp.lpSum([Rat[i] * x[i] for i in range(n)]), "Minimize_the_maximum"

        # Problem Constraints
        
        # Time constraints, not more than self.max_num_film_week activities each week
        for i in range(n):
            dot_SameWeek_x = pulp.lpSum([ SameWeek[j][i] * x[j] for j in range(n) ])
            label = "SameWeek_Act_constraint_%d" % i 
            condition = pulp.lpSum([dot_SameWeek_x]) <= self.max_num_film_week
            self.lp_prob += condition, label

        # Time constraints, not more than self.max_num_film_day activity each day
        for i in range(n):
            dot_SameDay_x = pulp.lpSum([ SameDay[j][i] * x[j] for j in range(n) ])
            label = "SameDay_Act_constraint_%d" % i 
            condition = pulp.lpSum([dot_SameDay_x]) <= self.max_num_film_day
            self.lp_prob += condition, label
        
        # Time constraints, no activity at the same time
        for i in range(n):
            dot_Overlap_x = pulp.lpSum([ Overlap[j][i] * x[j] for j in range(n) ])
            #            
            max_ev_in_overlap = OverlapMaxVect[i]
            label = "Overlap_Act_constraint_%d" % i 
            condition = pulp.lpSum([dot_Overlap_x]) <= max_ev_in_overlap
            self.lp_prob += condition, label


        # Type 1 line for each movie, 1 column for each type 
        for i in range(len(Type[0])):
            label = "Max_Type_Act_constraint_Type_%s" % self.type_names[i]
            dot_Type_x = pulp.lpSum([Type[j][i] * x[j] for j in range(n)])
            condition = pulp.lpSum([dot_Type_x]) <= 1
            self.lp_prob += condition, label
        
        self.lp_prob.writeLP("MinmaxProblem.lp")  # optional

    def decideActivities(self):
        
        self.__writeProblem()
        self.lp_prob.solve()

        print "Status:", pulp.LpStatus[self.lp_prob.status]
        best_activities = []

        for v in self.lp_prob.variables():
            if v.varValue == 1:
                best_activities.append(self.act_LPname_map[v.name])
        maxValue = pulp.value(self.lp_prob.objective)
        best_activities.sort(key=lambda x: x.interval.start)
        return best_activities, maxValue
