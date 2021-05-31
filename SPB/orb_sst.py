from netCDF4 import Dataset
import pandas as pd
import numpy as np
import sys
sys.path.append(r'E:\\PC_project\\SPB')
import rm_mean as rm
import matplotlib.pyplot as plt


sst = Dataset('E:\\py_data\\orb_sst\\orb_sst.nc')
# print(sst.variables.keys())

z_t = sst.variables['z_t'][:]
temp = sst.variables['Temp_1000hpa'][:]
lat = sst.variables['TLAT'][:]
lon = sst.variables['TLONG'][:]
time = sst.variables['time'][:]
time_bound = sst.variables['time_bound'][:]

#
# print(lat[:, 30])
# print(lon[0, :])
#
#
# print(np.argwhere(lat == -4.78841)) #41
# print(np.argwhere(lat == 4.8110747)) #56
#
# print(lat[41:57, :])
#
# print(np.argwhere(lon == 172.1)) #58
# print(np.argwhere(lon == 190.1)) #63


t = np.squeeze(np.mean(np.squeeze(np.mean(np.squeeze(temp[:, :, 41:57, 58:64]), 1)), 1))
# print(t, np.shape(t))

t2 = t.reshape((-1, 12))
binsize = 30
total = 100
mo = 12
corr = np.zeros((mo, mo+1, total))
grid = np.zeros((mo, mo+1, total))
maxindex = np.zeros((mo, total))
mon = np.linspace(1, 12, 12)
tau = np.linspace(0, 12, 13)
m1, tau1 = np.meshgrid(mon, tau)
pb_time = np.zeros((total, 1))
pb_std = np.zeros((total, 1))
total_intensity = np.zeros((total, 1))
pb_mo = np.zeros((mo, total))

for k in range(total):
    print(k)
    t1 = t2[k*binsize:(k+1)*binsize, :]
    # t1 = rm.rm(t2)

    for i in range(0, mo):
        for j in range(i, i+mo+1):
            if j < mo:
                corr[i, j-i, k] = np.min(np.min(np.corrcoef(t1[:, i], t1[:, j])))
            else:
                tem1 = np.delete(t1[:, i], -1, axis=0)
                tem2 = np.delete(t1[:, j-mo], 0, axis=0)
                corr[i, j-i, k] = np.min(np.min(np.corrcoef(tem1, tem2)))
            '''
            else:
                index1 = [-2, -1]
                index2 = [0, 1]
                temp3 = np.delete(t1[:, i], index1, axis=0)
                temp4 = np.delete(t1[:,j-12], index2, axis=0)
               corr[i, j-i] = np.min(np.min(np.corrcoef(temp3, temp4)))
               '''
    #print(corr)
    #算梯度

    for i in range(0, mo):
        grid[i, 0, k] = corr[i, 0, k]-corr[i, 1, k]
        grid[i, mo, k] = corr[i, mo-1, k]-corr[i, mo, k]
    for i in range(0, mo):
        for j in range(0, mo-1):
            grid[i, j+1, k] = (corr[i, j, k]-corr[i, j+2, k])/2

    # for i in range(0, mo):
    #     maxindex[i, :, k] = np.argmax(grid[i, :, k])


    for i in range(0, mo):
        maxindex[i, k] = np.argmax(grid[i, :, k])
        pb_mo[i, k] = maxindex[i, k] + i
        if pb_mo[i, k] > (mo - 1):
            pb_mo[i, k] = pb_mo[i, k] - (mo - 1)
    pb_time[k, :] = np.sum(pb_mo[:, k]) / mo  # PB hour
    pb_std[k, :] = np.std(pb_mo[:, k])  # PB std
    # 黑点的值

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    cmap = plt.cm.jet
    gci = ax.contourf(tau1, m1, corr[:, :, k].transpose(), cmap=cmap)
    plt.scatter(maxindex[:, k], np.linspace(1, mo, mo), s=50, c='k')
    plt.xlim(0, mo)
    plt.ylim(1, mo)
    ax.set_xticks(np.linspace(0, mo, mo+1))
    ax.set_xticklabels(('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'))
    ax.set_yticks(np.linspace(1, mo, mo))
    ax.set_yticklabels(('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'))
    cbar = plt.colorbar(gci)
    #cbar.ax.set_ylabel('Autocorrelation Coefficient',fontsize=15)
    plt.title('ACF (Niño 3.4)', x =0.25, fontdict={'weight': 'normal', 'size': 20})
    plt.xlabel('Lag(month)', fontdict={'weight': 'normal', 'size': 15})
    plt.ylabel('Initial Month', fontdict={'weight': 'normal', 'size': 15})
    plt.savefig('E:\\gif_PB\\SPB_fig\\{:0>2d}.png'.format(k))
    plt.close()

max_grid = np.squeeze(np.amax(grid, axis=1))
total_intensity = np.sum(max_grid)


#*****************************************************************
'''
fig1 = plt.figure()
year = np.linspace(1, 100, 100)
plt.plot(year, pb_time, 'k')
plt.title('a) PB Month', x =0.2, fontdict={'weight': 'normal', 'size': 20})
plt.xlabel('Year (*30)', fontdict={'weight': 'normal', 'size': 15})
plt.ylabel('Month', fontdict={'weight': 'normal', 'size': 15})
# plt.ylim([])
plt.xlim([1, 100])

fig2 = plt.figure()
year = np.linspace(1, 100, 100)
plt.plot(year, total_intensity, 'r')
plt.title('b) PB Intensity', x =0.25, fontdict={'weight': 'normal', 'size': 20})
plt.xlabel('Year (*30)', fontdict={'weight': 'normal', 'size': 15})
plt.ylabel('Intensity', fontdict={'weight': 'normal', 'size': 15})
# plt.ylim([])
plt.xlim([1, 100])

fig3 = plt.figure()
year = np.linspace(1, 100, 100)
plt.plot(year, pb_std, 'b')
plt.title('c) PB Std', x = 0.15, fontdict={'weight': 'normal', 'size': 20})
plt.xlabel('Year (*30)', fontdict={'weight': 'normal', 'size': 15})
plt.ylabel('Std', fontdict={'weight': 'normal', 'size': 15})
# plt.ylim([])
plt.xlim([1, 100])
'''