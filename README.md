# SOFA-Prostate

First tests using SOFA frame-work and python3 scenes

- "Data" folder contains stl and mesh files of pelvic structures generated from segmented MR images.
- test_needle_prostate.py has the SOFA scene with:
  - Prostate model
  - Syringe
  - Floor
  - The syringe moves to produce a contact/insertion into the prostate model
  - This code used the liver.py example provided at https://github.com/sofa-framework/SofaPython3/blob/master/examples/liver.py

- "Older" folder contains prevoius attempts using the STLIB.

## Build intructions
- Tested on Ubuntu 20.04
- Download SOFA source code and build it following the instructions at https://www.sofa-framework.org/community/doc/getting-started/build/macos/
- Remmember to activate the CMake option SOFA_FETCH_SOFAPYTHON3 as in the instructions at https://sofapython3.readthedocs.io/en/latest/menu/Compilation.html 



