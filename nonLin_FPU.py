import numpy as np
from sympy import symbols, Eq, solve, Matrix
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os 
import imageio.v2 as imageio



#Assume k=m=1

def systemGen(N:int,alpha:float,nonLin:int=2):
    """
    Generate the equations of motion for a chain of N+1 unit masses coupled by springs of unit strength. The system is perturbed by the FPUT factor alpha. 
    The nonliniearity exponent is governed by th eparameter nonLin. The two values of interest are nonLin = {2,3} , which correspond to the quadratic and cubic FPU problem respectively
    y[0], y[2], y[4], ... => for any even j, y[j] is the momenta p for the j/2th particle (includes 0th particle)
    y[1], y[3], y[5], ... => for any odd j, y[j] is the position x for the (j-1)/2th particle (includes 0th particle)
    """
    def generator(t,y):
        eqn=[
            (y[3]-2*y[1])+alpha* ((y[3]-y[1])**nonLin -(y[1])**nonLin) ,
            y[0]
        ]
        i=3 #i=3 IS ODD (first odd after i=1) => access particle 1 position => i leads to position index => to access momentum use i-1
        while i<2*N:
            delta=(y[i+2]-y[i])**nonLin-(y[i]-y[i-2])**nonLin
            eqn.append((y[i+2]+y[i-2]-2*y[i])+alpha*delta) 
            eqn.append(y[i-1])
            i+=2
        eqn.append((y[i-2]-2*y[i])+alpha*(y[i]**nonLin - (y[i]-y[i-2])**nonLin))        
        eqn.append(y[i-1])
        return np.array(eqn)
    return generator

def initialise(N):
    """
    Initialise the state vector with custom initial conditions. The state vector has the following format:
    initConds=[p0, x0, p1, x1, ..., pN, xN]
    Containing the states for N+1 unit masses (Since index starts from 0)
    """
    initConds=[]
    i=0 
    while i<2*(N):
        print(63*"~")
        initConds.append(float(input("Input initial momentum of mass "+str(int(i/2+1))+": "))) #i+1 is shown because normal people dont count from 0
        initConds.append(float(input("Input initial displacement of mass "+str(int(i/2+1))+": ")))
        i+=2
    return initConds 

def hamiltonian(N, alpha, initConds, tMax, iters):
    """
    Compute energies for each mass. The nonlinear energies are neglected, as per Fermi, Pasta and Ulman's original paper.  
    """
    times, momenta, displacements = solverFunc(N, alpha, initConds, tMax, iters)
    energies=[]
    i=0 
    while i<=N:
        E0=0.5*momenta[i][0]**2+0.5 * ( (displacements[i][1]-displacements[i][0])**2+(displacements[i][0])**2 )
        localEnergy=[E0]
        j=1 
        while j<len(momenta[i])-1:
            momentum=momenta[i][j]
            displacement=displacements[i][j]
            E=0.5*(momentum)**2+0.5 * ( (displacements[i][j+1]-displacement)**2+(displacement-displacements[i][j-1])**2 )
            localEnergy.append(E)
            j+=1
        momentum=momenta[i][j]
        displacement=displacements[i][j]
        EN=0.5*(momentum)**2+0.5 * ( (displacement)**2+(displacement-displacements[i][j-1])**2 )
        localEnergy.append(EN)
        energies.append(localEnergy)
        i+=1 
    return times, energies

def plotHamiltonian(N, alpha, initConds, tMax, iters):
    """
    Plot energies for each mass. The nonlinear energies are neglected, as per Fermi, Pasta and Ulman's original paper.  
    """
#    print("Solver running...")
    times, energies= hamiltonian(N,alpha,initConds, tMax, iters)
    target=0
    while target<len(energies):
        targetEnergies=energies[target]
        plt.plot(times,targetEnergies,label="Mass "+str(target+1))
        target+=1
    plt.legend(loc='upper right',  bbox_to_anchor=(1.129, 1))
    plt.xlabel("Time")
    plt.ylabel("Energy")
    plt.show()
    return None

def automaticInitialiser(N, p, x):
    """
    Initialise all N+1 masses (indexed from n=0 to n=N) with initial momentum p and initial position x
    """
    i=0 
    initConds=[]
    while i<=N:
        initConds.append(p)
        initConds.append(x)
        i+=1 
    return initConds

