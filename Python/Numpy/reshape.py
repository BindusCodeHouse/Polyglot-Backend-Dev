
# reshape(rows,columns) does not copy the data it create a view of original array. but, does not change parmanent to the original array.
'''

import numpy as np

arr = np.array([1,2,3,4,5,6])
print(arr.reshape(2,3))
print(arr)
'''


# when you want to reshape single dimension to multiDimension then use reshape whereAs, you want to reshape multiDimension to the single dimension then you use flatten || ravel. but, ravel share memory to the original array whereAs flatten not share Memory so, it not affect to the original array.
'''
import numpy as np

arr = np.array([[1,2,3],[4,5,6]])
rvl = arr.flatten()
print(rvl)
print(arr)
rvl[0] = 100
print(rvl)
print(arr)

#output :

[1 2 3 4 5 6]
[[1 2 3]
 [4 5 6]]
[100   2   3   4   5   6]
[[100   2   3]
 [  4   5   6]]

'''

'''
import numpy as np

arr = np.array([[1,2,3],[4,5,6]])
rvl = arr.ravel()
print(rvl)
print(arr)
rvl[0] = 100
print(rvl)
print(arr)

#output :

[1 2 3 4 5 6]
[[1 2 3]
 [4 5 6]]
[100   2   3   4   5   6]
[[1 2 3]
 [4 5 6]]
'''