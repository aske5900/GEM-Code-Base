from partition_vertices import partitions
from miscfunctions import factorial

# ------------------------------------------------------------------------------

# Functions to generate mu in standard form with a certain number of cycles

# This is similar to partition_permutations for sigma, however, rather than find
# all partitions generated in algorithm_u with entries in increasing order, the
# partitions are generated directly using an 'integer partitions' function
# (from partition_vertices.py).

# Integer partitions of 'n' into 'k' parts are generated, determining the number
# of entries of mu in each of the cycles.

# For example, if k = 2, and n = 5, partitions [1,4], [2,3] are generated, and
# mu is constructed as [[0], [1,2,3,4]] and [[0,1], [2,3,4]]. The isomorphisms
# of mu, (iso), in each case are calculated, and each pair [mu, iso] is returned
# in an array to the main file.

# ------------------------------------------------------------------------------


# Select partitions that have k number of parts.

def k_integer_partitions(n, k):
    all_partitions = list(partitions(n))
    k_partitions = []

    for partition in all_partitions:
        if len(partition) == k: # only use partitions with k parts
            k_partitions.append(partition)

    return k_partitions


# Create mu from k integer partition. Set mu to have cycles in increasing cycle
# length (this is determined by the initial partition function which outputs
# partitions with parts in increasing order).

def find_mu(n, int_partition):
    mu = []
    i = 0

    while i < n:
        for part in int_partition: # part gives the length of our cycle
            cycle = []

            for j in range(0,part): # add integer part worth of entries to cycle
                cycle.append(i)
                i += 1
            mu.append(cycle)

    return mu


# Determine isomorphisms of mu (easiest to do from the integer partition)

def find_isomorphisms(int_partition):

    remaining_cycles = int_partition
    isomorphisms = 1

    while len(remaining_cycles) != 0:

        for c1 in remaining_cycles: # the first cycle

            m = 1  # number of times cycle appears
            remaining_cycles.remove(c1)

            for c2 in remaining_cycles:
                if c2 == c1:
                    m += 1

            for i in range(0,m-1):
                remaining_cycles.remove(c1)

            isomorphisms *= (factorial(m)*c1**m)

    isomorphisms *= 2 # for reflection symmetries

    return isomorphisms



# Apply find_mu to all integer partitions to find all possible mu permutations

def find_k_cycle_mu(n,k):

    Mu = [] # list of mu's
    k_partitions = k_integer_partitions(n,k)

    for int_partition in k_partitions[0:]:
        mu = find_mu(n, int_partition)

        isomorphisms = find_isomorphisms(int_partition)

        Mu.append([mu, isomorphisms])

    return Mu
