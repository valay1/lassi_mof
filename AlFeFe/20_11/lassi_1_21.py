import numpy as np
import sys
from pyscf import gto, scf, tools,lib, mcscf
from pyscf.mcscf import avas,project_init_guess
from pyscf import mcscf
from mrh.my_pyscf.tools import molden
from mrh.my_pyscf.mcscf import lasscf_async as asyn
mol_name='Al_Fe_Fe.xyz' # Al-Fe-Fe MOF node
basis={'C': 'cc-pvdz','H': 'cc-pvdz','O': 'cc-pvtz','Al': 'cc-pvtz','Fe': 'cc-pvtz'}
n=21
output='r1_n'+str(n)+'.log'
mol=gto.M(atom=mol_name,verbose=4,spin=9,charge=0,basis=basis, output=output) #spin = 2S
mf=scf.RHF(mol)
mf.init_guess='atom'
mf=mf.density_fit()
mf.max_cycle=1
mf.kernel()
mf.mo_coeff=np.load('hf.npy')
#np.save('hf',mf.mo_coeff)
#ncas,nelecas,guess_mo_coeff=avas.kernel(mf,['Fe 3d', 'Fe 4d'],minao=mol.basis, openshell_option=3)
#mc_test = mcscf.CASCI (mf, ncas, nelecas)
#tools.molden.from_mo(mol,'avas.molden',guess_mo_coeff[:,mc_test.ncore:][:,:ncas])
#final_list=[5,6,8,9,10,11,12,13,14]#,15,16,17,18,19,20,21,22,23,24,25]+mc_test.ncore

mo_guess=np.load('las_20_11.npy')
las=asyn.LASSCF(mf,(10,10),((1,5),(5,0)),spin_sub=(5,6),verbose=4) # spin is 2S+1
las.set_fragments_(([17],[19]),mo_guess)
las.mo_coeff=mo_guess
from mrh.my_pyscf.lassi import states
las=states.spin_shuffle(las)
#for _ in range(i):
las=states.all_single_excitations(las)
ncsf=las.get_ugg().ncsf_sub
lroots=np.minimum(n,ncsf)
las.lasci()
las.lasci(lroots=lroots)
e_roots, si= las.lassi(opt=1)
from mrh.my_pyscf.lassi.sitools import analyze
analyze(las,si, state=[0,1,2,3,4])
