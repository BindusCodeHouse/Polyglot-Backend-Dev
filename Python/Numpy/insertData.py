# for insert record in array use insert or append function in which in insert function we need to pass index in which index you want to add data whereAs, in append function you don't need to pass index at insert at the end of data.
'''
import numpy as np
arr = np.array([1,2,3,4,5,6])
arr2 = np.insert(arr,5,10)
print(arr)
print(arr2)

#  axis = 0 it means add Row
#  axis = 1 it means add Column

import numpy as np
arr = np.array([[1,2],[3,4],[5,6]])
arr2 = np.insert(arr,2,[7,8,9], axis=1)
print(arr)
print(arr2)
'''


import numpy as np
arr = np.array([1,2,3,4,5,6])
arr2 = np.append(arr,[7,8,9])
print(arr)
print(arr2)