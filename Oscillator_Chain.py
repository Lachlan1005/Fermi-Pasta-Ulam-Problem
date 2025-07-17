from sympy import symbols, Eq, solve, Matrix
import numpy as np 
import Matrix_Equation_Solver as MES
import matplotlib.pyplot as plt

def matrixRepr(x:float, N:int):
    """
    Generate a matrix M such that Mv=0 where v is a vector of dimension N with its nth component representing the coefficient of the equation of motion of each mass. 
    We assume a solution of x_n(t)=A_n\exp(i\alpha t) where A_n is the unique coefficient for every mass
    """
    matrix=[]
    i=0 
    while i<N:
       # print(i)
        row=[]
        j=0
        while j<N:
        #    print(j)
            if j==i:
                row.append(x**2-1)
            elif abs(abs(j-i)-1)<0.1:
                row.append(-1)
            else: 
                row.append(0)
            j+=1 
        matrix.append(row)
        i+=1 
    return matrix 


def normal_angular_frequencies(N:int, m:float, k:float):
    """
    Return the angular frequencies of the normal modes of a 2 identical mass (m) coupled by spring (k) system
    """
    w=np.sqrt(k/m)
    def matrixGen(x):
        mat=matrixRepr(x,N)
        return (w**2)*Matrix(matrixRepr(x,N))
    rawsols, realsols = MES.detFinder(matrixGen, False)
    Afreqs=[]
    for sol in realsols:
        if sol>0:
            Afreqs.append(sol*w)
    print("Normal Mode Angular Frequencies: ", Afreqs)
    return Afreqs

def angularPlots(minN:int, maxN:int):
    """
    Plot the nornmal mode angular frequencies of a chain of N masses connected by springs from N=minN to N=maxN
    """
    while minN<=maxN:
        freqs=normal_angular_frequencies(minN, 1,1)
        for freq in freqs:
            #plt.plot(minN, freq, "o",color="black")
            plt.plot(minN, len(freqs), "o",color="black")
        minN+=1 
    plt.show()
    return None

def terminalWizard():
    print("=== Linear Normal Modal Angular Frequencies ===")
    N=int(input("Enter the number of masses: "))
    m=float(input("Enter the mass of the masses: "))
    k=float(input("Enter the force constant of the springs: "))
    return normal_angular_frequencies(N, m, k )
#angularPlots(1,8)