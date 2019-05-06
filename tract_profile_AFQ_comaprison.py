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


def load_tract (tract_filename):
    
    streams,hdr=nib.trackvis.read(tract_filename)   
    tracks = np.array([s[0] for s in streams], dtype=np.object)
    
    return tracks
    

def load_fa (fa_filename):
    
   
    FA_img = nib.load(fa_filename)
    FA_data = FA_img.get_data()
    
    return FA_data

def showavgAfq(flag,health_profile=None,patient_profile=None):
    
    if health_profile==None:
     profile= patient_profile
    
    else: 
     profile= health_profile 
     
    if flag=="avg"  :
     fig, ax = plt.subplots(1)
     ax.plot(profile)
     plt.title('Average tract profile over 9 different subject by using AFQ ')
     plt.show()
     
    if flag=="avg_all"  : 
     fig, ax = plt.subplots(1)
     red_patch = mpatches.Patch(color='red', label='healthy_dataset')
     green_patch = mpatches.Patch(color='green', label='patient_dataset')
     plt.legend(handles=[red_patch,green_patch])
     ax.plot(health_profile,'r',patient_profile,'g',)
     plt.title('Average tract profile')
     plt.show()
         
def showallafq():   
      
     fig, ax = plt.subplots(1)
     for i in median_fa:
      ax.plot(i)     
     plt.title('tract profile by using AFQ for 9 different subject ')     
     plt.show()
def tract_profile(tracks, FA_data):
    
    print("Tract profiles...")
  
    profile = seg.calculate_tract_profile(FA_data, tracks.tolist())
    return profile
    
def average_profile_calculation(sub_list):
    global median_fa
    median_fa=[]
   
    for sub in sub_list:
        print (sub)
        tract_filename=PATH   
        #tract_filename= "/media/nusrat/3a7255f4-81fe-4fa7-8595-e4cdadc062a9/home/nusrat/Desktop/dataset_thesis/Mapping_Dataset/ROI/"+sub+"/NILAB_bao_cst_left.trk"
        tract= load_tract(tract_filename)
        #fa_filename="/media/nusrat/3a7255f4-81fe-4fa7-8595-e4cdadc062a9/home/nusrat/Desktop/dataset_thesis_new/Nifti/"+sub+"/MP_Rage_1x1x1_ND_3/T1_flirt_out.nii.gz"
        fa_filename=PATH
        FA_data= load_fa(fa_filename)
        profile= tract_profile(tract, FA_data) 
        median_fa.append(profile)
    
    avg_profile = [np.sum(median_fa[i][j])/len(sub_list) for i in range(0,len(sub_list))for j in range(0,median_fa[0].shape[0])] 
    return avg_profile
    
if __name__ == '__main__':
    
    healthy_subject_list = ["201","202","203","204","205","206","207","208","209"]
    patient_subject_list = ["101","103","104","105","107","109","111","112","113"]
    
    print ("average profile for healthy subject")
    avg_profile_healthy=average_profile_calculation(healthy_subject_list)
    showallafq()
    showavgAfq(flag="avg",health_profile=avg_profile_healthy,patient_profile=None)

    print ("average profile for Patient subject")
    avg_profile_patient=average_profile_calculation(patient_subject_list)
    showallafq()
    showavgAfq(flag="avg",health_profile=None,patient_profile=avg_profile_patient)
    
    
    showavgAfq(flag="avg_all",health_profile=avg_profile_healthy,patient_profile=avg_profile_patient)

    