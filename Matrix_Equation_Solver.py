from sympy import symbols, Eq, solve, Matrix
import numpy as np 

def matrixGen(x):
    """
    Generates a matrix with the input variable x compatible for use in the solver
    """
    return Matrix([
       [x-1, 2, 3, 5, 8],
       [0, 3-x, 9, 9, 6] ,    
       [9, 6, 8+x, 10, 3],
       [3, 12, 0, 9-x, 1],
       [1, 8, 16, 21, x+10]
    ])

def detFinder(matrix:callable, verbosity:bool=True):
    """
    Solves an equation of the form det(M)=0 where M is a matrix with its terms consisting of some variable x. 
    Example: M=[[1-x, 0], [0, 1+x]] would result in an output of x=[1,-1] since that results in the determinant being 
    """
    print("Solver running...")
    x=symbols("x")
    M=matrix(x)
    det=M.det()
    sols=solve(Eq(det,0), x)
    rawSols=[]
    realSols=[]
    for sol in sols:
        num=sol.evalf()
        rawSols.append(num)
        if abs(num.as_real_imag()[1])<10e-15:
            realSols.append(num.as_real_imag()[0])
    if verbosity:
        print("\n===Solutions===\n\nCOMPLEX: x=", rawSols, "leads to a determinant of 0\n")
        print("REAL: x=", realSols, "leads to a determinant of 0\n\n")
    return rawSols, realSols

#detFinder() 
