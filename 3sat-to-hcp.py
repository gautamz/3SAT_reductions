# from graphviz import Digraph
import sys
import load3sat
print(sys.version)

class HC_graph:
    def __init__(self):
        self.dimension: int = 0
        self.edge_list = []
        self.adj_list = {}
        self.vmap = {}

show_descriptive_mapping = 0

# complement of a literal
def not_var(literal):
    if literal[0] == "-":
        return literal[1:]
    else:
        return "-" + literal

# # to draw graph set as adjcency list
# def draw_graph(digraph):
#     dg = Digraph()

#     for in_node in digraph:
#         for out_nodes in digraph[in_node]:
#             dg.edge(str(in_node), str(out_nodes))

#     dg.view()

# reduce 3SAT to Hamilatonian Graph
# we will present graph as an adjacency list and edge list
def cnf_to_hamiltonian_cycle(cnf_formula):
    hcgraph = HC_graph()

    # create vertices Pi...n,j...m
    # where i -> corresponds to cnf variable, n = total number of variables
    # where j -> number of times it appears in the cnf instance, m = 2 x total number of times
    n = cnf_formula.nbvars
    for i in range(1,n+1):
        m = 2 * cnf_formula.vcount[str(i)]
        for j in range(1,m+1):
            new_vert = 'P'+str(i)+str(j)
            hcgraph.adj_list[new_vert] = []
    # for a given i, connect all Pi,j both ways, sequentially
    # connect Pi,1 to Pi+1,1 & Pi+1, m
    # connect Pi,m to Pi+1,m & Pi+1, 1
            if j == 1:
                if i != n:
                    conn1 = 'P' + str(i + 1) + str(1)
                    conn2 = 'P' + str(i + 1) + str(2 * cnf_formula.vcount[str(i + 1)])
                    hcgraph.adj_list[new_vert] = [conn1, conn2]
                conn3 = 'P' + str(i) + str(j + 1)
                hcgraph.adj_list[new_vert].append(conn3)
            elif j == m:
                conn3 = 'P' + str(i) + str(j - 1)
                hcgraph.adj_list[new_vert] = [conn3]
                if i != n:
                    conn1 = 'P' + str(i + 1) + str(2 * cnf_formula.vcount[str(i + 1)])
                    conn2 = 'P' + str(i + 1) + str(1)
                    hcgraph.adj_list[new_vert].extend([conn2, conn1])
            else:
                conn1 = 'P' + str(i) + str(j - 1)
                conn2 = 'P' + str(i) + str(j + 1)
                hcgraph.adj_list[new_vert] = [conn1, conn2]

    # create one vertex for each clause
    # connect clause vertex left to right if clause has x
    # connect clause vertex right to left if clause has -x
    clv_count = {}
    for i in cnf_formula.variables:
        clv_count[i] = 1

    cl_count = 1
    for cl in cnf_formula.clauses:
        new_vert = 'C'+str(cl_count)
        hcgraph.adj_list[new_vert] = []
        # print(cl)
        for clv in cl:
            # print(clv)
            if clv.startswith('-'):
                hcgraph.adj_list[new_vert].append('P' + clv[1] + str(clv_count[clv[1]]))
                # print(new_vert, 'P' + clv[1] + str(clv_count[clv[1]]))
                clv_count[clv[1]] = clv_count[clv[1]] + 1
                hcgraph.adj_list['P' + clv[1] + str(clv_count[clv[1]])].append(new_vert)
                # print(new_vert, 'P' + clv[1] + str(clv_count[clv[1]]))
                clv_count[clv[1]] = clv_count[clv[1]] + 1
            else:
                hcgraph.adj_list['P' + clv + str(clv_count[clv])].append(new_vert)
                # print(new_vert, 'P' + clv + str(clv_count[clv]))
                clv_count[clv] = clv_count[clv] + 1
                hcgraph.adj_list[new_vert].append('P' + clv + str(clv_count[clv]))
                # print(new_vert, 'P' + clv + str(clv_count[clv]))
                clv_count[clv] = clv_count[clv] + 1

        cl_count = cl_count + 1

    # create vertices s (source) and t (targert)
    # connect t to s
    # connect s to P1,1 and P1,m
    # connect Pn,1 and Pn,m to t
    hcgraph.adj_list['t'] = ['s']
    hcgraph.adj_list['s'] = ['P11', 'P1' + str(2 * cnf_formula.vcount['1'])]
    hcgraph.adj_list['P' + str(n) + '1'].append('t')
    hcgraph.adj_list['P' + str(n) + str(2 * cnf_formula.vcount[str(n)])].append('t')

    # create edge_list
    num_verts = 0
    oldkeys = []
    for key in hcgraph.adj_list.keys():
        num_verts = num_verts + 1
        hcgraph.vmap[key] = num_verts
        oldkeys.append(key)

    hcgraph.dimension = num_verts

    if show_descriptive_mapping == 1:
        for key in hcgraph.adj_list:
            print(key, '=>', hcgraph.adj_list[key])
        print()
        for key in hcgraph.vmap:
            print(key, '=>', hcgraph.vmap[key])
        print()

    for key in oldkeys:
        tmpl = []
        for item in hcgraph.adj_list[key]:
            tmpl.append(hcgraph.vmap[item])
        newkey = hcgraph.vmap[key]
        hcgraph.adj_list[newkey] = hcgraph.adj_list.pop(key)
        hcgraph.adj_list[newkey] = tmpl

    for key in hcgraph.adj_list:
        for val in hcgraph.adj_list[key]:
            hcgraph.edge_list.append([key,val])

    return hcgraph

def write_out_graph(hcgraph, filename):
    file_object = open(filename, 'w')
    file_object.write('NAME : '+filename)
    file_object.write('\nTYPE : HCP_DIRECTED')
    file_object.write('\nDIMENSION : ' + str(hcgraph.dimension))
    file_object.write('\nEDGE_DATA_FORMAT : EDGE_LIST')
    file_object.write('\nEDGE_DATA_SECTION')
    for edge in hcgraph.edge_list:
        file_object.write('\n'+str(edge[0])+' '+str(edge[1]))
    file_object.write('\n-1')
    file_object.write('\nEOF')
    file_object.close()
    return 0

def run_prog(filename="test.dimacs"):
    formula = load3sat.read_dimacs_file(filename)
    verts = list(formula.variables)
    verts.sort()

    # npcl = np.array(formula.clauses)
    print("cnf => ", formula.nbvars, 'variables and', formula.nbclauses, 'clauses')
    print("variables =>", verts)
    print("var counts => ", formula.vcount)
    print("loaded clauses => \n", formula.clauses)
    print()
    hg = cnf_to_hamiltonian_cycle(formula)
    for key in hg.adj_list:
        print(key, '=>', hg.adj_list[key])
    # for key in hg.vmap:
    #     print(key, '=>', hg.vmap[key])
    # print(hg.edge_list)
    # print(hg.dimension)

    write_out_graph(hg, 'testo.hcp')
    return 0

# run_prog()
run_prog("testg.dimacs")
# run_prog("test7.dimacs")
# run_prog("test8.dimacs")
# run_prog("unsat5.dimacs")
# run_prog("unsat9.dimacs")
# run_prog("unsat10.dimacs")
# run_prog("5.dimacs")
