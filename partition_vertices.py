
# ------------------------------------------------------------------------------
# partition_vertices: Functions to generate vertex partitions for mu, sigma and
# mu*simga.
# ------------------------------------------------------------------------------

# First, partition integer 'v' into all parts.
# Taken from: https://stackoverflow.com/questions/10035752/elegant-python-
#             code-for-integer-partitioning

def partitions(n, I=1):
    yield [n]
    for i in range(I, n//2 + 1):
        for p in partitions(n-i, i):
            yield [i] + p


# Find all ways to partition v into three parts (for the three vertices).

def three_partitions(p):
    t = []
    for pi in p: # all partitions in p array
        if len(pi)==3:
            t.append(pi)
    return t


# The partitions function outputs the partitions in increasing order, so select
# the largest (at index 2) for mu. Find all possible partitions for sigma and
# mu*sigma by assigning the remaining two vertices in two ways.

def all_three_partitions(t):
    v = []

    for ti in t:
        v_mu = ti[2] # choose mu to have the higest number of vertices
        u    = ti[0] # vertice choices for sigma and mu*sigma
        w    = ti[1]

        if u == w:
            vi = [v_mu, u, w]
            v.append(vi)

        else:
            vi1 = [v_mu, u, w] # for both possible arrangement of vertices of
            vi2 = [v_mu, w, u] # mu and sigma
            v.append(vi1)
            v.append(vi2)

    return v


# Combine functions above

def find_vertice_partitions(v):

    p = list(partitions(v))
    t = three_partitions(p)

    return all_three_partitions(t)



#------ TEST ------

# p = list(partitions(v))
# t = three_partitions(p)
#
# print("Vertices: ", v, "\n")
#
# print("----------------")
# print("Partition into three:\n", t, "\n")
#
#
# print("----------------")
# print("All possible three partitions:\n", all_three_partitions(t), "\n")
