# Code organisation

## Parameters

- Create a file to read/write the parameters needed for the simulation.
With default values and unit (see walter?).

- Separate the definition of parameters from the code.
    * in a parameter file (resp. openalea)
    * in a test, explicitly in python
    * in visualea, in a given workflow

### Basic (main.py)
- Set the parameters directly in a test.

## Architecture (mtg_xxx.py)

Define global simulation programs of several plant architectures (various phenotypes) (brassicaea napus cv. AVISO, VIGO+) with an above and below ground part.
Each part is represented as an MTG. But may have different scale and properties for the above and below ground part.
As well as for between plants.

## CN re-allocation (aptos.py)

* Why ? : Define the nutrient re-allocation process into the CN allocation mecanism

* Brief description of the concept : 
Senescence = N remobilization of N avalaible from N source organ (cf N source-sink competition status), and lead to leaf falling 

* To who ? : researchers, students, programmers

* What is it ? : an executable script

* The code is open source and on the collaborative platform GitHub

* Contributors ? : Solen FARRA, Laurene PERTHAME, Christophe PRADAL, Frederic REES

### Algorithm

















