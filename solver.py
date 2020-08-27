from ortools.sat.python import cp_model
#install ortools by writting 'pip3 install ortools' in a terminal

def solve(grid):    #grid must be a tuple of tuples
    n=len(grid)
    assert(not(n%2))
    model=cp_model.CpModel()
    
    #Variables
    lines=[model.NewIntVar(sum([pow(2,i) for i in range(n//2)]),sum([pow(2,i) for i in range(n//2+1,n)]),"line"+str(j)) for j in range(n)]
    columns=[model.NewIntVar(sum([pow(2,i) for i in range(n//2)]),sum([pow(2,i) for i in range(n//2+1,n)]),"column"+str(j)) for j in range(n)]
    binaryGrid=[[model.NewBoolVar("cell"+str(i)+"_"+str(j)) for i in range(n)] for j in range(n)]
    
    #Constraint
    #connection to the grid
    for i in range(n):
        for j in range(n):
            if grid[i][j]==1:
                model.Add(binaryGrid[i][j]==1)
            elif grid[i][j]==0:
                model.Add(binaryGrid[i][j]==0)
    #AllDifferent
    model.AddAllDifferent(lines)
    model.AddAllDifferent(columns)
    #Int to boolean var
    for i in range(n):
        model.Add(cp_model.LinearExpr.ScalProd(binaryGrid[i],[2**(n-1-j) for j in range(n)])==lines[i])
        model.Add(cp_model.LinearExpr.ScalProd([binaryGrid[j][i] for j in range(n)],[2**(n-1-j) for j in range(n)])==columns[i])
    #Balance in each line
    for i in range(n):
        model.Add(cp_model.LinearExpr.Sum(binaryGrid[i])==n//2)
        model.Add(cp_model.LinearExpr.Sum([binaryGrid[j][i] for j in range(n)])==n//2)
    #No triplets
    for i in range(n):
        for j in range(n-2):
            model.AddLinearConstraint(binaryGrid[i][j]+binaryGrid[i][j+1]+binaryGrid[i][j+2],1,2)
            model.AddLinearConstraint(binaryGrid[j][i]+binaryGrid[j+1][i]+binaryGrid[j+2][i],1,2)
    
    #Solve
    solver=cp_model.CpSolver()
    status=solver.Solve(model)
    if status==cp_model.FEASIBLE:
        return [intToBinaryTuple(solver.Value(lines[i])) for i in range(n)]
    else:
        return ()

def intToBinaryTuple(integer,size=0):
    binaryList=[]
    n=0
    while integer:
        binaryList.append(integer%2)
        integer=integer//2
        n+=1
    for i in range(n,size):
        binaryList.append(0)
    binaryList.reverse()
    return tuple(binaryList)

example=((-1,1,-1,-1,-1,0),(-1,-1,-1,1,-1,-1),(-1,1,-1,-1,-1,-1),(-1,-1,-1,-1,1,-1),(-1,-1,0,-1,1,-1),(0,-1,0,-1,-1,-1))
print(example)
print(solve(example))
