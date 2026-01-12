# =============================
# Student Names:
# Group ID:
# Date:
# =============================
# CISC 352
# heuristics.py
# desc:
#


#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete problem solution.

'''This file will contain different constraint propagators to be used within
   the propagators

1. ord_dh (worth 0.25/3 points)
    - a Variable ordering heuristic that chooses the next Variable to be assigned 
      according to the Degree heuristic

2. ord_mv (worth 0.25/3 points)
    - a Variable ordering heuristic that chooses the next Variable to be assigned 
      according to the Minimum-Remaining-Value heuristic


var_ordering == a function with the following template
    var_ordering(csp)
        ==> returns Variable

    csp is a CSP object---the heuristic can use this to get access to the
    Variables and constraints of the problem. The assigned Variables can be
    accessed via methods, the values assigned can also be accessed.

    var_ordering returns the next Variable to be assigned, as per the definition
    of the heuristic it implements.
   '''

def ord_dh(csp):
    ''' return next Variable to be assigned according to the Degree Heuristic '''
    # IMPLEMENT
    vars = csp.get_all_unasgn_cars()
    next = vars(0)
    numInvolved = 0
    for v in vars:
        if numInvolved < csp.get_cons_with_var(v):
            next = v
    return v
    #pass

def ord_mrv(csp):
    ''' return Variable to be assigned according to the Minimum Remaining Values heuristic '''
    # IMPLEMENT
    vars = csp.get_all_unasgn_cars()
    next = vars(0)
    for v in vars:
        if v.cur_domain_size() < next.cur_domain_size():
            next = v
        if next.cur_domain_size() == 1:
            break
    return next
    #pass
