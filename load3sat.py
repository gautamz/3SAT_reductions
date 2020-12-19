import sys
print(sys.version)

# class/object format to store CNF formula data
class CNFformula:
    def __init__(self, nbv=0, nbc=0, cl=None):
        self.nbvars: int = nbv       # number of variables
        self.nbclauses: int = nbc    # number of clauses
        self.clauses = []            # list of the clauses, each clause is a set, consider using collections.dequeue here.
        self.variables = set()       # the variables
        self.vcount = {}             # count of each variable

# read CNF formula from a file in dimacs format
def read_dimacs_file(filename):
    content = []
    with open(filename) as file_object:
        for line in file_object:
            content.append(line.strip())

    cnf_formula = CNFformula()

    for rec in content:
        rec = rec.strip()

        # split line into words
        substrs = rec.split()

        # check if cnf and record details if cnf
        if rec[0].startswith("p"):
            if substrs[1] != "cnf":
                print("Not a CNF formula")
                break
            else:
                # record the details of the cnf instance
                cnf_formula.nbvars = int(substrs[2])
                cnf_formula.nbclauses = int(substrs[3])

        # for cnf entries record has to start with a number or a minus sign
        elif (rec[0].isdigit()) or (rec[0].startswith("-")):
            flen = len(substrs)-1
            tmpcl = substrs[:flen]
            tmpcl.sort()
            cnf_formula.clauses.append(tmpcl)

            # make a list of all variables and prep the map to store variable counts
            for i in range(flen):
                tmpvr = substrs[i]
                if tmpvr.startswith('-'):
                    tmpvr = tmpvr[1]
                cnf_formula.vcount[tmpvr] = 0
                cnf_formula.variables.add(tmpvr)

    # sort the list of clauses based on number of terms in the clause
    cnf_formula.clauses.sort(key=lambda x: (x[0], x[1], x[2]))

    # get the count of each variable (incl its negation) in the cnf instance
    for tmpcl in cnf_formula.clauses:
        for tmpvr in tmpcl:
            if tmpvr.startswith('-'):
                tmpvr = tmpvr[1]
            cnf_formula.vcount[tmpvr] = cnf_formula.vcount[tmpvr] + 1

    file_object.close()

    return cnf_formula