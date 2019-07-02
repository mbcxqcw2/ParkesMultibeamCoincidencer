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

#destroy candidate files are named with convention: SMCXXX_YYBB_DM.pls
#where XXX_YY refers to pointing (e.g. 021_008)
#BB refers to beam (B1=11, B2=21, ... BD=D1)
#DM is the dispersion measure (e.g. 631.0)

#sort candidates into sublist containing all beams for each pointing, DM

print candfiles[0:9]
print np.unique(candfiles[0:9])


