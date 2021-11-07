import csv
from miscfunctions import *

# ------------------------------------------------------------------------------
# Enumerate through csv files of valid permutations to determine the number
# of valid sigma for each mu, vertex partition and (v,g). Also count number of
# connected triangulations. Save data (with isomorphisms of mu) in a csv file.
# 'C' denotes connected triangulations.
# ------------------------------------------------------------------------------

for v in range(3,7):

    g = 0
    n = v + 2 * g - 2

    if n < 3:
        continue

    # --------------------------------------------------------------------------

    d_folder = f"Data/Genus {g}/"
    a_folder = f"Analysis/Genus {g}/"

    filename = d_folder + f"IC_n{n:02d}_v{v:02d}_g{g}.csv"
    freqname = a_folder + f"IC_n{n:02d}_v{v:02d}_g{g}_freq.csv"

    d = open(filename, 'r')
    f = open(freqname, 'w')

    reader = csv.reader(d)
    data   = list(reader)

    # --------------------------------------------------------------------------

    f.write(f"{to_string(data[0])}\n\n\n")
    f.write("Cycle Partition, Mu, # Iso, # Sigmas, C, # Tot Sigmas, C, # All Paritions, C, Percent Connected\n")

    print(line())
    print(b_bold(filename))
    print(line())

    # --------------------------------------------------------------------------
    # variable set-up for counting connected/non-connected:

    mu_tot,        c_mu_tot        = 0, 0
    partition_tot, c_partition_tot = 0, 0
    tot_tot,       c_tot_tot       = 0, 0

    cycle_partition=''
    mu=''

    data_idx = 0

    # --------------------------------------------------------------------------
    # analysis:

    data = data[3:] # remove first three lines

    for dataline in data:

        # print(dataline)

        data_idx += 1
        if data_idx%1000 == 0:  # keep track of proccess
            print(data_idx)

        if len(dataline) == 0:
            continue

        elif data_idx == 1:
            cycle_partition = dataline[0][17:] # store partition
            in_partition = True

        elif len(dataline[0]) != 0 and data_idx != 1: # found partition

            "Calculate previous mu totals"
            f.write(f"{cycle_partition}, {mu}, {mu_iso}, {mu_tot}, {c_mu_tot}\n")

            "Calculate partition totals"
            f.write(f"{cycle_partition},,,,,{partition_tot}, {c_partition_tot}\n\n")

            in_partition = False
            mu_tot = 0
            c_mu_tot = 0

            partition_tot = 0
            c_partition_tot = 0

            # store new partition
            cycle_partition = dataline[0][17:] # store partition
            in_partition = True

        elif dataline == ['', 'mu', 'isomorphisms', ' sigma', ' phi', ' C']:
            continue

        elif len(dataline[1]) != 0: # found mu

            if partition_tot != 0: # i.e. this is not the first mu
                "Write previous mu totals and reset mu total"
                f.write(f"{cycle_partition}, {mu}, {mu_iso}, {mu_tot}, {c_mu_tot}\n")

                mu_tot = 0
                c_mu_tot = 0

            "Assign new mu and isomorphisms"
            mu = dataline[1]
            mu_iso = dataline[2]

        elif len(dataline[3]) != 0: # find sigma and phi

            "Add to sigma and determine whether connected"
            mu_tot += 1
            partition_tot += 1
            tot_tot += 1

            if dataline[5] == '1':
                c_mu_tot += 1
                c_partition_tot += 1
                c_tot_tot += 1

    f.write(f"{cycle_partition}, {mu}, {mu_iso}, {mu_tot}, {c_mu_tot}\n")
    f.write(f"{cycle_partition},,,,,{partition_tot}, {c_partition_tot}\n\n")
    "Calculate overall totals and percent connected"
    f.write(f",,,,,,,{tot_tot},{c_tot_tot},{c_tot_tot*100/tot_tot}\n")

    d.close()
    f.close()
