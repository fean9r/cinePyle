
from numpy import dot , random as np

import pulp


def solve_minmax(n, a, B, x_min=None, x_max=None):
    x = pulp.LpVariable.dicts("x", range(n + 1), x_min, x_max)
    lp_prob = pulp.LpProblem("Minmax Problem", pulp.LpMinimize)
    lp_prob += pulp.lpSum([x[n]]), "Minimize_the_maximum"

    for i in range(n):
        label = "Max_constraint_%d" % i
        dot_B_x = pulp.lpSum([B[i][j] * x[j] for j in range(n)])
        condition = pulp.lpSum([x[n]]) >= a[i] + dot_B_x
        lp_prob += condition, label

    lp_prob.writeLP("MinmaxProblem.lp")  # optional
    lp_prob.solve()

    print "Status:", pulp.LpStatus[lp_prob.status]
    for v in lp_prob.variables():
        print v.name, "=", v.varValue
    print "Total Cost =", pulp.value(lp_prob.objective)
    
n = 50
a = 2. * np.random(n) - 1.
B = 2. * np.random((n, n)) - 1.
f = lambda (i, x): a[i] + np.dot(B[i], x)
objective = lambda x: max([f(i, x) for i in range(n)])

# solve_minmax(n,a,B, 0,1)

max_num_film_week = 3
max_num_film_day = 1

# num film
n = 6
Rat = np.random_sample(n) * 10
print sum(Rat)

#                Overlap
#         0    1    2    3    4    5
#      +-------------------------------+   
#    0 |  1    0    0    0    0    0   |
#    1 |  0    1    0    0    0    0   |
#    2 |  0    0    1    0    0    0   |
# N  3 |  0    0    0    1    0    0   |
#    4 |  0    0    0    0    1    0   |
#    5 |  0    0    0    0    0    1   |
#      +-------------------------------+
Overlap = [[1, 0, 0, 0, 0, 0],
           [0, 1, 0, 0, 1, 0],
           [0, 0, 1, 0, 0, 0],
           [0, 0, 0, 1, 0, 0],
           [0, 1, 0, 0, 1, 0],
           [0, 0, 0, 0, 0, 1]]
#Overlap[i,j] == 1 if activity i timing overlaps with activity j
#                Type
#         A    B    C    D    E
#      +-------------------------   
#    0 |  1    0    0    0    0
#    1 |  0    1    0    0    0
#    2 |  1    0    0    0    0
# N  3 |  0    0    1    0    0
#    4 |  0    0    0    0    1
#    5 |  0    0    0    1    0
#      +-------------------------  
TypeNames = ['A' , 'B' , 'C'  , 'D' , 'E']
Type = [[1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0], 
        [1, 0, 0, 0, 0], 
        [0, 0, 1, 0, 0], 
        [0, 0, 0, 0, 1], 
        [0, 0, 0, 1, 0]]



# Variables
# x == True if event x is decided 0 otherwise
x = pulp.LpVariable.dicts("x", range(n + 1), cat=pulp.LpBinary)

 # Objective Function 
lp_prob = pulp.LpProblem("Minmax Problem", pulp.LpMaximize)
lp_prob += pulp.lpSum([Rat[i] * x[i] for i in range(n)]), "Minimize_the_maximum"

# Constraints
label = "Max_Act week constraint"
condition = pulp.lpSum([ x[i] for i in range(n)]) <= max_num_film_week 
lp_prob += condition, label

label = "Max_Act day constraint"

# Time constraints, no activity at the same time
for i in range(n):
    label = "Overlap_Act_constraint_%d" % i 
    dot_Overlap_x = pulp.lpSum([ Overlap[j][i] * x[j] for j in range(n) ])
    condition = pulp.lpSum([dot_Overlap_x]) <= 1
    lp_prob += condition, label


# Type 1 line for each movie, 1 coloumn for each type 
for i in range(len(Type[0])):
    label = "Max_Type_Act_constraint_Type_%s" % TypeNames[i]
    dot_Type_x = pulp.lpSum([Type[j][i] * x[j] for j in range(n)])
    condition = pulp.lpSum([dot_Type_x]) <= 1
    lp_prob += condition, label

lp_prob.writeLP("MinmaxProblem.lp")  # optional
lp_prob.solve()


print "Status:", pulp.LpStatus[lp_prob.status]
for v in lp_prob.variables():
    print v.name, "=", v.varValue
print "Total Cost =", pulp.value(lp_prob.objective)
