import numpy as np
arr = np.array([1,2,3,4,5])

'''
print(np.sum(arr))
print(arr.sum()) 

both are return same result because if your array is already numpy array then numpy give function access which use direct like arr.sum 
whereas, if you declare like arr=[10,20,30] then you need to use np.sum(arr) so, it work like that.here, give both same reason because 
your array is numpy array.
'''
print(np.sum(arr))
print(arr.sum())

print(np.mean(arr))
print(arr.mean())

print(arr.min())
print(arr.max())
print(arr.argmin())
print(arr.argmax())
print(arr.var())
print(arr.std())