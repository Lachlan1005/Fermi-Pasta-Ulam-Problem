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
    print("4 -> Shannon Entropy")
    print("\n--- Linear Oscillations ---")
    print ("5 -> Normal Modal Angular Frequencies\n")
    print("\n--- Wizard Commands---")
    print("q -> Exit program")
    typer=input("\nYour Input: ")
    if typer=="q":
        print("Stopping FPU solver...")
        exit("Solver stopped") 
    try:
        typer=int(typer)
    except ValueError:
        print(typer, " is not a valid command. See main menu for valid commands.")
        input("Press any key to try again: ")
        wizardTool()
    if typer==0:
        fpu.terminalWizard()
    elif typer==1:
        fpu.terminalEnergy()
    elif typer==2:
        ms.terminalWizard()
    elif typer==3:
        ms.energyWizard()
    elif typer==4:
        ms.entropyWizard()
    elif typer==5:
        oc.terminalWizard()
    else:
        print(typer, " is not a valid command. See main menu for valid commands.")
        input("Press any key to try again: ")
        wizardTool()
    print("\n\n")
    return wizardTool()

wizardTool()