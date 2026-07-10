'''
we do not compare Nan value with Nan value.
like, np.nan == np.nan it is retun False in numpy
'''

import numpy as np
arr = np.array([10, np.nan, 20])
print(np.isnan(arr))


# set Default value on the space Nan
import numpy as np
arr = np.array([10, np.nan, 20])
arr2 = np.nan_to_num(arr)
print(arr2)