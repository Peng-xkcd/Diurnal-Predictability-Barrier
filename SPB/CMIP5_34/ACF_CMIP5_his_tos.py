# @author: Peng Wang
# @data: 2020/9/15 9:37

from netCDF4 import Dataset
import os
import numpy as np
import math
import matplotlib.pyplot as plt

root_dir = 'E:\JYS_DATA\historical_1900-2005'
list_dir = os.listdir(root_dir)

month = 12
mon = np.linspace(1, month, month)
tau = np.linspace(0, month, month+1)
tau1, m1 = np.meshgrid(tau, mon)
total_int = np.zeros((1, len(list_dir)))

for i in range(0, len(list_dir)):
    path_nc = os.path.join(root_dir, list_dir[i])
    if os.path.isfile(path_nc):

        data = Dataset(path_nc)
        sst = data.variables['TOS'][:]
        time = data.variables['TIME'][:]
        lat = data.variables['LAT'][:]
        lon = data.variables['LONN179_180'][:]
        '''
        #Nino 3.4
                print(np.argwhere(lat == -4.5), np.argwhere(lat == 4.5), np.argwhere(lon == -169.5), \
                      np.argwhere(lon == -120.5)) # NIno3.4区域
                lat_s = np.argwhere(lat == -4.5) #85
                lat_e = np.argwhere(lat == 4.5) #94
                lon_s = np.argwhere(lon == -169.5) #10
                lon_e = np.argwhere(lon == -120.5) #59
        '''
        t_enson1 = np.squeeze(np.mean(np.squeeze(np.mean(sst[:, 85:95, :], axis=1))[:, 10:60], axis=1))
        t_enson = t_enson1[0:(len(t_enson1)//month)*month]
        t_use = t_enson.reshape(math.floor(len(t_enson)/month), -1)

        corr = np.zeros((month, month + 1))
        grid = np.zeros((month, month + 1))
        maxindex = np.zeros((month, 1))

        for mo in range(0, month):
            for mo_lag in range(mo, mo+1+month):
                if mo_lag < month:
                    corr[mo, mo_lag-mo] = np.min(np.min(np.corrcoef(t_use[:, mo], t_use[:, mo_lag])))
                else:
                    tem1 = np.delete(t_use[:, mo], -1, axis=0)
                    tem2 = np.delete(t_use[:, mo_lag - month], 0, axis=0)
                    corr[mo, mo_lag-mo] = np.min(np.min(np.corrcoef(tem1, tem2)))


        for k in range(0, month):
            grid[k, 0] = corr[k, 0] - corr[k, 1]
            grid[k, month] = corr[k, month - 1] - corr[k, month]
        for n in range(0, month):
            for j in range(0, month - 1):
                grid[n, j + 1] = (corr[n, j] - corr[n, j + 2]) / 2

        for m in range(0, month):
            maxindex[m, :] = np.argmax(grid[m, :])

        #total PB intensity
        total_int[0, i] = np.sum(np.max(grid, axis=1))

        # figure
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        cmap = plt.cm.jet
        gci = ax.contourf(tau1, m1, corr, cmap=cmap)
        plt.scatter(maxindex, np.linspace(1, month, month), s=50, c='k')
        plt.xlim(0, month)
        plt.ylim(1, month)
        ax.set_xticks(np.linspace(0, month, month + 1))
        ax.set_xticklabels(('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'))
        ax.set_yticks(np.linspace(1, month, month))
        ax.set_yticklabels(('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'))
        cbar = plt.colorbar(gci)
        # cbar.ax.set_ylabel('Autocorrelation Coefficient',fontsize=15)
        plt.title('{} (Niño 3.4)'.format(list_dir[i]), fontdict={'weight': 'normal', 'size': 20})
        plt.xlabel('Lag(month)', fontdict={'weight': 'normal', 'size': 15})
        plt.ylabel('Initial Month', fontdict={'weight': 'normal', 'size': 15})
        # plt.savefig('E:\\JYS_DATA\\Figs-historical_tos\\{}.png'.format(list_dir[i]))
        plt.close()
np.save('total_int_his.npy', total_int)








