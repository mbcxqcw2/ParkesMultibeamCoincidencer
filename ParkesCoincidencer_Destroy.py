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

#sort candidate files into sublists containing all beams for each pointing, DM

#get all unique pointing and dms
cand_pointings=[i[0:10] for i in candfiles] #get all pointings
cand_pointings=np.unique(cand_pointings) #get uniques

cand_dms = [i.split('_')[-1][0:-4] for i in candfiles] #get all dms
cand_dms = np.unique(cand_dms) #get uniques



cands_grouped = [] #initialise array for grouped beams

for p in cand_pointings: #loop over all pointings in folder

    for dm in cand_dms: #loop over all potential dms
        beamlist = [] #initialise an array to hold grouped beams

        for c in candfiles: #loop over all candidate files
            print p,dm,c,(('_'+dm in c) and (p in c))
            if ('_'+dm in c) and (p in c):
                print 'true'
                beamlist.append(c) #group beams for same pointing and dm

        cands_grouped.append(beamlist) #append group to grouped beams list

print cands_grouped




