from itertools import permutations
from sympy.combinatorics import Permutation

import time
import math

from miscfunctions import *

# ------------------------------------------------------------------------------
# Functions to generate all permutations of n letters with k-cycles.
# ------------------------------------------------------------------------------

# algorithm_u: Generate all k (or m in the algorithm) subset partitions of array
# [0,...,n-1].

# Knuth Algorithm, unchanged from: https://codereview.stackexchange.com/
# questions/1526/finding-all-k-subset-partitions

# (Note, mu and sigma in the algorithm are not the mu and sigma from the main
# file. here, they are just variables.)

# The algorithm generates all partitions with 0 in the first entry of the first
# part of the partition.
#       (1) The other numbers are *not* placed in the partitions in increasing
#           order
#       (2) And the parts also do not have lengths in increasing order.

# I.e. (1) it is possible to have [0, 1],[2] and [0,2],[1],
# and (2) it is possible to have [0,1],[2] and [0],[1,2]. (Other partition
# functions might only produce [0],[1,2]).

# Using this, we are able to produce all possible partitions.

def algorithm_u(ns, m):
    if m == 1:
        return [[ns]]

    def visit(n, a):
        ps = [[] for i in range(m)]
        for j in range(n):
            ps[a[j + 1]].append(ns[j])
        return ps

    def f(mu, nu, sigma, n, a):
        if mu == 2:
            yield visit(n, a)
        else:
            for v in f(mu - 1, nu - 1, (mu + sigma) % 2, n, a):
                yield v
        if nu == mu + 1:
            a[mu] = mu - 1
            yield visit(n, a)
            while a[nu] > 0:
                a[nu] = a[nu] - 1
                yield visit(n, a)
        elif nu > mu + 1:
            if (mu + sigma) % 2 == 1:
                a[nu - 1] = mu - 1
            else:
                a[mu] = mu - 1
            if (a[nu] + sigma) % 2 == 1:
                for v in b(mu, nu - 1, 0, n, a):
                    yield v
            else:
                for v in f(mu, nu - 1, 0, n, a):
                    yield v
            while a[nu] > 0:
                a[nu] = a[nu] - 1
                if (a[nu] + sigma) % 2 == 1:
                    for v in b(mu, nu - 1, 0, n, a):
                        yield v
                else:
                    for v in f(mu, nu - 1, 0, n, a):
                        yield v

    def b(mu, nu, sigma, n, a):
        if nu == mu + 1:
            while a[nu] < mu - 1:
                yield visit(n, a)
                a[nu] = a[nu] + 1
            yield visit(n, a)
            a[mu] = 0
        elif nu > mu + 1:
            if (a[nu] + sigma) % 2 == 1:
                for v in f(mu, nu - 1, 0, n, a):
                    yield v
            else:
                for v in b(mu, nu - 1, 0, n, a):
                    yield v
            while a[nu] < mu - 1:
                a[nu] = a[nu] + 1
                if (a[nu] + sigma) % 2 == 1:
                    for v in f(mu, nu - 1, 0, n, a):
                        yield v
                else:
                    for v in b(mu, nu - 1, 0, n, a):
                        yield v
            if (mu + sigma) % 2 == 1:
                a[nu - 1] = 0
            else:
                a[mu] = 0
        if mu == 2:
            yield visit(n, a)
        else:
            for v in b(mu - 1, nu - 1, (mu + sigma) % 2, n, a):
                yield v

    n = len(ns)
    a = [0] * (n + 1)
    for j in range(1, m + 1):
        a[n - m + j] = j - 1
    return f(m, n, 0, n, a)



# For each partition, p, generated from the algorithm, we need to find all
# possible (1-cycle) permutations of the individual parts in p.

# E.g. take p = [[0,1,2],[3,4],[5]].
# We need to find the permutations of [0,1,2], [3,4], [5] individually.
# Both [3,4], [5] only have one permutation (3 4), (5).
# But [0,1,2] has two, (0 1 2), (0 2 1).

# ------------------------------------------------------------------------------

# "permutations_of_parts(partition)" takes a partition, and
# outputs the possible permutations of its parts as an array:
#       [ [array of perms of part 1], [array of perms of part 2], ... ]

# I.e. for [[0,1,2],[3,4],[5]], we output:
#                 [ [ [0,1,2],[0,2,1] ], [[3,4]], [[5]] ] ---------- (*)


