import numpy as np
import numpy.matlib
def rm(x):
    a1 = np.mean(x, axis=1)
    a2 = np.matlib.repmat(a1, x.shape[1], 1)
    a3 = x - a2.transpose()
    return a3