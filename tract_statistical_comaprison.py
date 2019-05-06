# -*- coding: utf-8 -*-
"""
Created on Wed May  1 20:24:09 2019

@author: nusrat
"""
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
import AFQ.segmentation as seg
import matplotlib.patches as mpatches                  
from dipy.tracking.utils import length
from dipy.tracking import utils
from dipy.tracking.vox2track import streamline_mapping

def load_tract (sub):
    
    tract_filename=PATH
    streams,hdr=nib.trackvis.read(tract_filename)   
    tracks = np.array([s[0] for s in streams], dtype=np.object)
    
    return tracks
    

def avg_fa (sub):
    
    fa_filename=PATH
    FA_img = nib.load(fa_filename)
    FA_data = FA_img.get_data()
    
    FA_data=np.array(FA_data)
    
    return np.average(FA_data)

def length_info(tract):
    
    lengths = np.array(list(length(tract)))
    return lengths.max(),lengths.min(),np.average(lengths)
    
     
def voxel_count(affine,tract ):
    return len(streamline_mapping(tract,affine=affine).keys())

         
if __name__ == '__main__':
    
    healthy_subject_list = ["201","202","203","204","205","206","207","208","209"]
    patient_subject_list = ["101","103","104","105","107","109","111","112","113"]
    
    affine=utils.affine_for_trackvis(voxel_size=np.array([2,2,2]))

    
    print ("......................Healthy ..............")
    length_info_healthy= np.array([length_info (load_tract(sub)) for sub in healthy_subject_list])
    print("average maximum length= "  , np.average( length_info_healthy[0])) 
    print("average minimum length= ",  np.average( length_info_healthy[1]))
    #print("average maximum length= ", np.average( length_info_healthy[2]) )
    
    print ("......................Patient ..............")
    length_info_patient= np.array([length_info (load_tract(sub)) for sub in patient_subject_list])
    print("average maximum length= "  , np.average( length_info_patient[0])) 
    print("average minimum length= ",  np.average( length_info_patient[1]))
    #print("average maximum length= ", np.average( length_info[2]) )
    
    print ("......................Healthy ..............")
    FA_info_healthy= np.array([avg_fa(sub) for sub in healthy_subject_list])
    print("average FA value= "  , np.average(FA_info_healthy[0])) 
    print("Standard Deviation FA value= "  ,  FA_info_healthy.std()  ) 
    
    print ("......................Patient..............") 
    FA_info_patient= np.array([avg_fa(sub) for sub in patient_subject_list])
    print("average FA value= "  , np.average(FA_info_patient[0])) 
    print("Standard Deviation FA value= "  ,  FA_info_patient.std()  ) 
    
    print ("......................Healthy ..............")
    streamline_no_info_healthy= np.array([len(load_tract(sub)) for sub in healthy_subject_list])
    print("average number of streamline = "  , np.average(streamline_no_info_healthy[0])) 
    print("Standard deviation of streamline= "  ,  streamline_no_info_healthy.std()  ) 
    
    print ("......................Patient..............") 
    streamline_no_info_patient= np.array([len(load_tract(sub)) for sub in patient_subject_list])
    print("average number of streamline= "  , np.average(streamline_no_info_patient[0])) 
    print("Standard deviation of streamline= "  ,  streamline_no_info_patient.std()  ) 
    
    print ("......................Healthy ..............")
    voxel_no_info_healthy= np.array([voxel_count(affine,load_tract(sub ))for sub in healthy_subject_list])
    print("average number of voxel= "  , np.average(voxel_no_info_healthy[0])) 
    print("Standard Deviation voxel no = "  ,  voxel_no_info_healthy.std()  ) 
    
    print ("......................Patient..............") 
    voxel_no_info_patient= np.array([voxel_count(affine,load_tract(sub )) for sub in patient_subject_list])
    print("average number of voxel= "  , np.average(voxel_no_info_patient[0])) 
    print("Standard Deviation voxel no= "  ,  voxel_no_info_patient.std()  ) 