def permutations_of_parts(partition):

    perms_of_parts = [] # i.e. eventually, (*)

    for part in partition: # find all permutations of individual parts

        if len(part) == 0 or len(part) == 1 or len(part) == 2:
            perms_of_parts.append([part])
            continue

        # else, generate possible unique permutations (when put in cycle notation)
        unique_perms = []

        # Fix index 0 as the first entry and generate all permutations of
        # remaining elements ('sub_perms'), to ensure there are no duplicates
        sub_perms = list(permutations(part[1:]))

        for perm in sub_perms:
            unique_perms.append([part[0]]+list(perm))

        if len(unique_perms) != math.factorial(len(part[1:])):
            error("Insufficient permutations")

        perms_of_parts.append(unique_perms)

    return perms_of_parts


# ------------------------------------------------------------------------------

# "total_permutations_of_individial_parts" takes the 'perms_of_parts'
# generated in the previous function and finds all possible k-cycles
# formed by combining the single-cycle permutations of the parts.

# For example, for [ [ [0,1,2],[0,2,1] ], [[3,4]], [[5]] ], we want to output
# [ [ [0,1,2],[3,4],[5] ], [ [0,2,1],[3,4],[5] ]  ]
# So that we can get the permutations (012)(34)(5), and (021)(34)(5)

# ------------------------------------------------------------------------------

# The algorithm:
#
# - Generate empty array for possible permutations.
# - Loop through the cycles and add 'current_sub_len' worth of each type of cycle
#   to the array.
# - Repeat (alternating between the different choices of the perms for that
#   cycle) until the array is filled.
# - After each cycle, increase the number of repetitions, and decrease the
#   current_sub_len.

#
#      E.g. suppose perms_of_parts = [ [x1, x2, x3], [y1, y2, y3], [z1] ]
#      (x1,..,x3,y1,...,y3,z1 are permutations generated in the prev func.)
#
#      There are 9 possible permutations we can form, so make:
#              tot_permutations =   [ [],[],[],[],[],[],[],[],[] ]
#
#      (1st cycle)
#      - current_sub_len = (# tot permutations/len(1st cycle)) = 3
#      - repeat = 1
#      - allocate 3*x1s, 3*x2s, 3*x3s, and loop only once
#      - tot_permutations = [x1], [x1], [x1], [x2], [x2], [x2], [x3], [x3], [x3]
#
#      (2nd cycle)
#      - current_sub_len = 3/len(2nd cycle) = 1
#      - repeat = 1 * len(1st cycle) = 3 (for each of the x 'intervals' created
#        previously)
#      - tot_permutations = [ [x1,y1], [x1,y2], [x1,y3],
#                             [x2,y1], [x2,y2], [x2,y3], ... ]
#
#      (3rd cycle)
#      - current_sub_len = 1/len(3rd cycle) = 1
#      - repeat = 3 * len(2nd cycle) = 9 (as of y 'intervals' have length 1)
#        (i.e. add z to all permutations)
#      - tot_permutations = [ [x1,y1,z], [x1,y2,z], [x1,y3,z],
#                             [x2,y1,z], [x1,y2,z], [x2,y3,z], ... ]


def total_permutations_of_individial_parts(perms_of_parts):

    # find total number of permutations
    num_tot_permutations=1

    for cycle in perms_of_parts:
        num_tot_permutations=num_tot_permutations*len(cycle)

    # create empty array for permutations
    tot_permutations=[]

    for i in range(0,num_tot_permutations):
        tot_permutations.append([])


    repeat = 1 #begin with 1 repetition

    current_sub_len = int(num_tot_permutations/len(perms_of_parts[0]))

    for cycle in perms_of_parts:

        if cycle!=perms_of_parts[0]:
            current_sub_len = int(current_sub_len/len(cycle))

        cycle_len=len(cycle)
        i=0

        for repetition in range(0,repeat):

            for j in range(0,cycle_len):
                sub_idx = 0
                while sub_idx < current_sub_len:
                    tot_permutations[i].append(cycle[j])
                    i += 1
                    sub_idx += 1

        repeat = repeat*cycle_len

    if len(tot_permutations) != num_tot_permutations:
        error("Insufficient tot # permutations")

    return tot_permutations


# ------------------------------------------------------------------------------

# "find_k_cycle_sigma" combines the functions above.
#       n = number of nodes, k = number of cycles.

# Loop through all partitions generated in the algorithm, and find all the
# possible permutations of each of the partitions. Add to 'k_cycles' and
# return the array.

def find_k_cycle_sigma(n, k):
    k_cycles=[]
    nodes=list(range(n))

    for partitions in list(algorithm_u(nodes,k)):

        perms_of_parts=permutations_of_parts(partitions)
        tot_permutations = total_permutations_of_individial_parts(perms_of_parts)
        k_cycles += tot_permutations

    return k_cycles