def terminalWizard():
    """
    Execute the solver in terminal. Custom conditions are optional.
    """
    print("\n\n=== Fermi-Pasta-Ulam Problem Numerical Solver ===")
    print(50*"-")
    preset=int(input("Enter 0 to view a preset or enter any other number to continue: "))
    if preset==0:
        N=3
        initConds=[0,1.08,0,0.9,0,1.05,0,1.03]
        alpha=1/6
        maxT=60
        tSpan=(0,maxT)
        nonLin=2
        totalSteps=5000
        tRange=np.linspace(0,maxT,totalSteps)
        spacing=1.2
    else:
        N=int(input("Enter the number of masses: "))-1
        auto=int(input("Enter 1 to initialise uniform initial conditions. Enter any other number key to continue:"))
        if auto==1:
            print(50*"~")
            p=float(input("Enter the initial momentum for all the masses: "))
            x=float(input("Enter the initial displacement for all the masses: "))
            initConds=automaticInitialiser(N,p,x)
        else:
            initConds=initialise(N+1)
        print(50*"-")
        print("Simulation Settings: ")
        nonLin=int(input("Enter the nonliniearity exponent (2 or 3): "))
        alpha=float(input("Enter the FPUT perturbation constant: "))
        maxT=float(input("Enter maximum simulation time: "))
        totalSteps=int(input("Enter the total timesteps allowed: "))
        spacing=float(input("Enter the spacing between the masses. Enter 0 to plot their displacements from equillibrium: "))
        tSpan=(0,maxT)
        tRange=np.linspace(0,maxT,totalSteps)
    print("Solver running...")
    sol=solve_ivp(systemGen(N,alpha, nonLin),tSpan, initConds, t_eval=tRange, method='BDF')
    #Suppose each mass is spaced a distance of variable "spacing" apart. Need convert displacements into positions.
    #plt.plot(sol.t, sol.y[0], color="blue") #momentum
    #EVEN THOUGH THE OUTPUT COUNTS FROM 1 FOR USABILITY, REMEMBER THE WHOLE SCRIPT STILL COUNTS FROM 0 
    i=1
    plt.figure(figsize=(12, 6))
    while i<=N*2+1:
        plt.plot(sol.t, sol.y[i]+((i-1)/2)*spacing,label="Mass "+str(int(i/2+1)))
     #   plt.plot(sol.t, (i-1)/2 * np.ones_like(sol.t), label=f'Constant y = {(i-1)/2}', linestyle=":")
        i+=2
    print("Solving complete. See output graph for results. ")
    if nonLin==3:
         plt.title(r"Cubic Fermi-Pasta-Ulam Problem for $\beta$="+str(round(alpha*100)/100)+ ", N="+str(N)+" ("+str(N+1)+" masses)")
    else:
        plt.title(r"Quadratic Fermi-Pasta-Ulam Problem for $\alpha$="+str(round(alpha*100)/100)+ ", N="+str(N)+" ("+str(N+1)+" masses)")
    plt.legend(loc='upper right',  bbox_to_anchor=(1.129, 1))
    plt.xlabel("Time")
    plt.ylabel("Position")
    plt.show()
    return sol


def terminalEnergy():
    """
    Execute the solver in terminal. Custom conditions are optional.
    """
    print("\n\n=== Fermi-Pasta-Ulam Problem Numerical Solver ===")
    print(50*"-")
    preset=int(input("Enter 0 to view a preset or enter any other number to continue: "))
    if preset==0:
        N=3
        initConds=[0,1.08,0,0.9,0,1.05,0,1.03]
        alpha=1/6
        maxT=60
        tSpan=(0,maxT)
        nonLin=2
        totalSteps=5000
        tRange=np.linspace(0,maxT,totalSteps)
        spacing=1.2
    else:
        N=int(input("Enter the number of masses: "))-1
        auto=int(input("Enter 1 to initialise uniform initial conditions. Enter any other number key to continue:"))
        if auto==1:
            print(50*"~")
            p=float(input("Enter the initial momentum for all the masses: "))
            x=float(input("Enter the initial displacement for all the masses: "))
            initConds=automaticInitialiser(N,p,x)
        else:
            initConds=initialise(N+1)
        print(50*"-")
        print("Simulation Settings: ")
        nonLin=int(input("Enter the nonliniearity exponent (2 or 3): "))
        alpha=float(input("Enter the FPUT perturbation constant: "))
        maxT=float(input("Enter maximum simulation time: "))
        totalSteps=int(input("Enter the total timesteps allowed: "))
        tSpan=(0,maxT)
        tRange=np.linspace(0,maxT,totalSteps)
    print("Solver running...")
    print("Solving complete. See output plot for results.")
    return plotHamiltonian(N,alpha,initConds,maxT,totalSteps)

