import numpy as np
import sys
from pyscf import gto, scf, tools,lib, mcscf
from pyscf.mcscf import avas,project_init_guess
from pyscf import mcscf
from mrh.my_pyscf.tools import molden
from mrh.my_pyscf.mcscf import lasscf_async as asyn
mol_name='Al_Fe_Fe.xyz' # Al-Fe-Fe MOF node
basis={'C': 'cc-pvdz','H': 'cc-pvdz','O': 'cc-pvtz','Al': 'cc-pvtz','Fe': 'cc-pvtz'}
r=0;n=5
output='r'+str(r)+'_n'+str(n)+'.log'
mol=gto.M(atom=mol_name,verbose=4,spin=9,charge=0,basis=basis, output=output) #spin = 2S
mf=scf.RHF(mol)
mf=mf.density_fit()
mf.max_cycle=1
mf.kernel()
mf.mo_coeff=np.load('hf.npy')

mo_guess=np.load('las_10_11.npy')
las=asyn.LASSCF(mf,(5,5),((1,5),(5,0)),spin_sub=(5,6),verbose=4) # spin is 2S+1
las.set_fragments_(([17],[19]),mo_guess)
las.mo_coeff=mo_guess
from mrh.my_pyscf.lassi import states
las=states.spin_shuffle(las)
for _ in range(r):
	las=states.all_single_excitations(las)
ncsf=las.get_ugg().ncsf_sub
lroots=np.minimum(n,ncsf)
las.lasci()
las.lasci(lroots=lroots)
e_roots, si= las.lassi(opt=1)
