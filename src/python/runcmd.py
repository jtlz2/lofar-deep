import subprocess

#usage: sys.argv[2] must be 'CAL' or 'FIELD'. The script will load the appropriate parameters based on this step. 
cmd1 = './tungsten_RPD.py initparmsCAL.py CAL'
proc=subprocess.Popen(cmd1,shell=True,executable='/bin/bash',\
                                 stdout=subprocess.PIPE)
proc.wait()



cmd2 = './tungsten_RPD.py initparmsFIELD.py'
proc=subprocess.Popen(cmd1,shell=True,executable='/bin/bash',\
                                 stdout=subprocess.PIPE)
proc.wait()

