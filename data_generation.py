from sympy.combinatorics import Permutation
from sympy.combinatorics.perm_groups import PermutationGroup

import math
import time

from permutations_sigma import find_k_cycle_sigma
from partition_vertices import find_vertice_partitions
from partition_mu import find_k_cycle_mu

from miscfunctions import *

# ------------------------------------------------------------------------------
# Summary:
#           - This is the 'main-file' -- choose v and n (or g) and loop through
#             all ways to partition the vertices between mu,sigma,mu*sigma.
#
#             For each vertice partition, generate possible permutations for
#             mu and sigma with set number of vertices (using partition_mu and
#             permutations_sigma). Check if mu*sigma has the correct number of
#             cycles, and if so, save the permutations to the csv file.
#
#           - partition_vertices - generates all ways 'v' can be partitioned to
#             each of mu, sigma, mu*sigma. Ouput partitions in array.
#
#           - permutations_sigma - generates all possible permutations of sigma
#             with k cycles. Each permutation is represented as an array.
#             Outputs all permutations in an array.
#
#           - partition_mu - generates all possible permutations of mu (in
#             standard form) with k cycles. Mu is represented as an array and
#             and all standard forms of mu are outputted in array.
#
#           - miscfunctions - other functions, e.g. for formatting on terminal
#
#           - Note that we refer to 'mu' in these files, but really mean 'mu^-1'
#
# ------------------------------------------------------------------------------

# Set a g and iterate through range of v
for v in range(3,7):

    g = 0
    n = v + 2 * g - 2 # using chi(S) = v - n, and chi(S) = 2 - 2g

    if n < 3:
        continue

    # --------------------------------------------------------------------------

    num_tot_permutations = 0

    Vertice_partitions = find_vertice_partitions(v)

    # create files to store data and number of isomorphisms of mu
    i_folder = f"Isomorphisms/Genus {g}/"
    d_folder = f"Data/Genus {g}/"

    i_filename = i_folder + f"isomorphisms_n{n:02d}_v{v:02d}_g{g}.csv"
    filename   = d_folder + f"IC_n{n:02d}_v{v:02d}_g{g}.csv"
    # (IC: isomorphisms for mu are calculated and connectness is tested for)

    i = open(i_filename, "w")
    f = open(filename, "w")

    i.write(f"Partitions: {to_string(Vertice_partitions)}\n\n\n")
    f.write(f"Partitions: {to_string(Vertice_partitions)}\n\n\n")

    # --------------------------------------------------------------------------
    # to monitor progress

    print(f"\n{filename}\t", b_bold(f"n = {n}, v = {v}, g = {int(g)}\n"))
    print(b_bold(f"Vertice Partitions: {Vertice_partitions}\n"))

    # --------------------------------------------------------------------------

    for vertice_partition in Vertice_partitions:

        # assign vertices
        mu_v    = vertice_partition[0]
        sigma_v = vertice_partition[1]
        phi_v   = vertice_partition[2]

        # if phi_v < sigma_v:  # to not double count vertice partitions
        #     continue

        Mu = find_k_cycle_mu(n, mu_v)          # all mu with mu_v vertices
        Sigma = find_k_cycle_sigma(n, sigma_v) # all sigma with sigma_v Vertices

        print()
        print(line())
        print("\tn =", n, "  v =", v, "  g =", int(g), '\t',
              b_bold(f"Cycle Partition: {vertice_partition}"))

        f.write(f"Cycle Partition: {to_string(vertice_partition)}\n")
        i.write(f"Cycle Partition: {to_string(vertice_partition)}\n")

        # ----------------------------------------------------------------------

        for mu_iso in Mu: # for each pairing of mu (with isomorphisms attached)

            mu_count = 0 # track how many sigma are found (for large data sets)

            mu = mu_iso[0]
            iso = mu_iso[1]

            mu = Permutation(mu)  # convert to permutation data type

            f.write(f",mu,isomorphisms, sigma, phi, C\n,{mu}, {iso}\n")
            i.write(f",mu,isomorphisms\n,{mu}, {iso}\n")

            # to monitor progress
            print(line())
            print("  ", b_bold(f"mu {mu}, isomorphisms {iso}"))
            print(line())

            # ------------------------------------------------------------------

            valid_sigmas = []

            for sigma in Sigma:

                sigma = Permutation(sigma)
                phi = mu * sigma

                if (phi.cycles) == (phi_v):

                    valid_sigmas.append(sigma)

                    G = PermutationGroup([mu,sigma]) # test if connected
                    if G.is_transitive():
                        f.write(f",,,{sigma},{phi},1\n")
                    else:
                        f.write(f",,,{sigma},{phi},0\n")

                    mu_count += 1

                    if mu_count%1000 == 0:
                        print(mu_count)

            f.write(f"\n")
            i.write(f"\n")

            print(f"\n\tFound", len(valid_sigmas), "valid permutations\n")
            num_tot_permutations += len(valid_sigmas)

    i.close()
    f.close()

    print(line())
    print(b_bold(f"\nFound {num_tot_permutations} total valid permutations\n"))
    print()
