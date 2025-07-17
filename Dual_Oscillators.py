from sympy import symbols, Eq, solve, Matrix
import numpy as np 
import Matrix_Equation_Solver as MES

def normal_angular_frequencies(m:float, k:float):
    """
    Return the angular frequencies of the normal modes of a 2 identical mass (m) coupled by spring (k) system
    """
    w=np.sqrt(k/m)
    def matrixGen(x):
        return Matrix([[2*w**2-x**2, -w**2], [-w**2, 2*w**2-x**2]])
    rawsols, realsols = MES.detFinder(matrixGen, False)
    Afreqs=[]
    for sol in realsols:
        if sol>0:
            Afreqs.append(sol)
    print("Normal Mode Angular Frequencies: ", Afreqs)
    return Afreqs

normal_angular_frequencies(1,1)