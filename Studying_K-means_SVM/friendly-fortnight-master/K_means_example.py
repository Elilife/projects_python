#matplotlib inline
from copy import deepcopy
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
plt.rcParams['figure.figsize']=(16,9)
plt.style.use('ggplot')

#Importing the data set
data=pd.read_csv('xclara.csv')
print(data.shape)
print(data.head())

#getting values to plot
f1=data['V1'].values
f2=data['V2'].values
X=np.array(list(zip(f1,f2)))
plt.scatter(f1,f2,c='black',s=7)