def solverFunc(N, alpha, initConds, tMax, iters, nonLin=2):
    """
    For use in other modules. Returns the solutions of the equations of motion in the following form

    times, momenta, displacements = [0, t1, t2, ... tMax], [ [p0(0), p0(t1),...,p0(tMax)], [p1(0), p1(t1),...,p1(tMax)] ,..., [pN(0), pN(t1),...,pN(tMax)] ]  , [ [x0(0), x0(t1),...,x0(tMax)], [x1(0), x1(t1),...,x1(tMax)] ,..., [xN(0), xN(t1),...,xN(tMax)] ]
    """
    tRange=np.linspace(0,tMax,iters)
    system=systemGen(N,alpha, nonLin)
    sol=solve_ivp(system, (0, tMax), initConds, t_eval=tRange, method="BDF")
    times=sol.t
    momenta=[]
    displacements=[]
    i=0 
    while i<len(sol.y):
        if i%2==0:
            momenta.append(sol.y[i])
        else:
            displacements.append(sol.y[i])
        i+=1
    return times, momenta, displacements


def exciteMode(N, k):
    """
    Generate inital conditions that excites mode k for a FPU chain of length N+1 (index from 0 to N => N+1 particles)
    Recall even entries are momenta and odd entries are displacements
    Using the initial conditions generated by this, the spectral plot should return a large amplitude of oscillation for mode k and small amplitudes for everything else
    """
    initConds=[]
    i=0 
    while i<2*(N+1):
        initConds.append(0)
        initConds.append(np.sqrt(2/(N+1))*np.sin((np.pi*k*(i//2))/(N+1)))
        i+=2 
    return initConds


def videoPlotter(N, alpha, initConds, tMax, iters, nonLin=2, fpsCustom=100):
    times, momenta, displacements = solverFunc(N, alpha, initConds, tMax, iters, nonLin)
    i=0 
    print("plotting...")
    os.makedirs("frames", exist_ok=True)
    displacements=np.array(displacements)
    while i<iters:
        j=0 
        print(30*"\n", "plotting instance ", str(i), "out of ", str(iters))
        plt.ylim(np.min(displacements), np.max(displacements))
        jList=[]
        disps=[]
        while j<N:
            plt.plot(j, displacements[j][i], ".", color="gray")
            jList.append(j)
            disps.append(displacements[j][i])
            j+=1       
        plt.plot(jList ,disps, color="black")  
        frame_path = f"frames/frame_{i:04d}.png"
        plt.savefig(frame_path)
        plt.close()
        i+=1
    k=0 
    output_path ="/Users/kanlachlan/Documents/VS_Code/Personal Projects/FPU Problem/1D_Sim_Output.mp4"
    with imageio.get_writer(output_path, fps=fpsCustom) as writer:
        while k<iters:
            print(30*"\n", "Frames constructed. Assembling video...")
            frame_path = f"frames/frame_{k:04d}.png"
            image = imageio.imread(frame_path)
            writer.append_data(image)
            k+=1
    print(30*"\n", "Frames constructed. Assembling video...")
    print(" Video saved as 2D_Sim_Output.mp4 with path ", output_path)

#videoPlotter(100, 0.25, automaticInitialiser(100,0,1), 200, 1000, 2, 50)
videoPlotter(100, 0.5, exciteMode(100,2), 500, 1000, 50)
#plotHamiltonian(3, 0.25, [0,1.08,0,0.9,0,1.05,0,1.03], 10, 500000)
#plotHamiltonian(32, 0.25, automaticInitialiser(32,0,1), 100, 100000)
#print(hamiltonian(3, 0.25, [0,1.08,0,0.9,0,1.05,0,1.03], 30, 10000))
#terminalWizard()

