# author: Peng Wang
# data: 2020/10/21 12:00

import numpy as np
import matplotlib.pyplot as plt
# import os
#
# root_dir = 'E:\JYS_DATA\historical_1900-2005'
# list_dir = os.listdir(root_dir)
# model_names = np.delete(list_dir, [6])

rcp_int1 = np.load('total_int_rcp.npy')
his_int1 = np.load('total_int_his.npy')
rcp_int = np.delete(rcp_int1, [9])
his_int = np.delete(his_int1, [6])
diff = rcp_int - his_int
model_names = ['FIO-ESM', 'GISS-E2-R', 'bcc-csm1-1-m',
       'CCSM4', 'CESM1-BGC', 'CESM1-CAM5',
       'CMCC-CM', 'CMCC-CMS', 'GFDL-CM3',
       'GFDL-ESM2M', 'GISS-E2-H', 'IPSL-CM5B-LR',
       'MIROC5', 'MRI-CGCM3', 'MPI-ESM-LR',
       'GFDL-ESM2G', 'NorESM1-M', 'ACCESS1-0',
       'ACCESS1-3', 'CSIRO-Mk3-6-0', 'EC-EARTH',
       'HadGEM2-AO', 'HadGEM2-CC', 'HadGEM2-ES',
       'inmcm4', 'IPSL-CM5A-LR', 'IPSL-CM5A-MR',
       'bcc-csm1-1', 'CanEsm2', 'MPI-ESM-MR',
       'NorESM1-ME']


x_z = np.arange(1, 32, 1)
plt.figure(1)
plt.scatter(x_z, diff, s=30, c='black')
plt.plot([-1, 33], [0, 0], 'r')
plt.xlim([0, 32])
plt.title('Intensity Difference of rcp85 and historical (Niño 3.4)', fontsize=15)
plt.ylabel('Intensity Difference')
# plt.xlabel('Model')
plt.xticks(x_z, model_names, rotation=90)
plt.tight_layout()