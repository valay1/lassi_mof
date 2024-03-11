import os
import subprocess
file_list=['lassi_1_11.py',
'lassi_1_13.py',
'lassi_1_14.py',
'lassi_1_15.py',
'lassi_1_17.py',
'lassi_1_19.py',
'lassi_1_21.py',
'lassi_1_3.py',
'lassi_1_5.py',
'lassi_1_7.py',
'lassi_1_9.py']

for inp_file in file_list:
    os.system("sbatch B_2_L %s" %inp_file)
         
