import numpy as np

# return datatype -> <class 'numpy.ndarray'>
'''
arr = np.array([1,2,3,4,5,6])
print(type(arr))
'''

# return datatype of inner Element -> int32
'''
arr = np.array([1,2,3,4,5,6])
print(arr.dtype)
'''

# store zeros value
'''
arr = np.zeros(5)
print(arr)
'''

# store ones value
'''
arr = np.ones((3,2))
print(arr)
'''

# store any single value with different Dimension
'''
arr = np.full((3,3),2)
print(arr)
'''

# if you want to sequence of number with step then use arange  -> [1 4 7]
'''
arr = np.arange(1,10,3)
print(arr)
'''

# want to create Identity metrix
'''
Use np.identity() when you specifically need a square identity matrix.
Use np.eye() when you need more control, such as creating a rectangular matrix or shifting the diagonal. Because of its flexibility, np.eye() is used more often in practice.

arr = np.identity(3)
arr1 = np.eye(3)
print(arr)
print(arr1)

# Rectangular matrix
arr = np.eye(5, 5)
print(arr)

# Upper Diagonal
arr = np.eye(5, 5, 2)
print(arr)

# Lower Diagonal
arr = np.eye(5, 5, -2)
print(arr)
'''

# find shape of Array -> (2, 3)
'''
arr = np.array([[1,2,3],[4,5,6]])
print(arr.shape)
'''

# find Total Number Of Element -> 6
'''
arr = np.array([[1,2,3],[4,5,6]])
print(arr.size)
'''

# find Number Of Dimension -> 2
'''
arr = np.array([[1,2,3],[4,5,6]])
print(arr.ndim)
'''

# change type of Array value
'''
arr = np.array([11.2,2.50,3.13])
tp = arr.astype(int)
print(tp)
print(tp.dtype)
'''