#test for coincidencing destroy candidates from parkes multibeam reciever observations

#imports
import os
import numpy as np
from matplotlib import pyplot as plt

#folder with destroy .pls candidate files to test
folder = '/share/nas1/cwalker/SKA_work/SMC_search_dev/test_files/LorimerBurst/SMC021_008_results/'

#list destroy files
allfiles = os.listdir(folder)
candfiles = [i for i in allfiles if i[-4:]=='.pls']

print candfiles
