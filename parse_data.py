import os
import numpy as np
import matplotlib.pyplot as plt

from mpl_toolkits import mplot3d

def parse_location(tgt_dir):

    # location_list = np.empty((0,2), dtype=np.float64)
    location_list = []
    all_location = sorted(os.listdir(tgt_dir))

    for loc in all_location:
        hold_arr = []
        for line in open(loc):
            if 'longitude' in line:
                splitval = line.split(sep='\"')
                float_split_long = float(splitval[3])
                hold_arr.append(float_split_long)

            if 'latitude' in line:
                splitval = line.split('\"')
                float_split_lat = float(splitval[3])
                hold_arr.append(float_split_lat)

            if 'altitude' in line:
                splitval = line.split('\"')
                float_split_alt = float(splitval[3])
                # hold_arr.append(float_split_alt)
                hold_arr.append(60.0)
        # print(hold_arr[0], ",", hold_arr[1])
        location_list.append(hold_arr)

    return location_list

currentPath = os.getcwd()
datadir = currentPath + '/sample_metadata'

print(datadir)
os.chdir(datadir)
location_list = parse_location(datadir)

np_loc_list = np.array(location_list, dtype=np.float64)

print(np_loc_list.shape)

fig = plt.figure()
ax = plt.axes(projection='3d')

xdata = np_loc_list[:,0]
ydata = np_loc_list[:,1]
zdata = np_loc_list[:,2]

print(xdata)

# ax.set_box_aspect((np.ptp(xdata), np.ptp(ydata), np.ptp(zdata)))

ax.scatter3D(zdata, ydata,xdata, c=xdata, cmap='tab10')

plt.savefig('output.png')
