import nonLin_FPU as fpu 
import Oscillator_Chain as oc 
import modeSpectra as ms 

def wizardTool():
    print("=== Fermi-Pasta-Ulam Solver ===")
    print("\nMain Menu")
    print("--- Nonlinear Oscillations ---")
    print("0 -> Equations of Motion")
    print("1 -> Energy Evolution")
    print("2 -> Modal Spectra")
    print("3 -> Spectral Energy Evolution")
    print("\n--- Linear Oscillations ---")
    print ("4 -> Normal Modal Angular Frequencies\n")
    typer=int(input("Your Input: "))
    if typer==0:
        return fpu.terminalWizard()
    elif typer==1:
        return fpu.terminalEnergy()
    elif typer==2:
        return ms.terminalWizard()
    elif typer==3:
        return ms.energyWizard()
    elif typer==4:
        return oc.terminalWizard()
    else:
        print(typer, " is not a valid command. See main menu for valid commands.")
    
wizardTool()