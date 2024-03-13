Representative input and output files are presented. 
Both AlFeFe and FeFeFe have the geometry, converged ROHF orbitals and LASSCF orbitals for each studied active space.
Sample input file and correspondning output file for performing LASSI calculations is provided. 

Dependencies
PYSCF https://github.com/pyscf/pyscf commit: 53511781bd27f294a4ae53477acabf94fb9e930f
MRH https://github.com/MatthewRHermes/mrh commit: ae2dfda23bf2c43f685234f5bfc8d53b5b33a7db

LASSI calculation has two parameters (r) - number of charge hops from one fragment to another which is done by adding the line 
from mrh.lassi import states
for _ in range(r):
	las=states.all_single_excitations(las)

, and (q) - number of local excited states which is done by
ncsf=las.get_ugg().ncsf_sub
lroots=np.minimum(q,ncsf)
las.lasci()
las.lasci(lroots=lroots)
e_roots,si=las.lassi(opt=1)


