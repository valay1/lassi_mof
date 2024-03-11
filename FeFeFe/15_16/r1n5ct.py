import numpy as np
import sys
from pyscf import gto, scf, tools,lib, mcscf
from pyscf.mcscf import avas,project_init_guess
from pyscf import mcscf
from mrh.my_pyscf.tools import molden
from mrh.my_pyscf.mcscf import lasscf_async as asyn
mol_name='Fe_Fe_Fe.xyz' # Al-Fe-Fe MOF node
basis={'C': 'cc-pvdz','H': 'cc-pvdz','O': 'cc-pvtz','Al': 'cc-pvtz','Fe': 'cc-pvtz'}
output='analyze_r1_n5_ct.log'
mol=gto.M(atom=mol_name,verbose=4,spin=14,charge=0,basis=basis, output=output) #spin = 2S
mf=scf.RHF(mol)
#mf.init_guess='atom'
mf=mf.density_fit()
mf.max_cycle=1
mf.kernel()
#mf=mf.newton()
#mf.max_cycle=1
#mf.kernel()
mf.mo_coeff=np.load('hf.npy')
#ncas,nelecas,guess_mo_coeff=avas.kernel(mf,['Fe 3d', 'Fe 4d'],minao=mol.basis, openshell_option=3)
#mc_test = mcscf.CASCI (mf, ncas, nelecas)
#final_list=[8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37]+mc_test.ncore
mo_converged=np.load('las_15_16.npy')
las=asyn.LASSCF(mf,(5,5,5),((3,3),(0,5),(5,0)),spin_sub=(5,6,6),verbose=4) 
las.set_fragments_(([17],[19],[22]),mo_converged)
las.mo_coeff=mo_converged

from mrh.my_pyscf.lassi import states
from mrh.my_pyscf.mcscf.lasci import get_space_info
las=states.spin_shuffle(las)
las=states.all_single_excitations(las)
ncsf=las.get_ugg().ncsf_sub
charges, spins, smults, wfnsyms = get_space_info (las)
lroots=np.minimum(5,ncsf)
#lroots[charges.T==0] =1
las.lasci(lroots=lroots)
eroots,si=las.lassi()
from mrh.my_pyscf.lassi.sitools import analyze
ci1, si1, space_weights, navg, maxw, entr = analyze(las,si, state=[0,1,2,6,12,17,21,23],return_metrics=True)
#np.save('r1_n5_ct/ci1',ci1)
#np.save('r1_n5_ct/si1',si1)
np.save('r1_n5_ct/space_weights',space_weights)
np.save('r1_n5_ct/navg',navg)
np.save('r1_n5_ct/maxw',maxw)
np.save('r1_n5_ct/entr',entr)
