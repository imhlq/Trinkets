### Use h5py to view the HDF5 file. Print the structure of file.

import h5py
def h5view(h5, lev=0):
    if type(h5) == h5py._hl.group.Group or type(h5) == h5py._hl.files.File:
        for key in h5.keys():
            print('- ' * lev + key)
            h5view(h5[key], lev+1) # Recurrsion
    elif type(h5) == h5py._hl.dataset.Dataset:
        print("- " * lev + str(h5))
        return 1
    else:
        raise
        
# f = h5py.File("path...", 'r')
# h5view(f)
