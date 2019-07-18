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
        #print('WARNING: INPUT CANDIDATE FILE IS EMPTY') #print warning
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

    BeamID = beamIDs[np.where(np.array(beamnumbers)==beamNumber)[0][0]]

    return BeamID
    
    


###################################################################################################

#begin script

#folder with destroy .pls candidate files to test
folder = '/share/nas1/cwalker/SKA_work/SMC_search_dev/test_files/LorimerBurst/SMC021_008_results/'

#file containing acceptable beam combinations
GoodBeamList = 'AllowedParkesBeamCombos.txt'

#load good beam combos into an array
goodbeamcombos=[]
with open(GoodBeamList,'r') as f:
    goodbeamcombos=[line.strip("''[]\n") for line in f.readlines()]#strip unecessary characters


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
    #declare empty arrays for candidates
    dms=np.empty(0)
    downsamp=np.empty(0)
    sample=np.empty(0)
    snrs=np.empty(0)
    beamids=np.empty(0)
    
    #loop over beams in pointing
    for j in range(len(pointing)):
        #print 'Count',j
        beam = pointing[j]
        #print 'Beam',beam
        #extract candidates
        cands = ReadDestroyCandFile(folder+beam)
        print 'Cands',cands
        #extract beam id
        beamid = np.chararray(np.shape(cands)[0],itemsize=2)
        beamid[:]=GenBeamID(beam)
        #print 'Beamid',beamid

        #print cands[:,0],cands[:,1],cands[:,2],cands[:,3]


        #put candidates in their own arrays


        dms=np.concatenate((dms,np.array(cands[:,0])))
        downsamp=np.concatenate((downsamp,np.array(cands[:,1])))
        sample=np.concatenate((sample,np.array(cands[:,2])))
        snrs=np.concatenate((snrs,np.array(cands[:,3])))
        beamids=np.concatenate((beamids,np.array(beamid)))

    #zip candidates into new array containing beam ids
    zipcands =np.array(zip(dms,downsamp,sample,snrs,beamids))

    #sort candidates by sample time column
    print zipcands,np.shape(zipcands)
    print zipcands[zipcands[:,2].argsort()]


    zipcands_sorted = zipcands[zipcands[:,2].argsort()]



    #merge duplicates
    zipcands_merged = [] #i itialise array
    #loop over candidates
    for i in range(len(zipcands_sorted[:,2])):
        cand = zipcands_sorted[i,:]
        #first candidate
        #print i
        if i==0:
            #print zipcands_merged
            zipcands_merged.append(cand)
        #remaining candidates
        else:
            #check if timesample matches previous candidate appended to merge list
            #print zipcands_merged[-1][2]#,zipcands_merged[i-1][2]
            if cand[2]==zipcands_merged[-1][2]:
                # if S/N is greater in new candidate:
                if cand[3]>zipcands_merged[-1][3]:
                    # append previous beams to this candidate and update merged list
                    cand[4]+=' '+zipcands_merged[-1][4]
                    zipcands_merged[-1]=cand
                #if S/N is not greater in the new candidate:
                if cand[3]<=zipcands_merged[-1][3]:
                    # append new beam to previous candidate in merge list
                    zipcands_merged[-1][4]+=' '+cand[4]
            #if timesample is different to previous candidate in merge list:
            else:
                #it is a new candidate. Append new item to merge list
                zipcands_merged.append(cand)

    print zipcands_merged

    #check whether beam patterns are acceptable
    zipcands_merged_checked = []#initialise array


    #loop over each fully merged candidate:
    for j in range(len(np.array(zipcands_merged)[:,4])):
        #sort candidate beams numerically
        sorted_beams = sorted(zipcands_merged[j][4].split())
        print sorted_beams
        #if sorted beam combination is acceptable, append candidate to new list


#print candfiles
print goodbeamcombos



















