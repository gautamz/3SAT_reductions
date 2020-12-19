# 3SAT Reductions
This repo is meant to host code for reductions from 3SAT to Hamiltonian Cycle, 3 Dimensional Matching, Set Cover, 3-Coloring, Subset Sum and Subset Product.
The code is not yet focussed on performance but doing the correct reductions, in line with the known algorithms.

Right now the repo has -
1) A file to load a 3SAT/3CNF instance stored in a .dimacs file
2) Code for reducing 3CNF to Hamiltonian Cycle

# TODO
1) 3SAT > 3 Dimensional Matching
2) 3SAT > Set Cover
3) 3SAT > Exact 3 Cover
4) 3SAT > Subset Product
5) 3SAT > 3 Coloring
6) 3SAT > Subset Sum
7) Plotting the output of the reductions graphically, where possible
8) Improve code performance

STRETCH) Write the reductions in Go, Lisp/Clojure and Zig.
