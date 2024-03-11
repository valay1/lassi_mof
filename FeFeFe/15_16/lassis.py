import numpy as np
import sys
from pyscf import gto, scf, tools,lib, mcscf
from pyscf.mcscf import avas,project_init_guess
from pyscf import mcscf
from mrh.my_pyscf.tools import molden
from mrh.my_pyscf.mcscf import lasscf_async as asyn
mol_name='Fe_Fe_Fe.xyz' # Al-Fe-Fe MOF node
basis={'C': 'cc-pvdz','H': 'cc-pvdz','O': 'cc-pvtz','Al': 'cc-pvtz','Fe': 'cc-pvtz'}
output='lassis_test.log'
mol=gto.M(atom=mol_name,verbose=4,spin=14,charge=0,basis=basis, output=output) #spin = 2S
mf=scf.RHF(mol)
mf=mf.density_fit()
mf.max_cycle=1
mf.kernel()
mf.mo_coeff=np.load('hf.npy')
mo_converged=np.load('las_15_16.npy')
las=asyn.LASSCF(mf,(5,5,5),((3,3),(0,5),(5,0)),spin_sub=(5,6,6),verbose=4) 
las.set_fragments_(([17],[19],[22]),mo_converged)
las.mo_coeff=mo_converged
las.max_cycle_macro=1
las.kernel()
las.mo_coeff=mo_converged
from mrh.my_pyscf import lassi
las.lasci_(mo_converged)
lsi=lassi.LASSIS(las).run()
#from mrh.my_pyscf.lassi import states
#from mrh.my_pyscf.mcscf.lasci import get_space_info
#las=states.spin_shuffle(las)
#las=states.all_single_excitations(las)
#ncsf=las.get_ugg().ncsf_sub
#charges, spins, smults, wfnsyms = get_space_info (las)
#np.save('spins',spins)
#np.save('smults',smults)
#np.save('charges',charges)
#exit()
#lroots=np.minimum(6,ncsf)
#lroots[charges.T==0] =1
#las.lasci(lroots=lroots)
#eroots,si=las.lassi()
#from mrh.my_pyscf.lassi.sitools import analyze
#ci1, si1, space_weights, navg, maxw, entr = analyze(las,si, state=[0,1,2,6,12,17,21,23],return_metrics=True)
#np.save('r1_n5_ct/ci1',ci1)
#np.save('r1_n5_ct/si1',si1)
#np.save('r1_n5_ct/space_weights',space_weights)
#np.save('r1_n5_ct/navg',navg)
#np.save('r1_n5_ct/maxw',maxw)
#np.save('r1_n5_ct/entr',entr)
