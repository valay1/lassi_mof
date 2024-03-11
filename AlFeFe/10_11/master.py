import os
import subprocess
def generate_inp_file(r,n):
    inpfile_name='lassi_r'+str(r)+'_n'+str(n)+'.py'
    os.system('cat temp| sed -e "s/r=\;n=/r={}\;n={}/">>{}'.format(r,n,inpfile_name))
    return inpfile_name
def execute(filename):
    print(filename)
    os.system("sbatch B_2_L %s" %filename)
for r in range(4):
    for n in range(1,11):
        inpfile_name=generate_inp_file(r,n)
        execute(inpfile_name)
