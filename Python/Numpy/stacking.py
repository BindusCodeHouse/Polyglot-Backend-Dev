'''
vstack = vertically stack
hstack = horizontally stack
'''

import numpy as np
arr = np.array([[1,2,3],[4,5,6]])
vstk = np.vstack(arr)
hstk = np.hstack(arr)
print(vstk)
print(hstk)