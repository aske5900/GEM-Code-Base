# GEM-Code-Base
Code for the generation and analysis of valid triangulations, and previously collected data.

The code in this repository was made in Semester 2 2021 as part of a project for SCDL1991 at 
the University of Sydney. The code was designed to generate all triangulations with a given
number of vertices, for a given genus surface. We have provided these code files and the data
generated (note: IC_n09_v11_g0.csv is missing as it was too large to upload).

"data_generation.py" is the main file and uses functions from partition_mu, partition_vertices,
permutations_sigma and miscfunctions. Lists of valid permutations sorted by vertex partition
and standard forms of mu are saved in csv files in the "Data" folder sorted by genus. Lists of 
isomorphisms of mu are also saved in csv files in "Isomorphisms" for covienience. Csv files 
containing already generated data have been provided in these folders.

"single_file_analysis.py" sorts through the csv files of generated data to summarise the total
number of valid triangulations found. Data from this is saved in additional csv files in the 
"Analysis" folders.

Authors: Chantal Kander (SID: 510290197) and Amelie Skelton (SID: 510415217).
