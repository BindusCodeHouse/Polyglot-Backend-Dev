'''
Broadcasting = "Different shapes can still work together."
Vectorization = "No loops."
'''

# Broadcasting
import numpy as np

b = np.array([[1],
              [2],
              [3]])
a = np.array([10,20,30])

print(a)
print(b)

print(a + b)

# Vectorization
'''
import numpy as np

a = np.array([[1,2,3],
              [4,5,6],
              [7,8,9]])
b = a * 10
print(a)
print(b)
'''