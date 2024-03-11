import os
import subprocess
def generate_inp_file(n):
    inpfile_name='lassi_r1_n'+str(n)+'.py'
    os.system('cat temp| sed -e "s/n=\;/n={}\;/">>{}'.format(n,inpfile_name))
    return inpfile_name
def execute(filename):
    print(filename)
    os.system("sbatch script %s" %filename)
for n in range(3,10):
    inpfile_name=generate_inp_file(n)
    execute(inpfile_name)
