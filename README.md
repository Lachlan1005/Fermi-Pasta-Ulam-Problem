# Fermi-Pasta-Ulam Problem

This project provides the tools to solve the problem proposed by Fermi, Pasta, and Ulam (FPU) in their paper *"Studies of Non Linear Dynamics"* published in 1955. This includes the unperturbed case, as well as the 
FPU - $\alpha$ and FPU - $\beta$ cases.

## Unperturbed Case

The FPU problem reduces to a simple 1D linear chain of masses in the unperturbed case. The normal modes are directly solved for in **Oscillator_Chain.py** for arbitrary mass and force constant.

## Perturbed Case

The main focus of this project. The parameter $\gamma$ can be set to 2 or 3 to solve for the quadratic or cubic perturbation cases respectively. The energies and states are solved for in **nonLin_FPU.py**, and the modal spectra are solved for in **modeSpectra.py**.

## Instructions and Notes

To use the solver, run **Simulation_Wizard.py** in the command line. Mac users may need to use `python3` instead of `python` when calling the function, as shown below:

```
python3 Simulation_Wizard.py
```

After running the command, follow the prompts shown on screen. To view the fully rendered notes and some saved results, visit the **"FPU Notes"** folder and open **FPU_Notes.pdf**.

## Dependencies

There are multiple dependencies that need to be installed before running the program. They are as follows:

- scipy  
- matplotlib  
- numpy  
- sympy

Without these dependencies, the code cannot run.
