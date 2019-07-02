#test for coincidencing destroy candidates from parkes multibeam reciever observations

#imports
import os
import numpy as np
from matplotlib import pyplot as plt

#folder with destroy .pls candidate files to test
folder = '/share/nas1/cwalker/SKA_work/SMC_search_dev/test_files/LorimerBurst/SMC021_008_results/'

#list destroy candidate files
allfiles = os.listdir(folder)
candfiles = [i for i in allfiles if i[-4:]=='.pls']

#destroy candidate files are named with convention: SMCXXX_YYBB_ZZZDM.pls
#where XXX_YY refers to pointing (e.g. 021_008)
#BB refers to beam (B1=11, B2=21, ... BD=D1)
#ZZZ is the dispersion measure (e.g. 631.0)

#sort candidates into sublist containing all beams for each pointing, DM

#get all unique pointing and dms
cand_pointings=[i[0:9] for i in candfiles] #get pointings
cand_pointings=np.unique(cand_pointings)

cand_dms = [i.split('_')[-1][0:-4] for i in candfiles] #get dms
cand_dms = np.unique(cand_dms)

print cand_pointings,cand_dms




