#test for coincidencing destroy candidates from parkes multibeam reciever observations

###################################################################################################

#imports
import os
import numpy as np
from matplotlib import pyplot as plt

###################################################################################################

#functions

def ReadDestroyCandFile(DestroyFile):
    """
    Reads in a candidate file created by charlie's modified version of the DESTROY single
    pulse search software.

    INPUTS :

    DestroyFile : (str) name and location of destroy candidate file

    RETURNS :

    cands : (2-D array) array of candidates within file. Columns are DM, Downsamp factor, sample number, S/N


    """

    #initialise destroy candidate array (contains four columns)
    cands=np.empty((1,4))
    #load file
    check=np.loadtxt(DestroyFile)
    if check.shape!=(0,): #if cand file is not empty
        if check.shape==(4,): #if only one candidate, reshape to allow appending
            check=check.reshape(1,4)
        cands=np.concatenate((cands,check),axis=0) #append candidates
    elif check.shape==(0,):#if cand file is empty
        print('WARNING: INPUT CANDIDATE FILE IS EMPTY') #print warning
        return cands

    return cands

def GenBeamID(DestroyFileName):
    """
    Returns the beam ID of a destroy candidate file

    Based on naming convention: SMCXXX_YYBB_ZZZDM.pls
    #where XXX_YY refers to pointing (e.g. 021_008)
    #BB refers to beam (B1=11, B2=21, ... BD=D1)
    #ZZZ is the dispersion measure (e.g. 631.0)


    INPUTS :

    DestroyFileName : (str) name of destroy candidate file

    RETURNS :

    BeamID : (str) the Beam ID of the candidate file

    """

    beamnumbers = ['11','21','31','41','51','61','71','81','91','A1','B1','C1','D1'] #Parkes data beam numbers
    beamIDs     = ['B1','B2','B3','B4','B5','B6','B7','B8','B9','BA','BB','BC','BD'] #Beam IDs according to my naming convention

    beamNumber = DestroyFileName.split('_')[1][-2:] #extract beam number
    print beamNumber
    BeamID = np.where(beamnumbers==beamNumber)

    return BeamID
    
    


###################################################################################################

#begin script

#folder with destroy .pls candidate files to test
folder = '/share/nas1/cwalker/SKA_work/SMC_search_dev/test_files/LorimerBurst/SMC021_008_results/'

#list destroy candidate files
allfiles = os.listdir(folder)
candfiles = [i for i in allfiles if i[-4:]=='.pls']

#destroy candidate files are named with convention: SMCXXX_YYBB_ZZZDM.pls
#where XXX_YY refers to pointing (e.g. 021_008)
#BB refers to beam (B1=11, B2=21, ... BD=D1)
#ZZZ is the dispersion measure (e.g. 631.0)



#get all unique pointing and dms
cand_pointings=[i[0:10] for i in candfiles] #get all pointings
cand_pointings=np.unique(cand_pointings) #get uniques

cand_dms = [i.split('_')[-1][0:-4] for i in candfiles] #get all dms
cand_dms = np.unique(cand_dms) #get uniques
print cand_dms


#sort candidate files into sublists containing all beams for each pointing, DM
cands_grouped = [] #initialise array for grouped beams

for p in cand_pointings: #loop over all pointings in folder

    for dm in cand_dms: #loop over all potential dms
        beamlist = [] #initialise an array to hold grouped beams

        for c in candfiles: #loop over all candidate files
            #print p,dm,c,(('_'+dm in c) and (p in c))
            if ('_'+dm in c) and (p in c):
                #print 'true'
                beamlist.append(c) #group beams for same pointing and dm

        cands_grouped.append(beamlist) #append group to grouped beams list

print cands_grouped

#for each group of beams
for i in range(len(cands_grouped)):
    pointing = cands_grouped[i]
    print pointing
    
    #loop over beams in pointing
    for j in range(len(pointing)):
        beam = pointing[j]
        
        #read in first beam
        if j==0:
            cands = ReadDestroyCandFile(folder+beam)
            #reassign candidates to arrays
            dms = cands[:,0]
            downsamp = cands[:,1]
            sample = cands[:,2]
            snrs = cands[:,3]
            #create new array to hold beams cand was found in
            print beam,GenBeamID(beam)
            
            print snrs
    


    #sort and merge duplicates

#print candfiles


